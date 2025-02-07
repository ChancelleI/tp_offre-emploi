from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from .models import JobOffer, JobSeekerProfile, Recruiter
from .serializers import JobOfferSerializer, JobSeekerProfileSerializer, RecruiterProfileSerializer
from rest_framework.permissions import AllowAny


class JobOfferViewSet(viewsets.ModelViewSet):
    queryset = JobOffer.objects.all()
    serializer_class = JobOfferSerializer
    # permission_classes = [IsAuthenticated]  # Assure-toi que l'utilisateur est authentifié
    permission_classes = [AllowAny]  # Autorise l'accès sans authentification

    @action(detail=True, methods=['get'])
    def custom_action(self, request, pk=None):
        job_offer = self.get_object()
        # Ajouter une action personnalisée si nécessaire
        return Response({"detail": "Custom Action for Job Offer"})

class JobSeekerProfileViewSet(viewsets.ModelViewSet):
    queryset = JobSeekerProfile.objects.all()
    serializer_class = JobSeekerProfileSerializer
    permission_classes = [IsAuthenticated]

class RecruiterProfileViewSet(viewsets.ModelViewSet):
    queryset = Recruiter.objects.all()
    serializer_class = RecruiterProfileSerializer
    permission_classes = [IsAuthenticated]

# def home(request):
#     return HttpResponse("Bienvenue sur le système d'offres d'emploi !")

