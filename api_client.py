from httpx import Client, QueryParams, Response
from http import HTTPStatus
from context import Context


class APIClient:
    def __init__(self, base_url="http://127.0.0.1:8000/api"):
        self.base_url = base_url
        self.client = Client(base_url=base_url)
        self.headers = lambda token: {"Authorization": f"Token {token}"}

    def extract_data(self, response: Response, page_name: str = "") -> Context:
        context = {
            "page_name": page_name,
            "error": "",
            "data": None,
        }
        data = response.json()
        if (
            response.status_code == HTTPStatus.NOT_FOUND
            or response.status_code == HTTPStatus.BAD_REQUEST
            or response.status_code == HTTPStatus.UNAUTHORIZED
            or response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
        ):
            context["error"] = data.get("detail")
        elif response.status_code == HTTPStatus.OK:
            context["data"] = data

        return Context(**context)
    def get(self, url, token="", **query_params):
        if token:
            response = self.client.get(
                url, headers=self.headers(token), params=QueryParams(**query_params)
            )
        else:
            response = self.client.get(url=url, params=QueryParams(**query_params))
        return self.extract_data(response, url)
    
    def post(self, url, json=None, data=None, files=None, token=""):
        if token:
            response = self.client.post(
                url=url,
                headers=self.headers(token),
                json=json,
                data=data,
                files=files
            )
        else:
            response = self.client.post(url=url, json=json, data=data, files=files)
        return self.extract_data(response, url)


print(HTTPStatus.UNAUTHORIZED)
