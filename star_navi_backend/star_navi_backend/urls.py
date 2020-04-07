from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from s_network.views import Validation

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('s_network.urls')),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('auth/validate/', Validation.as_view())
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
