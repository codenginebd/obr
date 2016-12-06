import threading


class BRRequestMiddleware(object):
    _request = {}

    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        self.__class__.set_request(request)
        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response

    """
        Always have access to the current request
        """

    def process_request(self, request):
        """
        Store request
        """
        self.__class__.set_request(request)

    def process_response(self, request, response):
        """
        Delete request
        """
        self.__class__.del_request()
        return response

    def process_exception(self, request, exception):
        """
        Delete request
        """
        self.__class__.del_request()

    @classmethod
    def get_request(cls, default=None):
        """
        Retrieve request
        """
        return cls._request.get(threading.current_thread(), default)

    @classmethod
    def set_request(cls, request):
        """
        Store request
        """
        cls._request[threading.current_thread()] = request

    @classmethod
    def del_request(cls):
        """
        Delete request
        """
        cls._request.pop(threading.current_thread(), None)
