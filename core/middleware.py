from django.shortcuts import redirect
from django.urls import reverse
from django.conf import settings

class PremiumContentMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        response = self.get_response(request)
        return response
        
    def process_view(self, request, view_func, view_args, view_kwargs):
        # Skip for these URLs
        if request.path.startswith('/admin/') or request.path.startswith('/accounts/'):
            return None
            
        # Check for premium content access
        if hasattr(request, 'resolver_match') and request.resolver_match.url_name == 'post_detail':
            post_slug = view_kwargs.get('slug')
            if post_slug:
                from content.models import Post
                try:
                    post = Post.objects.get(slug=post_slug)
                    if post.access_level == 'PR' and not request.user.is_authenticated:
                        return redirect(f"{reverse('account_login')}?next={request.path}")
                    if post.access_level == 'PR' and not request.user.is_premium:
                        return redirect(reverse('subscribe'))
                except Post.DoesNotExist:
                    pass
        return None