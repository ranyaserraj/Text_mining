"""
Projet d'Analyse de Text Mining - VERSION FINALE
Discours des Partis Politiques Marocains

APPROCHE HYBRIDE:
- Topics: Approche manuelle avec 14 themes predefinis (plus clair)
- Sentiment: Rule-Based + ML supervise (BERT optionnel)
- Visualisations: Professionnelles avec noms clairs
"""

import os
import re
from collections import Counter, defaultdict
from itertools import combinations
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import spacy
import warnings
warnings.filterwarnings('ignore')

# Tentative d'import BERT (optionnel)
try:
    from transformers import pipeline
    import torch
    BERT_AVAILABLE = True
except:
    BERT_AVAILABLE = False

print("="*80)
print("CHARGEMENT DES MODELES")
print("="*80)

# SpaCy
try:
    nlp = spacy.load("fr_core_news_sm")
    print("[OK] Modele spaCy francais charge")
except OSError:
    print("[ERREUR] Modele spaCy non trouve")
    nlp = None

# BERT (optionnel)
sentiment_classifier = None
if BERT_AVAILABLE:
    try:
        print("[INFO] Chargement du modele BERT pour sentiment...")
        sentiment_classifier = pipeline(
            "sentiment-analysis",
            model="nlptown/bert-base-multilingual-uncased-sentiment",
            device=-1  # CPU
        )
        print("[OK] Modele BERT charge (Classification SUPERVISEE)")
    except Exception as e:
        print(f"[AVERTISSEMENT] BERT non disponible: {str(e)[:50]}")
        sentiment_classifier = None

print("="*80)
print()

plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['figure.figsize'] = (14, 8)
sns.set_style("whitegrid")

class AnalyseTextMiningFinal:
    """Classe finale pour analyse text mining hybride"""
    
    def __init__(self, dossier="."):
        self.dossier = dossier
        self.partis = ["PAM", "PI", "PJD", "RNI"]
        self.textes_bruts = {}
        self.textes_nettoyes = {}
        self.themes_par_parti = {}
        self.sentiments_rulebased = {}
        self.sentiments_ml = {}
        
        self.stopwords_fr = set([
            'le', 'la', 'les', 'un', 'une', 'des', 'de', 'du', 'et', 'ou', 'mais',
            'donc', 'car', 'ni', 'ne', 'dans', 'par', 'pour', 'avec', 'sans',
            'sur', 'sous', 'entre', 'vers', 'chez', 'ce', 'ces', 'cet', 'cette',
            'mon', 'ton', 'son', 'notre', 'votre', 'leur', 'mes', 'tes', 'ses',
            'nos', 'vos', 'leurs', 'je', 'tu', 'il', 'elle', 'nous', 'vous', 'ils',
            'elles', 'on', 'qui', 'que', 'quoi', 'dont', 'ou', 'est', 'sont', 'etre',
            'avoir', 'faire', 'dire', 'aller', 'voir', 'pouvoir', 'vouloir', 'au',
            'aux', 'a', 'plus', 'moins', 'tres', 'tout', 'tous', 'toute', 'toutes',
            'meme', 'si', 'ainsi', 'aussi', 'encore', 'deja', 'comme', 'apres',
            'avant', 'pendant', 'depuis', 'alors', 'encore', 'enfin', 'puis',
            's', 'd', 'l', 'c', 'j', 'n', 'm', 't', 'qu', 'ete', 'a', 'ont', 'etait'
        ])
        
        # 14 THEMES PREDEFINIS (Approche manuelle - plus claire)
        self.themes_keywords = {
            'Education': ['ecole', 'education', 'enseignement', 'eleve', 'formation', 
                         'universite', 'professeur', 'enseignant', 'scolarite',
                         'scolaire', 'etudiant', 'apprentissage', 'prescolaire'],
            'Sante': ['sante', 'medical', 'hopital', 'soin', 'medecin', 'amo', 
                     'assurance', 'maladie', 'hospitalier', 'ramediste', 'ramed',
                     'professionnel', 'prestation'],
            'Emploi': ['emploi', 'travail', 'chomage', 'recrutement', 'jeune',
                      'stage', 'entreprise', 'salaire', 'prime', 'poste', 'creation'],
            'Economie': ['economie', 'croissance', 'investissement', 'developpement',
                        'pib', 'industriel', 'secteur', 'ressource', 'financier',
                        'industrie', 'production', 'tissu', 'richesse', 'exportation'],
            'Logement': ['logement', 'habitat', 'construction', 'batiment',
                        'immobilier', 'menage', 'habitation', 'ruine'],
            'Justice': ['justice', 'droit', 'loi', 'equite', 'corruption',
                       'transparence', 'legal', 'tribunal', 'equitable', 'hogra',
                       'legislatif', 'reglementation'],
            'Social': ['social', 'pauvrete', 'solidarite', 'inegalite', 'dignite',
                      'vulnerable', 'citoyen', 'population', 'societe', 'menage',
                      'personne', 'age', 'revenu', 'pouvoir', 'achat'],
            'Environnement': ['environnement', 'eau', 'energie', 'hydrique', 'climat',
                            'ressource', 'durabilite', 'renouvelable', 'energetique',
                            'hydrocarbure', 'pollution', 'ecologique'],
            'Gouvernance': ['gouvernance', 'politique', 'institution', 'administration',
                          'etat', 'public', 'reforme', 'democratie', 'regionalisation',
                          'gouvernement', 'autorite', 'concurrence', 'regulation'],
            'Agriculture': ['agriculture', 'rural', 'agriculteur', 'agricole', 
                          'culture', 'territorial', 'territoire', 'oasis', 'montagne'],
            'Tourisme': ['tourisme', 'touristique', 'hotel', 'visiteur'],
            'Droits_Femme': ['femme', 'famille', 'genre', 'egalite'],
            'Jeunesse': ['jeunesse', 'jeune', 'etudiant'],
            'Infrastructure': ['infrastructure', 'route', 'transport', 'autoroute',
                             'pont', 'equipement', 'connectivite']
        }
        
        # Sentiments
        self.sentiment_positif = [
            'ameliorer', 'renforcer', 'developper', 'garantir', 'soutenir',
            'creer', 'augmenter', 'elargir', 'encourager', 'promouvoir',
            'favoriser', 'valoriser', 'moderniser', 'reussir', 'succes', 'progres',
            'avancee', 'meilleur', 'optimiser', 'accompagner', 'confiance', 'restaurer',
            'assurer', 'prosperite', 'qualite', 'efficace', 'performance', 'excellence'
        ]
        
        self.sentiment_negatif = [
            'probleme', 'crise', 'difficulte', 'manque', 'insuffisant',
            'faible', 'retard', 'echec', 'penurie', 'carence', 'deficit',
            'deterioration', 'baisse', 'recul', 'stagnation', 'inefficace',
            'corruption', 'inegalite', 'injustice', 'hogra', 'vulnerabilite'
        ]
        
        self.sentiment_neutre = [
            'situation', 'contexte', 'niveau', 'taux', 'nombre', 'secteur',
            'domaine', 'projet', 'programme', 'mesure', 'action', 'politique'
        ]
    
    def charger_fichiers(self):
        """Charge les fichiers"""
        print("="*80)
        print("CHARGEMENT DES FICHIERS")
        print("="*80)
        
        for parti in self.partis:
            fichier = os.path.join(self.dossier, f"{parti}_Discours.txt")
            try:
                with open(fichier, 'r', encoding='utf-8') as f:
                    texte = f.read()
                    self.textes_bruts[parti] = texte
                    nb_mots = len(texte.split())
                    print(f"[OK] {parti}: {nb_mots} mots charges")
            except FileNotFoundError:
                print(f"[ERREUR] Fichier {fichier} introuvable")
                self.textes_bruts[parti] = ""
        
        print()
    
    def pretraiter_textes(self):
        """Pretraitement avec lemmatisation"""
        print("="*80)
        print("PRETRAITEMENT AVEC LEMMATISATION")
        print("="*80)
        
        for parti, texte in self.textes_bruts.items():
            texte_propre = texte.lower()
            texte_propre = re.sub(r'[^\w\s]', ' ', texte_propre)
            texte_propre = re.sub(r'\d+', '', texte_propre)
            texte_propre = re.sub(r'\s+', ' ', texte_propre).strip()
            
            if nlp:
                doc = nlp(texte_propre)
                lemmes = [
                    token.lemma_ for token in doc 
                    if not token.is_punct 
                    and not token.is_space 
                    and token.lemma_ not in self.stopwords_fr
                    and len(token.lemma_) > 2
                ]
                texte_final = ' '.join(lemmes)
                reduction = ((len(texte_propre.split()) - len(lemmes)) / len(texte_propre.split())) * 100
                print(f"[OK] {parti}: {len(texte_propre.split())} mots -> {len(lemmes)} lemmes ({reduction:.1f}% reduction)")
            else:
                mots = [mot for mot in texte_propre.split() 
                       if mot not in self.stopwords_fr and len(mot) > 2]
                texte_final = ' '.join(mots)
                print(f"[OK] {parti}: {len(texte_propre.split())} mots -> {len(mots)} mots filtres")
            
            self.textes_nettoyes[parti] = texte_final
        
        print()
    
    def analyser_themes(self):
        """Analyse thematique MANUELLE (14 themes predefinis)"""
        print("="*80)
        print("ANALYSE THEMATIQUE (Approche Manuelle)")
        print("="*80)
        print(f"14 themes predefinis analyses")
        print()
        
        for parti, texte in self.textes_nettoyes.items():
            mots = texte.split()
            themes_count = {}
            
            for theme, keywords in self.themes_keywords.items():
                count = sum(1 for mot in mots if mot in keywords)
                themes_count[theme] = count
            
            self.themes_par_parti[parti] = themes_count
            
            # Top 3 themes
            top_themes = sorted(themes_count.items(), key=lambda x: x[1], reverse=True)[:3]
            print(f"[OK] {parti}:")
            for theme, count in top_themes:
                print(f"     - {theme}: {count} mentions")
        
        print()
    
    def analyser_sentiments_rulebased(self):
        """Sentiment Rule-Based (Baseline)"""
        print("="*80)
        print("SENTIMENT ANALYSIS : Rule-Based (Baseline)")
        print("="*80)
        
        for parti, texte in self.textes_nettoyes.items():
            mots = texte.split()
            
            nb_positif = sum(1 for mot in mots if mot in self.sentiment_positif)
            nb_negatif = sum(1 for mot in mots if mot in self.sentiment_negatif)
            nb_neutre = sum(1 for mot in mots if mot in self.sentiment_neutre)
            
            total = nb_positif + nb_negatif + nb_neutre
            
            if total > 0:
                score = (nb_positif - nb_negatif) / total
            else:
                score = 0
            
            if score > 0.1:
                label = "Positif"
            elif score < -0.1:
                label = "Negatif"
            else:
                label = "Neutre"
            
            self.sentiments_rulebased[parti] = {
                'positifs': nb_positif,
                'negatifs': nb_negatif,
                'neutres': nb_neutre,
                'score': score,
                'label': label
            }
            
            print(f"[OK] {parti}: {label} (score: {score:+.3f})")
        
        print()
    
    def analyser_sentiments_ml(self):
        """Sentiment ML Supervise (BERT)"""
        print("="*80)
        print("SENTIMENT ANALYSIS : ML Supervise (BERT)")
        print("="*80)
        
        if not sentiment_classifier:
            print("[INFO] BERT non disponible - utiliser seulement Rule-Based")
            print()
            return
        
        for parti, texte in self.textes_bruts.items():
            segments = self.decouper_texte(texte, max_length=500)
            
            scores_numeriques = []
            
            print(f"[INFO] Analyse {parti}: {len(segments)} segments...")
            
            for segment in segments[:10]:  # Limite a 10 segments pour rapidite
                try:
                    result = sentiment_classifier(segment)[0]
                    label = result['label']
                    
                    if '1 star' in label:
                        score_num = -1.0
                    elif '2 stars' in label:
                        score_num = -0.5
                    elif '3 stars' in label:
                        score_num = 0.0
                    elif '4 stars' in label:
                        score_num = 0.5
                    elif '5 stars' in label:
                        score_num = 1.0
                    else:
                        score_num = 0.0
                    
                    scores_numeriques.append(score_num)
                    
                except Exception as e:
                    scores_numeriques.append(0.0)
            
            if scores_numeriques:
                score_moyen = np.mean(scores_numeriques)
                
                if score_moyen > 0.3:
                    label_final = "Positif"
                elif score_moyen < -0.3:
                    label_final = "Negatif"
                else:
                    label_final = "Neutre"
                
                self.sentiments_ml[parti] = {
                    'score': score_moyen,
                    'label': label_final
                }
                
                print(f"[OK] {parti}: {label_final} (score ML: {score_moyen:+.3f})")
        
        print()
    
    def decouper_texte(self, texte, max_length=500):
        """Decoupe texte en segments"""
        mots = texte.split()
        segments = []
        for i in range(0, len(mots), max_length):
            segment = ' '.join(mots[i:i+max_length])
            segments.append(segment)
        return segments
    
    # ========================================================================
    # VISUALISATIONS
    # ========================================================================
    
    def visualiser_themes(self):
        """Graphique themes par parti"""
        print("="*80)
        print("GENERATION: Graphique Themes par Parti")
        print("="*80)
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 7))
        
        # Graphique 1: Top 5 themes par parti
        colors_partis = {'PAM': '#e74c3c', 'PI': '#3498db', 'PJD': '#2ecc71', 'RNI': '#f39c12'}
        
        for idx, parti in enumerate(self.partis):
            themes_count = self.themes_par_parti[parti]
            top_themes = sorted(themes_count.items(), key=lambda x: x[1], reverse=True)[:5]
            
            themes_names = [t[0] for t in top_themes]
            themes_values = [t[1] for t in top_themes]
            
            y_pos = np.arange(len(themes_names)) + idx * 6
            
            ax1.barh(y_pos, themes_values, height=0.8, 
                    label=parti, color=colors_partis[parti], alpha=0.8, edgecolor='black')
            
            for i, (name, value) in enumerate(zip(themes_names, themes_values)):
                ax1.text(value + 1, y_pos[i], f'{name} ({value})', 
                        va='center', fontsize=9, fontweight='bold')
        
        ax1.set_xlabel('Nombre de mentions', fontsize=13, fontweight='bold')
        ax1.set_title('Top 5 Themes par Parti (Approche Manuelle)', fontsize=15, fontweight='bold')
        ax1.legend(loc='lower right', fontsize=11)
        ax1.set_yticks([])
        ax1.grid(axis='x', alpha=0.3)
        
        # Graphique 2: Heatmap tous themes
        data_heatmap = []
        themes_order = list(self.themes_keywords.keys())
        
        for parti in self.partis:
            row = [self.themes_par_parti[parti][theme] for theme in themes_order]
            data_heatmap.append(row)
        
        data_heatmap = np.array(data_heatmap)
        
        im = ax2.imshow(data_heatmap, cmap='YlOrRd', aspect='auto')
        
        ax2.set_xticks(np.arange(len(themes_order)))
        ax2.set_yticks(np.arange(len(self.partis)))
        ax2.set_xticklabels(themes_order, rotation=45, ha='right', fontsize=10)
        ax2.set_yticklabels(self.partis, fontsize=12, fontweight='bold')
        
        ax2.set_title('Heatmap : Intensite des 14 Themes', fontsize=15, fontweight='bold')
        
        # Annoter les valeurs
        for i in range(len(self.partis)):
            for j in range(len(themes_order)):
                value = data_heatmap[i, j]
                if value > 0:
                    ax2.text(j, i, int(value), ha='center', va='center', 
                            color='white' if value > data_heatmap.max()/2 else 'black',
                            fontsize=8, fontweight='bold')
        
        plt.colorbar(im, ax=ax2, label='Nombre de mentions')
        
        plt.tight_layout()
        plt.savefig('themes_analyse_manuelle.png', dpi=300, bbox_inches='tight')
        print("[OK] Graphique sauvegarde: themes_analyse_manuelle.png")
        print()
    
    def visualiser_sentiments(self):
        """Graphique sentiments (Rule-Based et optionnel ML)"""
        print("="*80)
        print("GENERATION: Graphique Sentiments")
        print("="*80)
        
        if self.sentiments_ml:
            # Avec ML: 2 graphiques côte à côte
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
            
            partis = list(self.sentiments_rulebased.keys())
            scores_rb = [self.sentiments_rulebased[p]['score'] for p in partis]
            scores_ml = [self.sentiments_ml[p]['score'] for p in partis]
            
            colors_rb = ['#2ecc71' if s > 0.1 else '#e74c3c' if s < -0.1 else '#95a5a6' for s in scores_rb]
            colors_ml = ['#2ecc71' if s > 0.3 else '#e74c3c' if s < -0.3 else '#95a5a6' for s in scores_ml]
            
            # Graphique 1: Rule-Based
            ax1.barh(partis, scores_rb, color=colors_rb, alpha=0.8, edgecolor='black', linewidth=1.5)
            ax1.axvline(x=0, color='black', linestyle='--', linewidth=1.5)
            ax1.set_xlabel('Score de Sentiment', fontsize=13, fontweight='bold')
            ax1.set_title('Sentiment Rule-Based (Lexicon)', fontsize=14, fontweight='bold')
            ax1.set_xlim(-1, 1)
            ax1.grid(axis='x', alpha=0.3)
            
            for i, (parti, score) in enumerate(zip(partis, scores_rb)):
                label = self.sentiments_rulebased[parti]['label']
                ax1.text(score + 0.05 if score > 0 else score - 0.05, i, 
                        f'{score:+.3f}\n{label}', va='center', fontsize=10, fontweight='bold')
            
            # Graphique 2: ML
            ax2.barh(partis, scores_ml, color=colors_ml, alpha=0.8, edgecolor='black', linewidth=1.5)
            ax2.axvline(x=0, color='black', linestyle='--', linewidth=1.5)
            ax2.set_xlabel('Score de Sentiment', fontsize=13, fontweight='bold')
            ax2.set_title('Sentiment ML Supervise (BERT)', fontsize=14, fontweight='bold')
            ax2.set_xlim(-1, 1)
            ax2.grid(axis='x', alpha=0.3)
            
            for i, (parti, score) in enumerate(zip(partis, scores_ml)):
                label = self.sentiments_ml[parti]['label']
                ax2.text(score + 0.05 if score > 0 else score - 0.05, i, 
                        f'{score:+.3f}\n{label}', va='center', fontsize=10, fontweight='bold')
            
        else:
            # Sans ML: 1 graphique seul
            fig, ax1 = plt.subplots(1, 1, figsize=(10, 6))
            
            partis = list(self.sentiments_rulebased.keys())
            scores_rb = [self.sentiments_rulebased[p]['score'] for p in partis]
            colors_rb = ['#2ecc71' if s > 0.1 else '#e74c3c' if s < -0.1 else '#95a5a6' for s in scores_rb]
            
            ax1.barh(partis, scores_rb, color=colors_rb, alpha=0.8, edgecolor='black', linewidth=1.5)
            ax1.axvline(x=0, color='black', linestyle='--', linewidth=1.5)
            ax1.set_xlabel('Score de Sentiment', fontsize=13, fontweight='bold')
            ax1.set_title('Sentiment Analysis Rule-Based', fontsize=15, fontweight='bold')
            ax1.set_xlim(-1, 1)
            ax1.grid(axis='x', alpha=0.3)
            
            for i, (parti, score) in enumerate(zip(partis, scores_rb)):
                label = self.sentiments_rulebased[parti]['label']
                ax1.text(score + 0.05 if score > 0 else score - 0.05, i, 
                        f'{score:+.3f}\n{label}', va='center', fontsize=11, fontweight='bold')
        
        plt.tight_layout()
        plt.savefig('sentiments_analyse.png', dpi=300, bbox_inches='tight')
        print("[OK] Graphique sauvegarde: sentiments_analyse.png")
        print()
    
    def visualiser_resume(self):
        """Graphique resume complet"""
        print("="*80)
        print("GENERATION: Graphique Resume Complet")
        print("="*80)
        
        fig = plt.figure(figsize=(18, 10))
        gs = fig.add_gridspec(2, 2, hspace=0.3, wspace=0.3)
        
        partis = self.partis
        colors_partis = {'PAM': '#e74c3c', 'PI': '#3498db', 'PJD': '#2ecc71', 'RNI': '#f39c12'}
        
        # 1. Sentiment
        ax1 = fig.add_subplot(gs[0, 0])
        scores = [self.sentiments_rulebased[p]['score'] for p in partis]
        colors_bars = [colors_partis[p] for p in partis]
        ax1.bar(partis, scores, color=colors_bars, alpha=0.7, edgecolor='black', linewidth=1.5)
        ax1.axhline(y=0, color='black', linestyle='--', linewidth=1)
        ax1.set_ylabel('Score Sentiment', fontweight='bold')
        ax1.set_title('1. Sentiment (Rule-Based)', fontsize=13, fontweight='bold')
        ax1.grid(axis='y', alpha=0.3)
        ax1.set_ylim(-1, 1)
        
        # 2. Volume de lemmes
        ax2 = fig.add_subplot(gs[0, 1])
        volumes = [len(self.textes_nettoyes[p].split()) for p in partis]
        ax2.bar(partis, volumes, color=colors_bars, alpha=0.7, edgecolor='black', linewidth=1.5)
        ax2.set_ylabel('Nombre de lemmes', fontweight='bold')
        ax2.set_title('2. Volume de Discours', fontsize=13, fontweight='bold')
        ax2.grid(axis='y', alpha=0.3)
        
        # 3. Top theme par parti
        ax3 = fig.add_subplot(gs[1, 0])
        top_themes = []
        top_values = []
        for p in partis:
            themes = self.themes_par_parti[p]
            top = sorted(themes.items(), key=lambda x: x[1], reverse=True)[0]
            top_themes.append(f"{p}\n{top[0]}")
            top_values.append(top[1])
        
        x_pos = np.arange(len(partis))
        ax3.bar(x_pos, top_values, color=colors_bars, alpha=0.7, edgecolor='black', linewidth=1.5)
        ax3.set_xticks(x_pos)
        ax3.set_xticklabels(top_themes, fontsize=10)
        ax3.set_ylabel('Nombre de mentions', fontweight='bold')
        ax3.set_title('3. Theme Dominant par Parti', fontsize=13, fontweight='bold')
        ax3.grid(axis='y', alpha=0.3)
        
        # 4. Comparaison sentiment si ML disponible
        ax4 = fig.add_subplot(gs[1, 1])
        if self.sentiments_ml:
            x = np.arange(len(partis))
            width = 0.35
            
            scores_rb = [self.sentiments_rulebased[p]['score'] for p in partis]
            scores_ml = [self.sentiments_ml[p]['score'] for p in partis]
            
            ax4.bar(x - width/2, scores_rb, width, label='Rule-Based', 
                   color='#3498db', alpha=0.7, edgecolor='black')
            ax4.bar(x + width/2, scores_ml, width, label='ML (BERT)', 
                   color='#e74c3c', alpha=0.7, edgecolor='black')
            
            ax4.set_ylabel('Score Sentiment', fontweight='bold')
            ax4.set_title('4. Comparaison Rule-Based vs ML', fontsize=13, fontweight='bold')
            ax4.set_xticks(x)
            ax4.set_xticklabels(partis)
            ax4.legend()
            ax4.axhline(y=0, color='black', linestyle='--', linewidth=1)
            ax4.grid(axis='y', alpha=0.3)
        else:
            # Distribution pos/neg/neutre
            data_dist = []
            for parti in partis:
                s = self.sentiments_rulebased[parti]
                total = s['positifs'] + s['negatifs'] + s['neutres']
                if total > 0:
                    data_dist.append([s['positifs'], s['neutres'], s['negatifs']])
                else:
                    data_dist.append([0, 0, 0])
            
            data_dist = np.array(data_dist)
            x = np.arange(len(partis))
            
            ax4.bar(x, data_dist[:, 0], label='Positif', color='#2ecc71', alpha=0.7, edgecolor='black')
            ax4.bar(x, data_dist[:, 1], bottom=data_dist[:, 0], label='Neutre', 
                   color='#95a5a6', alpha=0.7, edgecolor='black')
            ax4.bar(x, data_dist[:, 2], bottom=data_dist[:, 0]+data_dist[:, 1], 
                   label='Negatif', color='#e74c3c', alpha=0.7, edgecolor='black')
            
            ax4.set_ylabel('Nombre de mots', fontweight='bold')
            ax4.set_title('4. Distribution des Mots de Sentiment', fontsize=13, fontweight='bold')
            ax4.set_xticks(x)
            ax4.set_xticklabels(partis)
            ax4.legend()
            ax4.grid(axis='y', alpha=0.3)
        
        plt.suptitle('RESUME COMPLET - Analyse Text Mining', fontsize=16, fontweight='bold', y=0.98)
        
        plt.savefig('resume_complet.png', dpi=300, bbox_inches='tight')
        print("[OK] Graphique sauvegarde: resume_complet.png")
        print()
    
    def generer_rapport(self):
        """Rapport textuel"""
        print("="*80)
        print("GENERATION: Rapport Textuel")
        print("="*80)
        
        rapport = []
        rapport.append("="*80)
        rapport.append("RAPPORT D'ANALYSE TEXT MINING")
        rapport.append("Version Finale Hybride")
        rapport.append("="*80)
        rapport.append("")
        rapport.append("METHODOLOGIE:")
        rapport.append("- Topics: Approche manuelle avec 14 themes predefinis")
        rapport.append("- Sentiment: Rule-Based + ML supervise (BERT)")
        rapport.append("")
        
        for parti in self.partis:
            rapport.append(f"\n{'='*80}")
            rapport.append(f"PARTI : {parti}")
            rapport.append(f"{'='*80}\n")
            
            # Volume
            nb_lemmes = len(self.textes_nettoyes[parti].split())
            rapport.append(f"Volume : {nb_lemmes} lemmes")
            rapport.append("")
            
            # Themes
            themes = self.themes_par_parti[parti]
            top_themes = sorted(themes.items(), key=lambda x: x[1], reverse=True)[:5]
            rapport.append("Top 5 Themes:")
            for theme, count in top_themes:
                rapport.append(f"  - {theme}: {count} mentions")
            rapport.append("")
            
            # Sentiment
            sent_rb = self.sentiments_rulebased[parti]
            rapport.append(f"Sentiment Rule-Based:")
            rapport.append(f"  Label: {sent_rb['label']}")
            rapport.append(f"  Score: {sent_rb['score']:+.3f}")
            rapport.append("")
            
            if parti in self.sentiments_ml:
                sent_ml = self.sentiments_ml[parti]
                rapport.append(f"Sentiment ML (BERT):")
                rapport.append(f"  Label: {sent_ml['label']}")
                rapport.append(f"  Score: {sent_ml['score']:+.3f}")
                rapport.append("")
        
        rapport.append("\n" + "="*80)
        rapport.append("FIN DU RAPPORT")
        rapport.append("="*80)
        
        with open('rapport_final.txt', 'w', encoding='utf-8') as f:
            f.write('\n'.join(rapport))
        
        print("[OK] Rapport sauvegarde: rapport_final.txt")
        print()
    
    def generer_tableau_excel(self):
        """Tableau Excel comparatif"""
        print("="*80)
        print("GENERATION: Tableau Excel")
        print("="*80)
        
        data = []
        
        for parti in self.partis:
            row = {'Parti': parti}
            
            # Volume
            row['Lemmes'] = len(self.textes_nettoyes[parti].split())
            
            # Theme dominant
            themes = self.themes_par_parti[parti]
            top_theme = sorted(themes.items(), key=lambda x: x[1], reverse=True)[0]
            row['Theme_Dominant'] = top_theme[0]
            row['Theme_Mentions'] = top_theme[1]
            
            # Sentiment RB
            sent_rb = self.sentiments_rulebased[parti]
            row['Sentiment_RB_Label'] = sent_rb['label']
            row['Sentiment_RB_Score'] = sent_rb['score']
            
            # Sentiment ML
            if parti in self.sentiments_ml:
                sent_ml = self.sentiments_ml[parti]
                row['Sentiment_ML_Label'] = sent_ml['label']
                row['Sentiment_ML_Score'] = sent_ml['score']
            
            data.append(row)
        
        df = pd.DataFrame(data)
        
        df.to_excel('synthese_finale.xlsx', index=False)
        df.to_csv('synthese_finale.csv', index=False, encoding='utf-8')
        
        print("[OK] Tableaux sauvegardes:")
        print("     - synthese_finale.xlsx")
        print("     - synthese_finale.csv")
        print()
        print("Apercu:")
        print(df.to_string())
        print()
    
    def executer_analyse_complete(self):
        """Execute l'analyse complete"""
        print("\n")
        print("="*80)
        print("ANALYSE TEXT MINING - VERSION FINALE HYBRIDE")
        print("="*80)
        print()
        
        self.charger_fichiers()
        self.pretraiter_textes()
        
        # Topics : Approche manuelle
        self.analyser_themes()
        
        # Sentiment : Rule-Based + ML
        self.analyser_sentiments_rulebased()
        self.analyser_sentiments_ml()
        
        # Visualisations
        self.visualiser_themes()
        self.visualiser_sentiments()
        self.visualiser_resume()
        
        # Rapports
        self.generer_rapport()
        self.generer_tableau_excel()
        
        print("="*80)
        print("ANALYSE COMPLETE TERMINEE")
        print("="*80)
        print()
        print("FICHIERS GENERES:")
        print("  1. themes_analyse_manuelle.png  <- 14 themes predefinis")
        print("  2. sentiments_analyse.png       <- Rule-Based + ML (si dispo)")
        print("  3. resume_complet.png           <- Vue d'ensemble")
        print("  4. rapport_final.txt            <- Rapport textuel")
        print("  5. synthese_finale.xlsx/csv     <- Tableau Excel")
        print()


if __name__ == "__main__":
    print("\n" * 2)
    print("="*80)
    print("=         ANALYSE TEXT MINING - VERSION FINALE HYBRIDE               =")
    print("=           Discours Politiques Marocains                            =")
    print("="*80)
    print()
    
    analyse = AnalyseTextMiningFinal(dossier=".")
    analyse.executer_analyse_complete()
    
    print("\n" * 2)
    print("="*80)
    print("PROJET TERMINE - Version Finale Hybride")
    print("Topics: Approche Manuelle | Sentiment: Rule-Based + ML")
    print("="*80)

