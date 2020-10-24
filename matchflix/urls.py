from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings

from accounts import views
from accounts.views import RegistrationView, ProfileView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('flix.urls')),
    path('accounts/', include('accounts.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
