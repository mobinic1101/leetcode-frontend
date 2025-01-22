from werkzeug.datastructures import FileStorage
from io import BufferedReader


def extract_form_data(request):
    """Extract form data from a request"""
    form = request.form
    data = {key: val for key, val in form.items()}
    return data


get_authorization_header = lambda token: {"Authorization": f"Token {token}"}


def convert_to_regular_file(file: FileStorage):
    """converts FileStorage files to regular files like the output of open() function.
    so we can upload the on the server without issues like we had before.

    Args:
        file (FileStorage): the file you got form request.files.get()

    Returns:
        file (BufferedReader): __description__
    """    
    file.name = file.filename
    file = BufferedReader(file)
    return file