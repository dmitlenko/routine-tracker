from django.http import HttpResponse


def forced_htmx_redirect(response: HttpResponse, url: str, code: int = 200) -> HttpResponse:
    """Forces an htmx redirect by setting the status code to 200 and adding the htmx redirect header.

    Args:
        response (HttpResponse): Response object.
        url (str): URL to redirect
        code (int, optional): Response code. Defaults to 200.

    Returns:
        HttpResponse: Response object.
    """

    response['HX-Redirect'] = url
    response.status_code = code
    return response
