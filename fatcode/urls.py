from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from fatcode import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('courses/', include('src.courses.urls')),
    path('questions/', include('src.questions.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('api/v1/', include('src.profiles.urls'))
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
