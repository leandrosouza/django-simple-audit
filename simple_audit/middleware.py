# threadlocals middleware
from .models import AuditRequest

class TrackingRequestOnThreadLocalMiddleware(object):
    """Middleware that gets various objects from the
    request object and saves them in thread local storage."""
    def process_request(self, request):
        user = None if request.user.is_anonymous() else request.user
        #get real ip
        if 'HTTP_X_FORWARDED_FOR' in request.META:
            ip = request.META['HTTP_X_FORWARDED_FOR']
        elif 'Client-IP' in request.META:
            ip = request.META['Client-IP']
        else:
            ip = request.META['REMOTE_ADDR']
        AuditRequest.new_request(request.get_full_path(), user, ip)

    def process_response(self, request, response):
        AuditRequest.cleanup_request()
