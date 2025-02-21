import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Fonction pour configurer Selenium
def configure_selenium():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-software-rasterizer')
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

                job = {"title": title, "company": company, "location": location, "source": "Indeed"}
                jobs.append(job)
            except AttributeError:
                continue  

        print(f"✅ {len(jobs)} offres récupérées sur Indeed.")
        return jobs
    except Exception as e:
        print(f"❌ Erreur scraping Indeed : {e}")
        return []


# Scraping HelloWork
def scrape_hellowork(keyword):
    print(f"🔍 Scraping HelloWork pour '{keyword}'...")
    url = f"https://www.hellowork.com/fr-fr/emploi/recherche.html?k={keyword}"
    
    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(response.text, "html.parser")
        jobs = []

        job_elements = soup.find_all("li", class_="hw-card")  # Repère les offres
        for element in job_elements:
            try:
                title = element.find("h3", class_="hw-card__title").text.strip()
                company = element.find("span", class_="hw-card__company").text.strip()
                location = element.find("span", class_="hw-card__location").text.strip()

                job = {"title": title, "company": company, "location": location, "source": "HelloWork"}
                jobs.append(job)
            except AttributeError:
                continue  

        print(f"✅ {len(jobs)} offres récupérées sur HelloWork.")
        return jobs
    except Exception as e:
        print(f"❌ Erreur scraping HelloWork : {e}")
        return []


# Scraping LinkedIn
def scrape_linkedin(keyword):
    print(f"🔍 Scraping LinkedIn pour '{keyword}'...")
    url = f"https://www.linkedin.com/jobs/search/?keywords={keyword}"
    driver = configure_selenium()
    
    try:
        driver.get(url)
        time.sleep(5)  
        jobs = []

        job_elements = driver.find_elements(By.CLASS_NAME, "base-search-card__info")
        for element in job_elements:
            try:
                title = element.find_element(By.CLASS_NAME, "base-search-card__title").text.strip()
                company = element.find_element(By.CLASS_NAME, "base-search-card__subtitle").text.strip()
                location = element.find_element(By.CLASS_NAME, "job-search-card__location").text.strip()

                job = {"title": title, "company": company, "location": location, "source": "LinkedIn"}
                jobs.append(job)
            except Exception:
                continue  

        print(f"✅ {len(jobs)} offres récupérées sur LinkedIn.")
        return jobs
    except Exception as e:
        print(f"❌ Erreur scraping LinkedIn : {e}")
        return []
    finally:
        driver.quit()  

# Fonction principale pour collecter les offres d'emploi
def run():
    keyword = "data engineer"
    print("\n=============================")
    print(f"🔍 Début du scraping pour '{keyword}'")
    print("=============================")

    jobs = []
    jobs.extend(scrape_indeed(keyword))
    jobs.extend(scrape_hellowork(keyword))
    jobs.extend(scrape_linkedin(keyword))

    print("=============================")
    print(f"🎯 Total des offres collectées : {len(jobs)}")
    print("=============================\n")

    # Affichage des résultats
    for job in jobs:
        print(f"{job['title']} - {job['company']} ({job['location']}) [{job['source']}]")

    print("✅ Scraping terminé !")

# Exécution du script
if __name__ == "__main__":
    run()
