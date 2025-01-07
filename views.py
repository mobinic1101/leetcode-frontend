from flask import Blueprint, render_template, request
from api_client import APIClient
from pprint import pprint

blueprint = Blueprint("views", __name__)
client = APIClient()


@blueprint.route("/")
def home():
    token = request.headers.get("Authorization")
    print("token: ", token)
    if token:
        token = token.decode("utf-8")
    context = client.get("/users/me/", token)
    context.page_name = home.__name__.capitalize()
    context = context.get_dict()
    pprint(context)
    return render_template("home.html", context=context)

