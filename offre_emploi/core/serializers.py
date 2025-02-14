# définir des sérializers qui transformeront tes objets Django en JSON.

# core/serializers.py
from rest_framework import serializers
from .models import JobOffer, JobSeekerProfile, Recruiter

class JobOfferSerializer(serializers.ModelSerializer):
    """ Sérialiseur pour les offres d'emploi. """
    
    class Meta:
        model = JobOffer
        exclude = ['salary']  # Exclure le champ salary

    def validate_title(self, value):
        """ Vérifie que le titre de l'offre n'est pas vide. """
        if not value.strip():
            raise serializers.ValidationError("Le titre de l'offre ne peut pas être vide.")
        return value
    
    def validate_description(self, value):
        """ Vérifie que la description n'est pas vide. """
        if not value.strip():
            raise serializers.ValidationError("La description ne peut pas être vide.")
        return value

class JobSeekerProfileSerializer(serializers.ModelSerializer):
    """ Sérialiseur pour les profils des chercheurs d'emploi. """
    
    class Meta:
        model = JobSeekerProfile
        fields = '__all__'

class RecruiterProfileSerializer(serializers.ModelSerializer):
    """ Sérialiseur pour les profils des recruteurs. """
    
    class Meta:
        model = Recruiter
        fields = '__all__'

