# core/tests/test_permissions.py
import pytest
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient
from core.models import JobOffer

@pytest.mark.django_db
def test_job_seeker_permission():
    # Créer un utilisateur chercheur d'emploi
    job_seeker = get_user_model().objects.create_user(
        username='jobseeker1', password='password', role='job_seeker'
    )
    
    # Créer une offre d'emploi pour un recruteur
    recruiter = get_user_model().objects.create_user(
        username='recruiter1', password='password', role='recruiter'
    )
    job_offer = JobOffer.objects.create(
        title='Data Engineer',
        description='Offre pour un Data Engineer',
        location='Paris',
        contract_type='CDI',
        recruiter=recruiter
    )
    
    # Authentifier le chercheur d'emploi
    client = APIClient()
    client.login(username='jobseeker1', password='password')
    
    # Essayer d'accéder à une offre d'emploi (devrait échouer)
    url = f"/api/joboffers/{job_offer.id}/"
    response = client.get(url)
    
    # Vérifier que l'accès est interdit
    assert response.status_code == status.HTTP_403_FORBIDDEN
