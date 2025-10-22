from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from tinymce import urls as tinymce_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('place.urls')),
    path('tinymce/', include(tinymce_urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
