from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from fatcode import settings
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="fatcode API",
        default_version='v1',
        description="Test description",
    ),
    public=True,
)

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
    path('api/v1/swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-fatcode-ui')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
