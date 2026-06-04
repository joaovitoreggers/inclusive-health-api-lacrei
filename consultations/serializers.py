from django.utils import timezone
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator


from .models import Consultation


class ConsultationSerializer(serializers.ModelSerializer):


    class Meta:
        model = Consultation
        fields = [
            "id",
            "professional",   
            "data",           
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]
        validators = [
        UniqueTogetherValidator(
            queryset=Consultation.objects.all(),
            fields=["professional", "date"],
            message="Este profissional já tem consulta nesse horário.",
        )
    ]

    
    def validate_data(self, value):
        if value < timezone.now():
            raise serializers.ValidationError("A consulta não pode ser no passado.")
        return value
    
    