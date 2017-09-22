from django.http import JsonResponse
from generics.views.base_template_view import BaseTemplateView


class DeactivateBaseView(BaseTemplateView):
    model = None

    def get_object_ids(self, request):
        return []

    def get(self, request, *args, **kwargs):
        response = {
            "status": "FAILED"
        }
        if self.model:
            self.model.deactivate(id_list=self.get_object_ids())
            response["status"] = "SUCCESSFUL"
        return JsonResponse(response)
