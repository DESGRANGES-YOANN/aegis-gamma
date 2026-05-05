# AEGIS-Γ - Veille stratégique et détection de désinformation

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)]()

## 🚀 Description
AEGIS-Γ est un système de veille stratégique capable d'analyser n'importe quel sujet (ex: "Amazon recyclage") en collectant automatiquement des messages depuis Twitter, Reddit et la presse.

## 📊 Fonctionnalités
- ✅ Collecte automatique (Twitter, Reddit, Articles)
- ✅ Détection des campagnes coordonnées
- ✅ Identification des super-amplificateurs / amplificateurs
- ✅ Calcul du niveau d'alerte (0-10)
- ✅ Recommandations de communication
- ✅ 34 modules d'analyse unifiés

## 🛠️ Installation

```bash
git clone https://github.com/DESGRANGES-YOANN/aegis-gamma.git
cd aegis-gamma
pip install numpy

▶️ Utilisation
bash

# Analyser un sujet (recommandé)
python aegis_gamma.py --analyse "Amazon recyclage"

# Mode interactif
python aegis_gamma.py --v5

# Démo avec campagne générée
python aegis_gamma.py --demo

# Test rapide
python aegis_gamma.py --test

📈 Exemple de résultat
bash

python aegis_gamma.py --analyse "Amazon recyclage"

text

🚀 Analyse de 'Amazon recyclage'...
🌐 DÉBUT DE LA COLLECTE pour : Amazon recyclage
  🐦 30 tweets collectés
  📖 25 posts Reddit collectés
  📰 15 articles collectés
✅ COLLECTE TERMINÉE : 70 messages

📊 RÉSUMÉ DE L'ANALYSE
========================================
📝 Sujet: Amazon recyclage
📡 Messages collectés: 70
🚨 Niveau d'alerte: 5.2/10
🎯 Score confiance: 5.6/10
👥 Amplificateurs: 0

💡 RECOMMANDATIONS:
   🟠 Surveiller activement Amazon recyclage
   📈 Analyser la tendance

📊 Comparaison des scores
Type de campagne	Niveau d'alerte	Interprétation
Campagne coordonnée (simulation)	8.8/10	🔴 CRITIQUE - Enquête prioritaire
Sujet réel normal	5.2/10	🟠 MODÉRÉ - Surveillance active

👤 Auteur

DESGRANGES Yoann
