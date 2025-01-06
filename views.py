from flask import Blueprint, render_template, request
from httpx import Client

blueprint = Blueprint("app", __name__)
client = Client(base_url="http://127.0.0.1:8000/api/")
client_headers = lambda token: {"Authorization": f"Bearer {token}"}


def get_context(page_name, is_authenticated, error=None, data: dict={}):
    return {
        "page_name": page_name,
        "is_authenticated": is_authenticated,
        "error": error,
        **data
    }


@blueprint.route("/")
def home():
    context = {"page_name": str(home.__name__), "is_authenticated": True}
    token = request.cookies.get("token")

    return render_template("home.html", context={"page_name": "Home"})

