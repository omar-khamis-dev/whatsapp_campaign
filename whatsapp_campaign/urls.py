from django.urls import path, include
from django.contrib import admin

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),  # لتغيير اللغة من النموذج
    path('admin/', admin.site.urls),
    path('', include('campaign.urls')),  # تطبيقك الأساسي
]
