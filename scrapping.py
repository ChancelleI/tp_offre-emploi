# pip install requests beautifulsoup4 selenium pandas sqlite3 dash streamlit scikit-learn pytest

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time

# Configuration de Selenium pour le scraping dynamique
def configure_selenium():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Exécution en arrière-plan
    driver = webdriver.Chrome(options=options)
    return driver

# Scraping des offres d'emploi sur LinkedIn
def scrape_linkedin(keyword):
    url = f"https://www.linkedin.com/jobs/search/?keywords={keyword}"
    driver = configure_selenium()
    driver.get(url)
    time.sleep(5)  # Attendre que la page se charge

    jobs = []
    job_elements = driver.find_elements(By.CLASS_NAME, "base-search-card__info")
    for element in job_elements:
        title = element.find_element(By.CLASS_NAME, "base-search-card__title").text
        company = element.find_element(By.CLASS_NAME, "base-search-card__subtitle").text
        location = element.find_element(By.CLASS_NAME, "job-search-card__location").text
        jobs.append({"title": title, "company": company, "location": location, "source": "LinkedIn"})

    driver.quit()
    return jobs

# Scraping des offres d'emploi sur Indeed
def scrape_indeed(keyword):
    url = f"https://www.indeed.com/jobs?q={keyword}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    jobs = []
    job_elements = soup.find_all("div", class_="job_seen_beacon")
    for element in job_elements:
        title = element.find("h2", class_="jobTitle").text
        company = element.find("span", class_="companyName").text
        location = element.find("div", class_="companyLocation").text
        jobs.append({"title": title, "company": company, "location": location, "source": "Indeed"})

    return jobs

# Scraping des offres d'emploi sur Glassdoor
def scrape_glassdoor(keyword):
    url = f"https://www.glassdoor.com/Job/jobs.htm?suggestCount=0&suggestChosen=false&clickSource=searchBtn&typedKeyword={keyword}"
    driver = configure_selenium()
    driver.get(url)
    time.sleep(5)

    jobs = []
    job_elements = driver.find_elements(By.CLASS_NAME, "jobListItem")
    for element in job_elements:
        title = element.find_element(By.CLASS_NAME, "jobTitle").text
        company = element.find_element(By.CLASS_NAME, "employerName").text
        location = element.find_element(By.CLASS_NAME, "location").text
        jobs.append({"title": title, "company": company, "location": location, "source": "Glassdoor"})

    driver.quit()
    return jobs

# Scraping des offres d'emploi sur HelloWork
def scrape_hellowork(keyword):
    url = f"https://www.hellowork.com/fr-fr/emploi/recherche.html?k={keyword}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    jobs = []
    job_elements = soup.find_all("div", class_="job-offer")
    for element in job_elements:
        title = element.find("h2", class_="job-offer-title").text
        company = element.find("div", class_="job-offer-company").text
        location = element.find("div", class_="job-offer-location").text
        jobs.append({"title": title, "company": company, "location": location, "source": "HelloWork"})

    return jobs

# Scraping des offres d'emploi sur Google Jobs
def scrape_google_jobs(keyword):
    url = f"https://www.google.com/search?q={keyword}+jobs"
    driver = configure_selenium()
    driver.get(url)
    time.sleep(5)

    jobs = []
    job_elements = driver.find_elements(By.CLASS_NAME, "BjJfJf")
    for element in job_elements:
        title = element.find_element(By.CLASS_NAME, "BjJfJf").text
        company = element.find_element(By.CLASS_NAME, "vNEEBe").text
        location = element.find_element(By.CLASS_NAME, "Qk80Jf").text
        jobs.append({"title": title, "company": company, "location": location, "source": "Google Jobs"})

    driver.quit()
    return jobs

# Fonction principale pour collecter les offres d'emploi
def collect_jobs(keyword):
    jobs = []
    jobs.extend(scrape_linkedin(keyword))
    jobs.extend(scrape_indeed(keyword))
    jobs.extend(scrape_glassdoor(keyword))
    jobs.extend(scrape_hellowork(keyword))
    jobs.extend(scrape_google_jobs(keyword))
    return jobs


import sqlite3

# Création d'une base de données SQLite pour stocker les offres d'emploi
def create_database():
    conn = sqlite3.connect("job_offers.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            company TEXT,
            location TEXT,
            source TEXT
        )
    """)
    conn.commit()
    conn.close()

# Insertion des offres d'emploi dans la base de données
def save_jobs_to_db(jobs):
    conn = sqlite3.connect("job_offers.db")
    cursor = conn.cursor()
    for job in jobs:
        cursor.execute("""
            INSERT INTO jobs (title, company, location, source)
            VALUES (?, ?, ?, ?)
        """, (job["title"], job["company"], job["location"], job["source"]))
    conn.commit()
    conn.close()


import dash
from dash import dcc, html
import pandas as pd
import sqlite3

# Création d'un tableau de bord avec Dash
def create_dashboard():
    conn = sqlite3.connect("job_offers.db")
    df = pd.read_sql_query("SELECT * FROM jobs", conn)
    conn.close()

    app = dash.Dash(__name__)
    app.layout = html.Div([
        html.H1("Tableau de Bord des Offres d'Emploi"),
        dcc.Graph(
            id="job-offers",
            figure={
                "data": [
                    {"x": df["source"], "y": df.groupby("source").size(), "type": "bar", "name": "Offres par Source"}
                ],
                "layout": {"title": "Répartition des Offres d'Emploi par Source"}
            }
        )
    ])

    app.run_server(debug=True)


import pytest

# Test unitaire pour vérifier la collecte des offres d'emploi
def test_job_collection():
    jobs = collect_jobs("data scientist")
    assert len(jobs) > 0, "Aucune offre d'emploi collectée"

# Exécution des tests
if __name__ == "__main__":
    pytest.main()