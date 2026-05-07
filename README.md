# 🛡️ AEGIS-Γ

**Console d'analyse narrative | Détection de coordination et signaux faibles**

[![Version](https://img.shields.io/badge/version-5.1-blue.svg)](https://github.com/DESGRANGES-YOANN/aegis-gamma)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)]()
[![Demo](https://img.shields.io/badge/demo-live-brightgreen.svg)](https://desgranges-yoann.github.io/aegis-gamma/)

---

## 🌐 Démo en ligne

👉 **https://desgranges-yoann.github.io/aegis-gamma/**

Interface interactive pour tester l'analyse narrative sur différents sujets.

⚠️ **Prototype de démonstration** — Les scores sont simulés à des fins d'interface.

---

## 📌 À propos

AEGIS-Γ est une **console d'analyse narrative** permettant de visualiser des signaux de coordination, polarisation et amplification.

**Cas d'usage** : veille stratégique, analyse OSINT, détection de tendances.

---

## ✨ Fonctionnalités

| Fonctionnalité | Description |
|----------------|-------------|
| 📊 **Intensité de signal** | Score 0-10 basé sur détection de signaux |
| 🎯 **Confiance analyse** | Niveau de fiabilité |
| 📡 **Sources OSINT** | Détection des plateformes actives |
| 📈 **Timeline temporelle** | Visualisation activité sur 7 jours |
| 🔬 **Facteurs identifiés** | Signaux positifs/négatifs |
| 📋 **Clusters narratifs** | Segmentation thématique |
| ⚙️ **34 modules UI** | NLP, Coordination, Temporal, Clustering, Emotion... |

---

## 🛠️ Installation (version Python)

### Prérequis
- Python 3.8+
- pip

### Installation

```bash
git clone https://github.com/DESGRANGES-YOANN/aegis-gamma.git
cd aegis-gamma
pip install numpy

Utilisation
bash

# Analyser un sujet (simulation)
python aegis_gamma.py --analyse "Amazon recyclage"

# Mode interactif
python aegis_gamma.py --v5

# Démo avec campagne générée
python aegis_gamma.py --demo

# Test rapide
python aegis_gamma.py --test

📊 Exemple de résultat
bash

python aegis_gamma.py --analyse "Président Macron"

text

📊 RÉSUMÉ DE L'ANALYSE
========================================
📝 Sujet: Président Macron
📡 Messages collectés: 70
🚨 Niveau d'alerte: 6.9/10
🎯 Score confiance: 6.5/10
👥 Amplificateurs: 2

💡 RECOMMANDATIONS:
   🟠 Surveillance renforcée
   📈 Analyser la tendance

📋 PLAN D'ACTION STRATÉGIQUE
========================================
🔴 ACTIONS IMMÉDIATES :
   • Renforcer l'analyse humaine
   • Produire un rapport de situation

📊 Comparaison des scores
Type de campagne	Niveau	Interprétation
Sujet neutre (Jeux Olympiques)	4.8/10	Veille normale
Sujet économique (Amazon)	5.2/10	Surveillance active
Sujet politique (Macron)	6.9/10	Surveillance renforcée
Sujet désinformation (simulation)	8.8/10	Analyse approfondie
🛣️ Roadmap
Version	Statut	Fonctionnalités
v5.1	✅ Terminé	Interface carbone, 34 modules, simulation déterministe
v5.2	🚧 En cours	Intégration API Reddit (données réelles)
v5.3	📋 Planifiée	Export PDF, historique analyses
v6.0	🔮 Vision	API publique, dashboard temps réel
🏗️ Architecture
text

AEGIS-Γ
├── Frontend (HTML/CSS/JS)
│   ├── Interface console carbone
│   ├── Timeline, clusters, sources
│   └── Simulation déterministe (hashCode)
│
├── Backend Python
│   ├── 34 modules d'analyse
│   ├── Simulation de collecte
│   └── Plan d'action stratégique
│
└── API (future)
    └── Reddit / RSS

📝 Disclaimer

⚠️ Ce projet est un prototype de démonstration

    Les scores et analyses sont simulés pour illustrer l'interface

    Ne constitue pas une mesure réelle de manipulation ou coordination

    À des fins de démonstration, portfolio et exploration technique

🤝 Contribution

Les contributions sont les bienvenues !

    Fork le projet

    Crée ta branche (git checkout -b feature/amazing-feature)

    Commit (git commit -m 'Add amazing feature')

    Push (git push origin feature/amazing-feature)

    Ouvre une Pull Request

📄 Licence

Distribué sous licence MIT. Voir LICENSE pour plus d'informations.
📬 Contact

Yoann Desgranges - desgranges06@gmail.com

🔗 Démo : desgranges-yoann.github.io/aegis-gamma/
🐙 GitHub : github.com/DESGRANGES-YOANN/aegis-gamma
⭐ Show your support
