from flask import request
from httpx import Client, QueryParams, Response
from http import HTTPStatus
from context import Context
import settings


class APIClient:
    def __init__(self, base_url=settings.DRF_HOST):
        self.base_url_raw = base_url
        self.base_url = base_url + "/api"
        self.client = Client(base_url=self.base_url)
        self.headers = lambda token: {"Authorization": f"Token {token}"}

    def extract_data(self, response: Response, page_name: str = "") -> Context:
        context = {
            "page_name": page_name,
            "error": "",
            "data": None,
        }
        # print("RESPONSE CONTENT: ", response.content)
        data = response.json()
        # print("BACKEND RESPONSE: ", data)
        if (
            response.status_code == HTTPStatus.NOT_FOUND
            or response.status_code == HTTPStatus.BAD_REQUEST
            or response.status_code == HTTPStatus.UNAUTHORIZED
            or response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
        ):
            context["error"] = data.get("detail")
            if data.get("non_field_errors", None):
                context["error"] = data["non_field_errors"][0]

        elif response.status_code == HTTPStatus.OK:
            context["data"] = data

        return Context(**context)

    def get(self, url, token="", extract_data=False, query_params: dict={}):
        if token:
            response = self.client.get(
                url, headers=self.headers(token), params=query_params
            )
        else:
            response = self.client.get(url=url, params=query_params)
        if extract_data:
            return self.extract_data(response, url)
        return response

    def post(self, url, json={}, data=None, files=None, token="", extract_data=True):
        if token:
            response = self.client.post(
                url=url, headers=self.headers(token), json=json, data=data, files=files
            )
        else:
            response = self.client.post(url=url, json=json, data=data, files=files)
        if extract_data:
            return self.extract_data(response, url)
        return response

    def get_quick_user_details(self):
        """
        Retrieves quick user details from the server using an authentication token
        stored in the user's cookies. If the token is valid, it returns the user's
        username, profile picture URL, and authentication status. If the token is
        missing or invalid, it returns default values indicating the user is not
        authenticated.

        Returns:
            dict: A dictionary containing the user's username, profile picture URL,
                and authentication status.
                example output if authenticated (if not the is_authenticated will be False and username will be None):
                {
                    "username": "someusername",
                    "profile_pic": "http://127.0.0.1:8000/media/profile_pics/someprofile.jpg",
                    "is_authenticated": True
                }
        """
        quick_user_details = {
            "is_authenticated": False,
        }
        token = request.cookies.get("token")
        print("TOKEN: ", token)
        if token:
            response: Response = self.client.get(
                "/users/me/",
                headers=self.headers(request.cookies.get("token")),
                params={"quick": "yes"},
            )
            if response.status_code == 200:
                data = response.json()
                data["profile_pic"] = self.base_url_raw + data["profile_pic"] # "http://127.0.0.1:8000/media/profile_pics/someprofile.jpg"
                quick_user_details.update(data)
                # quick_user_details["username"] = data["username"]
                quick_user_details["is_authenticated"] = True
        return quick_user_details
