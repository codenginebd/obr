from django.conf import settings
from django.utils import translation

class LanguageMiddleware(object):

    def process_request(self, request):
        if hasattr(request, 'session'):
            language = request.session.get('CURRENT_LANGUAGE', settings.LANGUAGE_CODE)
        else:
            language = settings.LANGUAGE_CODE
        translation.activate(language)

        request.LANGUAGE_CODE = translation.get_language()