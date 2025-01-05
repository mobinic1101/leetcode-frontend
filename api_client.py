from httpx import Client
from string import Template
from typing import Dict


class ApiClient:
    DEFAULT_BASE_URL = "http://127.0.0.1:8000/"
    endpoints = {
        "sign_up": Template("/sign-up/"),
        "login": Template("api-token-auth/"),
        "logout": Template("logout/"),
        "user_detail": Template("users/$pk/"),
        "update_user_detail": Template("users/me/update/"),
        "user_solved_problems": Template("users/me/solved-problems/"),
        "problem_list": Template("problems/"),
        "problem_detail": Template("problems/$pk/"),
        "problem_comments": Template("problems/$pk/comments/"),
        "topic_list": Template("topics/"),
        "testcase_list": Template("problems/$problem_id/testcases/"),
        "run_code": Template("problems/$problem_id/run/"),
        "get_code_running_result": Template("problems/get-result/$problem_id/$execution_id/"),
    }
    def __init__(self, base_url: str = DEFAULT_BASE_URL):
        self.client = Client(base_url=base_url)
        self.base_url = base_url

    def get_raw_url(self, name, **kwargs):
        return self.base_url + self.endpoints[name].substitute(**kwargs)

    def get_url(self, name, **kwargs):
        return self.endpoints[name].substitute(**kwargs)
    
    def sign_up(self, username, password, token=None):
        url = self.get_url("sign_up")
        return self.client.post(url, json={"username": username, "password": password}, headers={"Authorization": f"Token {token}"})

    def login(self, username, password, token=None):
        url = self.get_url("login")
        return self.client.post(url, json={"username": username, "password": password}, headers={"Authorization": f"Token {token}"})

    def logout(self, token):
        url = self.get_url("logout")
        return self.client.post(url, headers={"Authorization": f"Token {token}"})

    def get_user_detail(self, pk, token=None):
        url = self.get_url("user_detail", pk=pk)
        return self.client.get(url, headers={"Authorization": f"Token {token}"})

    def update_user_detail(self, data: Dict, token=None):
        url = self.get_url("update_user_detail")
        return self.client.put(url, json=data, headers={"Authorization": f"Token {token}"})

    def get_user_solved_problems(self, token=None):
        url = self.get_url("user_solved_problems")
        return self.client.get(url, headers={"Authorization": f"Token {token}"})

    def get_problems_list(self, token=None):
        url = self.get_url("problem_list")
        return self.client.get(url, headers={"Authorization": f"Token {token}"})

    def get_problem_detail(self, pk, token=None):
        url = self.get_url("problem_detail", pk=pk)
        return self.client.get(url, headers={"Authorization": f"Token {token}"})

    def get_problem_comments(self, pk, token=None):
        url = self.get_url("problem_comments", pk=pk)
        return self.client.get(url, headers={"Authorization": f"Token {token}"})

    def post_comment(self, pk, comment: str, token=None):
        url = self.get_url("problem_comments", pk=pk)
        return self.client.post(url, json={"comment": comment}, headers={"Authorization": f"Token {token}"})

    def get_topics(self, token=None):
        url = self.get_url("topic_list")
        return self.client.get(url, headers={"Authorization": f"Token {token}"})

    def get_testcases(self, problem_id, token=None):
        url = self.get_url("testcase_list", problem_id=problem_id)
        return self.client.get(url, headers={"Authorization": f"Token {token}"})

    def run_code(self, problem_id, python_file, token=None):
        url = self.get_url("run_code", problem_id=problem_id)
        return self.client.post(url, json={"python_file": python_file}, headers={"Authorization": f"Token {token}"})

    def get_code_running_result(self, problem_id, execution_id, token=None):
        url = self.get_url("get_code_running_result", problem_id=problem_id, execution_id=execution_id)
        return self.client.get(url, headers={"Authorization": f"Token {token}"})


# urlpatterns = [
# 	path("api-token-auth/", obtain_auth_token),
# 	path("sign-up/", auth.sign_up, name="sign_up"),
#   path("logout/", auth.logout, name="logout"),


#     # User-related paths
#     path("users/<int:pk>/", views.UserDetailView.as_view(), name="user_detail"),
    # path("users/me/update/", views.update_user_detail, name="update_user_detail"),
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