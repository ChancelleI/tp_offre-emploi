from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

# Modèle utilisateur personnalisé
class User(AbstractUser):
    ROLE_CHOICES = (
        ('job_seeker', 'Chercheur d\'emploi'),
        ('recruiter', 'Recruteur'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, db_index=True)

    # Ajouter un related_name unique pour éviter les conflits avec AbstractUser
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions_set',
        blank=True,
    )

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip() or self.username

    def __str__(self):
        return self.get_full_name()

# Modèle pour les notifications
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Notification for {self.user.username} - {self.message[:30]}..."

# Modèle pour les recruteurs
class Recruiter(models.Model):
   user = models.ForeignKey(User, on_delete=models.CASCADE)
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
    description = models.TextField()
    location = models.CharField(max_length=255)
    contract_type = models.CharField(max_length=50, choices=CONTRACT_TYPES, db_index=True)
    published_at = models.DateTimeField(auto_now_add=True)
    # recruiter = models.ForeignKey(User, related_name='job_offers', on_delete=models.CASCADE, limit_choices_to={'role': 'recruiter'})
    recruiter = models.ForeignKey(Recruiter, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-published_at']

    def __str__(self):
        return self.title
        # return f"{self.title} ({self.contract_type})"

# Modèle pour les profils des chercheurs d'emploi
class JobSeekerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', limit_choices_to={'role': 'job_seeker'})
    skills = models.TextField()  # Liste des compétences
    experience = models.TextField()  # Expérience professionnelle
    preferences = models.TextField()  # Préférences de recherche d'emploi

    def __str__(self):
        return f"{self.user.get_full_name()} - Profile"

# Modèle pour les candidatures
class Application(models.Model):
    STATUS_CHOICES = [
        ('pending', 'En attente'),
        ('accepted', 'Acceptée'),
        ('rejected', 'Refusée'),
    ]

    job_offer = models.ForeignKey(JobOffer, on_delete=models.CASCADE)
    job_seeker = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'job_seeker'})
    application_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending', db_index=True)

    class Meta:
        unique_together = ('job_offer', 'job_seeker')
        ordering = ['-application_date']

    def __str__(self):
        return f"{self.job_seeker.username} applied for {self.job_offer.title}"

# Modèle pour les recommandations
class Recommendation(models.Model):
    job_seeker = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'job_seeker'})
    job_offer = models.ForeignKey(JobOffer, on_delete=models.CASCADE)
    recommendation_score = models.FloatField()  # Score de pertinence de la recommandation

    class Meta:
        ordering = ['-recommendation_score']

    def __str__(self):
        return f"Recommendation for {self.job_seeker.username} to {self.job_offer.title} ({self.recommendation_score:.2f})"
