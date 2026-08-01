from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('messe.urls')),
]

# Render uchun media fayllarni ochib berish
if settings.DEBUG:
  urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
  urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)