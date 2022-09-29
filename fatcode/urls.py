from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.conf import settings

from .yasg import urlpatterns as doc_urls


urlpatterns = [
    path('api/v1/admin/', admin.site.urls),
    path('api/v1/ckeditor/', include('ckeditor_uploader.urls')),
    path('api/v1/api-auth/', include('rest_framework.urls')),
    path('api/v1/auth/', include('djoser.urls')),
    path('api/v1/auth/', include('djoser.urls.authtoken')),
    path('api/v1/profiles/', include('src.profiles.urls')),
    path('api/v1/knowledge/', include('src.knowledge.urls')),
    path('api/v1/courses/', include('src.courses.urls')),
    path('api/v1/questions/', include('src.questions.urls')),
    path('api/v1/team/', include('src.questions.urls')),
]

urlpatterns += doc_urls

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
