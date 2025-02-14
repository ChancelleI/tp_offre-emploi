from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import CustomUserCreationForm, JobOfferForm, ApplicationForm
from django.contrib.auth.decorators import login_required
from .decorators import is_recruiter_required, is_job_seeker_required

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from .models import JobOffer, JobSeekerProfile, Application, Recruiter
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
# # Vue pour l'API
# def home(request):
#     return JsonResponse({"message": "Bienvenue sur l'API des offres d'emploi !"})

# Vue pour le frontend (HTML)
def home(request):
    offres = JobOffer.objects.all()  # Récupère toutes les offres d'emploi
    if request.user.is_authenticated:
        user_role = getattr(request.user, 'role', None)  # Récupérer le rôle proprement
        print(f"DEBUG - Utilisateur connecté: {request.user.username}, Role: {user_role}")
        # if hasattr(request.user, 'role'): 
    #     # print(f"User role: {request.user.role}")  # Debug
        if user_role == 'recruiter':
           return redirect('recruiter_dashboard')  # Rediriger vers le tableau de bord du recruteur
        elif user_role == 'job_seeker':
           return redirect('candidate_dashboard')  # Rediriger vers le tableau de bord du candidat
    return render(request, 'core/home.html', {'offres': offres})  # Passe les offres à la page d'accueil

def job_offers(request):
    offers = JobOffer.objects.all()  # Récupérer toutes les offres
    return render(request, 'core/job_offers.html', {'job_offers': offers})
    # return render(request, 'core/job_offers.html')  # Assure-toi d'avoir ce template

def job_offer_detail(request, offer_id):
    # Récupère l'offre d'emploi par son ID
    job_offer = get_object_or_404(JobOffer, id=offer_id)
    return render(request, 'core/job_offer_detail.html', {'job_offer': job_offer})

# Vue pour l'inscription
def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            login(request, user)  # Connexion automatique après l'inscription

           # Redirection en fonction du rôle
            if user.role == 'candidate':
                return redirect('candidate_dashboard')  # Redirige vers le tableau de bord du candidat
            elif user.role == 'recruiter':
                return redirect('recruiter_dashboard')  # Redirige vers le tableau de bord du recruteur

    else:
        form = CustomUserCreationForm()

    return render(request, "core/register.html", {"form": form})

# Vue pour la connexion
def login_view(request):
    # Récupère le paramètre 'next' s'il est présent dans l'URL, sinon redirige vers la page d'accueil
    next_url = request.GET.get('next', 'home')  # 'home' est la page par défaut si 'next' n'est pas trouvé

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Bienvenue {username} !')

                # Rediriger en fonction du rôle de l'utilisateur
                if user.role == 'recruiter':
                    return redirect('recruiter_dashboard')  # Redirection vers le tableau de bord recruteur
                elif user.role == 'job_seeker':
                    return redirect('candidate_dashboard')  # Redirection vers le tableau de bord candidat
                else:
                    return redirect(next_url)  # Redirige vers l'URL spécifiée dans 'next'
            else:
                messages.error(request, 'Identifiants incorrects')
        else:
            messages.error(request, 'Formulaire invalide')
    else:
        form = AuthenticationForm()
    
    return render(request, 'core/login.html', {'form': form})

def logout_view(request):
    """ Déconnecte l'utilisateur et le redirige vers la page d'accueil """
    logout(request)
    messages.success(request, 'Déconnexion réussie.')
    return redirect('home')

# Vues pour les recruteurs
@login_required
@is_recruiter_required  # S'assure que seul un recruteur peut accéder à cette vue
def recruiter_dashboard(request):
    recruiter = get_object_or_404(Recruiter, user=request.user)
    job_offers = JobOffer.objects.filter(recruiter=recruiter)
    return render(request, 'core/recruiter_dashboard.html', {'job_offers': job_offers})

@login_required
def view_applications(request, job_offer_id):
    job_offer = get_object_or_404(JobOffer, id=job_offer_id)
    applications = Application.objects.filter(job_offer=job_offer)
    return render(request, 'core/view_applications.html', {'job_offer': job_offer, 'applications': applications})

# Vues pour les candidats
@login_required
@is_job_seeker_required  # S'assure que seul un candidat peut accéder à cette vue
def candidate_dashboard(request):
    job_seeker = request.user
    applications = Application.objects.filter(job_seeker=job_seeker)
    return render(request, 'core/candidate_dashboard.html', {'applications': applications})

@login_required
def applied_jobs(request):
     print(f"Rôle de l'utilisateur : {request.user.role}")  # Débogage
     job_seeker = request.user
     applications = Application.objects.filter(job_seeker=job_seeker)
     job_offers = [application.job_offer for application in applications]
     return render(request, 'core/applied_jobs.html', {'job_offers': job_offers})

@login_required
def postuler(request, offer_id):
    job_offer = get_object_or_404(JobOffer, id=offer_id)
    Application.objects.create(job_seeker=request.user, job_offer=job_offer)
    return redirect('candidate_dashboard')  # Redirige vers le tableau de bord candidat après la candidature

@login_required
def publier_offre(request):
    if request.user.role != 'recruiter':  
        return redirect('home')  # Empêche les candidats de publier des offres

    if request.method == 'POST':
        form = JobOfferForm(request.POST)
        if form.is_valid():
            job_offer = form.save(commit=False)
            job_offer.recruiter = request.user.recruiter
            job_offer.save()
            return redirect('recruiter_dashboard')  # Redirige après publication
    else:
        form = JobOfferForm()

    return render(request, 'core/publier_offre.html', {'form': form})

@login_required
def apply_for_job(request, offer_id):
    job_offer = get_object_or_404(JobOffer, id=offer_id)

    # Si l'utilisateur n'est pas connecté, redirige vers la page de connexion avec le paramètre `next`
    if not request.user.is_authenticated:
        return redirect(f"/login/?next=/job/{offer_id}/apply/")  

    # Si l'utilisateur n'est pas un chercheur d'emploi
    if request.user.role != "job_seeker":
        messages.error(request, "Seuls les candidats peuvent postuler aux offres.")
        return redirect('job_offer_detail', job_id=offer_id)

    # Vérifie si l'utilisateur a déjà postulé
    if Application.objects.filter(job_offer=job_offer, job_seeker=request.user).exists():
        messages.warning(request, "Vous avez déjà postulé à cette offre.")
        return redirect('job_offer_detail', job_id=offer_id)

    # Si c'est une soumission de formulaire (POST)
    if request.method == "POST":
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.job_offer = job_offer
            application.job_seeker = request.user  # Associe le candidat connecté
            application.save()
            messages.success(request, "Votre candidature a été envoyée avec succès !")
            return redirect("job_offer_detail", job_id=offer_id)
        else:
            messages.error(request, "Il y a des erreurs dans votre formulaire. Veuillez les corriger.")
    else:
        form = ApplicationForm()

    return render(request, "core/apply_for_job.html", {"form": form, "job_offer": job_offer})

