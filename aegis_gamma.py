"""
AEGIS-Γ - Système de contrôle narratif
Version complète pour test
"""

import numpy as np
import random
from datetime import datetime, timedelta
from typing import List, Dict, Any, Tuple, Optional
from collections import Counter
from dataclasses import dataclass, field
from enum import Enum
import argparse
import asyncio

# ============================================================
# ÉNUMÉRATIONS
# ============================================================

class TypeSource(Enum):
    ARTICLE_PRESSE = "article_presse"
    THEORIE_ALTERNATIVE = "theorie_alternative"
    POST_RESEAU_SOCIAL = "post_reseau_social"

class TypeOpacite(Enum):
    COMPLEXITE_TECHNIQUE = "complexite_technique"
    ABSENCE_SOURCE = "absence_source"

class TypeTension(Enum):
    EMOTIONNELLE = "emotionnelle"
    COGNITIVE = "cognitive"

class ProfilEthique(Enum):
    CITOYEN = "citoyen"
    INSTITUTIONNEL = "institutionnel"

# ============================================================
# FONCTIONS UTILITAIRES
# ============================================================

def maintenant():
    return datetime.now()

def clamp(valeur, min_val, max_val):
    return max(min_val, min(max_val, valeur))

def moyenne(valeurs):
    return sum(valeurs) / len(valeurs) if valeurs else 0.0

# ============================================================
# MODÈLE D'UN FRAGMENT NARRATIF
# ============================================================

@dataclass
class FragmentNarratif:
    id: str
    sujet: str
    type_source: TypeSource
    contenu: str
    charge_emotionnelle: float
    date_collecte: datetime
    coherence_interne: float = 0.5
    divergence_externe: float = 0.5
    auteur: Optional[str] = None

# ============================================================
# MODÈLE D'UNE ZONE DE TENSION
# ============================================================

@dataclass
class ZoneDeTension:
    id: str
    sujet: str
    fragments_ids: List[str]
    niveau_alerte: float
    energie_estimee: float
    formes_opacite_detectees: List[TypeOpacite]
    date_creation: datetime
    resilience_narrative: float = 1.0
    
    def to_dict(self):
        return {
            "id": self.id,
            "sujet": self.sujet,
            "niveau_alerte": round(self.niveau_alerte, 1),
            "energie_estimee": round(self.energie_estimee, 1),
            "resilience_narrative": round(self.resilience_narrative, 2),
            "nombre_fragments": len(self.fragments_ids)
        }

# ============================================================
# CARTOGRAPHE - LE CERVEAU DU SYSTÈME
# ============================================================

class CartographeBrouillage:
    def __init__(self):
        self.fragments = {}
        self.zones_tension = {}
        self._fragments_vus = set()
    
    def ajouter_fragment(self, sujet: str, type_src: str, contenu: str, 
                         charge: float = 5.0, auteur: str = None) -> Optional[str]:
        
        # Éviter les doublons
        identifiant_unique = f"{sujet}::{hash(contenu)}"
        if identifiant_unique in self._fragments_vus:
            print(f"  ⚠️ Fragment doublon ignoré")
            return None
        self._fragments_vus.add(identifiant_unique)
        
        # Déterminer le type de source
        if "theorie" in type_src:
            type_source = TypeSource.THEORIE_ALTERNATIVE
        elif "social" in type_src:
            type_source = TypeSource.POST_RESEAU_SOCIAL
        else:
            type_source = TypeSource.ARTICLE_PRESSE
        
        # Créer le fragment
        fragment_id = f"FRAG_{len(self.fragments)}_{int(maintenant().timestamp())}"
        fragment = FragmentNarratif(
            id=fragment_id,
            sujet=sujet,
            type_source=type_source,
            contenu=contenu[:500],
            charge_emotionnelle=clamp(charge, 0, 10),
            date_collecte=maintenant(),
            auteur=auteur
        )
        
        self.fragments[fragment_id] = fragment
        print(f"  ✅ Fragment ajouté: {sujet[:30]}... (charge: {charge})")
        return fragment_id
    
    def analyser_sujet(self, sujet: str) -> Optional[ZoneDeTension]:
        # Récupérer tous les fragments du sujet
        fragments_sujet = [f for f in self.fragments.values() if f.sujet == sujet]
        
        if not fragments_sujet:
            print(f"  ❌ Aucun fragment trouvé pour {sujet}")
            return None
        
        print(f"  📊 Analyse de {len(fragments_sujet)} fragments...")
        
        # Calculer la charge émotionnelle moyenne
        charges = [f.charge_emotionnelle for f in fragments_sujet]
        charge_moyenne = moyenne(charges)
        
        # Calculer le niveau d'alerte (plus la charge est élevée, plus l'alerte monte)
        niveau_alerte = clamp(charge_moyenne * 1.2, 0, 10)
        
        # Énergie estimée = charge * nombre de fragments
        energie = charge_moyenne * len(fragments_sujet)
        
        # Créer ou mettre à jour la zone
        zone_id = f"ZONE_{sujet}"
        
        zone = ZoneDeTension(
            id=zone_id,
            sujet=sujet,
            fragments_ids=[f.id for f in fragments_sujet],
            niveau_alerte=niveau_alerte,
            energie_estimee=energie,
            formes_opacite_detectees=[],
            date_creation=maintenant()
        )
        
        self.zones_tension[zone_id] = zone
        print(f"  ✅ Zone créée - Niveau d'alerte: {niveau_alerte:.1f}/10")
        return zone

# ============================================================
# VALIDATEUR TERRAIN
# ============================================================

class ValidateurTerrain:
    def __init__(self, cartographe):
        self.cartographe = cartographe
    
    def tester_hypothese(self, zone: ZoneDeTension) -> Dict:
        fragments = [self.cartographe.fragments[fid] for fid in zone.fragments_ids if fid in self.cartographe.fragments]
        
        # Compter les fragments suspects (charge émotionnelle élevée)
        fragments_suspects = [f for f in fragments if f.charge_emotionnelle > 7]
        anomalies = len(fragments_suspects)
        
        return {
            "anomalies_detectees": anomalies,
            "hypothese_rejetee": anomalies >= 2,
            "confiance_validation": min(100, anomalies * 30),
            "explication": f"{anomalies} fragment(s) suspect(s) détecté(s)"
        }

# ============================================================
# GÉNÉRATEUR DE CAMPAGNE DE TEST
# ============================================================

class GenerateurCampagne:
    @staticmethod
    def generer(nb_messages: int = 30) -> List[Dict]:
        print(f"  📡 Génération d'une campagne de {nb_messages} messages...")
        
        # 5 faux comptes pour simuler une coordination
        faux_comptes = ["compte1", "compte2", "compte3", "compte4", "compte5"]
        
        # Messages typiques de désinformation
        messages_type = [
            "Les vaccins sont dangereux !",
            "On nous cache la vérité !",
            "Partagez avant suppression !",
            "Les médias mentent !",
            "Révélation choquante !"
        ]
        
        campagne = []
        for i in range(nb_messages):
            campagne.append({
                "auteur": random.choice(faux_comptes),
                "contenu": random.choice(messages_type),
                "charge_emotionnelle": random.uniform(6, 9),  # Charges élevées
                "timestamp": maintenant() + timedelta(minutes=i)
            })
        
        print(f"  ✅ Campagne générée avec {len(set(m['auteur'] for m in campagne))} auteurs")
        return campagne

# ============================================================
# DÉTECTEUR DE RÔLES
# ============================================================

class DetecteurRoles:
    @staticmethod
    def analyser(campagne: List[Dict]) -> Dict[str, Any]:
        # Compter les messages par auteur
        compteur = Counter()
        for message in campagne:
            compteur[message["auteur"]] += 1
        
        # Identifier les super-amplificateurs (plus de 7 messages)
        roles = {}
        super_amplis = []
        amplis = []
        
        for auteur, nb in compteur.items():
            if nb > 7:
                roles[auteur] = "🔴 SUPER-AMPLIFICATEUR"
                super_amplis.append(auteur)
            elif nb > 3:
                roles[auteur] = "🟠 AMPLIFICATEUR"
                amplis.append(auteur)
            else:
                roles[auteur] = "⚪ NORMAL"
        
        return {
            "roles": roles,
            "super_amplificateurs": len(super_amplis),
            "amplificateurs": len(amplis),
            "total_auteurs": len(compteur)
        }

# ============================================================
# SYSTÈME PRINCIPAL
# ============================================================

class SystemeAEGIS:
    def __init__(self):
        self.cartographe = CartographeBrouillage()
        self.validateur = ValidateurTerrain(self.cartographe)
        self.historique_decisions = []
        print("\n" + "="*50)
        print("🚀 AEGIS-Γ INITIALISÉ")
        print("="*50 + "\n")
    
    def analyser_campagne(self, sujet: str, campagne: List[Dict]) -> Dict:
        print(f"\n🔍 ANALYSE DE LA CAMPAGNE: {sujet}")
        print("-" * 40)
        
        # Étape 1 : Ingérer tous les fragments
        print("\n📥 1. INGESTION DES FRAGMENTS")
        for msg in campagne:
            self.cartographe.ajouter_fragment(
                sujet=sujet,
                type_src="post_reseau_social",
                contenu=msg["contenu"],
                charge=msg["charge_emotionnelle"],
                auteur=msg["auteur"]
            )
        
        # Étape 2 : Analyser le sujet
        print("\n📊 2. ANALYSE DES TENSIONS")
        zone = self.cartographe.analyser_sujet(sujet)
        
        if not zone:
            return {"erreur": "Analyse impossible"}
        
        # Étape 3 : Valider l'hypothèse
        print("\n🔬 3. VALIDATION TERRAIN")
        validation = self.validateur.tester_hypothese(zone)
        print(f"   {validation['explication']}")
        print(f"   Confiance: {validation['confiance_validation']}%")
        
        # Étape 4 : Score de confiance final
        score_confiance = min(10, zone.niveau_alerte * 0.7 + validation["confiance_validation"] / 10)
        
        # Étape 5 : Recommandations
        if zone.niveau_alerte >= 7:
            recommandations = ["🔴 URGENT - Enquête prioritaire", "Cartographier les auteurs suspects"]
        elif zone.niveau_alerte >= 5:
            recommandations = ["🟠 Surveillance renforcée", "Analyser les patterns de coordination"]
        else:
            recommandations = ["🟢 Surveillance normale", "Veille informationnelle"]
        
        resultat = {
            "sujet": sujet,
            "niveau_alerte": round(zone.niveau_alerte, 1),
            "score_confiance": round(score_confiance, 1),
            "validation": validation,
            "recommandations": recommandations,
            "zone": zone.to_dict()
        }
        
        self.historique_decisions.append(resultat)
        
        # Afficher le résumé
        print("\n" + "="*40)
        print("📋 RÉSUMÉ DE L'ANALYSE")
        print("="*40)
        print(f"   Sujet: {sujet}")
        print(f"   Niveau d'alerte: {resultat['niveau_alerte']}/10")
        print(f"   Score de confiance: {resultat['score_confiance']}/10")
        print(f"\n   RECOMMANDATIONS:")
        for r in recommandations:
            print(f"   • {r}")
        print("="*40 + "\n")
        
        return resultat

# ============================================================
# FONCTION DE DÉMONSTRATION
# ============================================================

def faire_la_demonstration():
    print("\n" + "🎬"*20)
    print("   AEGIS-Γ - DÉMONSTRATION COMPLÈTE")
    print("🎬"*20 + "\n")
    
    # 1. Créer le système
    print("📌 ÉTAPE 1: Initialisation du système...")
    systeme = SystemeAEGIS()
    
    # 2. Générer une campagne de test
    print("\n📌 ÉTAPE 2: Génération d'une campagne de désinformation...")
    campagne = GenerateurCampagne.generer(nb_messages=20)
    
    # Afficher un aperçu
    print("\n   📝 APERÇU DES MESSAGES:")
    for i, msg in enumerate(campagne[:5]):
        print(f"      [{i+1}] {msg['auteur']}: {msg['contenu']}")
    if len(campagne) > 5:
        print(f"      ... et {len(campagne)-5} autres messages")
    
    # 3. Analyser les rôles
    print("\n📌 ÉTAPE 3: Détection des rôles...")
    analyse_roles = DetecteurRoles.analyser(campagne)
    print(f"\n   👥 RÔLES DÉTECTÉS:")
    print(f"      • Super-amplificateurs: {analyse_roles['super_amplificateurs']}")
    print(f"      • Amplificateurs: {analyse_roles['amplificateurs']}")
    print(f"      • Total acteurs: {analyse_roles['total_auteurs']}")
    
    for auteur, role in list(analyse_roles['roles'].items())[:3]:
        print(f"      • {auteur}: {role}")
    
    # 4. Lancer l'analyse AEGIS
    print("\n📌 ÉTAPE 4: Analyse AEGIS...")
    resultat = systeme.analyser_campagne("desinformation_covid", campagne)
    
    # 5. Conclusion
    print("\n" + "🌟"*20)
    print("   DÉMONSTRATION TERMINÉE")
    print("🌟"*20 + "\n")
    
    return resultat

# ============================================================
# POINT D'ENTRÉE PRINCIPAL
# ============================================================

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--demo", action="store_true", help="Lancer la démonstration")
    parser.add_argument("--test", action="store_true", help="Lancer un test rapide")
    
    args = parser.parse_args()
    
    if args.demo:
        faire_la_demonstration()
    elif args.test:
        print("Test rapide - vérification des imports...")
        print(f"✅ NumPy version: {np.__version__}")
        print("✅ Tous les modules sont chargés")
    else:
        print("AEGIS-Γ - Système de contrôle narratif")
        print("\nPour lancer la démo: python aegis_gamma.py --demo")
        print("Pour tester: python aegis_gamma.py --test")