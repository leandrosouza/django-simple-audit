# threadlocals middleware
import uuid
from threading import local

all = ['get_current_user', 'get_current_request_id', 'get_current_request']
_thread_locals = local()


def get_current_request():
    return getattr(_thread_locals, 'request', None)


def get_current_user():
    return getattr(get_current_request(), 'user', None)


def get_current_request_id():
    return getattr(get_current_request(), 'request_id', None)


class RequestThreadLocalMiddleware(object):
    """Middleware that gets various objects from the
    request object and saves them in thread local storage."""
    def process_request(self, request):
        # generate request_id
        setattr(request, 'request_id', self.__generate_id())
        _thread_locals.request = request

    def process_response(self, request, response):
        _thread_locals.request = None
        del _thread_locals.request
        return response

    def __generate_id(self):
            return uuid.uuid4().hex
