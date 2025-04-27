from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from dotenv import load_dotenv
import time
import os

# Charger les variables d'environnement
load_dotenv()

# Récupérer les identifiants
FREE_LOGIN = os.getenv('FREE_MOBILE_LOGIN')
FREE_PASSWORD = os.getenv('FREE_MOBILE_PASSWORD')

# Configuration
DOWNLOAD_DIR = "./factures_freebox"

# Préparer le dossier de téléchargement
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# Configurer Chrome pour télécharger automatiquement les PDF
chrome_options = Options()
prefs = {
    "download.default_directory": os.path.abspath(DOWNLOAD_DIR),
    "plugins.always_open_pdf_externally": True
}
chrome_options.add_experimental_option("prefs", prefs)

# Activer le mode headless
chrome_options.add_argument("--headless=new")  # Important
chrome_options.add_argument("--window-size=1920,1080")  # Facultatif : fixe une taille standard pour éviter des bugs de chargement

# Démarrer le navigateur
driver = webdriver.Chrome(options=chrome_options)

try:
    # Aller sur la page de connexion Freebox
    driver.get("https://subscribe.free.fr/login/")

    # Entrer les identifiants
    driver.find_element(By.ID, "login_b").send_keys(FREE_LOGIN)
    driver.find_element(By.ID, "pass_b").send_keys(FREE_PASSWORD)
    driver.find_element(By.ID, "ok").click()
    print("Authentification OK.")

    # Attendre la redirection
    time.sleep(3)

    # Aller dans la section Factures
    all_facture_links = driver.find_element(By.XPATH, "//a[contains(@href, 'facture_liste.pl') and @title='Voir toutes mes factures']")
    all_facture_links.click()
    print("Lien 'Voir toutes mes factures' cliqué.")

    # Attendre le chargement de la page
    time.sleep(3)

    # Récupérer tous les liens vers les factures
    facture_links = driver.find_elements(By.XPATH,
                                         "//a[contains(@href, 'facture_pdf.pl') and contains(@class, 'btn_download') and @title='Télécharger votre facture en PDF']")

    print(f"Nombre de factures trouvées : {len(facture_links)}")

    for link in facture_links:
        facture_url = link.get_attribute('href')
        print(f"Téléchargement : {facture_url}")
        driver.execute_script(f"window.open('{facture_url}', '_blank');")
        time.sleep(2)  # Laisse le temps au téléchargement de démarrer

finally:
    # Fermer le navigateur après 30 secondes pour finir les téléchargements
    print("Attente de la fin des téléchargements...")
    time.sleep(30)
    driver.quit()