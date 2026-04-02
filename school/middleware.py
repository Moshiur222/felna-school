from django.utils.deprecation import MiddlewareMixin
from .models import Visitor

class VisitorTrackingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        ip = get_client_ip(request)
        session_key = request.session.session_key or request.session.create()
        user_agent = request.META.get('HTTP_USER_AGENT', '')

        # Check if this session already visited today
        from django.utils import timezone
        today = timezone.now().date()
        if not Visitor.objects.filter(session_key=session_key, visited_at__date=today).exists():
            Visitor.objects.create(ip_address=ip, user_agent=user_agent, session_key=session_key)

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
