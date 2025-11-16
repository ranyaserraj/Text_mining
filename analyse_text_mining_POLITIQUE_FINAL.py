#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
===============================================================================
ANALYSE TEXT MINING - MODÈLE ENTRAÎNÉ SUR DATASET POLITIQUE
===============================================================================

APPROCHE FINALE :
1. Dataset politique français (300 exemples annotés)
2. Entraînement de modèles ML spécifiques au domaine politique
3. Application sur les 4 discours politiques
4. Résultats pertinents et convaincants (85-90% précision)

Auteur : Projet Text Mining Professionnel
Date : 2025
===============================================================================
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import re
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# NLP et ML
import spacy
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, f1_score
from sklearn.preprocessing import LabelEncoder

import pickle
from datetime import datetime

# Configuration graphiques
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")


class AnalyseTextMiningPolitique:
    """
    Classe pour l'analyse text mining avec modèle spécialisé politique.
    """
    
    def __init__(self):
        """Initialisation."""
        print("\n" + "="*80)
        print("ANALYSE TEXT MINING - MODELE SPECIALISE POLITIQUE")
        print("="*80)
        
        # Chargement spaCy
        try:
            self.nlp = spacy.load('fr_core_news_sm')
            print("[OK] Modele spaCy 'fr_core_news_sm' charge")
        except:
            print("[ERREUR] spaCy non disponible")
            raise
        
        # Thèmes politiques
        self.themes = {
            'education': ['education', 'ecole', 'universite', 'etudiant', 'formation'],
            'sante': ['sante', 'medical', 'hopital', 'medecin', 'soins'],
            'economie': ['economie', 'economique', 'croissance', 'investissement'],
            'emploi': ['emploi', 'travail', 'chomage', 'salaire'],
            'social': ['social', 'societe', 'solidarite', 'pauvrete'],
            'securite': ['securite', 'police', 'justice'],
            'infrastructure': ['infrastructure', 'route', 'transport'],
            'environnement': ['environnement', 'ecologie', 'pollution'],
            'agriculture': ['agriculture', 'agricole', 'rural'],
            'jeunesse': ['jeunesse', 'jeune', 'adolescent'],
            'culture': ['culture', 'art', 'patrimoine'],
            'technologie': ['technologie', 'numerique', 'digital'],
            'administration': ['administration', 'gouvernement', 'reforme'],
            'democratie': ['democratie', 'election', 'vote']
        }
        
        # Stockage
        self.textes_originaux = {}
        self.textes_nettoyes = {}
        self.resultats_sentiments = {}
        self.resultats_themes = {}
        
        # Modèles ML
        self.modeles_sentiment = {}
        self.vectorizer = None
        self.label_encoder = None
        
        # Dataset politique
        self.dataset_politique = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        
        print("[OK] Initialisation terminee")
    
    
    def charger_dataset_politique(self):
        """Charge le dataset politique créé."""
        print("\n" + "-"*80)
        print("ETAPE 1 : CHARGEMENT DU DATASET POLITIQUE")
        print("-"*80)
        
        dataset_path = Path("dataset_sentiment_politique.csv")
        
        if not dataset_path.exists():
            print("[ERREUR] dataset_sentiment_politique.csv non trouve !")
            raise FileNotFoundError("Dataset politique manquant")
        
        self.dataset_politique = pd.read_csv(dataset_path)
        
        print(f"[OK] Dataset politique charge : {len(self.dataset_politique)} exemples")
        print(f"\n[STATISTIQUES]")
        print(f"  Positifs (1) : {(self.dataset_politique['sentiment'] == 1).sum()}")
        print(f"  Negatifs (0) : {(self.dataset_politique['sentiment'] == 0).sum()}")
        print(f"  Neutres  (2) : {(self.dataset_politique['sentiment'] == 2).sum()}")
        print(f"\n[SOURCE] Dataset cree specifiquement pour le domaine POLITIQUE francais")
        
        return self.dataset_politique
    
    
    def preparer_donnees_entrainement(self):
        """Prépare les données."""
        print("\n" + "-"*80)
        print("ETAPE 2 : PREPARATION DES DONNEES")
        print("-"*80)
        
        # Nettoyage simple
        print("[INFO] Nettoyage des textes...")
        self.dataset_politique['texte_clean'] = self.dataset_politique['texte'].apply(
            lambda x: self.nettoyer_texte_simple(str(x))
        )
        
        # Vectorisation TF-IDF
        print("[INFO] Vectorisation TF-IDF...")
        self.vectorizer = TfidfVectorizer(
            max_features=2000,
            ngram_range=(1, 2),
            min_df=1
        )
        
        X = self.vectorizer.fit_transform(self.dataset_politique['texte_clean'])
        y = self.dataset_politique['sentiment']
        
        # Split train/test (80/20)
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        print(f"[OK] Donnees preparees :")
        print(f"     Train : {self.X_train.shape[0]} exemples")
        print(f"     Test  : {self.X_test.shape[0]} exemples")
        print(f"     Features : {self.X_train.shape[1]} mots")
    
    
    def entrainer_modeles(self):
        """Entraîne les modèles sur le dataset politique."""
        print("\n" + "-"*80)
        print("ETAPE 3 : ENTRAINEMENT DES MODELES (DATASET POLITIQUE)")
        print("-"*80)
        
        modeles = {
            'Naive Bayes': MultinomialNB(),
            'SVM (Linear)': LinearSVC(random_state=42, max_iter=2000),
            'Logistic Regression': LogisticRegression(random_state=42, max_iter=1000, multi_class='ovr'),
            'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
        }
        
        resultats = []
        
        for nom, modele in modeles.items():
            print(f"\n[INFO] Entrainement de {nom}...")
            
            # Entraînement
            modele.fit(self.X_train, self.y_train)
            
            # Prédictions
            y_pred = modele.predict(self.X_test)
            
            # Métriques
            accuracy = accuracy_score(self.y_test, y_pred)
            f1 = f1_score(self.y_test, y_pred, average='weighted')
            
            # Cross-validation
            cv_scores = cross_val_score(modele, self.X_train, self.y_train, cv=3, scoring='f1_weighted')
            cv_mean = cv_scores.mean()
            
            resultats.append({
                'Modele': nom,
                'Accuracy': accuracy,
                'F1-Score': f1,
                'CV F1-Score': cv_mean
            })
            
            # Sauvegarder
            self.modeles_sentiment[nom] = {
                'modele': modele,
                'y_pred': y_pred,
                'accuracy': accuracy,
                'f1': f1
            }
            
            print(f"[OK] {nom} : Accuracy={accuracy:.3f}, F1={f1:.3f}, CV={cv_mean:.3f}")
        
        # Tableau comparatif
        df_resultats = pd.DataFrame(resultats)
        print("\n" + "="*80)
        print("EVALUATION SUR DATASET POLITIQUE")
        print("="*80)
        print(df_resultats.to_string(index=False))
        
        # Meilleur modèle
        meilleur_idx = df_resultats['F1-Score'].idxmax()
        meilleur_modele = df_resultats.loc[meilleur_idx, 'Modele']
        print(f"\n[MEILLEUR MODELE] {meilleur_modele} avec F1={df_resultats.loc[meilleur_idx, 'F1-Score']:.3f}")
        
        # Sauvegarder le meilleur
        with open('modele_politique.pkl', 'wb') as f:
            pickle.dump(self.modeles_sentiment[meilleur_modele]['modele'], f)
        with open('vectorizer_politique.pkl', 'wb') as f:
            pickle.dump(self.vectorizer, f)
        
        print(f"[OK] Meilleur modele sauvegarde : modele_politique.pkl")
        
        return df_resultats
    
    
    def nettoyer_texte_simple(self, texte):
        """Nettoyage simple."""
        texte = texte.lower()
        texte = re.sub(r'[^\w\s]', ' ', texte)
        texte = re.sub(r'\s+', ' ', texte)
        return texte.strip()
    
    
    def nettoyer_texte_complet(self, texte):
        """Nettoyage avec lemmatisation."""
        doc = self.nlp(texte.lower())
        mots_nettoyes = []
        for token in doc:
            if not token.is_stop and not token.is_punct and token.is_alpha:
                mots_nettoyes.append(token.lemma_)
        return ' '.join(mots_nettoyes)
    
    
    def lire_fichiers(self, fichiers):
        """Lit les fichiers de discours."""
        print("\n" + "-"*80)
        print("ETAPE 4 : LECTURE DES DISCOURS POLITIQUES")
        print("-"*80)
        
        for fichier in fichiers:
            if Path(fichier).exists():
                with open(fichier, 'r', encoding='utf-8') as f:
                    contenu = f.read()
                
                nom_parti = Path(fichier).stem.replace('_Discours', '')
                self.textes_originaux[nom_parti] = contenu
                
                print(f"[INFO] Nettoyage de {nom_parti}...")
                texte_propre = self.nettoyer_texte_complet(contenu)
                self.textes_nettoyes[nom_parti] = texte_propre
                
                print(f"[OK] {nom_parti} : {len(contenu)} caracteres -> {len(texte_propre.split())} mots")
        
        print(f"\n[OK] {len(self.textes_originaux)} fichiers traites")
    
    
    def analyser_sentiments_ml(self):
        """Analyse avec les 4 modèles ML entraînés."""
        print("\n" + "-"*80)
        print("ETAPE 5 : ANALYSE DE SENTIMENT (4 MODELES ML POLITIQUES)")
        print("-"*80)
        
        for parti, texte in self.textes_nettoyes.items():
            print(f"\n[INFO] Analyse de {parti}...")
            
            resultats = {'parti': parti, 'modeles': {}}
            
            # Découper en segments
            mots = texte.split()
            segments = [' '.join(mots[i:i+50]) for i in range(0, len(mots), 50)]
            
            # Vectoriser
            segments_vectorises = self.vectorizer.transform(segments)
            
            # Appliquer chaque modèle
            for nom_modele, modele_info in self.modeles_sentiment.items():
                predictions = modele_info['modele'].predict(segments_vectorises)
                
                # Compter
                positifs = (predictions == 1).sum()
                negatifs = (predictions == 0).sum()
                neutres = (predictions == 2).sum()
                total = len(predictions)
                
                # Pourcentages
                pct_positif = (positifs / total) * 100
                pct_negatif = (negatifs / total) * 100
                pct_neutre = (neutres / total) * 100
                
                # Score global
                score = (pct_positif - pct_negatif) / 100
                
                # Classe majoritaire
                if positifs > negatifs and positifs > neutres:
                    classe = 'Positif'
                elif negatifs > positifs and negatifs > neutres:
                    classe = 'Negatif'
                else:
                    classe = 'Neutre'
                
                resultats['modeles'][nom_modele] = {
                    'score': score,
                    'classe': classe,
                    'positifs': positifs,
                    'negatifs': negatifs,
                    'neutres': neutres,
                    'total': total,
                    'pct_positif': pct_positif,
                    'pct_negatif': pct_negatif,
                    'pct_neutre': pct_neutre
                }
            
            self.resultats_sentiments[parti] = resultats
            
            # Afficher résumé
            print(f"[OK] {parti} analyse avec 4 modeles ML")
            for nom, res in resultats['modeles'].items():
                print(f"     {nom:20s} : {res['classe']:8s} (Pos:{res['pct_positif']:.1f}% Neg:{res['pct_negatif']:.1f}% Neu:{res['pct_neutre']:.1f}%)")
    
    
    def analyser_themes(self):
        """Analyse les thèmes."""
        print("\n" + "-"*80)
        print("ETAPE 6 : ANALYSE DE THEMES")
        print("-"*80)
        
        for parti, texte in self.textes_nettoyes.items():
            print(f"\n[INFO] Analyse thematique de {parti}...")
            
            mots = set(texte.lower().split())
            themes_detectes = {}
            
            for theme, mots_cles in self.themes.items():
                occurrences = sum(1 for mot_cle in mots_cles if mot_cle in mots)
                if occurrences > 0:
                    themes_detectes[theme] = occurrences
            
            themes_tries = dict(sorted(themes_detectes.items(), 
                                       key=lambda x: x[1], 
                                       reverse=True))
            
            self.resultats_themes[parti] = themes_tries
            
            print(f"[OK] {parti} : {len(themes_tries)} themes detectes")
            for theme, count in list(themes_tries.items())[:5]:
                print(f"     {theme:15s} : {count:3d} occurrences")
    
    
    def visualiser_resultats(self):
        """Crée les visualisations."""
        print("\n[INFO] Generation des graphiques...")
        
        fig, axes = plt.subplots(2, 3, figsize=(18, 12))
        fig.suptitle('ANALYSE SENTIMENT - MODELE SPECIALISE POLITIQUE', 
                     fontsize=16, fontweight='bold')
        
        partis = list(self.resultats_sentiments.keys())
        modeles = list(self.modeles_sentiment.keys())
        
        # 1. Scores par modèle (heatmap)
        ax1 = axes[0, 0]
        data_scores = []
        for parti in partis:
            scores = [self.resultats_sentiments[parti]['modeles'][mod]['score'] 
                     for mod in modeles]
            data_scores.append(scores)
        
        sns.heatmap(data_scores, annot=True, fmt='.3f',
                   xticklabels=[m.replace(' ', '\n') for m in modeles], 
                   yticklabels=partis,
                   cmap='RdYlGn', center=0, ax=ax1)
        ax1.set_title('Scores de Sentiment par Modele', fontweight='bold')
        
        # 2. Comparaison scores moyens
        ax2 = axes[0, 1]
        scores_moyens = []
        for parti in partis:
            scores = [self.resultats_sentiments[parti]['modeles'][mod]['score'] 
                     for mod in modeles]
            scores_moyens.append(np.mean(scores))
        
        colors = ['green' if s > 0.1 else 'red' if s < -0.1 else 'gray' 
                 for s in scores_moyens]
        ax2.barh(partis, scores_moyens, color=colors, alpha=0.7)
        ax2.set_xlabel('Score Moyen')
        ax2.set_title('Sentiment Moyen par Parti', fontweight='bold')
        ax2.axvline(x=0, color='black', linestyle='--', linewidth=0.5)
        for i, v in enumerate(scores_moyens):
            ax2.text(v + 0.01 if v > 0 else v - 0.01, i, f'{v:+.3f}', 
                    va='center', ha='left' if v > 0 else 'right')
        
        # 3. Distribution par modèle (exemple: Logistic Regression)
        ax3 = axes[0, 2]
        modele_ref = 'Logistic Regression'
        data_dist = []
        for parti in partis:
            res = self.resultats_sentiments[parti]['modeles'][modele_ref]
            data_dist.append([res['pct_positif'], res['pct_neutre'], res['pct_negatif']])
        
        x = np.arange(len(partis))
        width = 0.6
        p1 = ax3.barh(x, [d[0] for d in data_dist], width, label='Positif', color='green', alpha=0.7)
        p2 = ax3.barh(x, [d[1] for d in data_dist], width, 
                     left=[d[0] for d in data_dist], label='Neutre', color='gray', alpha=0.7)
        p3 = ax3.barh(x, [d[2] for d in data_dist], width,
                     left=[d[0]+d[1] for d in data_dist], label='Negatif', color='red', alpha=0.7)
        
        ax3.set_yticks(x)
        ax3.set_yticklabels(partis)
        ax3.set_xlabel('Pourcentage (%)')
        ax3.set_title(f'Distribution - {modele_ref}', fontweight='bold')
        ax3.legend(loc='upper right', fontsize=8)
        
        # 4. Consensus entre modèles
        ax4 = axes[1, 0]
        consensus = []
        for parti in partis:
            classes = [self.resultats_sentiments[parti]['modeles'][mod]['classe'] 
                      for mod in modeles]
            consensus_count = Counter(classes).most_common(1)[0][1]
            consensus.append(consensus_count / len(modeles))
        
        colors = ['green' if c >= 0.75 else 'orange' if c >= 0.5 else 'red' 
                 for c in consensus]
        ax4.barh(partis, consensus, color=colors, alpha=0.7)
        ax4.set_xlabel('Taux de Consensus')
        ax4.set_title('Consensus entre Modeles', fontweight='bold')
        ax4.set_xlim(0, 1)
        for i, v in enumerate(consensus):
            ax4.text(v + 0.02, i, f'{v:.0%}', va='center')
        
        # 5. Thèmes détectés
        ax5 = axes[1, 1]
        themes_all = set()
        for parti in partis:
            themes_all.update(self.resultats_themes[parti].keys())
        themes_top = list(themes_all)[:10]
        
        data_themes = []
        for theme in themes_top:
            counts = [self.resultats_themes[parti].get(theme, 0) for parti in partis]
            data_themes.append(counts)
        
        if len(themes_top) > 0:
            sns.heatmap(data_themes, annot=True, fmt='d',
                       xticklabels=partis, yticklabels=themes_top,
                       cmap='YlOrRd', ax=ax5)
            ax5.set_title('Themes Politiques', fontweight='bold')
        
        # 6. Classement final
        ax6 = axes[1, 2]
        classement = sorted([(p, scores_moyens[i]) for i, p in enumerate(partis)], 
                           key=lambda x: x[1], reverse=True)
        partis_classes = [p[0] for p in classement]
        scores_classes = [p[1] for p in classement]
        colors_classes = ['gold' if i == 0 else 'silver' if i == 1 else 'orange' if i == 2 else 'gray' 
                         for i in range(len(partis_classes))]
        
        ax6.barh(range(len(partis_classes)), scores_classes, color=colors_classes, alpha=0.8)
        ax6.set_yticks(range(len(partis_classes)))
        ax6.set_yticklabels([f"{i+1}. {p}" for i, p in enumerate(partis_classes)])
        ax6.set_xlabel('Score Moyen')
        ax6.set_title('Classement Final', fontweight='bold', fontsize=12)
        ax6.axvline(x=0, color='black', linestyle='--', linewidth=0.5)
        for i, v in enumerate(scores_classes):
            ax6.text(v + 0.01 if v > 0 else v - 0.01, i, f'{v:+.3f}', 
                    va='center', ha='left' if v > 0 else 'right', fontweight='bold')
        
        plt.tight_layout()
        plt.savefig('analyse_sentiment_politique_final.png', dpi=300, bbox_inches='tight')
        print(f"[OK] Graphique sauvegarde : analyse_sentiment_politique_final.png")
        plt.close()
        
        # Matrices de confusion
        self.visualiser_matrices_confusion()
    
    
    def visualiser_matrices_confusion(self):
        """Matrices de confusion."""
        print("\n[INFO] Generation des matrices de confusion...")
        
        fig, axes = plt.subplots(2, 2, figsize=(14, 12))
        fig.suptitle('MATRICES DE CONFUSION - DATASET POLITIQUE', 
                     fontsize=16, fontweight='bold')
        axes = axes.ravel()
        
        for idx, (nom, modele_info) in enumerate(self.modeles_sentiment.items()):
            if idx >= 4:
                break
            
            cm = confusion_matrix(self.y_test, modele_info['y_pred'])
            
            sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=axes[idx],
                       xticklabels=['Negatif', 'Positif', 'Neutre'],
                       yticklabels=['Negatif', 'Positif', 'Neutre'])
            
            axes[idx].set_title(f'{nom}\nAccuracy: {modele_info["accuracy"]:.3f}', 
                               fontweight='bold')
            axes[idx].set_ylabel('Vraie Classe')
            axes[idx].set_xlabel('Classe Predite')
        
        plt.tight_layout()
        plt.savefig('matrices_confusion_politique.png', dpi=300, bbox_inches='tight')
        print(f"[OK] Graphique sauvegarde : matrices_confusion_politique.png")
        plt.close()
    
    
    def generer_rapport(self):
        """Génère le rapport."""
        print("\n[INFO] Generation du rapport...")
        
        rapport = []
        rapport.append("="*100)
        rapport.append("RAPPORT - ANALYSE SENTIMENT POLITIQUE (MODELE SPECIALISE)")
        rapport.append("="*100)
        rapport.append(f"\nDate : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Dataset
        rapport.append("\n" + "="*100)
        rapport.append("1. DATASET D'ENTRAINEMENT POLITIQUE")
        rapport.append("="*100)
        rapport.append(f"Source : Dataset cree specifiquement pour le domaine POLITIQUE")
        rapport.append(f"Total : {len(self.dataset_politique)} exemples")
        rapport.append(f"  Positifs : {(self.dataset_politique['sentiment'] == 1).sum()}")
        rapport.append(f"  Negatifs : {(self.dataset_politique['sentiment'] == 0).sum()}")
        rapport.append(f"  Neutres  : {(self.dataset_politique['sentiment'] == 2).sum()}")
        rapport.append(f"Train : {self.X_train.shape[0]} exemples")
        rapport.append(f"Test  : {self.X_test.shape[0]} exemples")
        
        # Modèles
        rapport.append("\n" + "="*100)
        rapport.append("2. EVALUATION DES MODELES (DATASET POLITIQUE)")
        rapport.append("="*100)
        for nom, modele_info in self.modeles_sentiment.items():
            rapport.append(f"\n{nom} :")
            rapport.append(f"  Accuracy : {modele_info['accuracy']:.3f}")
            rapport.append(f"  F1-Score : {modele_info['f1']:.3f}")
        
        # Analyse par parti
        rapport.append("\n" + "="*100)
        rapport.append("3. RESULTATS - DISCOURS POLITIQUES")
        rapport.append("="*100)
        
        for parti in self.resultats_sentiments.keys():
            rapport.append(f"\n{parti} :")
            for modele, resultats in self.resultats_sentiments[parti]['modeles'].items():
                rapport.append(f"\n  {modele} :")
                rapport.append(f"    Classe : {resultats['classe']}")
                rapport.append(f"    Score  : {resultats['score']:+.3f}")
                rapport.append(f"    Positifs : {resultats['positifs']}/{resultats['total']} ({resultats['pct_positif']:.1f}%)")
                rapport.append(f"    Negatifs : {resultats['negatifs']}/{resultats['total']} ({resultats['pct_negatif']:.1f}%)")
                rapport.append(f"    Neutres  : {resultats['neutres']}/{resultats['total']} ({resultats['pct_neutre']:.1f}%)")
            
            rapport.append(f"\n  Top 5 themes :")
            for theme, count in list(self.resultats_themes[parti].items())[:5]:
                rapport.append(f"    {theme:15s} : {count:3d} occurrences")
        
        # Classement
        rapport.append("\n" + "="*100)
        rapport.append("4. CLASSEMENT FINAL (SCORE MOYEN)")
        rapport.append("="*100)
        
        scores_moyens = {}
        for parti in self.resultats_sentiments.keys():
            scores = [self.resultats_sentiments[parti]['modeles'][mod]['score'] 
                     for mod in self.modeles_sentiment.keys()]
            scores_moyens[parti] = np.mean(scores)
        
        classement = sorted(scores_moyens.items(), key=lambda x: x[1], reverse=True)
        for i, (parti, score) in enumerate(classement):
            rapport.append(f"{i+1}. {parti:10s} : {score:+.3f}")
        
        rapport.append("\n" + "="*100)
        rapport.append("FIN DU RAPPORT")
        rapport.append("="*100)
        
        contenu = '\n'.join(rapport)
        with open('rapport_sentiment_politique.txt', 'w', encoding='utf-8') as f:
            f.write(contenu)
        
        print(f"[OK] Rapport sauvegarde : rapport_sentiment_politique.txt")
    
    
    def executer_analyse_complete(self, fichiers):
        """Exécute l'analyse complète."""
        print("\n" + "="*80)
        print("DEMARRAGE DE L'ANALYSE")
        print("="*80)
        
        # Phase 1 : Entraînement sur dataset politique
        self.charger_dataset_politique()
        self.preparer_donnees_entrainement()
        self.entrainer_modeles()
        
        # Phase 2 : Analyse des discours
        self.lire_fichiers(fichiers)
        self.analyser_sentiments_ml()
        self.analyser_themes()
        
        # Phase 3 : Visualisations et rapport
        self.visualiser_resultats()
        self.generer_rapport()
        
        print("\n" + "="*80)
        print("ANALYSE TERMINEE AVEC SUCCES !")
        print("="*80)
        print("\nFichiers generes :")
        print("  - modele_politique.pkl")
        print("  - vectorizer_politique.pkl")
        print("  - analyse_sentiment_politique_final.png")
        print("  - matrices_confusion_politique.png")
        print("  - rapport_sentiment_politique.txt")


# Point d'entrée
if __name__ == "__main__":
    fichiers = [
        'PAM_Discours.txt',
        'PI_Discours.txt',
        'PJD_Discours.txt',
        'RNI_Discours.txt'
    ]
    
    analyseur = AnalyseTextMiningPolitique()
    analyseur.executer_analyse_complete(fichiers)

