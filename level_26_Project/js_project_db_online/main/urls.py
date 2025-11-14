from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from shop.views import HomeView

urlpatterns = [
    path('administrator/', admin.site.urls),
    path('auth/', include('user.urls.urls_auth')),
    path('account/', include('user.urls.urls_account')),
    path('shop/', include('shop.urls')),
    path('admin/', include('adminapp.urls')),
    path('', HomeView.as_view(), name='home'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)