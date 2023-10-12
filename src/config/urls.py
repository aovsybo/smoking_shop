from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from config.yasg import urlpatterns as doc_urls


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('users.api.urls')),
    path('api/v1/', include('products.api.urls')),
    path('api/v1/', include('cart.api.urls')),
]
urlpatterns += doc_urls
if settings.DEBUG:
    urlpatterns += (
            static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) +
            static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    )
