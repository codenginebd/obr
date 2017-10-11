from django.http import JsonResponse
from generics.views.base_template_view import BaseTemplateView


class BaseRejectView(BaseTemplateView):
    model = None

    def get_object_ids(self, request):
        object_ids = []
        id_str = request.GET.get('id', "")
        id_list = id_str.split(',')
        object_ids = [int(_id) for _id in id_list if _id]
        return object_ids

    def get(self, request, *args, **kwargs):
        response = {
            "status": "FAILED"
        }
        if self.model:
            self.model.reject(id_list=self.get_object_ids(request=self.request))
            response["status"] = "SUCCESSFUL"
        return JsonResponse(response)
