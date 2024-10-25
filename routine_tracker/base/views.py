from django.views.generic import TemplateView


class DashboardView(TemplateView):
    def get_template_names(self) -> list[str]:
        if self.request.user.is_authenticated:
            return ["base/dashboard.html"]
        return ["base/index.html"]
