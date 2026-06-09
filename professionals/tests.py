from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from professionals.models import Professional

User = get_user_model()


class ProfessionalAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='tester', password='senha-123')
        self.client.force_authenticate(user=self.user)

        self.payload = {
            'social_name': 'Alex Andrade',
            'profession': 'MEDICINE',   
            'address': 'Rua das Flores, 100',
            'email': 'alex@exemplo.com',
            'phone': '45999990000',
        }
        self.professional = Professional.objects.create(**self.payload)
        self.list_url = '/api/v1/professionals/'
        self.detail_url = f'/api/v1/professionals/{self.professional.id}/'

    # ---- CRUD ----
    def test_list(self):
        resp = self.client.get(self.list_url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_create(self):
        novo = {**self.payload, 'email': 'outro@exemplo.com'}
        resp = self.client.post(self.list_url, novo, format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Professional.objects.count(), 2)

    def test_retrieve(self):
        resp = self.client.get(self.detail_url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['social_name'], 'Alex Andrade')

    def test_update(self):
        resp = self.client.patch(self.detail_url, {'social_name': 'Alex Souza'}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.professional.refresh_from_db()
        self.assertEqual(self.professional.social_name, 'Alex Souza')

    def test_delete(self):
        resp = self.client.delete(self.detail_url)
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Professional.objects.count(), 0)

    # ---- erros ----
    def test_create_missing_required_field(self):
        resp = self.client.post(self.list_url, {'profession': 'PSICOLOGIA'}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('social_name', resp.data)

    def test_create_invalid_email(self):
        bad = {**self.payload, 'email': 'nao-eh-email'}
        resp = self.client.post(self.list_url, bad, format='json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', resp.data)

    # ---- auth ----
    def test_write_requires_authentication(self):
        self.client.force_authenticate(user=None)  # desautentica
        resp = self.client.post(self.list_url, self.payload, format='json')
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)