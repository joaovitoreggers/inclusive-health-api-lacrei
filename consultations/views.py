import uuid

from rest_framework import viewsets
from rest_framework.exceptions import ValidationError

from .models import Consultation
from .serializers import ConsultationSerializer


class ConsultationViewSet(viewsets.ModelViewSet):


    serializer_class = ConsultationSerializer

    def get_queryset(self):

        queryset = Consultation.objects.select_related('professional')

        professional_id = self.request.query_params.get('professional')
        if professional_id:

            try:
                uuid.UUID(professional_id)
            except ValueError:
                raise ValidationError(
                    {'professional': 'ID de profissional inválido.'}
                )
            queryset = queryset.filter(professional_id=professional_id)

        return queryset