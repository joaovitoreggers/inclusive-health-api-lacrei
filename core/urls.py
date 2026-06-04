from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

 
from professionals.views import ProfessionalViewSet
from consultations.views import ConsultationViewSet
 
router = DefaultRouter()
router.register(r"professionals", ProfessionalViewSet, basename="professional")
router.register(r"consultations", ConsultationViewSet, basename="consultation")
 
urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include(router.urls)),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
 