from django.db import models

class Professional(models.Model):


    class Professions(models.TextChoices):
        MEDICINE = 'MEDICINE', 'Medicine'
        PSYCHOLOGY = 'PSYCHOLOGY', 'Psychology'
        NURSING = 'NURSING', 'Nursing'
        NUTRITION = "NUTRITION", "Nutrition"
        PHYSIOTHERAPY = 'PHYSIOTHERAPY', 'Physiotherapy'
        SOCIAL_SERVICE = 'SOCIAL_SERVICE', 'Social Service'
        DENTISTRY = 'DENTISTRY', 'Dentistry'
        OTHER = 'OTHER', 'Other'

    social_name = models.CharField(
        verbose_name='Nome Social', 
        max_length=255
    )

    profession = models.CharField(
        verbose_name='Profissão',
        choices=Professions.choices
    )

    address = models.CharField(
        verbose_name='Endereço',
        max_length=255
    )

    email = models.EmailField(verbose_name='Email')

    phone = models.CharField(
        verbose_name='Telefone',
        max_length=20
    )

    created_at = models.DateTimeField(
        'Criado em', 
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        'Atualizado em', 
        auto_now=True
    )

    class Meta:
        verbose_name = 'profissional'
        verbose_name_plural = 'profissionais'
        ordering = ['social_name']
 
    def __str__(self):
        return self.social_name