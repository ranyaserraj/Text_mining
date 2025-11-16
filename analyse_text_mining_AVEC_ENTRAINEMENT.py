"""
Projet d'Analyse de Text Mining AVEC ENTRAINEMENT DE MODELE
Discours des Partis Politiques Marocains

APPROCHE FINALE:
- Topics: Approche manuelle avec 14 themes predefinis
- Sentiment: Rule-Based + MODELE ENTRAINE (Classification Supervisee)
  * Création d'un dataset d'entrainement
  * Entrainement d'un classifieur (Naive Bayes, SVM, etc.)
  * Comparaison Rule-Based vs Modele Entraine
"""

import os
import re
from collections import Counter
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import spacy
import warnings
warnings.filterwarnings('ignore')

# Imports Machine Learning
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import pickle

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

print("="*80)
print()

plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['figure.figsize'] = (14, 8)
sns.set_style("whitegrid")

class AnalyseTextMiningAvecEntrainement:
    """Classe avec entrainement de modele de classification"""
    
    def __init__(self, dossier="."):
        self.dossier = dossier
        self.partis = ["PAM", "PI", "PJD", "RNI"]
        self.textes_bruts = {}
        self.textes_nettoyes = {}
        self.themes_par_parti = {}
        self.sentiments_rulebased = {}
        self.sentiments_ml_entraine = {}
        
        # Modele entraine
        self.modele_sentiment = None
        self.vectorizer = None
        
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
        
        # 14 THEMES PREDEFINIS
        self.themes_keywords = {
            'Education': ['ecole', 'education', 'enseignement', 'eleve', 'formation', 
                         'universite', 'professeur', 'enseignant', 'scolarite',
                         'scolaire', 'etudiant', 'apprentissage', 'prescolaire'],
            'Sante': ['sante', 'medical', 'hopital', 'soin', 'medecin', 'amo', 
                     'assurance', 'maladie', 'hospitalier', 'ramediste', 'ramed'],
            'Emploi': ['emploi', 'travail', 'chomage', 'recrutement', 'jeune',
                      'stage', 'entreprise', 'salaire', 'prime', 'poste', 'creation'],
            'Economie': ['economie', 'croissance', 'investissement', 'developpement',
                        'pib', 'industriel', 'secteur', 'ressource', 'financier',
                        'industrie', 'production', 'tissu', 'richesse', 'exportation'],
            'Logement': ['logement', 'habitat', 'construction', 'batiment',
                        'immobilier', 'menage', 'habitation'],
            'Justice': ['justice', 'droit', 'loi', 'equite', 'corruption',
                       'transparence', 'legal', 'tribunal', 'equitable', 'hogra'],
            'Social': ['social', 'pauvrete', 'solidarite', 'inegalite', 'dignite',
                      'vulnerable', 'citoyen', 'population', 'societe', 'menage',
                      'personne', 'age', 'revenu', 'pouvoir', 'achat'],
            'Environnement': ['environnement', 'eau', 'energie', 'hydrique', 'climat',
                            'ressource', 'durabilite', 'renouvelable', 'energetique',
                            'pollution', 'ecologique'],
            'Gouvernance': ['gouvernance', 'politique', 'institution', 'administration',
                          'etat', 'public', 'reforme', 'democratie', 'regionalisation',
                          'gouvernement', 'autorite'],
            'Agriculture': ['agriculture', 'rural', 'agriculteur', 'agricole', 
                          'culture', 'territorial', 'territoire', 'oasis', 'montagne'],
            'Tourisme': ['tourisme', 'touristique', 'hotel', 'visiteur'],
            'Droits_Femme': ['femme', 'famille', 'genre', 'egalite'],
            'Jeunesse': ['jeunesse', 'jeune', 'etudiant'],
            'Infrastructure': ['infrastructure', 'route', 'transport', 'autoroute',
                             'pont', 'equipement', 'connectivite']
        }
        
        # Sentiments pour Rule-Based
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
        """Analyse thematique MANUELLE"""
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
            
            top_themes = sorted(themes_count.items(), key=lambda x: x[1], reverse=True)[:3]
            print(f"[OK] {parti}:")
            for theme, count in top_themes:
                print(f"     - {theme}: {count} mentions")
        
        print()
    
    def analyser_sentiments_rulebased(self):
        """Sentiment Rule-Based (Baseline)"""
        print("="*80)
        print("SENTIMENT ANALYSIS 1 : Rule-Based (Baseline)")
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
    
    # ========================================================================
    # NOUVEAU : ENTRAINEMENT DE MODELE DE CLASSIFICATION
    # ========================================================================
    
    def creer_dataset_entrainement(self):
        """Cree un dataset d'entrainement pour le sentiment"""
        print("="*80)
        print("CREATION DU DATASET D'ENTRAINEMENT")
        print("="*80)
        print("Creation d'exemples etiquetes pour entrainer le modele...")
        print()
        
        # Dataset d'exemples (vous pouvez l'enrichir)
        exemples_positifs = [
            "nous allons ameliorer la situation economique",
            "renforcer le systeme de sante publique",
            "developper l emploi pour les jeunes",
            "garantir l acces a l education",
            "soutenir les entreprises et l innovation",
            "creer des opportunites pour tous",
            "augmenter les investissements",
            "promouvoir la justice sociale",
            "valoriser les competences",
            "moderniser les infrastructures",
            "reussir ensemble le developpement",
            "progres et prosperite pour tous",
            "meilleur avenir pour nos enfants",
            "confiance et performance",
            "accompagner les citoyens",
            "assurer la qualite de vie",
            "excellence dans les services",
            "elargir les droits",
            "favoriser l egalite",
            "encourager la participation"
        ]
        
        exemples_negatifs = [
            "probleme majeur dans le secteur",
            "crise economique grave",
            "difficultes importantes",
            "manque cruel de ressources",
            "systeme insuffisant et faible",
            "retard considerable",
            "echec des politiques",
            "penurie de logements",
            "carence dans les services",
            "deficit budgetaire",
            "deterioration de la situation",
            "baisse du pouvoir achat",
            "recul des droits",
            "stagnation economique",
            "inefficace et corrompu",
            "inegalites croissantes",
            "injustice sociale",
            "vulnerabilite des citoyens",
            "corruption generalisee",
            "hogra et mepris"
        ]
        
        exemples_neutres = [
            "la situation actuelle du pays",
            "le contexte economique national",
            "le niveau des indicateurs",
            "le taux de croissance",
            "le nombre de projets",
            "le secteur public",
            "le domaine de l education",
            "le programme gouvernemental",
            "les mesures prises",
            "l action publique",
            "la politique nationale",
            "les institutions du pays",
            "le cadre legislatif",
            "le systeme actuel",
            "les services administratifs",
            "la strategie nationale",
            "le plan de developpement",
            "les donnees statistiques",
            "l etat des lieux",
            "le bilan des actions"
        ]
        
        # Creer le dataset
        textes = exemples_positifs + exemples_negatifs + exemples_neutres
        labels = (
            ['positif'] * len(exemples_positifs) + 
            ['negatif'] * len(exemples_negatifs) + 
            ['neutre'] * len(exemples_neutres)
        )
        
        print(f"[INFO] Dataset cree:")
        print(f"       - {len(exemples_positifs)} exemples POSITIFS")
        print(f"       - {len(exemples_negatifs)} exemples NEGATIFS")
        print(f"       - {len(exemples_neutres)} exemples NEUTRES")
        print(f"       - Total: {len(textes)} exemples")
        print()
        
        return textes, labels
    
    def entrainer_modele_sentiment(self):
        """Entraine un modele de classification pour le sentiment"""
        print("="*80)
        print("SENTIMENT ANALYSIS 2 : ENTRAINEMENT DU MODELE (ML Supervise)")
        print("="*80)
        print("Type: Classification SUPERVISEE")
        print("Algorithmes testes: Naive Bayes, SVM, Random Forest")
        print()
        
        # 1. Creer le dataset
        X_textes, y_labels = self.creer_dataset_entrainement()
        
        # 2. Vectorisation TF-IDF
        print("[ETAPE 1] Vectorisation TF-IDF...")
        self.vectorizer = TfidfVectorizer(max_features=500, ngram_range=(1, 2))
        X_vectors = self.vectorizer.fit_transform(X_textes)
        print(f"[OK] Matrice: {X_vectors.shape[0]} exemples x {X_vectors.shape[1]} features")
        print()
        
        # 3. Split train/test
        X_train, X_test, y_train, y_test = train_test_split(
            X_vectors, y_labels, test_size=0.25, random_state=42, stratify=y_labels
        )
        
        print(f"[ETAPE 2] Split des donnees:")
        print(f"          Train: {X_train.shape[0]} exemples")
        print(f"          Test:  {X_test.shape[0]} exemples")
        print()
        
        # 4. Tester plusieurs modeles
        print("[ETAPE 3] Entrainement et evaluation de 3 modeles:")
        print()
        
        modeles = {
            'Naive Bayes': MultinomialNB(),
            'SVM': LinearSVC(random_state=42, max_iter=2000),
            'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42)
        }
        
        resultats = {}
        
        for nom, modele in modeles.items():
            # Entrainement
            modele.fit(X_train, y_train)
            
            # Prediction
            y_pred = modele.predict(X_test)
            
            # Evaluation
            accuracy = accuracy_score(y_test, y_pred)
            
            # Cross-validation
            cv_scores = cross_val_score(modele, X_vectors, y_labels, cv=5)
            cv_mean = cv_scores.mean()
            
            resultats[nom] = {
                'modele': modele,
                'accuracy': accuracy,
                'cv_mean': cv_mean,
                'y_pred': y_pred
            }
            
            print(f"  {nom}:")
            print(f"    - Accuracy (test): {accuracy:.3f}")
            print(f"    - CV Score (mean): {cv_mean:.3f}")
            print()
        
        # 5. Choisir le meilleur modele
        meilleur_nom = max(resultats.items(), key=lambda x: x[1]['cv_mean'])[0]
        self.modele_sentiment = resultats[meilleur_nom]['modele']
        
        print(f"[OK] Meilleur modele selectionne: {meilleur_nom}")
        print(f"     Accuracy: {resultats[meilleur_nom]['accuracy']:.3f}")
        print()
        
        # 6. Rapport de classification detaille
        print("[ETAPE 4] Rapport de classification (meilleur modele):")
        print()
        y_pred_best = resultats[meilleur_nom]['y_pred']
        print(classification_report(y_test, y_pred_best, target_names=['negatif', 'neutre', 'positif']))
        
        # 7. Sauvegarder le modele
        with open('modele_sentiment.pkl', 'wb') as f:
            pickle.dump(self.modele_sentiment, f)
        with open('vectorizer_sentiment.pkl', 'wb') as f:
            pickle.dump(self.vectorizer, f)
        
        print("[OK] Modele et vectorizer sauvegardes (modele_sentiment.pkl, vectorizer_sentiment.pkl)")
        print()
        
        return resultats
    
    def predire_sentiment_ml(self):
        """Predit le sentiment des 4 discours avec le modele entraine"""
        print("="*80)
        print("PREDICTION DU SENTIMENT AVEC LE MODELE ENTRAINE")
        print("="*80)
        
        for parti, texte in self.textes_nettoyes.items():
            # Decouper en segments
            segments = self.decouper_texte(texte, max_length=50)
            
            # Vectoriser
            X_segments = self.vectorizer.transform(segments)
            
            # Predire
            predictions = self.modele_sentiment.predict(X_segments)
            
            # Calculer distribution
            counter = Counter(predictions)
            total = len(predictions)
            
            # Score numerique
            score_positif = counter.get('positif', 0) / total
            score_negatif = counter.get('negatif', 0) / total
            score_neutre = counter.get('neutre', 0) / total
            
            # Score global (-1 a +1)
            score_global = score_positif - score_negatif
            
            # Label final
            if score_global > 0.2:
                label_final = "Positif"
            elif score_global < -0.2:
                label_final = "Negatif"
            else:
                label_final = "Neutre"
            
            self.sentiments_ml_entraine[parti] = {
                'score': score_global,
                'label': label_final,
                'distribution': dict(counter),
                'nb_segments': total,
                'score_positif': score_positif,
                'score_negatif': score_negatif,
                'score_neutre': score_neutre
            }
            
            print(f"[OK] {parti}: {label_final} (score ML: {score_global:+.3f})")
            print(f"     Distribution: Pos={score_positif:.2%}, Neg={score_negatif:.2%}, Neu={score_neutre:.2%}")
        
        print()
    
    def decouper_texte(self, texte, max_length=50):
        """Decoupe texte en segments"""
        mots = texte.split()
        segments = []
        for i in range(0, len(mots), max_length):
            segment = ' '.join(mots[i:i+max_length])
            if len(segment.split()) >= 5:  # Au moins 5 mots
                segments.append(segment)
        return segments if segments else [texte]
    
    # ========================================================================
    # VISUALISATIONS
    # ========================================================================
    
    def visualiser_themes(self):
        """Graphique themes"""
        print("="*80)
        print("GENERATION: Graphique Themes")
        print("="*80)
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 7))
        
        colors_partis = {'PAM': '#e74c3c', 'PI': '#3498db', 'PJD': '#2ecc71', 'RNI': '#f39c12'}
        
        # Top 5 themes
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
        ax1.set_title('Top 5 Themes par Parti', fontsize=15, fontweight='bold')
        ax1.legend(loc='lower right', fontsize=11)
        ax1.set_yticks([])
        ax1.grid(axis='x', alpha=0.3)
        
        # Heatmap
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
        
        ax2.set_title('Heatmap des 14 Themes', fontsize=15, fontweight='bold')
        
        for i in range(len(self.partis)):
            for j in range(len(themes_order)):
                value = data_heatmap[i, j]
                if value > 0:
                    ax2.text(j, i, int(value), ha='center', va='center', 
                            color='white' if value > data_heatmap.max()/2 else 'black',
                            fontsize=8, fontweight='bold')
        
        plt.colorbar(im, ax=ax2, label='Mentions')
        
        plt.tight_layout()
        plt.savefig('themes_analyse.png', dpi=300, bbox_inches='tight')
        print("[OK] Sauvegarde: themes_analyse.png")
        print()
    
    def visualiser_comparaison_sentiments(self):
        """Compare Rule-Based vs Modele Entraine"""
        print("="*80)
        print("GENERATION: Comparaison Rule-Based vs Modele Entraine")
        print("="*80)
        
        fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(20, 6))
        
        partis = self.partis
        
        # Graph 1: Rule-Based
        scores_rb = [self.sentiments_rulebased[p]['score'] for p in partis]
        colors_rb = ['#2ecc71' if s > 0.1 else '#e74c3c' if s < -0.1 else '#95a5a6' for s in scores_rb]
        
        ax1.barh(partis, scores_rb, color=colors_rb, alpha=0.8, edgecolor='black', linewidth=1.5)
        ax1.axvline(x=0, color='black', linestyle='--', linewidth=1.5)
        ax1.set_xlabel('Score', fontsize=12, fontweight='bold')
        ax1.set_title('Rule-Based (Lexicon)', fontsize=13, fontweight='bold')
        ax1.set_xlim(-1, 1)
        ax1.grid(axis='x', alpha=0.3)
        
        for i, (p, s) in enumerate(zip(partis, scores_rb)):
            ax1.text(s + 0.05 if s > 0 else s - 0.05, i, 
                    f'{s:+.3f}', va='center', fontsize=10, fontweight='bold')
        
        # Graph 2: Modele Entraine
        scores_ml = [self.sentiments_ml_entraine[p]['score'] for p in partis]
        colors_ml = ['#2ecc71' if s > 0.2 else '#e74c3c' if s < -0.2 else '#95a5a6' for s in scores_ml]
        
        ax2.barh(partis, scores_ml, color=colors_ml, alpha=0.8, edgecolor='black', linewidth=1.5)
        ax2.axvline(x=0, color='black', linestyle='--', linewidth=1.5)
        ax2.set_xlabel('Score', fontsize=12, fontweight='bold')
        ax2.set_title('Modele Entraine (ML Supervise)', fontsize=13, fontweight='bold')
        ax2.set_xlim(-1, 1)
        ax2.grid(axis='x', alpha=0.3)
        
        for i, (p, s) in enumerate(zip(partis, scores_ml)):
            ax2.text(s + 0.05 if s > 0 else s - 0.05, i, 
                    f'{s:+.3f}', va='center', fontsize=10, fontweight='bold')
        
        # Graph 3: Comparaison cote a cote
        x = np.arange(len(partis))
        width = 0.35
        
        ax3.bar(x - width/2, scores_rb, width, label='Rule-Based', 
               color='#3498db', alpha=0.8, edgecolor='black')
        ax3.bar(x + width/2, scores_ml, width, label='Modele Entraine', 
               color='#e74c3c', alpha=0.8, edgecolor='black')
        
        ax3.set_ylabel('Score Sentiment', fontsize=12, fontweight='bold')
        ax3.set_title('Comparaison des 2 Methodes', fontsize=13, fontweight='bold')
        ax3.set_xticks(x)
        ax3.set_xticklabels(partis, fontsize=11, fontweight='bold')
        ax3.legend(fontsize=11)
        ax3.axhline(y=0, color='black', linestyle='--', linewidth=1)
        ax3.grid(axis='y', alpha=0.3)
        ax3.set_ylim(-1, 1)
        
        plt.tight_layout()
        plt.savefig('comparaison_sentiments.png', dpi=300, bbox_inches='tight')
        print("[OK] Sauvegarde: comparaison_sentiments.png")
        print()
    
    def generer_rapport(self):
        """Rapport complet"""
        print("="*80)
        print("GENERATION: Rapport Final")
        print("="*80)
        
        rapport = []
        rapport.append("="*80)
        rapport.append("RAPPORT FINAL - ANALYSE TEXT MINING AVEC MODELE ENTRAINE")
        rapport.append("="*80)
        rapport.append("")
        rapport.append("METHODOLOGIE:")
        rapport.append("- Topics: 14 themes predefinis (approche manuelle)")
        rapport.append("- Sentiment:")
        rapport.append("  * Methode 1: Rule-Based (Lexicon) - Baseline")
        rapport.append("  * Methode 2: Modele ML Entraine (Classification Supervisee)")
        rapport.append(f"    Algorithme: {type(self.modele_sentiment).__name__}")
        rapport.append("    Dataset: 60 exemples etiquetes (20 pos, 20 neg, 20 neu)")
        rapport.append("")
        
        for parti in self.partis:
            rapport.append(f"\n{'='*80}")
            rapport.append(f"PARTI : {parti}")
            rapport.append(f"{'='*80}\n")
            
            # Themes
            themes = self.themes_par_parti[parti]
            top_themes = sorted(themes.items(), key=lambda x: x[1], reverse=True)[:5]
            rapport.append("Top 5 Themes:")
            for theme, count in top_themes:
                rapport.append(f"  - {theme}: {count} mentions")
            rapport.append("")
            
            # Sentiment Rule-Based
            sent_rb = self.sentiments_rulebased[parti]
            rapport.append(f"Sentiment Rule-Based:")
            rapport.append(f"  Label: {sent_rb['label']}")
            rapport.append(f"  Score: {sent_rb['score']:+.3f}")
            rapport.append("")
            
            # Sentiment ML
            sent_ml = self.sentiments_ml_entraine[parti]
            rapport.append(f"Sentiment Modele Entraine (ML):")
            rapport.append(f"  Label: {sent_ml['label']}")
            rapport.append(f"  Score: {sent_ml['score']:+.3f}")
            rapport.append(f"  Distribution: Pos={sent_ml['score_positif']:.1%}, Neg={sent_ml['score_negatif']:.1%}, Neu={sent_ml['score_neutre']:.1%}")
            rapport.append(f"  Segments analyses: {sent_ml['nb_segments']}")
            rapport.append("")
            
            # Comparaison
            diff = abs(sent_rb['score'] - sent_ml['score'])
            rapport.append(f"Difference entre methodes: {diff:.3f}")
            rapport.append("")
        
        rapport.append("\n" + "="*80)
        rapport.append("COMPARAISON GLOBALE DES METHODES")
        rapport.append("="*80)
        rapport.append("")
        rapport.append(f"{'Parti':<10} {'Rule-Based':<15} {'Modele ML':<15} {'Difference':<15}")
        rapport.append("-" * 80)
        
        for parti in self.partis:
            score_rb = self.sentiments_rulebased[parti]['score']
            score_ml = self.sentiments_ml_entraine[parti]['score']
            diff = abs(score_rb - score_ml)
            rapport.append(f"{parti:<10} {score_rb:+.3f}          {score_ml:+.3f}          {diff:.3f}")
        
        rapport.append("")
        rapport.append("="*80)
        rapport.append("FIN DU RAPPORT")
        rapport.append("="*80)
        
        with open('rapport_avec_modele_entraine.txt', 'w', encoding='utf-8') as f:
            f.write('\n'.join(rapport))
        
        print("[OK] Sauvegarde: rapport_avec_modele_entraine.txt")
        print()
    
    def generer_tableau_excel(self):
        """Tableau Excel"""
        print("="*80)
        print("GENERATION: Tableau Excel")
        print("="*80)
        
        data = []
        
        for parti in self.partis:
            row = {'Parti': parti}
            
            # Themes
            themes = self.themes_par_parti[parti]
            top_theme = sorted(themes.items(), key=lambda x: x[1], reverse=True)[0]
            row['Theme_Dominant'] = top_theme[0]
            row['Theme_Mentions'] = top_theme[1]
            
            # Sentiment RB
            sent_rb = self.sentiments_rulebased[parti]
            row['Sentiment_RB_Label'] = sent_rb['label']
            row['Sentiment_RB_Score'] = sent_rb['score']
            
            # Sentiment ML
            sent_ml = self.sentiments_ml_entraine[parti]
            row['Sentiment_ML_Label'] = sent_ml['label']
            row['Sentiment_ML_Score'] = sent_ml['score']
            
            # Difference
            row['Difference'] = abs(sent_rb['score'] - sent_ml['score'])
            
            data.append(row)
        
        df = pd.DataFrame(data)
        
        df.to_excel('synthese_avec_modele.xlsx', index=False)
        df.to_csv('synthese_avec_modele.csv', index=False, encoding='utf-8')
        
        print("[OK] Sauvegardes:")
        print("     - synthese_avec_modele.xlsx")
        print("     - synthese_avec_modele.csv")
        print()
        print("Apercu:")
        print(df.to_string())
        print()
    
    def executer_analyse_complete(self):
        """Execute analyse complete avec entrainement"""
        print("\n")
        print("="*80)
        print("ANALYSE TEXT MINING AVEC ENTRAINEMENT DE MODELE")
        print("="*80)
        print()
        
        self.charger_fichiers()
        self.pretraiter_textes()
        self.analyser_themes()
        
        # Sentiment : Rule-Based
        self.analyser_sentiments_rulebased()
        
        # Sentiment : Entrainement + Prediction ML
        self.entrainer_modele_sentiment()
        self.predire_sentiment_ml()
        
        # Visualisations
        self.visualiser_themes()
        self.visualiser_comparaison_sentiments()
        
        # Rapports
        self.generer_rapport()
        self.generer_tableau_excel()
        
        print("="*80)
        print("ANALYSE COMPLETE TERMINEE")
        print("="*80)
        print()
        print("FICHIERS GENERES:")
        print("  1. themes_analyse.png                      <- Themes manuels")
        print("  2. comparaison_sentiments.png              <- Rule-Based vs Modele")
        print("  3. rapport_avec_modele_entraine.txt        <- Rapport detaille")
        print("  4. synthese_avec_modele.xlsx/csv           <- Tableau Excel")
        print("  5. modele_sentiment.pkl                    <- Modele entraine")
        print("  6. vectorizer_sentiment.pkl                <- Vectorizer")
        print()


if __name__ == "__main__":
    print("\n" * 2)
    print("="*80)
    print("=    ANALYSE TEXT MINING AVEC ENTRAINEMENT DE MODELE ML         =")
    print("=         Discours Politiques Marocains                         =")
    print("="*80)
    print()
    
    analyse = AnalyseTextMiningAvecEntrainement(dossier=".")
    analyse.executer_analyse_complete()
    
    print("\n" * 2)
    print("="*80)
    print("PROJET TERMINE")
    print("Topics: Approche Manuelle | Sentiment: Rule-Based + Modele Entraine")
    print("="*80)

