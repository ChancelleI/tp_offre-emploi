
# core/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import JobOfferViewSet, JobSeekerProfileViewSet, RecruiterProfileViewSet, home

# Création d'un routeur pour les ViewSets
router = DefaultRouter()
router.register(r'joboffers', JobOfferViewSet, basename='joboffer')
router.register(r'jobseekers', JobSeekerProfileViewSet, basename='jobseeker')
router.register(r'recruiters', RecruiterProfileViewSet, basename='recruiter')

urlpatterns = [
    path('', include(router.urls)),  # Inclusion des routes API sous /api/
    # path('', home, name='home'),  # Redirection vers les offres d'emploi
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),  # URLs pour authentification
]

