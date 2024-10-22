from typing import Any

from django.utils.translation import gettext as _

from routine_tracker.base.utils.modal import ModalOptions, close_modal, trigger_modal


class ModalMixin:
    """Mixin to trigger a modal on GET request"""

    modal_options: ModalOptions = {}
    trigger_on_response: bool = True

    def get_modal_options(self) -> ModalOptions:
        return self.modal_options

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        if self.trigger_on_response:
            return trigger_modal(response, self.get_modal_options())
        return response


class ModalFormMixin(ModalMixin):
    title: str = ""
    button_text: str = ""
    form_url: str = ""
    form_id: str = ""

    def get_form_url(self) -> str:
        return self.form_url

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "title": self.title,
                "button_text": self.button_text,
                "form_url": self.get_form_url(),
                "form_id": self.form_id,
            }
        )
        return context

    def form_valid(self, form) -> Any:
        return close_modal(super().form_valid(form))


class ModalDeleteMixin(ModalFormMixin):
    callback: str = ""
    button_text: str = _("Delete")
    template_name = 'core/confirm_delete.html'
    message: str = _("Are you sure you want to delete this item?")

    def get_callback(self) -> str:
        return self.callback

    def get_form_url(self) -> str:
        return self.request.path

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context.update(
            {
                'callback': self.get_callback(),
                'message': self.message,
            }
        )
        return context

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        response.status_code = 204
        return close_modal(response)
