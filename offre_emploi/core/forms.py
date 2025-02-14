from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import User, JobOffer, Application  # 🔹 Ajout de JobOffer ici

User = get_user_model()
class CustomUserCreationForm(UserCreationForm):
    role_choices = [
        ('candidate', 'Candidat'),
        ('recruiter', 'Recruteur'),
    ]
    role = forms.ChoiceField(choices=User.ROLE_CHOICES, label="Rôle", widget=forms.Select())

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'role']

# 🔹 Ajout du formulaire pour créer une offre d'emploi
class JobOfferForm(forms.ModelForm):
    class Meta:
        model = JobOffer
        fields = ['title', 'company', 'description', 'location', 'contract_type', 'salary']

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ["resume", "cover_letter"]
