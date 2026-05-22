from django.shortcuts import redirect, render
from django.urls import reverse


class SessionExpiryRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.protected_prefixes = (
            '/dashboard/',
            '/viaturas/',
            '/quotas/',
            '/pagamentos/',
            '/tesouraria/',
        )
        self.exempt_paths = {
            '/',
            '/login/',
            '/registo/',
            '/logout/',
            '/sessao-expirada/',
        }

    def __call__(self, request):
        path = request.path
        has_session_cookie = bool(request.COOKIES.get('sessionid'))
        is_protected = any(path.startswith(prefix) for prefix in self.protected_prefixes)
        is_exempt = path in self.exempt_paths or path.startswith('/admin/') or path.startswith('/static/') or path.startswith('/media/')

        if is_protected and not request.user.is_authenticated and has_session_cookie and not is_exempt:
            return redirect(reverse('portal:session_expired'))

        response = self.get_response(request)

        if response.status_code == 404 and not is_exempt:
            return render(request, 'portal/404.html', status=404)

        return response
