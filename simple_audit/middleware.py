# threadlocals middleware
from .models import AuditRequest

class TrackingRequestOnThreadLocalMiddleware(object):
    """Middleware that gets various objects from the
    request object and saves them in thread local storage."""
    def process_request(self, request):
        if not request.user.is_anonymous():
            #get real ip
            if 'HTTP_X_FORWARDED_FOR' in request.META:
                ip = request.META['HTTP_X_FORWARDED_FOR']
            elif 'Client-IP' in request.META:
                ip = request.META['Client-IP']
            else:
                ip = request.META['REMOTE_ADDR']
            ip = ip.split(",")[0]
            AuditRequest.new_request(request.get_full_path(), request.user, ip)

    def process_response(self, request, response):
        AuditRequest.cleanup_request()
        return response
