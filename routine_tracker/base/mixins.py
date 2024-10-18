from routine_tracker.base.utils.modal import ModalOptions, trigger_modal


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
