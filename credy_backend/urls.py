from django.conf import settings
from django.conf.urls import include
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token

from users.api import CreateUserView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/login/', obtain_jwt_token, name='obtain_jwt_token'),
    path('auth/refresh-token/', refresh_jwt_token),
    path('auth/verify-token/', verify_jwt_token, name='api-jwt-verify'),
    path('user/registration', CreateUserView.as_view(), name='create_user'),
    path('', include('core.urls')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
