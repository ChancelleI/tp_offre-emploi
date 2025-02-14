"""
URL configuration for offre_emploi project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# offre_emploi/urls.py
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect  # Import pour la redirection
from django.http import HttpResponse
from core import views  
from django.contrib.auth import views as auth_views


# Une vue de test pour vérifier que l'URL fonctionne
# def offres_view(request):
#     return HttpResponse("Liste des offres")

urlpatterns = [
   path('admin/', admin.site.urls),
    # path('offres/', offres_view),  # Si tu as une vue pour les offres
    path('offres/', views.job_offers, name='job_offers'),  # Liste des offres
    path('api/', include('core.urls')),  # Inclure les routes de core sous l'API
    # path('', lambda request: redirect('/api/joboffers/')),  # Redirection de la page d'accueil
    path('', views.home, name='home'),  # Affiche la page d'accueil

    # Ajout des URLs pour les tableaux de bord du recruteur et du candidat
    path('recruiter/dashboard/', views.recruiter_dashboard, name='recruiter_dashboard'),
    path('candidate/dashboard/', views.candidate_dashboard, name='candidate_dashboard'),
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),

]

