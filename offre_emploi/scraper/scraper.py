import os
import sys

# Ajoute le chemin du projet Django
sys.path.append("D:/doc.fr icare/M1 DSP/Ecosysteme Data de lentreprise/tp_offre emploi/offre_emploi")
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Définit les paramètres Django avant d'importer Django
if not os.getenv('DJANGO_SETTINGS_MODULE'):
  os.environ.setdefault("DJANGO_SETTINGS_MODULE", "offre_emploi.settings")

# Maintenant, on importe Django
import django
if not django.apps.apps_ready:
  django.setup()

# Vérifie que Django est bien configuré
print("✅ Django est bien configuré !")

# Maintenant, tu peux importer tes modèles
try:
    from scraper.models import JobOffer  # Vérifie que ce module existe bien
except ImportError as e:
    print(f"❌ Erreur d'importation du modèle : {e}")
    sys.exit(1)

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Fonction pour configurer Selenium
def configure_selenium():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Exécution en arrière-plan
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    return webdriver.Chrome(options=options)

# Scraping Indeed
def scrape_indeed(keyword):
    print(f"🔍 Scraping Indeed pour '{keyword}'...")
    url = f"https://www.indeed.com/jobs?q={keyword}"
    
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        jobs = []

        job_elements = soup.find_all("div", class_="job_seen_beacon")
        for element in job_elements:
            try:
                title = element.find("h2", class_="jobTitle").text.strip()
                company = element.find("span", class_="companyName").text.strip()
                location = element.find("div", class_="companyLocation").text.strip()

                # Enregistrement dans la base Django
                job = JobOffer(title=title, company=company, location=location, source="Indeed")
                job.save()
                jobs.append(job)
            except AttributeError:
                continue  # Ignore les offres incomplètes

        print(f"✅ {len(jobs)} offres récupérées sur Indeed.")
        return jobs
    except Exception as e:
        print(f"❌ Erreur scraping Indeed : {e}")
        return []

# Scraping LinkedIn
def scrape_linkedin(keyword):
    print(f"🔍 Scraping LinkedIn pour '{keyword}'...")
    url = f"https://www.linkedin.com/jobs/search/?keywords={keyword}"
    driver = configure_selenium()
    
    try:
        driver.get(url)
        time.sleep(5)  # Attendre que la page se charge
        jobs = []

        job_elements = driver.find_elements(By.CLASS_NAME, "base-search-card__info")
        for element in job_elements:
            try:
                title = element.find_element(By.CLASS_NAME, "base-search-card__title").text.strip()
                company = element.find_element(By.CLASS_NAME, "base-search-card__subtitle").text.strip()
                location = element.find_element(By.CLASS_NAME, "job-search-card__location").text.strip()

                # Enregistrement dans la base Django
                job = JobOffer(title=title, company=company, location=location, source="LinkedIn")
                job.save()
                jobs.append(job)
            except Exception:
                continue  # Ignore les erreurs d'extraction

        print(f"✅ {len(jobs)} offres récupérées sur LinkedIn.")
        return jobs
    except Exception as e:
        print(f"❌ Erreur scraping LinkedIn : {e}")
        return []
    finally:
        driver.quit()  # Fermer Selenium

# Fonction principale pour collecter les offres d'emploi
def collect_jobs(keyword):
    print("\n=============================")
    print(f"🔍 Début du scraping pour '{keyword}'")
    print("=============================")

    jobs = []
    jobs.extend(scrape_indeed(keyword))
    jobs.extend(scrape_linkedin(keyword))

    print("=============================")
    print(f"🎯 Total des offres collectées : {len(jobs)}")
    print("=============================\n")
    return jobs

# Exécution du script en ligne de commande
if __name__ == "__main__":
    keyword = "data engineer"  # Modifier ici pour changer la recherche
    collect_jobs(keyword)
    print("✅ Scraping terminé !")
