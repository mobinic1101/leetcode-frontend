from flask import Blueprint, render_template, request, session, flash, redirect, make_response
from pprint import pprint
from api_client import APIClient
from context import Context

blueprint = Blueprint("views", __name__)
client = APIClient()


@blueprint.route("/")
def home():
    context = Context()
    context.data = client.get_quick_user_details()
    context.page_name = home.__name__.capitalize()
    context = context.get_dict()
    return render_template("home.html", **context)


@blueprint.route("/login", methods=["POST", "GET"])
def login():
    context = Context(data=client.get_quick_user_details())
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        context: Context = client.post("/api-token-auth/", json={"username": username, "password": password})
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
    return render_template("login.html", **context.get_dict())


# urlpatterns = [
# 	path("api-token-auth/", obtain_auth_token),
# 	path("sign-up/", auth.sign_up, name="sign_up"),
#     path("logout/", auth.logout, name="logout"),

#     # User-related paths
#     path("users/<int:pk>/", views.UserDetailView.as_view(), name="user_detail"),
#     path("users/me/", views.my_detail, name="my_detail"),
#     path("users/me/solved-problems/", views.UserSolvedProblemsView.as_view(), name="user_solved_problems"),

#     # Problem-related paths
#     path("problems/", views.ProblemListView.as_view(), name="problem_list"),  # List all problems
#     path("problems/<int:pk>/", views.ProblemDetailView.as_view(), name="problem_detail"),  # Retrieve a specific problem
#     path("problems/<int:pk>/comments/", views.ProblemCommentView.as_view(), name="problem_comments"),  # Comments on a specific problem

#     # Topic-related paths
#     path("topics/", views.TopicListView.as_view(), name="topic_list"),  # List all topics
    
#     # Test case-related paths
#     path("problems/<int:problem_id>/testcases/", views.TestCaseListView.as_view(), name="testcase_list"),  # List all test cases for a specific problem
#     path("problems/<int:problem_id>/run/", views.CodeRunningView.as_view(), name="run_code"),  # Run a code snippet for a specific problem
#     path("problems/get-result/<int:problem_id>/<str:execution_id>/", views.get_code_running_result, name="get_code_running_result"),  # Run a code snippet for a specific problem

# ]