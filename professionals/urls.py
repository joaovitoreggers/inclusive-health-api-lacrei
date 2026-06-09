from rest_framework.routers import SimpleRouter
 
from .views import ProfessionalViewSet
 
router = SimpleRouter()
router.register(r'professionals', ProfessionalViewSet, basename='professional')
 
urlpatterns = router.urls
 