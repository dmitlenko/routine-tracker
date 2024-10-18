from routine_tracker.base.utils.modal import ModalOptions, trigger_modal


class ModalMixin:
    modal_id: str = "modal"
    modal_options: ModalOptions = {}
    trigger_on_response: bool = True

    def get_modal_id(self) -> str:
        return self.modal_id

    def get_modal_options(self) -> ModalOptions:
        return self.modal_options

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["modal_id"] = self.get_modal_id()
        return context

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        if self.trigger_on_response:
            return trigger_modal(response, self.get_modal_id(), self.get_modal_options())
        return response
