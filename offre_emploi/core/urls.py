
# core/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import JobOfferViewSet, JobSeekerProfileViewSet, RecruiterProfileViewSet

router = DefaultRouter()
router.register(r'joboffers', JobOfferViewSet)
router.register(r'jobseekerprofile', JobSeekerProfileViewSet)
router.register(r'recruiterprofile', RecruiterProfileViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
