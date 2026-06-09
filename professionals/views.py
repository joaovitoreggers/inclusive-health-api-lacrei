from rest_framework.permissions import IsAuthenticatedOrReadOnly

from rest_framework import viewsets

from .models import Professional
from .serializers import ProfessionalSerializer


class ProfessionalViewSet(viewsets.ModelViewSet):

    permission_classes=[IsAuthenticatedOrReadOnly]
    queryset = Professional.objects.all()
    serializer_class = ProfessionalSerializer
