from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser

# Modèle utilisateur personnalisé
class User(AbstractUser):
    ROLE_CHOICES = (
        ('job_seeker', 'Chercheur d\'emploi'),
        ('recruiter', 'Recruteur'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    # Ajouter un related_name unique pour les relations groups et user_permissions
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',  # Changer le related_name ici
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions_set',  # Changer le related_name ici
        blank=True,
    )

    def __str__(self):
        return self.username

# Modèle pour les notifications
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.user.username} - {self.message}"

# Modèle pour les recruteurs
class Recruiter(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="recruiter_profile", limit_choices_to={'role': 'recruiter'})
    company_name = models.CharField(max_length=255)
    company_website = models.URLField(blank=True, null=True)
    contact_email = models.EmailField()

    def __str__(self):
        return f"{self.company_name} - {self.user.username}"

# Modèle pour les offres d'emploi
class JobOffer(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    contract_type = models.CharField(max_length=50)  # CDI, CDD, Freelance, etc.
    published_at = models.DateTimeField(auto_now_add=True)
    recruiter = models.ForeignKey(User, related_name='job_offers', on_delete=models.CASCADE, limit_choices_to={'role': 'recruiter'})

    def __str__(self):
        return self.title

# Modèle pour les profils des chercheurs d'emploi
class JobSeekerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', limit_choices_to={'role': 'job_seeker'})
    skills = models.TextField()  # Liste des compétences
    experience = models.TextField()  # Expérience professionnelle
    preferences = models.TextField()  # Préférences de recherche d'emploi

    def __str__(self):
        return f"{self.user.username}'s Profile"

# Modèle pour les candidatures
class Application(models.Model):
    job_offer = models.ForeignKey(JobOffer, on_delete=models.CASCADE)
    job_seeker = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'job_seeker'})
    application_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=[('pending', 'En attente'), ('accepted', 'Acceptée'), ('rejected', 'Refusée')], default='pending')

    def __str__(self):
        return f"{self.job_seeker.username} applied for {self.job_offer.title}"

# Modèle pour les recommandations
class Recommendation(models.Model):
    job_seeker = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'job_seeker'})
    job_offer = models.ForeignKey(JobOffer, on_delete=models.CASCADE)
    recommendation_score = models.FloatField()  # Score de pertinence de la recommandation

    def __str__(self):
        return f"Recommendation for {self.job_seeker.username} to {self.job_offer.title}"
