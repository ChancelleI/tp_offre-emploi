from django.contrib import admin

# Register your models here.
# core/admin.py
from .models import Recruiter, JobOffer

# Enregistrement du modèle Recruiter dans l'admin
# admin.site.register(Recruiter)

@admin.register(Recruiter)
class RecruiterAdmin(admin.ModelAdmin):
    list_display = ('user', 'company_name', 'contact_email')

@admin.register(JobOffer)
class JobOfferAdmin(admin.ModelAdmin):
    list_display = ('title', 'location', 'contract_type', 'published_at', 'recruiter')
