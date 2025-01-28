class Context:
    def __init__(self, page_name: str=None, error: str=None, data: dict={}):
        self.page_name = page_name
        self.error = error
        self.data = data
        if not data:
            self.data = {}

    def get_dict(self):
        """
        get a dictionary representation of the object,
        if data is a list the scheme will look like this:
        {
            "page_name": self.page_name,
            "error": self.error,
            "items": self.data
        }
        if not (if data was a dict) it will look like this:
        {
            "page_name": self.page_name,
            "error": self.error,
            **self.data
        }
        """
        data = {
            "error": self.error,
        }
        if isinstance(self.data, dict):
            data.update({**self.data})
        else:
            data["items"] = self.data
        
        return data