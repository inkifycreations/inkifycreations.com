from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from api.views import LoginPageView, SignupPageView, ProductPageView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    re_path(r'^(?!api/|admin/|static/|media/).*$', TemplateView.as_view(template_name='index.html'), name='spa'),
]

# Serve uploaded media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
