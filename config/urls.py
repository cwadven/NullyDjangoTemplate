from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    path('custom_account/', include('custom_account.urls')),
]

urlpatterns += [
    path('__debug__/', include('debug_toolbar.urls')),
]
