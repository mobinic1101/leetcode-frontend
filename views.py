from flask import (
    Blueprint,
    render_template,
    request,
    session,
    flash,
    redirect,
    make_response,
    url_for,
)
from werkzeug.datastructures import FileStorage
from pprint import pprint
from typing import Dict
from httpx import Client
from api_client import APIClient
from context import Context
import utils

views = Blueprint("views", __name__)
api_client = APIClient()
client = Client(base_url="http://127.0.0.1:8000/api")


@views.route("/")
def home():
    context = Context()
    context.data = api_client.get_quick_user_details()
    print("HOME CONTEXT DATA: ", context.data)
    context.page_name = home.__name__.capitalize()
    context = context.get_dict()
    return render_template("home.html", **context)

@views.route("/login", methods=["POST", "GET"])
def login():
    context = Context(data=api_client.get_quick_user_details())
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        context: Context = api_client.post(
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
    response = api_client.post("/logout/", token=token, extract_data=False)
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
    context = Context(page_name=page_name, data=api_client.get_quick_user_details())

    if request.method == "POST":
        username = request.form.get("username")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        if password1 == password2:
            api_response = api_client.post(
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


@views.route("/profile/me", methods=["GET", "POST"])
def my_profile():
    # get user data
    token = request.cookies.get("token")
    user = api_client.get("/users/me/", extract_data=1, token=token)
    user_data = user.get_dict()
    user_data["profile_pic"] = api_client.base_url_raw + user_data.get("profile_pic")

    # check if user is logged in
    if user.error:
        flash("Sorry you are not logged in yet.", category="error")
        return redirect(url_for("views.login"), code=302)

    # add page name and is_authenticated to user_data
    user_data.update({"page_name": my_profile.__name__.capitalize(), "is_authenticated": True})

    # handle GET request
    if request.method == 'GET':
        return render_template("dashboard.html", **user_data)

    # handle POST request
    if request.method == 'POST':
        # extract form data
        form: dict = utils.extract_form_data(request)
        username = form.get("username")
        if not username:
            form["username"] = user_data.get("username")

        # check if profile pic is uploaded
        profile_pic: FileStorage = request.files.get("profile_pic")

        if profile_pic:
            # update with profile pic
            files = {"profile_pic": utils.convert_to_regular_file(profile_pic)}
            response = client.post("/users/me/", data=form, files=files, headers=utils.get_authorization_header(token))
        else:
            # update without profile pic
            response = client.post("/users/me/", data=form, headers=utils.get_authorization_header(token))

        # check if response was successful
        if response.status_code == 200:
            flash("Profile updated successfully", category="success")
            return redirect(url_for("views.my_profile"), code=302)
        else:
            flash(response.json(), category="error")
            return render_template("dashboard.html", **user_data)


@views.route("/problems", methods=["GET"])
def problems():
    user = api_client.get_quick_user_details()
    query_params = {"with_topics": "yes"}

    # grabbing query parameters
    search = request.args.get("search", "")
    difficulty = request.args.get("difficulty", "")
    topics = request.args.getlist("topic")

    # adding query parameters to query_params
    query_params.update({"search": search, "difficulty": difficulty, "topic": topics if topics else ""})
    pprint(query_params)

    # calling api
    problems_and_topics: list = api_client.get("/problems/", query_params=query_params).json()
    page_name = problems.__name__.capitalize()
    # pprint(problems_and_topics)
    return render_template("problems.html", **user, **problems_and_topics, page_name=page_name)


@views.route("/problem/<int:problem_id>", methods=["GET", "POST"])
def problem(problem_id):
    return f"SORRY NOT IMPLEMENTED YET problem id == {problem_id}"


@views.route("/solved-problems/<int:userid>", methods=["GET"])
def solved_problems(userid: int):
    user = api_client.get_quick_user_details()
    problems = api_client.get(f"/users/{userid}/solved-problems/", extract_data=1)
    pprint(problems.get_dict())

    return render_template("list_solved.html", **user, **problems.get_dict())


    #TODO: handle pagination on pages correctly!