from django.http import HttpResponse


def forced_htmx_redirect(response: HttpResponse, url: str, code: int = 200, soft: bool = False) -> HttpResponse:
    """Forces an htmx redirect by setting the status code to 200 and adding the htmx redirect header.

    Args:
        response (HttpResponse): Response object.
        url (str): URL to redirect
        code (int, optional): Response code. Defaults to 200.
        soft (bool, optional): If True, uses HX-Location header instead of HX-Redirect. Defaults to False.

    Returns:
        HttpResponse: Response object.
    """
    header = 'HX-Redirect' if not soft else 'HX-Location'

    response[header] = url
    response.status_code = code
    return response


def custom_swap(
    response: HttpResponse,
    swap: str = None,
    target: str = None,
    select: str = None,
    *,
    status_code: int = 200,
    headers: dict = None,
) -> HttpResponse:
    """Custom htmx swap response.

    See https://htmx.org/reference/#response_headers for more information.

    Args:
        response (HttpResponse):
            Response object.
        swap (str):
            Allows you to specify how the response will be swapped. Defaults to None.
        target (str):
            A CSS selector that updates the target of the content update to a different element on the page.
            Defaults to None.
        select (str):
            A CSS selector that allows you to choose which part of the response is used to be swapped in.
            Defaults to None.
        status_code (int, optional):
            Response status code. Defaults to 200.
        headers (dict, optional):
            Additional headers to add to the response. Defaults to None.

    Returns:
        HttpResponse: Updated response object.
    """

    if swap:
        response.headers.setdefault('HX-Reswap', swap)

    if target:
        response.headers.setdefault('HX-Retarget', target)

    if select:
        response.headers.setdefault('HX-Reselect', select)

    if headers:
        for key, value in headers.items():
            response.headers.setdefault(key, value)

    response.status_code = status_code
    return response
