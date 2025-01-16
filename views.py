from flask import (
    Blueprint,
    render_template,
    request,
    session,
    flash,
    redirect,
    make_response,
)
from pprint import pprint
from typing import Dict
from api_client import APIClient
from context import Context

views = Blueprint("views", __name__)
client = APIClient()


@views.route("/")
def home():
    context = Context()
    context.data = client.get_quick_user_details()
    print("HOME CONTEXT DATA: ", context.data)
    context.page_name = home.__name__.capitalize()
    context = context.get_dict()
    return render_template("home.html", **context)


# user specific views
@views.route("/login", methods=["POST", "GET"])
def login():
    context = Context(data=client.get_quick_user_details())
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        context: Context = client.post(
            "/api-token-auth/", json={"username": username, "password": password}
        )
        if not context.error:
            flash("Logged in successfully", category="success")
            print("TOKEN: ", context.data.get("token"))
            token = context.data.get("token")
            response = redirect("/", code=302)
            response.set_cookie("token", token, secure=True, httponly=True)
            return response
        flash("Incorrect username or password", category="error")
        context.data.update({"username": username if username else ""})
    context.page_name = login.__name__
    last_used_username = ""
    if context.data.get("username"):
        last_used_username = context.data.get("username")
    return render_template(
        "login.html", **context.get_dict(), last_used_username=last_used_username
    )


@views.route("/logout", methods=["POST"])
def logout():
    token = request.cookies.get("token")
    if not token:
        return "<h1>Not logged in</h1>"
    response = client.post("/logout/", token=token, extract_data=False)
    print(response.status_code)
    if response.status_code == 200:
        flash("Logged out successfully", category="success")
        response = redirect("/", code=302)
        response.delete_cookie("token")
        return response
    return "<h1>Not logged in</h1>"


@views.route("/sign-up", methods=["POST", "GET"])
def sign_up():
    page_name = sign_up.__name__.replace("-", " ").title()
    last_used_username = ""
    context = Context(page_name=page_name, data=client.get_quick_user_details())

    if request.method == "POST":
        username = request.form.get("username")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        if password1 == password2:
            api_response = client.post(
                "/sign-up/",
                json={"username": username, "password": password1},
                extract_data=False,
            )
            data: Dict = api_response.json()
            if api_response.status_code == 201:
                token = data.get("token")
                response = redirect("/", code=302)
                response.set_cookie("token", token, secure=True, httponly=True)
                flash("Signed up successfully", category="success")
                return response
            else:
                flash(data.get("detail"), category="error")
        else:
            flash("Passwords don't match", category="error")
        last_used_username = username

    return render_template("sign-up.html", **context.get_dict(), last_used_username = last_used_username)


@views.route("/problems", methods=["GET"])
def problems():
    user = client.get_quick_user_details()
    problems_and_topics: list = client.get("/problems/", query_params={"with_topics": "1"}).json()
    page_name = problems.__name__.capitalize()
    pprint(problems_and_topics)
    return render_template("problems.html", **user, **problems_and_topics, page_name=page_name)

    # TODO: capture multiple selected topics in your backend to filter based on multiple topics.