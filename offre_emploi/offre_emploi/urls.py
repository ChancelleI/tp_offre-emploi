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

urlpatterns = [
   path('admin/', admin.site.urls),  # Interface d'administration
    path('api/', include('core.urls')),  # Inclusion des routes de l'application core sous /api/
    path('', lambda request: redirect('/api/joboffers/')),  # Redirection de la page d'accueil vers les offres d'emploi
    # la page d'accueil affiche directement les offres d'emploi donc j'ai Redirigé la page d'accueil vers l'API ou une autre vue
]

