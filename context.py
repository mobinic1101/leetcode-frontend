class Context:
    def __init__(self, page_name: str=None, error: str=None, data: dict={"is_authenticated": False}):
        self.page_name = page_name
        self.error = error
        self.data = data
        if not data:
            self.data = {}

    def get_dict(self):
        return {
            "page_name": self.page_name,
            "error": self.error,
            **self.data
        }