class Context:
    def __init__(self, page_name: str, is_authenticated: bool, error: str, data: dict={}) -> None:
        self.page_name = page_name
        self.is_authenticated = is_authenticated
        self.error = error
        self.data = data

    def get_dict(self):
        return {
            "page_name": self.page_name,
            "is_authenticated": self.is_authenticated,
            "error": self.error,
            **self.data
        }