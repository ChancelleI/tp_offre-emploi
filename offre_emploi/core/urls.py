from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import JobOfferViewSet, JobSeekerProfileViewSet, RecruiterProfileViewSet, home, job_offers, job_offer_detail, register, login_view, logout_view
from .views import recruiter_dashboard, view_applications, candidate_dashboard, applied_jobs, postuler, publier_offre, apply_for_job


# Création d'un routeur pour les ViewSets
router = DefaultRouter()
router.register(r'joboffers', JobOfferViewSet, basename='joboffer')
router.register(r'jobseekers', JobSeekerProfileViewSet, basename='jobseeker')
router.register(r'recruiters', RecruiterProfileViewSet, basename='recruiter')

urlpatterns = [
    path('', home, name='home'),
    path('offres/', job_offers, name='job_offers'),  # Liste des offres
    path('offres/<int:offer_id>/', job_offer_detail, name='job_offer_detail'),  # Détail d'une offre
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),  # URLs pour authentification
    path('api/', include(router.urls)),  # Inclusion des routes API sous /api/
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    
    
    path('recruiter/dashboard/', recruiter_dashboard, name='recruiter_dashboard'),
    path('job_offer/<int:job_offer_id>/applications/', view_applications, name='view_applications'),
    path('candidate/dashboard/', candidate_dashboard, name='candidate_dashboard'),
    path('applied_jobs/', applied_jobs, name='applied_jobs'),
    path('postuler/<int:offer_id>/', postuler, name='postuler'),
    path('publier-offre/', publier_offre, name='publier_offre'),
    path('offres/<int:offer_id>/postuler/', apply_for_job, name='apply_for_job'),
]
