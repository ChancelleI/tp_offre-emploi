from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.conf import settings

# Modèle utilisateur personnalisé
class User(AbstractUser):
    ROLE_CHOICES = (
        ('job_seeker', 'Chercheur d\'emploi'),
        ('recruiter', 'Recruteur'),
    )
    username = models.CharField(max_length=150, unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, db_index=True)
    # Ajouter un related_name unique pour éviter les conflits avec AbstractUser
    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_set',  # Un related_name unique
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_permissions_set',  # Un related_name unique
        blank=True,
    )

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip() or self.username

    def __str__(self):
        return self.get_full_name()

# Modèle pour les notifications
class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notifications")
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Notification for {self.user.username} - {self.message[:30]}..."

# Modèle pour les recruteurs
class Recruiter(models.Model):
   user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
   company_name = models.CharField(max_length=255)
   company_website = models.URLField(blank=True, null=True)
   contact_email = models.EmailField()

   def __str__(self):
        return self.user.username  # Permet d'afficher le nom du recruteur

# Modèle pour les offres d'emploi
class JobOffer(models.Model):
    CONTRACT_TYPES = (
        ('CDI', 'CDI'),
        ('CDD', 'CDD'),
        ('Freelance', 'Freelance'),
        ('Stage', 'Stage'),
        ('Alternance', 'Alternance'),
    )

    title = models.CharField(max_length=255)
    company = models.CharField(max_length=255, blank=True, null=True) 
    description = models.TextField()
    location = models.CharField(max_length=255)
    contract_type = models.CharField(max_length=50, choices=CONTRACT_TYPES, db_index=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    published_at = models.DateTimeField(auto_now_add=True)
    recruiter = models.ForeignKey(Recruiter, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-published_at']

    def __str__(self):
        return self.title

# Modèle pour les profils des chercheurs d'emploi
class JobSeekerProfile(models.Model):
   user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
   skills = models.TextField()  # Liste des compétences
   experience = models.TextField()  # Expérience professionnelle
   preferences = models.TextField()  # Préférences de recherche d'emploi

def __str__(self):
        return f"{self.user.get_full_name()} - Profile"

# Modèle pour les candidatures
from django.db import models
from django.contrib.auth.models import User

class Application(models.Model):
    STATUS_CHOICES = [
        ('pending', 'En attente'),
        ('accepted', 'Acceptée'),
        ('rejected', 'Refusée'),
    ]

    job_offer = models.ForeignKey("JobOffer", on_delete=models.CASCADE, related_name="applications")
    job_seeker = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    resume = models.FileField(upload_to="resumes/", null=True, blank=True)  # Ajout du CV
    cover_letter = models.TextField(null=True, blank=True)  # Ajout de la lettre de motivation
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()  # Nouveau champ pour l'email
    application_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending', db_index=True)

    class Meta:
        unique_together = ('job_offer', 'job_seeker')  # Empêche un candidat de postuler deux fois à la même offre
        ordering = ['-application_date']

    def __str__(self):
        return f"{self.job_seeker.username} applied for {self.job_offer.title}"


# Modèle pour les recommandations
class Recommendation(models.Model):
    job_seeker = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    job_offer = models.ForeignKey(JobOffer, on_delete=models.CASCADE)
    recommendation_score = models.FloatField()  # Score de pertinence de la recommandation

    class Meta:
        ordering = ['-recommendation_score']

    def __str__(self):
        return f"Recommendation for {self.job_seeker.username} to {self.job_offer.title} ({self.recommendation_score:.2f})"
