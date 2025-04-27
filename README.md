# 📅 Scraper de Factures Freebox et Free Mobile

Ce projet Python permet de :
- Se connecter à **Freebox** et **Free Mobile** automatiquement
- Saisir un **code OTP** si demandé (authentification renforcée)
- Détecter toutes les **lignes mobiles** (principale, secondaires, résiliées)
- Télécharger toutes les **factures** (au format PDF)

---

## 🚀 Fonctionnalités

- **Connexion** Freebox ou Free Mobile
- **Gestion automatique** du code OTP (uniquement Free Mobile)
- **Exploration** de toutes les lignes mobiles
- **Récupération** de toutes les factures
- **Navigation headless** (sans ouvrir visuellement Chrome)

---

## 📆 Prérequis

- Python 3.8+
- Google Chrome installé
- ChromeDriver installé (compatible avec Chrome)

---

## 📦 Installation

1. Clonez ce répertoire :

```bash
git clone https://github.com/votre-utilisateur/scraper-factures-free.git
cd scraper-factures-free
```

2. Lancez le script d'installation automatique :

```bash
bash install.sh
```

Cela créera automatiquement un environnement virtuel et installera toutes les dépendances.

3. Créez votre propre fichier `.env` à partir de l'exemple fourni :

```bash
cp .env.example .env
```

Remplissez votre `.env` avec vos identifiants Freebox ou Free Mobile.

---

## 🔄 Utilisation

**Pour Freebox** :

```bash
source venv/bin/activate
python scraper_factures_freebox.py
```

Le script téléchargera **automatiquement** toutes vos factures dans `factures_freebox/`.


**Pour Free Mobile** :

```bash
source venv/bin/activate
python scraper_factures_freemobile.py
```

Le script vous demandera votre **code OTP** si besoin, et téléchargera **automatiquement** toutes vos factures dans `factures_freemobile/`.

---

## 🔧 Technologies

- [Python](https://www.python.org/)
- [Selenium](https://selenium.dev/)
- [Requests](https://docs.python-requests.org/)
- [python-dotenv](https://pypi.org/project/python-dotenv/)

---

## ⚠️ Sécurité

- Ne partagez jamais votre fichier `.env` !
- Utilisez ce projet uniquement pour un usage personnel.

---

## 📅 TODOs futurs

- [ ] Renommer automatiquement les factures Free Mobile
- [ ] Ajout d'une barre de progression
- [ ] Accélération multi-thread
- [ ] Zip automatique des factures

---

## 👨‍💻 Auteur

**Julien SIMONCINI**

Contact : [julien@simoncini.fr](mailto:julien@simoncini.fr)

---

## 🔖 Licence

Projet distribué sous licence **GNU General Public License v3.0**.

Vous pouvez redistribuer, modifier et utiliser ce projet tant que toute redistribution préserve la même licence.
