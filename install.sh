#!/bin/bash

set -e

echo "📦 Création de l'environnement virtuel..."
python3 -m venv venv
source venv/bin/activate

echo "🔄 Installation des dépendances..."
pip install --upgrade pip
pip install -r requirements.txt

echo "✅ Installation terminée !"
echo "N'oubliez pas de créer votre fichier .env en vous basant sur .env.example."

echo "🔄 Pour activer l'environnement : source venv/bin/activate"
echo "🚀 Ensuite lancez : python scraper_factures_freebox.py ou python scraper_factures_freemobile.py"
