from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from dotenv import load_dotenv
import time
import os
import requests

# Charger les variables d'environnement
load_dotenv()

# Récupérer les identifiants
FREE_MOBILE_LOGIN = os.getenv('FREE_MOBILE_LOGIN')
FREE_MOBILE_PASSWORD = os.getenv('FREE_MOBILE_PASSWORD')

# Configuration
DOWNLOAD_DIR = "./factures_freemobile"

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
#chrome_options.add_argument("--headless=new")  # Important
#chrome_options.add_argument("--window-size=1920,1080")  # Facultatif : fixe une taille standard pour éviter des bugs de chargement

# Démarrer le navigateur
driver = webdriver.Chrome(options=chrome_options)

try:
    # Aller sur la page de connexion Freebox
    driver.get("https://mobile.free.fr/account/v2/login")

    # Entrer les identifiants
    driver.find_element(By.ID, "login-username").send_keys(FREE_MOBILE_LOGIN)
    driver.find_element(By.ID, "login-password").send_keys(FREE_MOBILE_PASSWORD)
    driver.find_element(By.ID, "auth-connect").click()
    print("Authentification OK.")

    # Attendre la redirection
    time.sleep(2)

    # --- Gestion du Code OTP split en 6 inputs ---
    try:
        # Trouver tous les inputs de type "number" pour l'OTP
        otp_inputs = driver.find_elements(By.CSS_SELECTOR, "input[type='number'][inputmode='numeric']")

        if len(otp_inputs) >= 6:
            otp_code = input("Code OTP reçu par SMS : ").strip()

            if len(otp_code) != 6 or not otp_code.isdigit():
                raise ValueError("Le code OTP doit contenir exactement 6 chiffres.")

            # Remplir chaque input avec le bon chiffre
            for idx, input_field in enumerate(otp_inputs[:6]):
                input_field.send_keys(otp_code[idx])
                time.sleep(0.1)  # Petite pause entre chaque saisie pour être plus naturel

            print("Code OTP saisi, envoi du formulaire...")

            # Trouver et cliquer sur le bouton "Valider" ou "Continuer" si nécessaire
            try:
                submit_button = driver.find_element(By.XPATH,
                                                    "//button[contains(.,'Continuer') or contains(.,'Valider')]")
                submit_button.click()
            except Exception:
                print("Pas de bouton 'Continuer' trouvé, passage automatique...")

        else:
            print("Pas de champ OTP détecté, connexion normale.")
    except Exception as e:
        print("Erreur lors de la saisie du code OTP :", e)

    # Attendre la redirection
    time.sleep(2)

    # --- Récupérer toutes les lignes mobiles disponibles ---
    all_lignes = driver.find_elements(By.XPATH,
                                          "//div[contains(@class, 'group flex items-center justify-between border-l-[3px] cursor-pointer')]")

    print(f"Nombre de lignes totales trouvées : {len(all_lignes)}")

    lignes_a_traiter = []

    for ligne in all_lignes:
        try:
            # Vérifier si on est dans la section "Lignes Résiliées"
            parent_text = ligne.find_element(By.XPATH, "./ancestor::div[contains(@class, 'mx-6')]").text

            if "LIGNES RÉSILIÉES" in parent_text:
                print("Ligne résiliée ignorée.")
                continue  # Ne pas traiter cette ligne
            else:
                lignes_a_traiter.append(ligne)
        except Exception as e:
            print("Erreur de détection, ligne ignorée :", e)

    print(f"Nombre de lignes actives détectées : {len(lignes_a_traiter)}")

    # On boucle sur chaque ligne
    for idx, ligne in enumerate(lignes_a_traiter):
        try:
            print(f"Traitement de la ligne {idx + 1}... ")

            # Cliquer sur la ligne
            driver.execute_script("arguments[0].click();", ligne)
            time.sleep(2)

            # Aller dans la section Factures
            mes_factures_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Mes factures')]")
            mes_factures_button.click()
            print("Bouton 'Mes factures' cliqué.")
            time.sleep(1)

            while True:
                try:
                    # Chercher le bouton "Voir plus"
                    voir_plus_button = driver.find_element(By.XPATH, "//button[.//span[text()='Voir plus']]")
                    voir_plus_button.click()
                    print("Bouton 'Voir plus' cliqué.")

                    # Attendre que de nouveaux éléments chargent
                    time.sleep(1)
                except NoSuchElementException:
                    # Plus de bouton "Voir plus" => on sort de la boucle
                    print("Plus de bouton 'Voir plus', fin de la boucle.")
                    break

            # Attendre le chargement de la page
            time.sleep(1)

            # Récupérer tous les liens vers les factures
            facture_links = driver.find_elements(By.XPATH,
                                                 "//a[contains(@href, '/account/v2/api/SI/invoice/') and contains(@href, 'display=1')]")

            print(f"Nombre de factures trouvées : {len(facture_links)}")

            for link in facture_links:
                facture_url = link.get_attribute('href')

                # Vérifie si l'URL est relative et la compléter si besoin
                if facture_url.startswith('/'):
                    facture_url = "https://mobile.free.fr" + facture_url

                print(f"Téléchargement : {facture_url}")

                # Extraire l'ID depuis l'URL
                facture_id = facture_url.split('/invoice/')[1].split('?')[0]
                print(f"ID extrait : {facture_id}")

                filename = f"{facture_id}.pdf"
                driver.execute_script(f"window.open('{facture_url}', '_blank');")

                time.sleep(2)  # Laisse le temps au téléchargement de démarrer

        except Exception as e:
            print(f"Erreur sur la ligne {idx + 0} : {e}")

finally:
    # Fermer le navigateur après 30 secondes pour finir les téléchargements
    print("Attente de la fin des téléchargements...")
    time.sleep(30)
    driver.quit()