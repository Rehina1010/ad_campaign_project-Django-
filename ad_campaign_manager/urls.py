from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path, include
from django.urls import path, re_path
from django.views.static import serve
from django.conf import settings
from django.conf.urls.static import static


def redirect_to_home(request):
    return redirect('users:home')


urlpatterns = [
    path('accounts/confirm-email/', redirect_to_home),
    path('', redirect_to_home),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('users/', include('users.urls')),
    path('campaigns/', include('campaigns.urls')),
    path('generate/', include('image_generator.urls')),
    path('trends/', include('google_trends.urls')),
    re_path(r'^robots\.txt$', serve, {'path': 'robots.txt', 'document_root': settings.STATICFILES_DIRS[0]}),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
