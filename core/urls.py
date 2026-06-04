from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
 
urlpatterns = [
    path("admin/", admin.site.urls),
    # Cada app e dona das proprias rotas; o core so as inclui.
    path("api/", include("professionals.urls")),
    path("api/", include("consultations.urls")),
    # Autenticacao e transversal (nao pertence a um dominio), entao fica no core.
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]