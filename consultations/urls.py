from rest_framework.routers import SimpleRouter
 
from .views import ConsultationViewSet
 
router = SimpleRouter()
router.register(r'consultations', ConsultationViewSet, basename='consultation')
 
urlpatterns = router.urls
 