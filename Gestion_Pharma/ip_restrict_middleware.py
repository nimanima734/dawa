# ip_restrict_middleware.py
from django.http import HttpResponseForbidden

# هنا تحط قائمة عناوين الـ IP المسموح بها
ALLOWED_IPS = [
    '192.168.8.114',   # مثال IP داخل
    '192.168.8.117',
    '192.168.8.140',
    '192.168.8.132',
    '154.255.21.18',
 


]

class RestrictIPMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip = self.get_client_ip(request)
        if ip not in ALLOWED_IPS:
            return HttpResponseForbidden("<h1>403 - Accès refusé</h1>")
        return self.get_response(request)

    def get_client_ip(self, request):
        """تحصل على عنوان IP الحقيقي حتى لو كان فيه proxy"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

