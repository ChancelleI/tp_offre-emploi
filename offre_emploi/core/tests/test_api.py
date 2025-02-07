# core/tests/test_api.py
import pytest
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

@pytest.mark.django_db
def test_create_job_offer():
    # Créer un utilisateur recruteur
    user = get_user_model().objects.create_user(
        username='recruiter1', password='password', role='recruiter'
    )
    
    # Authentifier l'utilisateur pour obtenir un token JWT
    client = APIClient()
    client.login(username='recruiter1', password='password')
    
    # URL de l'API pour créer une offre d'emploi
    url = reverse('joboffer-list')  # Assure-toi que 'joboffer-list' correspond à ta route d'API
    data = {
        'title': 'Data Scientist',
        'description': 'Description de l\'offre',
        'location': 'Paris',
        'contract_type': 'CDI',
    }
    
    # Envoyer la requête POST pour créer une nouvelle offre d'emploi
    response = client.post(url, data, format='json')
    
    # Vérifier que l'offre d'emploi a bien été créée
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['title'] == 'Data Scientist'
    assert response.data['location'] == 'Paris'
