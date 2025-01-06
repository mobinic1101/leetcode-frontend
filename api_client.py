from httpx import Client, QueryParams, Response
from http import HTTPStatus
from context import Context


class APIClient:
    def __init__(self, base_url="http://127.0.0.1:8000/api/"):
        self.base_url = base_url
        self.client = Client(base_url=base_url)
        self.headers = lambda token: {"Authorization": f"Token {token}"}

    def extract_data(self, response: Response, page_name: str="") -> Context:
        context = {
            "page_name": page_name,
            "is_authenticated": False,
            "error": "",
            "data": None
            }
        if response.status_code == HTTPStatus.NOT_FOUND:
            ...
        elif response.status_code == HTTPStatus.BAD_REQUEST:
            ...
        elif response.status_code == HTTPStatus.UNAUTHORIZED: # if invalid token
            ...

    def get(self, url, token, **query_params):
        response = self.client.get(url, self.headers(token), QueryParams(**query_params))
    

print(HTTPStatus.UNAUTHORIZED)