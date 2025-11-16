"""
Projet d'Analyse de Text Mining AVEC MACHINE LEARNING
Discours des Partis Politiques Marocains

NOUVEAUTÉS :
1. Classification SUPERVISÉE : Transformers pour sentiment analysis
2. Classification NON-SUPERVISÉE : K-means clustering + LDA topic modeling
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

# ============================================================================
# IMPORTATIONS MACHINE LEARNING
# ============================================================================
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.cluster import KMeans
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.metrics import silhouette_score
from transformers import pipeline
import torch

print("="*80)
print("CHARGEMENT DES MODÈLES ET BIBLIOTHÈQUES")
print("="*80)

# Charger le modèle français de spaCy pour la lemmatisation
try:
    nlp = spacy.load("fr_core_news_sm")
    print("[OK] Modèle spaCy français chargé")
except OSError:
    print("[ERREUR] Modèle spaCy non trouvé. Installation nécessaire:")
    print("  python -m spacy download fr_core_news_sm")
    nlp = None

# Charger le modèle Transformers pour sentiment analysis (SUPERVISÉ)
try:
    print("\n[INFO] Chargement du modèle Transformers pour sentiment analysis...")
    sentiment_classifier = pipeline(
        "sentiment-analysis",
        model="nlptown/bert-base-multilingual-uncased-sentiment",
        device=0 if torch.cuda.is_available() else -1
    )
    print("[OK] Modèle Transformers chargé (Classification SUPERVISÉE)")
except Exception as e:
    print(f"[AVERTISSEMENT] Impossible de charger le modèle Transformers: {e}")
    print("  Installation recommandée: pip install transformers torch")
    sentiment_classifier = None

print("="*80)
print()

# Configuration de matplotlib
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['figure.figsize'] = (14, 8)
sns.set_style("whitegrid")

class AnalyseTextMiningML:
    """Classe principale pour l'analyse de text mining avec MACHINE LEARNING"""
    
    def __init__(self, dossier="."):
        self.dossier = dossier
        self.partis = ["PAM", "PI", "PJD", "RNI"]
        self.textes_bruts = {}
        self.textes_nettoyes = {}
        self.themes_par_parti = {}
        
        # Résultats de sentiment : Rule-Based + ML
        self.sentiments_par_parti_rulebased = {}  # Méthode lexicon classique
        self.sentiments_par_parti_ml = {}         # Méthode ML supervisée
        
        # Résultats clustering et topic modeling
        self.clusters_par_parti = {}
        self.topics_lda = {}
        
        # Définition des stopwords français
        self.stopwords_fr = set([
            'le', 'la', 'les', 'un', 'une', 'des', 'de', 'du', 'et', 'ou', 'mais',
            'donc', 'car', 'ni', 'ne', 'dans', 'par', 'pour', 'avec', 'sans',
            'sur', 'sous', 'entre', 'vers', 'chez', 'ce', 'ces', 'cet', 'cette',
            'mon', 'ton', 'son', 'notre', 'votre', 'leur', 'mes', 'tes', 'ses',
            'nos', 'vos', 'leurs', 'je', 'tu', 'il', 'elle', 'nous', 'vous', 'ils',
            'elles', 'on', 'qui', 'que', 'quoi', 'dont', 'où', 'est', 'sont', 'être',
            'avoir', 'faire', 'dire', 'aller', 'voir', 'pouvoir', 'vouloir', 'au',
            'aux', 'à', 'plus', 'moins', 'très', 'tout', 'tous', 'toute', 'toutes',
            'même', 'si', 'ainsi', 'aussi', 'encore', 'déjà', 'comme', 'après',
            'avant', 'pendant', 'depuis', 'alors', 'encore', 'enfin', 'puis',
            's', 'd', 'l', 'c', 'j', 'n', 'm', 't', 'qu', 'été', 'a', 'ont', 'était'
        ])
        
        # Dictionnaire de thèmes avec mots-clés (pour comparaison avec LDA)
        self.themes_keywords = {
            'Éducation': ['école', 'éducation', 'enseignement', 'élèves', 'formation', 
                         'université', 'professeur', 'enseignant', 'scolarité',
                         'scolaire', 'étudiants', 'apprentissage', 'préscolaire'],
            'Santé': ['santé', 'médical', 'hôpital', 'soins', 'médecin', 'amo', 
                     'assurance', 'maladie', 'hospitalier', 'ramedistes', 'ramed',
                     'professionnels', 'prestations'],
            'Emploi': ['emploi', 'travail', 'chômage', 'recrutement', 'jeunes',
                      'stage', 'entreprise', 'salaire', 'prime', 'postes', 'création'],
            'Économie': ['économie', 'croissance', 'investissement', 'développement',
                        'pib', 'industriel', 'secteur', 'ressources', 'financier',
                        'industrie', 'production', 'tissu', 'richesse', 'exportation'],
            'Logement': ['logement', 'habitat', 'construction', 'bâtiments',
                        'immobilier', 'ménages', 'habitations', 'ruine'],
            'Justice': ['justice', 'droit', 'loi', 'équité', 'corruption',
                       'transparence', 'légal', 'tribunal', 'équitable', 'hogra',
                       'législatif', 'réglementation'],
            'Social': ['social', 'pauvreté', 'solidarité', 'inégalités', 'dignité',
                      'vulnérables', 'citoyens', 'population', 'société', 'ménages',
                      'personnes', 'âgées', 'revenu', 'pouvoir', 'achat'],
            'Environnement': ['environnement', 'eau', 'énergie', 'hydrique', 'climat',
                            'ressources', 'durabilité', 'renouvelables', 'énergétique',
                            'hydrocarbures', 'pollution', 'écologique'],
            'Gouvernance': ['gouvernance', 'politique', 'institutions', 'administration',
                          'état', 'public', 'réforme', 'démocratie', 'régionalisation',
                          'gouvernement', 'autorité', 'concurrence', 'régulation'],
            'Agriculture': ['agriculture', 'rural', 'agriculteurs', 'agricoles', 
                          'cultures', 'territorial', 'territoires', 'oasis', 'montagne'],
            'Tourisme': ['tourisme', 'touristiques', 'hôtel', 'visiteurs'],
            'Droits_Femme': ['femme', 'femmes', 'famille', 'genre', 'égalité'],
            'Jeunesse': ['jeunesse', 'jeunes', 'jeunesses', 'étudiants'],
            'Infrastructure': ['infrastructure', 'routes', 'transport', 'autoroutes',
                             'ponts', 'équipements', 'connectivité']
        }
        
        # Mots-clés pour l'analyse de sentiment RULE-BASED
        self.sentiment_positif = [
            'améliorer', 'renforcer', 'développer', 'garantir', 'soutenir',
            'créer', 'augmenter', 'élargir', 'encourager', 'promouvoir',
            'favoriser', 'valoriser', 'moderniser', 'réussir', 'succès', 'progrès',
            'avancées', 'meilleur', 'optimiser', 'accompagner', 'confiance', 'restaurer',
            'assurer', 'prospérité', 'qualité', 'efficace', 'performance', 'excellence'
        ]
        
        self.sentiment_negatif = [
            'problème', 'crise', 'difficultés', 'manque', 'insuffisant',
            'faible', 'retard', 'échec', 'pénurie', 'carence', 'déficit',
            'détérioration', 'baisse', 'recul', 'stagnation', 'inefficace',
            'corruption', 'inégalité', 'injustice', 'hogra', 'vulnérabilité'
        ]
        
        self.sentiment_neutre = [
            'situation', 'contexte', 'niveau', 'taux', 'nombre', 'secteur',
            'domaine', 'projet', 'programme', 'mesure', 'action', 'politique'
        ]
    
    def charger_fichiers(self):
        """Charge tous les fichiers texte des partis"""
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
                    print(f"[OK] {parti}: {nb_mots} mots chargés")
            except FileNotFoundError:
                print(f"[ERREUR] Fichier {fichier} introuvable")
                self.textes_bruts[parti] = ""
        
        print()
    
    def pretraiter_textes(self):
        """Prétraitement avec lemmatisation avancée"""
        print("="*80)
        print("PRÉTRAITEMENT AVEC LEMMATISATION (spaCy)")
        print("="*80)
        
        for parti, texte in self.textes_bruts.items():
            # Nettoyage basique
            texte_propre = texte.lower()
            texte_propre = re.sub(r'[^\w\s]', ' ', texte_propre)
            texte_propre = re.sub(r'\d+', '', texte_propre)
            texte_propre = re.sub(r'\s+', ' ', texte_propre).strip()
            
            # Lemmatisation avec spaCy
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
                print(f"[OK] {parti}: {len(texte_propre.split())} mots → {len(lemmes)} lemmes ({reduction:.1f}% réduction)")
            else:
                # Fallback sans lemmatisation
                mots = [mot for mot in texte_propre.split() 
                       if mot not in self.stopwords_fr and len(mot) > 2]
                texte_final = ' '.join(mots)
                print(f"[OK] {parti}: {len(texte_propre.split())} mots → {len(mots)} mots filtrés")
            
            self.textes_nettoyes[parti] = texte_final
        
        print()
    
    # ========================================================================
    # MÉTHODE 1 : SENTIMENT ANALYSIS RULE-BASED (Baseline)
    # ========================================================================
    
    def analyser_sentiments_rulebased(self):
        """Analyse de sentiment classique avec dictionnaire (baseline)"""
        print("="*80)
        print("MÉTHODE 1 : SENTIMENT ANALYSIS RULE-BASED (Baseline)")
        print("="*80)
        print("Type : Classification basée sur dictionnaire")
        print("Algorithme : Lexicon-Based Sentiment Analysis")
        print()
        
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
                label = "Négatif"
            else:
                label = "Neutre"
            
            self.sentiments_par_parti_rulebased[parti] = {
                'positifs': nb_positif,
                'negatifs': nb_negatif,
                'neutres': nb_neutre,
                'score': score,
                'label': label
            }
            
            print(f"[OK] {parti}: {label} (score: {score:+.3f})")
            print(f"     Positifs: {nb_positif}, Négatifs: {nb_negatif}, Neutres: {nb_neutre}")
        
        print()
    
    # ========================================================================
    # MÉTHODE 2 : SENTIMENT ANALYSIS ML SUPERVISÉ (Transformers)
    # ========================================================================
    
    def analyser_sentiments_ml_supervise(self):
        """
        Analyse de sentiment avec modèle pré-entraîné (Classification SUPERVISÉE)
        Modèle : BERT multilingual fine-tuné sur des données de sentiment
        """
        print("="*80)
        print("MÉTHODE 2 : SENTIMENT ANALYSIS ML SUPERVISÉ (Transformers)")
        print("="*80)
        print("Type : Classification SUPERVISÉE")
        print("Modèle : BERT multilingual (nlptown/bert-base-multilingual-uncased-sentiment)")
        print("Approche : Transfer Learning (modèle pré-entraîné)")
        print()
        
        if not sentiment_classifier:
            print("[ERREUR] Modèle Transformers non disponible")
            print("         Les résultats ML supervisés ne seront pas générés")
            print()
            return
        
        for parti, texte in self.textes_bruts.items():
            # Découper le texte en segments (max 512 tokens pour BERT)
            segments = self.decouper_texte(texte, max_length=500)
            
            sentiments_segments = []
            scores_numeriques = []
            
            print(f"[INFO] Analyse de {parti} : {len(segments)} segments...")
            
            for i, segment in enumerate(segments):
                try:
                    result = sentiment_classifier(segment)[0]
                    label = result['label']  # "1 star" à "5 stars"
                    score = result['score']
                    
                    # Convertir en échelle numérique (-1 à +1)
                    if '1 star' in label:
                        score_num = -1.0
                        sentiment = 'Très Négatif'
                    elif '2 stars' in label:
                        score_num = -0.5
                        sentiment = 'Négatif'
                    elif '3 stars' in label:
                        score_num = 0.0
                        sentiment = 'Neutre'
                    elif '4 stars' in label:
                        score_num = 0.5
                        sentiment = 'Positif'
                    elif '5 stars' in label:
                        score_num = 1.0
                        sentiment = 'Très Positif'
                    else:
                        score_num = 0.0
                        sentiment = 'Neutre'
                    
                    sentiments_segments.append(sentiment)
                    scores_numeriques.append(score_num)
                    
                except Exception as e:
                    print(f"     [AVERTISSEMENT] Segment {i+1}: {str(e)[:50]}")
                    scores_numeriques.append(0.0)
            
            # Calculer le score moyen
            if scores_numeriques:
                score_moyen = np.mean(scores_numeriques)
                
                if score_moyen > 0.3:
                    label_final = "Positif"
                elif score_moyen < -0.3:
                    label_final = "Négatif"
                else:
                    label_final = "Neutre"
                
                # Distribution des sentiments
                counter = Counter(sentiments_segments)
                
                self.sentiments_par_parti_ml[parti] = {
                    'score': score_moyen,
                    'label': label_final,
                    'distribution': dict(counter),
                    'nb_segments': len(segments)
                }
                
                print(f"[OK] {parti}: {label_final} (score ML: {score_moyen:+.3f})")
                print(f"     Distribution: {dict(counter)}")
            else:
                print(f"[ERREUR] {parti}: Aucun résultat ML")
        
        print()
    
    def decouper_texte(self, texte, max_length=500):
        """Découpe le texte en segments de longueur maximale"""
        mots = texte.split()
        segments = []
        
        for i in range(0, len(mots), max_length):
            segment = ' '.join(mots[i:i+max_length])
            segments.append(segment)
        
        return segments
    
    # ========================================================================
    # MÉTHODE 3 : CLUSTERING NON-SUPERVISÉ (K-means)
    # ========================================================================
    
    def clustering_kmeans(self, n_clusters=5):
        """
        Clustering des segments de texte (Classification NON-SUPERVISÉE)
        Algorithme : K-means avec TF-IDF
        """
        print("="*80)
        print("MÉTHODE 3 : CLUSTERING NON-SUPERVISÉ (K-means)")
        print("="*80)
        print("Type : Classification NON-SUPERVISÉE")
        print("Algorithme : K-means clustering")
        print("Représentation : TF-IDF (Term Frequency-Inverse Document Frequency)")
        print(f"Nombre de clusters : {n_clusters}")
        print()
        
        # Préparer les données : découper chaque texte en segments
        segments_tous = []
        parti_segments_map = []
        
        for parti, texte in self.textes_nettoyes.items():
            segments = self.decouper_texte(texte, max_length=100)
            for segment in segments:
                segments_tous.append(segment)
                parti_segments_map.append(parti)
        
        print(f"[INFO] Total segments à clustériser : {len(segments_tous)}")
        
        # Vectorisation TF-IDF
        vectorizer = TfidfVectorizer(max_features=500, min_df=2, max_df=0.8)
        X = vectorizer.fit_transform(segments_tous)
        
        print(f"[INFO] Matrice TF-IDF : {X.shape[0]} segments × {X.shape[1]} features")
        
        # K-means clustering
        kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        clusters = kmeans.fit_predict(X)
        
        # Calculer le silhouette score (qualité du clustering)
        if len(set(clusters)) > 1:
            silhouette = silhouette_score(X, clusters)
            print(f"[INFO] Silhouette Score : {silhouette:.3f} (qualité du clustering)")
        else:
            silhouette = 0
        
        # Analyser les clusters par parti
        for parti in self.partis:
            indices_parti = [i for i, p in enumerate(parti_segments_map) if p == parti]
            clusters_parti = [clusters[i] for i in indices_parti]
            
            if clusters_parti:
                counter = Counter(clusters_parti)
                cluster_dominant = counter.most_common(1)[0][0]
                
                self.clusters_par_parti[parti] = {
                    'distribution': dict(counter),
                    'cluster_dominant': cluster_dominant,
                    'nb_segments': len(clusters_parti),
                    'silhouette_score': silhouette
                }
                
                print(f"[OK] {parti}: Cluster dominant = {cluster_dominant}")
                print(f"     Distribution: {dict(counter)}")
        
        # Analyser les termes caractéristiques de chaque cluster
        print("\n[INFO] Termes caractéristiques par cluster :")
        feature_names = vectorizer.get_feature_names_out()
        
        for i in range(n_clusters):
            center = kmeans.cluster_centers_[i]
            top_indices = center.argsort()[-10:][::-1]
            top_terms = [feature_names[idx] for idx in top_indices]
            print(f"  Cluster {i}: {', '.join(top_terms[:5])}...")
        
        print()
        
        return kmeans, vectorizer
    
    # ========================================================================
    # MÉTHODE 4 : TOPIC MODELING NON-SUPERVISÉ (LDA)
    # ========================================================================
    
    def topic_modeling_lda(self, n_topics=10):
        """
        Topic Modeling automatique (Classification NON-SUPERVISÉE)
        Algorithme : Latent Dirichlet Allocation (LDA)
        """
        print("="*80)
        print("MÉTHODE 4 : TOPIC MODELING NON-SUPERVISÉ (LDA)")
        print("="*80)
        print("Type : Classification NON-SUPERVISÉE")
        print("Algorithme : Latent Dirichlet Allocation (LDA)")
        print("Objectif : Découvrir automatiquement les thèmes cachés dans les textes")
        print(f"Nombre de topics : {n_topics}")
        print()
        
        # Préparer les données
        textes_list = [self.textes_nettoyes[parti] for parti in self.partis]
        
        # Vectorisation Count (LDA nécessite des comptages, pas TF-IDF)
        vectorizer = CountVectorizer(max_features=500, min_df=1, max_df=0.8)
        X = vectorizer.fit_transform(textes_list)
        
        print(f"[INFO] Matrice de comptage : {X.shape[0]} documents × {X.shape[1]} features")
        
        # LDA
        lda = LatentDirichletAllocation(
            n_components=n_topics,
            random_state=42,
            max_iter=20,
            learning_method='online'
        )
        
        doc_topics = lda.fit_transform(X)
        
        print(f"[INFO] Log-vraisemblance : {lda.score(X):.2f}")
        print(f"[INFO] Perplexité : {lda.perplexity(X):.2f}")
        
        # Afficher les topics découverts
        feature_names = vectorizer.get_feature_names_out()
        
        print("\n[INFO] Topics découverts par LDA :")
        for topic_idx, topic in enumerate(lda.components_):
            top_indices = topic.argsort()[-10:][::-1]
            top_words = [feature_names[i] for i in top_indices]
            print(f"  Topic {topic_idx}: {', '.join(top_words[:7])}...")
        
        print()
        
        # Analyser la distribution des topics par parti
        for i, parti in enumerate(self.partis):
            topic_distribution = doc_topics[i]
            top_topics = topic_distribution.argsort()[-3:][::-1]
            
            self.topics_lda[parti] = {
                'distribution': topic_distribution,
                'top_topics': top_topics.tolist(),
                'top_weights': [topic_distribution[t] for t in top_topics]
            }
            
            print(f"[OK] {parti}: Topics dominants = {top_topics.tolist()}")
            print(f"     Poids: [{', '.join([f'{w:.3f}' for w in topic_distribution[top_topics]])}]")
        
        print()
        
        return lda, vectorizer, doc_topics
    
    # ========================================================================
    # VISUALISATIONS COMPARATIVES
    # ========================================================================
    
    def visualiser_comparaison_sentiments(self):
        """Compare les résultats Rule-Based vs ML Supervisé"""
        print("="*80)
        print("GÉNÉRATION : Comparaison Sentiments Rule-Based vs ML")
        print("="*80)
        
        if not self.sentiments_par_parti_ml:
            print("[INFO] Pas de résultats ML disponibles, graphique non généré")
            print()
            return
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
        
        # Graphique 1 : Rule-Based
        partis = list(self.sentiments_par_parti_rulebased.keys())
        scores_rb = [self.sentiments_par_parti_rulebased[p]['score'] for p in partis]
        colors_rb = ['green' if s > 0.1 else 'red' if s < -0.1 else 'gray' for s in scores_rb]
        
        ax1.barh(partis, scores_rb, color=colors_rb, alpha=0.7)
        ax1.axvline(x=0, color='black', linestyle='--', linewidth=1)
        ax1.set_xlabel('Score de Sentiment', fontsize=12)
        ax1.set_title('Méthode 1 : Rule-Based (Lexicon)', fontsize=14, fontweight='bold')
        ax1.set_xlim(-1, 1)
        
        for i, (parti, score) in enumerate(zip(partis, scores_rb)):
            ax1.text(score + 0.05 if score > 0 else score - 0.05, i, 
                    f'{score:+.3f}', va='center', fontsize=10)
        
        # Graphique 2 : ML Supervisé
        scores_ml = [self.sentiments_par_parti_ml[p]['score'] for p in partis]
        colors_ml = ['green' if s > 0.3 else 'red' if s < -0.3 else 'gray' for s in scores_ml]
        
        ax2.barh(partis, scores_ml, color=colors_ml, alpha=0.7)
        ax2.axvline(x=0, color='black', linestyle='--', linewidth=1)
        ax2.set_xlabel('Score de Sentiment', fontsize=12)
        ax2.set_title('Méthode 2 : ML Supervisé (BERT)', fontsize=14, fontweight='bold')
        ax2.set_xlim(-1, 1)
        
        for i, (parti, score) in enumerate(zip(partis, scores_ml)):
            ax2.text(score + 0.05 if score > 0 else score - 0.05, i, 
                    f'{score:+.3f}', va='center', fontsize=10)
        
        plt.tight_layout()
        plt.savefig('comparaison_sentiments_RB_vs_ML.png', dpi=300, bbox_inches='tight')
        print("[OK] Graphique sauvegardé : comparaison_sentiments_RB_vs_ML.png")
        print()
    
    def visualiser_clustering(self):
        """Visualise les résultats du clustering"""
        print("="*80)
        print("GÉNÉRATION : Visualisation Clustering K-means")
        print("="*80)
        
        if not self.clusters_par_parti:
            print("[INFO] Pas de résultats de clustering disponibles")
            print()
            return
        
        fig, ax = plt.subplots(figsize=(12, 6))
        
        partis = list(self.clusters_par_parti.keys())
        distributions = [self.clusters_par_parti[p]['distribution'] for p in partis]
        
        # Trouver tous les clusters présents
        all_clusters = set()
        for dist in distributions:
            all_clusters.update(dist.keys())
        all_clusters = sorted(list(all_clusters))
        
        # Préparer les données pour le graphique empilé
        data_stacked = []
        for dist in distributions:
            data_stacked.append([dist.get(c, 0) for c in all_clusters])
        
        data_stacked = np.array(data_stacked).T
        
        # Graphique empilé
        x = np.arange(len(partis))
        colors = plt.cm.Set3(np.linspace(0, 1, len(all_clusters)))
        
        bottom = np.zeros(len(partis))
        for i, cluster in enumerate(all_clusters):
            ax.bar(x, data_stacked[i], bottom=bottom, label=f'Cluster {cluster}',
                   color=colors[i], alpha=0.8)
            bottom += data_stacked[i]
        
        ax.set_xticks(x)
        ax.set_xticklabels(partis, fontsize=12)
        ax.set_ylabel('Nombre de segments', fontsize=12)
        ax.set_title('Classification NON-SUPERVISÉE : Distribution des Clusters par Parti',
                    fontsize=14, fontweight='bold')
        ax.legend(title='Clusters', bbox_to_anchor=(1.05, 1), loc='upper left')
        
        plt.tight_layout()
        plt.savefig('clustering_kmeans.png', dpi=300, bbox_inches='tight')
        print("[OK] Graphique sauvegardé : clustering_kmeans.png")
        print()
    
    def visualiser_topics_lda(self):
        """Visualise les topics LDA par parti"""
        print("="*80)
        print("GÉNÉRATION : Visualisation Topics LDA")
        print("="*80)
        
        if not self.topics_lda:
            print("[INFO] Pas de résultats LDA disponibles")
            print()
            return
        
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        axes = axes.flatten()
        
        for idx, parti in enumerate(self.partis):
            ax = axes[idx]
            
            distribution = self.topics_lda[parti]['distribution']
            topics = np.arange(len(distribution))
            
            colors = ['#1f77b4' if w > 0.1 else '#cccccc' for w in distribution]
            
            ax.bar(topics, distribution, color=colors, alpha=0.7)
            ax.set_xlabel('Topic ID', fontsize=11)
            ax.set_ylabel('Poids', fontsize=11)
            ax.set_title(f'{parti} - Distribution des Topics LDA',
                        fontsize=13, fontweight='bold')
            ax.set_ylim(0, max(distribution) * 1.2)
            
            # Annoter les top topics
            top_topics = self.topics_lda[parti]['top_topics']
            for t in top_topics[:2]:
                ax.text(t, distribution[t] + 0.01, f'{distribution[t]:.3f}',
                       ha='center', fontsize=9, fontweight='bold')
        
        plt.tight_layout()
        plt.savefig('topics_lda.png', dpi=300, bbox_inches='tight')
        print("[OK] Graphique sauvegardé : topics_lda.png")
        print()
    
    # ========================================================================
    # RAPPORTS ET SYNTHÈSES
    # ========================================================================
    
    def generer_rapport_ml(self):
        """Génère un rapport détaillé avec toutes les méthodes ML"""
        print("="*80)
        print("GÉNÉRATION : Rapport Complet avec Machine Learning")
        print("="*80)
        
        rapport = []
        rapport.append("="*80)
        rapport.append("RAPPORT D'ANALYSE TEXT MINING AVEC MACHINE LEARNING")
        rapport.append("Discours des Partis Politiques Marocains")
        rapport.append("="*80)
        rapport.append("")
        
        rapport.append("MÉTHODOLOGIE :")
        rapport.append("-" * 80)
        rapport.append("1. Prétraitement : Nettoyage + Lemmatisation (spaCy)")
        rapport.append("2. Sentiment Analysis Rule-Based : Lexicon-Based (Baseline)")
        rapport.append("3. Sentiment Analysis ML Supervisé : BERT multilingual")
        rapport.append("4. Clustering Non-Supervisé : K-means avec TF-IDF")
        rapport.append("5. Topic Modeling Non-Supervisé : Latent Dirichlet Allocation (LDA)")
        rapport.append("")
        
        rapport.append("="*80)
        rapport.append("RÉSULTATS PAR PARTI")
        rapport.append("="*80)
        rapport.append("")
        
        for parti in self.partis:
            rapport.append(f"\n{'='*80}")
            rapport.append(f"PARTI : {parti}")
            rapport.append(f"{'='*80}\n")
            
            # 1. Données de base
            texte_brut = self.textes_bruts.get(parti, "")
            texte_propre = self.textes_nettoyes.get(parti, "")
            nb_mots_brut = len(texte_brut.split())
            nb_mots_propre = len(texte_propre.split())
            
            rapport.append(f"Volume de texte :")
            rapport.append(f"  - Texte brut : {nb_mots_brut} mots")
            rapport.append(f"  - Après lemmatisation : {nb_mots_propre} lemmes")
            rapport.append(f"  - Réduction : {((nb_mots_brut - nb_mots_propre) / nb_mots_brut * 100):.1f}%")
            rapport.append("")
            
            # 2. Sentiment Rule-Based
            if parti in self.sentiments_par_parti_rulebased:
                sent_rb = self.sentiments_par_parti_rulebased[parti]
                rapport.append(f"1. SENTIMENT ANALYSIS RULE-BASED (Baseline) :")
                rapport.append(f"   Label : {sent_rb['label']}")
                rapport.append(f"   Score : {sent_rb['score']:+.3f}")
                rapport.append(f"   Détail : {sent_rb['positifs']} positifs, "
                             f"{sent_rb['negatifs']} négatifs, {sent_rb['neutres']} neutres")
                rapport.append("")
            
            # 3. Sentiment ML Supervisé
            if parti in self.sentiments_par_parti_ml:
                sent_ml = self.sentiments_par_parti_ml[parti]
                rapport.append(f"2. SENTIMENT ANALYSIS ML SUPERVISÉ (BERT) :")
                rapport.append(f"   Label : {sent_ml['label']}")
                rapport.append(f"   Score ML : {sent_ml['score']:+.3f}")
                rapport.append(f"   Segments analysés : {sent_ml['nb_segments']}")
                rapport.append(f"   Distribution : {sent_ml['distribution']}")
                rapport.append("")
            
            # 4. Clustering
            if parti in self.clusters_par_parti:
                clust = self.clusters_par_parti[parti]
                rapport.append(f"3. CLUSTERING NON-SUPERVISÉ (K-means) :")
                rapport.append(f"   Cluster dominant : {clust['cluster_dominant']}")
                rapport.append(f"   Distribution : {clust['distribution']}")
                rapport.append(f"   Silhouette Score : {clust['silhouette_score']:.3f}")
                rapport.append("")
            
            # 5. Topic Modeling
            if parti in self.topics_lda:
                topics = self.topics_lda[parti]
                rapport.append(f"4. TOPIC MODELING NON-SUPERVISÉ (LDA) :")
                rapport.append(f"   Topics dominants : {topics['top_topics']}")
                rapport.append(f"   Poids : {[f'{w:.3f}' for w in topics['top_weights']]}")
                rapport.append("")
        
        # Comparaison finale
        rapport.append("\n" + "="*80)
        rapport.append("COMPARAISON SENTIMENT : RULE-BASED vs ML SUPERVISÉ")
        rapport.append("="*80)
        rapport.append("")
        rapport.append(f"{'Parti':<10} {'Rule-Based':<15} {'ML Supervisé':<15} {'Différence':<15}")
        rapport.append("-" * 80)
        
        for parti in self.partis:
            if parti in self.sentiments_par_parti_rulebased and parti in self.sentiments_par_parti_ml:
                score_rb = self.sentiments_par_parti_rulebased[parti]['score']
                score_ml = self.sentiments_par_parti_ml[parti]['score']
                diff = abs(score_rb - score_ml)
                
                rapport.append(f"{parti:<10} {score_rb:+.3f}          {score_ml:+.3f}          {diff:.3f}")
        
        rapport.append("")
        rapport.append("="*80)
        rapport.append("FIN DU RAPPORT")
        rapport.append("="*80)
        
        # Sauvegarder le rapport
        with open('rapport_analyse_ML.txt', 'w', encoding='utf-8') as f:
            f.write('\n'.join(rapport))
        
        print("[OK] Rapport sauvegardé : rapport_analyse_ML.txt")
        print()
    
    def generer_tableau_comparatif_ml(self):
        """Génère un tableau Excel comparant toutes les méthodes"""
        print("="*80)
        print("GÉNÉRATION : Tableau Comparatif Excel (Toutes méthodes)")
        print("="*80)
        
        data = []
        
        for parti in self.partis:
            row = {'Parti': parti}
            
            # Données de base
            row['Mots_bruts'] = len(self.textes_bruts.get(parti, "").split())
            row['Lemmes'] = len(self.textes_nettoyes.get(parti, "").split())
            row['Reduction_%'] = ((row['Mots_bruts'] - row['Lemmes']) / row['Mots_bruts'] * 100) if row['Mots_bruts'] > 0 else 0
            
            # Sentiment Rule-Based
            if parti in self.sentiments_par_parti_rulebased:
                sent_rb = self.sentiments_par_parti_rulebased[parti]
                row['Sentiment_RB_Label'] = sent_rb['label']
                row['Sentiment_RB_Score'] = sent_rb['score']
            
            # Sentiment ML
            if parti in self.sentiments_par_parti_ml:
                sent_ml = self.sentiments_par_parti_ml[parti]
                row['Sentiment_ML_Label'] = sent_ml['label']
                row['Sentiment_ML_Score'] = sent_ml['score']
                row['Sentiment_Difference'] = abs(sent_rb['score'] - sent_ml['score']) if parti in self.sentiments_par_parti_rulebased else None
            
            # Clustering
            if parti in self.clusters_par_parti:
                clust = self.clusters_par_parti[parti]
                row['Cluster_Dominant'] = clust['cluster_dominant']
                row['Silhouette_Score'] = clust['silhouette_score']
            
            # LDA
            if parti in self.topics_lda:
                topics = self.topics_lda[parti]
                row['Topic_1'] = topics['top_topics'][0]
                row['Topic_2'] = topics['top_topics'][1]
                row['Topic_3'] = topics['top_topics'][2] if len(topics['top_topics']) > 2 else None
            
            data.append(row)
        
        df = pd.DataFrame(data)
        
        # Sauvegarder
        df.to_excel('synthese_ml_complete.xlsx', index=False)
        df.to_csv('synthese_ml_complete.csv', index=False, encoding='utf-8')
        
        print("[OK] Tableaux sauvegardés :")
        print("     - synthese_ml_complete.xlsx")
        print("     - synthese_ml_complete.csv")
        print()
        print("Aperçu :")
        print(df.to_string())
        print()
    
    # ========================================================================
    # EXÉCUTION COMPLÈTE
    # ========================================================================
    
    def executer_analyse_complete_ml(self):
        """Exécute l'analyse complète avec toutes les méthodes ML"""
        print("\n")
        print("="*80)
        print("DÉMARRAGE DE L'ANALYSE TEXT MINING AVEC MACHINE LEARNING")
        print("="*80)
        print()
        
        # Étape 1 : Chargement
        self.charger_fichiers()
        
        # Étape 2 : Prétraitement
        self.pretraiter_textes()
        
        # Étape 3 : Sentiment Rule-Based (Baseline)
        self.analyser_sentiments_rulebased()
        
        # Étape 4 : Sentiment ML Supervisé
        self.analyser_sentiments_ml_supervise()
        
        # Étape 5 : Clustering Non-Supervisé
        self.clustering_kmeans(n_clusters=5)
        
        # Étape 6 : Topic Modeling Non-Supervisé
        self.topic_modeling_lda(n_topics=10)
        
        # Étape 7 : Visualisations
        self.visualiser_comparaison_sentiments()
        self.visualiser_clustering()
        self.visualiser_topics_lda()
        
        # Étape 8 : Rapports
        self.generer_rapport_ml()
        self.generer_tableau_comparatif_ml()
        
        print("="*80)
        print("ANALYSE COMPLÈTE TERMINÉE AVEC SUCCÈS")
        print("="*80)
        print()
        print("FICHIERS GÉNÉRÉS :")
        print("  - comparaison_sentiments_RB_vs_ML.png")
        print("  - clustering_kmeans.png")
        print("  - topics_lda.png")
        print("  - rapport_analyse_ML.txt")
        print("  - synthese_ml_complete.xlsx / .csv")
        print()
        print("MÉTHODES UTILISÉES :")
        print("  1. Rule-Based Sentiment Analysis (Baseline)")
        print("  2. ML Supervisé : BERT multilingual (Transfer Learning)")
        print("  3. ML Non-Supervisé : K-means clustering (TF-IDF)")
        print("  4. ML Non-Supervisé : LDA Topic Modeling")
        print()


# ============================================================================
# POINT D'ENTRÉE PRINCIPAL
# ============================================================================

if __name__ == "__main__":
    print("\n" * 2)
    print("╔" + "="*78 + "╗")
    print("║" + " "*20 + "ANALYSE TEXT MINING AVEC ML" + " "*31 + "║")
    print("║" + " "*15 + "Discours Politiques Marocains" + " "*34 + "║")
    print("╚" + "="*78 + "╝")
    print()
    
    # Créer l'instance et exécuter
    analyse = AnalyseTextMiningML(dossier=".")
    analyse.executer_analyse_complete_ml()
    
    print("\n" * 2)
    print("="*80)
    print("PROJET TERMINÉ - Niveau : AVANCÉ avec Machine Learning")
    print("="*80)

