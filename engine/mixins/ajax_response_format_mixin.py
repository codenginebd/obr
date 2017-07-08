from engine.exceptions.br_exception import BRException


class AjaxResponseFormatMixin(object):
    response = {
        "status": "FAILURE",
        "data": None,
        "message": None,
        "code": None
    }

    def ensure_status(self, data):
        if data and not data.get('status'):
            raise BRException("Ajax response does not contain status field")
        return data
