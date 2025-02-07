# définir des sérializers qui transformeront tes objets Django en JSON.

# core/serializers.py
from rest_framework import serializers
from .models import JobOffer, JobSeekerProfile, Recruiter

class JobOfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobOffer
        fields = '__all__'

class JobSeekerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobSeekerProfile
        fields = '__all__'

class RecruiterProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recruiter
        fields = '__all__'

