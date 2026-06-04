import uuid
from django.db import models

class Consultation(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    professional = models.ForeignKey(
        'professionals.Professional',
        on_delete=models.PROTECT,
        related_name='consultations',
        verbose_name='professional'
    )

    date = models.DateTimeField(verbose_name='Data e Hora')

    created_at = models.DateTimeField(verbose_name='Criado em', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='atualizado em', auto_now=True)

    class Meta:
        verbose_name = 'consulta'
        verbose_name_plural = 'consultas'
        ordering = ['-date'] 
 
    def __str__(self):
        return f'Consulta de {self.professional} em {self.date:%d/%m/%Y %H:%M}'