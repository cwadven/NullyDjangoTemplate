from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path, include
from django.conf import settings

from config.views import home

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', home, name='home'),

    path('account/', include('allauth.urls')),

    path('custom_account/', include('custom_account.urls')),
    path('banner/', include('banner.urls')),
    path('cart/', include('cart.urls')),
    path('order/', include('order.urls')),
    path('product/', include('product.urls')),
    path('popup/', include('popup.urls')),
]

urlpatterns += [
    path('__debug__/', include('debug_toolbar.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
