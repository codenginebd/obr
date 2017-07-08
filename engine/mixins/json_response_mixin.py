from django.http.response import HttpResponse
import json


class JSONResponseMixin(object):
    def render_to_json(self, data):
        return HttpResponse(json.dumps(data))
