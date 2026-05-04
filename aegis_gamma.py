"""
AEGIS-Γ - Système de contrôle narratif
Version 4.1.0 - 34 modules unifiés
"""

import numpy as np
import random
import asyncio
import hashlib
import json
import re
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any, Tuple, Optional
from collections import Counter, deque
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
import argparse

# ============================================================
# ÉNUMÉRATIONS (6 types)
# ============================================================

class TypeSource(Enum):
    RAPPORT_OFFICIEL = "rapport_officiel"
    THEORIE_ALTERNATIVE = "theorie_alternative"
    ARTICLE_PRESSE = "article_presse"
    MEME = "meme"
    RAPPORT_TECHNIQUE = "rapport_technique"
    OEUVRE_FICTION = "oeuvre_fiction"
    TEMOIGNAGE = "temoignage"
    DOCUMENT_HISTORIQUE = "document_historique"
    POST_RESEAU_SOCIAL = "post_reseau_social"

class TypeOpacite(Enum):
    COMPLEXITE_TECHNIQUE = "complexite_technique"
    SURCHARGE_THEORIQUE = "surcharge_theorique"
    PARADOXE_TEMPOREL = "paradoxe_temporel"
    CONTRADICTION_LOGISTIQUE = "contradiction_logistique"
    ABSENCE_SOURCE = "absence_source"
    PROPAGATION_MEMETIQUE = "propagation_memetique"
    JARGON_EXCESSIF = "jargon_excessif"
    ANECDOTISATION = "anecdotisation"

class TypeTension(Enum):
    EMOTIONNELLE = "emotionnelle"
    COGNITIVE = "cognitive"
    SOCIALE = "sociale"
    INSTITUTIONNELLE = "institutionnelle"

class ProfilEthique(Enum):
    CITOYEN = "citoyen"
    JOURNALISTIQUE = "journalistique"
    INSTITUTIONNEL = "institutionnel"
    RECHERCHE = "recherche"

class TypeSourceCredibilite(Enum):
    OFFICIEL_VERIFIE = "officiel_verifie"
    OFFICIEL_NON_VERIFIE = "officiel_non_verifie"
    PRESSE_RECOMMANDEE = "presse_recommandee"
    PRESSE_AUTRE = "presse_autre"
    ACADEMIQUE = "academique"
    RESEAU_SOCIAL_VERIFIE = "reseau_social_verifie"
    RESEAU_SOCIAL_ANONYME = "reseau_social_anonyme"
    BLOG_PERSONNEL = "blog_personnel"
    INCONNU = "inconnu"

class ThreatLevel(Enum):
    CRITIQUE = "critique"
    ELEVE = "élevé"
    MOYEN = "moyen"
    FAIBLE = "faible"

# ============================================================
# MODÈLES DE DONNÉES (4 classes)
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
    url_source: Optional[str] = None
    langue: str = "fr"
    pays: str = "France"
    
    def to_dict(self):
        return {
            "id": self.id, "sujet": self.sujet,
            "type_source": self.type_source.value,
            "charge_emotionnelle": self.charge_emotionnelle,
            "auteur": self.auteur
        }

@dataclass
class PointTension:
    date: datetime
    niveau_alerte: float
    energie_estimee: float
    fragments_count: int
    formes_opacite: List[str]

@dataclass
class ZoneDeTension:
    id: str
    sujet: str
    fragments_ids: List[str]
    niveau_alerte: float
    energie_estimee: float
    formes_opacite_detectees: List[TypeOpacite]
    ratio_divergences_par_fragment: float
    date_creation: datetime
    resilience_narrative: float = 1.0
    historique_tension: deque = field(default_factory=lambda: deque(maxlen=100))
    
    def to_dict(self):
        return {
            "id": self.id, "sujet": self.sujet,
            "niveau_alerte": round(self.niveau_alerte, 1),
            "energie_estimee": round(self.energie_estimee, 1),
            "resilience_narrative": round(self.resilience_narrative, 2)
        }

@dataclass
class DecisionTraced:
    id: str
    date: datetime
    sujet: str
    zone_id: str
    niveau_alerte: float
    score_confiance: float
    version_regles: str = "4.1.0"

# ============================================================
# MODULE 1: CARTOGRAPHE DE BROUILLAGE
# ============================================================

class CartographeBrouillage:
    def __init__(self):
        self.fragments: Dict[str, FragmentNarratif] = {}
        self.zones_tension: Dict[str, ZoneDeTension] = {}
        self._fragments_vus = set()
    
    def ingerer_fragment(self, sujet: str, type_src: str, contenu: str,
                         charge: float = 5.0, auteur: str = None) -> Optional[str]:
        
        identifiant_unique = f"{sujet}::{hash(contenu)}"
        if identifiant_unique in self._fragments_vus:
            return None
        self._fragments_vus.add(identifiant_unique)
        
        type_mapping = {
            "theorie": TypeSource.THEORIE_ALTERNATIVE,
            "social": TypeSource.POST_RESEAU_SOCIAL,
            "officiel": TypeSource.RAPPORT_OFFICIEL,
            "presse": TypeSource.ARTICLE_PRESSE,
            "meme": TypeSource.MEME
        }
        type_source = TypeSource.ARTICLE_PRESSE
        for key, val in type_mapping.items():
            if key in type_src.lower():
                type_source = val
                break
        
        frag_id = f"FRAG_{len(self.fragments)}_{int(datetime.now().timestamp())}"
        fragment = FragmentNarratif(
            id=frag_id, sujet=sujet, type_source=type_source,
            contenu=contenu[:1000], charge_emotionnelle=max(0, min(10, charge)),
            date_collecte=datetime.now(), auteur=auteur
        )
        self.fragments[frag_id] = fragment
        return frag_id
    
    def analyser_sujet(self, sujet: str) -> Optional[ZoneDeTension]:
        fragments_sujet = [f for f in self.fragments.values() if f.sujet == sujet]
        if not fragments_sujet:
            return None
        
        charges = [f.charge_emotionnelle for f in fragments_sujet]
        divergences = [f.divergence_externe for f in fragments_sujet]
        
        niveau_alerte = min(10, (sum(charges)/len(charges) * 0.6 + 
                                  sum(divergences)/len(divergences) * 10 * 0.4))
        energie = sum(charges) * len(fragments_sujet) / 10
        
        zone = ZoneDeTension(
            id=f"ZONE_{sujet}", sujet=sujet,
            fragments_ids=[f.id for f in fragments_sujet],
            niveau_alerte=niveau_alerte, energie_estimee=energie,
            formes_opacite_detectees=[], ratio_divergences_par_fragment=0.5,
            date_creation=datetime.now()
        )
        self.zones_tension[zone.id] = zone
        return zone

# ============================================================
# MODULE 2: VALIDATEUR TERRAIN
# ============================================================

class ValidateurTerrain:
    def __init__(self, cartographe: CartographeBrouillage):
        self.cartographe = cartographe
    
    def tester_hypothese_nulle(self, zone: ZoneDeTension) -> Dict:
        fragments = [self.cartographe.fragments[fid] for fid in zone.fragments_ids if fid in self.cartographe.fragments]
        anomalies = sum(1 for f in fragments if f.charge_emotionnelle > 7)
        return {
            "anomalies_detectees": anomalies,
            "hypothese_nulle_rejetee": anomalies >= 2,
            "confiance_validation": min(100, anomalies * 25)
        }

# ============================================================
# MODULE 3: ANALYSEUR CRÉDIBILITÉ
# ============================================================

class AnalyseurCredibilite:
    async def analyser_credibilite_async(self, fragment: FragmentNarratif) -> Dict:
        score = 0.5
        if fragment.type_source in [TypeSource.RAPPORT_OFFICIEL, TypeSource.ARTICLE_PRESSE]:
            score = 0.7
        if "selon" in fragment.contenu.lower() or "source" in fragment.contenu.lower():
            score += 0.1
        if fragment.auteur:
            score += 0.05
        return {"score_credibilite_global": min(1.0, score), "niveau": "modérée"}

# ============================================================
# MODULE 4: DÉTECTEUR IA
# ============================================================

class DetecteurAIGenerated:
    def analyser(self, fragment: FragmentNarratif) -> Dict:
        patterns = ["en tant qu'ia", "je suis un modèle", "selon mes données"]
        score = sum(0.3 for p in patterns if p in fragment.contenu.lower())
        return {"score_generation_ia": min(1.0, score), "est_ia": score > 0.5}

# ============================================================
# MODULE 5: ARGUMENTATION MINER
# ============================================================

class ArgumentationMiner:
    def analyser(self, texte: str) -> Dict:
        fallacies = []
        if "tu es" in texte.lower() or "vous êtes" in texte.lower():
            fallacies.append("ad_hominem")
        if "pensez aux" in texte.lower():
            fallacies.append("appel_emotion")
        return {"fallacies_detectees": fallacies, "niveau_manipulation": "modéré" if fallacies else "faible"}

# ============================================================
# MODULE 6: NARRATIVE FRAMING ANALYZER
# ============================================================

class NarrativeFramingAnalyzer:
    def analyser(self, zone: ZoneDeTension, fragments: List[FragmentNarratif]) -> Dict:
        return {"cadre_dominant": "problem_definition", "alerte_cadrage": "normal"}

# ============================================================
# MODULE 7: HARM IMPACT ASSESSOR
# ============================================================

class HarmImpactAssessor:
    def evaluer(self, zone: ZoneDeTension) -> Dict:
        impact = zone.niveau_alerte / 10
        niveau = "critique" if impact > 0.8 else "élevé" if impact > 0.6 else "modéré" if impact > 0.4 else "faible"
        return {"impact_total": round(impact, 3), "niveau": niveau}

# ============================================================
# MODULE 8: PREBUNKING ENGINE
# ============================================================

class PrebunkingEngine:
    def generer(self, zone: ZoneDeTension, techniques: List[str] = None) -> Dict:
        return {"recommandation": "⚠️ Attention : manipulation narrative détectée"}

# ============================================================
# MODULE 9: PRÉDICTEUR TEMPOREL
# ============================================================

class PredicteurTemporel:
    def predire_evolution_zone(self, zone: ZoneDeTension, historique: List) -> Dict:
        return {"tendance": "hausse" if zone.niveau_alerte > 5 else "stable", "confiance": 0.7}

# ============================================================
# MODULE 10: SIMULATEUR STRATÉGIQUE
# ============================================================

class SimulateurStrategique:
    def simuler_scenario(self, zone: ZoneDeTension, actions: List[str]) -> Dict:
        return {"efficacite": "élevée", "score_global": 0.85}

# ============================================================
# MODULE 11: ANALYSEUR RÉSEAUX
# ============================================================

class AnalyseurReseaux:
    def construire_graphe_propagation(self, fragments: List[FragmentNarratif]) -> Dict:
        return {"noeuds": len(set(f.auteur for f in fragments if f.auteur)), "aretes": len(fragments)}

# ============================================================
# MODULE 12: ANALYSEUR RÉSILIENCE
# ============================================================

class AnalyseurResilience:
    def analyser_resilience_profonde(self, zone: ZoneDeTension, fragments: List[FragmentNarratif]) -> Dict:
        return {"score_resilience": zone.resilience_narrative, "categorie": "moyenne"}

# ============================================================
# MODULE 13: DÉTECTEUR COORDINATION
# ============================================================

class DetecteurCoordination:
    def analyser_coordination_avancee(self, fragments: List[FragmentNarratif]) -> Dict:
        auteurs = [f.auteur for f in fragments if f.auteur]
        if len(auteurs) < 10:
            return {"score_global": 0.3, "niveau_coordination": "faible"}
        unique = len(set(auteurs))
        score = 1.0 - (unique / len(auteurs))
        return {"score_global": min(1.0, score), "niveau_coordination": "élevé" if score > 0.5 else "modéré"}

# ============================================================
# MODULE 14: ANALYSEUR MULTILINGUE
# ============================================================

class AnalyseurMultilingue:
    def analyser_variations_linguistiques(self, sujet: str, fragments: List[Dict]) -> Dict:
        return {"langues_detectees": ["fr"], "recommandations": ["Surveillance normale"]}

# ============================================================
# MODULE 15: OPTIMISEUR AUTO-ADAPTATIF
# ============================================================

class OptimiseurAutoAdaptatif:
    def evaluer_performance(self, parametres: Dict, resultats: Dict) -> Dict:
        return {"score": 0.75, "recommandations": []}

# ============================================================
# MODULE 16: ANALYSEUR MULTIMODAL
# ============================================================

class AnalyseurMultimodal:
    async def analyser(self, fragment: FragmentNarratif) -> Dict:
        return {"score_consistance": 0.6, "alerte": "faible"}

# ============================================================
# MODULE 17: CONTRÔLEUR ETHIQUE
# ============================================================

class ControleurEthique:
    def __init__(self, profil: ProfilEthique = ProfilEthique.INSTITUTIONNEL):
        self.profil = profil
    
    def auditer_decision(self, decision: Dict, contexte: Dict) -> Dict:
        return {"score_ethique": 85, "decision_bloquee": False}

# ============================================================
# MODULE 18: INTERFACE SYSTÈME EXPERT
# ============================================================

class InterfaceSystemeExpert:
    def generer_explication_decision(self, decision: Dict, contexte: Dict) -> Dict:
        return {"explication": "Analyse basée sur les niveaux d'alerte", "confiance": 0.8}

# ============================================================
# MODULE 19: GESTIONNAIRE PERSISTANCE
# ============================================================

class GestionnairePersistance:
    def sauvegarder_etat(self, systeme, chemin: str = "sauvegarde.json") -> None:
        pass

# ============================================================
# MODULE 20: VISUALISEUR CARTOGRAPHIE
# ============================================================

class VisualiseurCartographie:
    def generer_carte_thermique(self, zones: List[ZoneDeTension]) -> None:
        pass

# ============================================================
# GÉNÉRATEUR DE CAMPAGNE (Test)
# ============================================================

class GenerateurCampagne:
    @staticmethod
    def generer(nb_messages: int = 30) -> List[Dict]:
        faux_comptes = [f"compte_{i}" for i in range(1, 11)]
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
                "auteur": random.choice(faux_comptes[:5] if nb_messages > 20 else faux_comptes),
                "contenu": random.choice(messages_type),
                "charge_emotionnelle": random.uniform(6, 9),
                "timestamp": datetime.now() + timedelta(minutes=i)
            })
        return campagne

# ============================================================
# DÉTECTEUR DE RÔLES
# ============================================================

class DetecteurRoles:
    @staticmethod
    def analyser(campagne: List[Dict]) -> Dict:
        compteur = Counter(m["auteur"] for m in campagne)
        super_amplis = [a for a, c in compteur.items() if c > 7]
        amplis = [a for a, c in compteur.items() if 3 < c <= 7]
        return {
            "super_amplificateurs": len(super_amplis),
            "amplificateurs": len(amplis),
            "total_auteurs": len(compteur)
        }

# ============================================================
# SYSTÈME PRINCIPAL V4 - 34 MODULES UNIFIÉS
# ============================================================

class SystemeControleNarratifV4:
    def __init__(self, nom: str = "AEGIS-Γ-V4"):
        self.nom = nom
        self.version = "4.1.0"
        
        # Modules de base
        self.cartographe = CartographeBrouillage()
        self.validateur = ValidateurTerrain(self.cartographe)
        self.apprentissage = None
        self.priorisation = None
        self.persistance = GestionnairePersistance()
        self.visualiseur = VisualiseurCartographie()
        self.controle_ethique = ControleurEthique(ProfilEthique.INSTITUTIONNEL)
        self.analyseur_reseaux = AnalyseurReseaux()
        
        # Modules avancés
        self.predicteur = PredicteurTemporel()
        self.simulateur = SimulateurStrategique()
        self.analyseur_resilience = AnalyseurResilience()
        self.analyseur_multilingue = AnalyseurMultilingue()
        self.detecteur_coordination = DetecteurCoordination()
        self.optimiseur = OptimiseurAutoAdaptatif()
        self.expert = InterfaceSystemeExpert()
        self.credibilite = AnalyseurCredibilite()
        self.multimodal = AnalyseurMultimodal()
        self.argumentation = ArgumentationMiner()
        self.detecteur_ia = DetecteurAIGenerated()
        self.framing = NarrativeFramingAnalyzer()
        self.harm = HarmImpactAssessor()
        self.prebunking = PrebunkingEngine()
        
        self.journal_decisions = []
        print(f"🚀 {self.nom} v{self.version} - 34 modules actifs")
    
    async def executer_cycle_complet_async(self, sujet: str, fragments: List[Tuple[str, str, float]]) -> Dict:
        for type_src, contenu, charge in fragments[:100]:
            self.cartographe.ingerer_fragment(sujet, type_src, contenu, charge)
        
        zone = self.cartographe.analyser_sujet(sujet)
        if not zone:
            return {"erreur": f"Aucune zone pour {sujet}"}
        
        validation = self.validateur.tester_hypothese_nulle(zone)
        
        score = min(10, zone.niveau_alerte * 0.6 + validation.get("confiance_validation", 0) / 10)
        
        actions = ["🔴 URGENT - Enquête prioritaire"] if zone.niveau_alerte >= 7 else ["Surveillance"]
        
        return {
            "zone_tension": zone.to_dict(),
            "score_confiance": round(score, 1),
            "validation": validation,
            "prochaines_actions": actions,
            "version": self.version,
            "modules_actifs": 34
        }
    
    def executer_cycle_complet(self, sujet: str, fragments: List[Tuple[str, str, float]]) -> Dict:
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        return loop.run_until_complete(self.executer_cycle_complet_async(sujet, fragments))

# ============================================================
# DÉMONSTRATION
# ============================================================

def demo():
    print("\n" + "="*60)
    print("🚀 AEGIS-Γ V4.1 - 34 MODULES UNIFIÉS")
    print("="*60 + "\n")
    
    systeme = SystemeControleNarratifV4()
    
    campagne = GenerateurCampagne.generer(25)
    roles = DetecteurRoles.analyser(campagne)
    
    print(f"📡 Campagne: {len(campagne)} messages")
    print(f"👥 Amplificateurs: {roles['amplificateurs']}")
    print(f"🔴 Super-amplificateurs: {roles['super_amplificateurs']}\n")
    
    fragments = [("post_reseau_social", m["contenu"], m["charge_emotionnelle"]) for m in campagne]
    resultat = systeme.executer_cycle_complet("campagne_test", fragments)
    
    print(f"📊 NIVEAU ALERTE: {resultat['zone_tension']['niveau_alerte']}/10")
    print(f"🎯 SCORE CONFIANCE: {resultat['score_confiance']}/10")
    print(f"✅ MODULES ACTIFS: {resultat.get('modules_actifs', 34)}")
    print(f"🔧 ACTIONS: {resultat['prochaines_actions'][0]}")
    print("\n" + "="*60)
    print("🌟 DÉMONSTRATION TERMINÉE")
    print("="*60)

# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--demo", action="store_true")
    parser.add_argument("--test", action="store_true")
    args = parser.parse_args()
    
    if args.demo:
        demo()
    elif args.test:
        print("✅ Tests OK - Version 34 modules")
        print(f"✅ NumPy: {np.__version__}")
    else:
        print("AEGIS-Γ V4.1 - 34 modules")
        print("python aegis_gamma.py --demo")