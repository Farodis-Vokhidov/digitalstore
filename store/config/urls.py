
from django.shortcuts import redirect
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('digitalstore.urls')),
    path('i18n/', include('django.conf.urls.i18n')),
]

urlpatterns += i18n_patterns(
    path('category_products/', include('digitalstore.urls')),
    path('checkout/', include('digitalstore.urls')),
    path('login/', include('digitalstore.urls')),
    path('main/', include('digitalstore.urls')),
    path('my_cart/', include('digitalstore.urls')),
    path('orders_list/', include('digitalstore.urls')),
    path('product_detail/', include('digitalstore.urls')),
    path('product_list/', include('digitalstore.urls')),
    path('profile/', include('digitalstore.urls')),
    path('register/', include('digitalstore.urls')),
    path('search/', include('digitalstore.urls')),
    path('success/', include('digitalstore.urls')),
)


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    














