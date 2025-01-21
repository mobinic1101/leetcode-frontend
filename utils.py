def extract_form_data(request):
    """Extract form data from a request"""
    form = request.form
    data = {key: val for key, val in form.items()}
    return data


get_authorization_header = lambda token: {"Authorization": f"Token {token}"}