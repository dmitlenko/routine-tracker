from django.http import HttpResponse


def file_response(file_name: str, content_type: str) -> HttpResponse:
    response = HttpResponse(content_type=content_type)
    response["Content-Disposition"] = f"attachment;filename={file_name}"
    return response
