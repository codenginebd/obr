from engine.mixins.ajax_response_format_mixin import AjaxResponseFormatMixin
from engine.mixins.json_response_mixin import JSONResponseMixin


class AjaxRendererMixin(AjaxResponseFormatMixin, JSONResponseMixin):
    def render_json(self, data):
        data = self.ensure_status(data)
        return self.render_to_json(data)