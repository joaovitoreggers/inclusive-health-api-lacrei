from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
 
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('professionals.urls')),
    path('api/v1/', include('consultations.urls')),
    path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]