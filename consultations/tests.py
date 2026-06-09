import uuid
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from professionals.models import Professional
from consultations.models import Consultation

User = get_user_model()


class ConsultationAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='tester', password='senha-123')
        self.client.force_authenticate(user=self.user)

        self.professional = Professional.objects.create(
            social_name='Alex Andrade', profession='PSICOLOGIA',
            address='Rua 1', email='alex@exemplo.com', phone='45999990000',
        )
        self.other = Professional.objects.create(
            social_name='Bia Costa', profession='MEDICINA',
            address='Rua 2', email='bia@exemplo.com', phone='45988880000',
        )
        self.date = timezone.now() + timedelta(days=1)
        self.consultation = Consultation.objects.create(
            professional=self.professional, date=self.date,
        )
        self.list_url = '/api/v1/consultations/'
        self.detail_url = f'/api/v1/consultations/{self.consultation.id}/'

    @staticmethod
    def _results(resp):
        return resp.data['results'] if isinstance(resp.data, dict) else resp.data

    def test_list(self):
        resp = self.client.get(self.list_url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_create(self):
        payload = {
            'professional': str(self.professional.id),
            'date': (timezone.now() + timedelta(days=2)).isoformat(),
        }
        resp = self.client.post(self.list_url, payload, format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Consultation.objects.count(), 2)

    def test_retrieve(self):
        resp = self.client.get(self.detail_url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_update(self):
        nova_data = (timezone.now() + timedelta(days=3)).isoformat()
        resp = self.client.patch(self.detail_url, {'date': nova_data}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_delete(self):
        resp = self.client.delete(self.detail_url)
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Consultation.objects.count(), 0)

    def test_search_by_professional(self):
        Consultation.objects.create(
            professional=self.other, date=timezone.now() + timedelta(days=5),
        )
        resp = self.client.get(self.list_url, {'professional': self.professional.id})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        for item in self._results(resp):
            self.assertEqual(item['professional'], self.professional.id)

    def test_search_invalid_professional_id(self):
        resp = self.client.get(self.list_url, {'professional': 'nao-eh-uuid'})
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    # ---- erros ----
    def test_create_missing_date(self):
        resp = self.client.post(
            self.list_url, {'professional': str(self.professional.id)}, format='json'
        )
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('date', resp.data)

    def test_create_nonexistent_professional(self):
        payload = {
            'professional': str(uuid.uuid4()),
            'date': (timezone.now() + timedelta(days=2)).isoformat(),
        }
        resp = self.client.post(self.list_url, payload, format='json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_duplicate_consultation(self):
        payload = {
            'professional': str(self.professional.id),
            'date': self.date.isoformat(),  
        }
        resp = self.client.post(self.list_url, payload, format='json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    # ---- auth ----
    def test_requires_authentication(self):
        self.client.force_authenticate(user=None)
        resp = self.client.get(self.list_url)
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)