# core/tests/test_models.py
import pytest
from django.contrib.auth import get_user_model
from core.models import JobOffer, Recruiter

@pytest.mark.django_db
def test_create_job_offer():
    # Créer un utilisateur recruteur
    user = get_user_model().objects.create_user(
        username='recruiter1', password='password', role='recruiter'
    )
    recruiter = Recruiter.objects.create(
        user=user, company_name='TechCompany', contact_email='contact@techcompany.com'
    )
    
    # Créer une offre d'emploi
    job_offer = JobOffer.objects.create(
        title='Data Engineer',
        description='Offre pour un Data Engineer',
        location='Paris',
        contract_type='CDI',
        recruiter=user
    )
    
    # Vérifier que l'offre d'emploi a bien été créée
    assert job_offer.title == 'Data Engineer'
    assert job_offer.recruiter == user
    assert job_offer.location == 'Paris'
