"""
Projet d'Analyse de Text Mining - Discours des Partis Politiques Marocains
Objectif: Analyser les sujets traités et les opinions/sentiments exprimés par chaque parti
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

# Charger le modèle français de spaCy pour la lemmatisation
try:
    nlp = spacy.load("fr_core_news_sm")
    print("[INFO] Modèle spaCy français chargé avec succès")
except OSError:
    print("[ERREUR] Modèle spaCy non trouvé. Installation nécessaire:")
    print("  python -m spacy download fr_core_news_sm")
    nlp = None

# Configuration de matplotlib pour afficher les caractères français/arabes
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['figure.figsize'] = (14, 8)
sns.set_style("whitegrid")

class AnalyseTextMining:
    """Classe principale pour l'analyse de text mining des discours politiques"""
    
    def __init__(self, dossier="."):
        self.dossier = dossier
        self.partis = ["PAM", "PI", "PJD", "RNI"]
        self.textes_bruts = {}
        self.textes_nettoyes = {}
        self.themes_par_parti = {}
        self.sentiments_par_parti = {}
        
        # Définition des stopwords français et arabes romanisés
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
        
        # Dictionnaire de thèmes avec mots-clés
        self.themes_keywords = {
            'Éducation': ['école', 'éducation', 'enseignement', 'élèves', 'formation', 
                         'université', 'formation', 'professeur', 'enseignant', 'scolarité',
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
        
        # Mots-clés pour l'analyse de sentiment
        self.sentiment_positif = [
            'améliorer', 'renforcer', 'développer', 'garantir', 'soutenir',
            'créer', 'augmenter', 'réduire', 'élargir', 'encourager', 'promouvoir',
            'favoriser', 'valoriser', 'moderniser', 'réussir', 'succès', 'progrès',
            'avancées', 'meilleur', 'optimiser', 'accompagner', 'confiance', 'restaurer',
            'généraliser', 'protéger', 'bénéficier', 'offre', 'nouvelle', 'nouveau',
            'engagement', 'mobilisation', 'reconquête', 'stratégie', 'vision'
        ]
        
        self.sentiment_negatif = [
            'crise', 'déficit', 'problème', 'limite', 'difficulté', 'faible',
            'échec', 'corruption', 'injustice', 'inégalités', 'défiance', 'pauvreté',
            'chômage', 'baisse', 'dégradation', 'défaut', 'défectueux', 'absence',
            'manque', 'inadapté', 'insuffisant', 'vulnérabilité', 'stress', 'fiasco',
            'catastrophique', 'scandales', 'fraude', 'banditisme', 'débâcle', 'défaite'
        ]
        
        self.sentiment_neutre = [
            'analyser', 'constater', 'observer', 'considérer', 'examiner',
            'étudier', 'évaluer', 'mesurer', 'identifier', 'définir', 'établir',
            'présenter', 'décrire', 'expliquer', 'mentionner', 'indiquer'
        ]

    def charger_textes(self):
        """Charge tous les fichiers texte des partis"""
        print("=" * 80)
        print("ÉTAPE 1: CHARGEMENT DES TEXTES")
        print("=" * 80)
        
        for parti in self.partis:
            fichier = os.path.join(self.dossier, f"{parti}_Discours.txt")
            try:
                with open(fichier, 'r', encoding='utf-8') as f:
                    contenu = f.read()
                    self.textes_bruts[parti] = contenu
                    nb_mots = len(contenu.split())
                    print(f"[OK] {parti}: {nb_mots} mots charges")
            except FileNotFoundError:
                print(f"[X] {parti}: Fichier non trouve")
                self.textes_bruts[parti] = ""
            except Exception as e:
                print(f"[X] {parti}: Erreur - {e}")
                self.textes_bruts[parti] = ""
        
        print()

    def pretraiter_textes(self):
        """Prétraitement: nettoyage, tokenisation et lemmatisation"""
        print("=" * 80)
        print("ÉTAPE 2: PRÉTRAITEMENT DES TEXTES (avec Lemmatisation)")
        print("=" * 80)
        
        for parti, texte in self.textes_bruts.items():
            if not texte:
                self.textes_nettoyes[parti] = []
                print(f"[!] {parti}: Texte vide, ignore")
                continue
            
            # Méthode 1: Avec lemmatisation (si spaCy disponible)
            if nlp is not None:
                print(f"[...] {parti}: Lemmatisation en cours...")
                
                # Nettoyage basique d'abord
                texte_nettoye = re.sub(r'\d+', '', texte)  # Supprimer chiffres
                texte_nettoye = re.sub(r'\s+', ' ', texte_nettoye).strip()
                
                # Lemmatisation avec spaCy
                doc = nlp(texte_nettoye)
                
                # Extraire les lemmes (forme de base des mots)
                lemmes = []
                for token in doc:
                    # Filtrer: pas de ponctuation, pas de stopwords, longueur > 2
                    if (not token.is_punct and 
                        not token.is_space and 
                        not token.is_stop and 
                        len(token.lemma_) > 2 and
                        token.lemma_.lower() not in self.stopwords_fr):
                        lemmes.append(token.lemma_.lower())
                
                self.textes_nettoyes[parti] = lemmes
                nb_mots_bruts = len(texte.split())
                print(f"[OK] {parti}: {len(lemmes)} lemmes extraits "
                      f"(reduit de {nb_mots_bruts} mots bruts)")
            
            # Méthode 2: Sans lemmatisation (fallback)
            else:
                print(f"[!] {parti}: Lemmatisation indisponible, mode simple")
                texte = texte.lower()
                texte = re.sub(r'[^\w\s\-éèêëàâäôöùûüçïî]', ' ', texte)
                texte = re.sub(r'\d+', '', texte)
                texte = re.sub(r'\s+', ' ', texte).strip()
                
                mots = texte.split()
                mots_filtres = [
                    mot for mot in mots 
                    if len(mot) > 2 and mot not in self.stopwords_fr
                ]
                
                self.textes_nettoyes[parti] = mots_filtres
                print(f"[OK] {parti}: {len(mots_filtres)} mots apres nettoyage")
        
        print()

    def analyser_themes(self):
        """Analyse thématique: identification des sujets par parti"""
        print("=" * 80)
        print("ÉTAPE 3: ANALYSE THÉMATIQUE")
        print("=" * 80)
        
        for parti, mots in self.textes_nettoyes.items():
            if not mots:
                self.themes_par_parti[parti] = {}
                continue
            
            texte_complet = ' '.join(mots)
            themes_detectes = {}
            
            for theme, keywords in self.themes_keywords.items():
                count = sum(texte_complet.count(kw) for kw in keywords)
                if count > 0:
                    themes_detectes[theme] = count
            
            self.themes_par_parti[parti] = themes_detectes
            
            print(f"\n{parti}:")
            if themes_detectes:
                for theme, count in sorted(themes_detectes.items(), 
                                          key=lambda x: x[1], reverse=True)[:5]:
                    print(f"  - {theme}: {count} mentions")
            else:
                print("  Aucun theme detecte")
        
        print()

    def analyser_sentiments(self):
        """Analyse de sentiment par thème et par parti"""
        print("=" * 80)
        print("ÉTAPE 4: ANALYSE DE SENTIMENT")
        print("=" * 80)
        
        for parti, mots in self.textes_nettoyes.items():
            if not mots:
                self.sentiments_par_parti[parti] = {}
                continue
            
            texte = ' '.join(mots)
            sentiments = {}
            
            # Compter les occurrences de mots de sentiment
            positif_count = sum(texte.count(mot) for mot in self.sentiment_positif)
            negatif_count = sum(texte.count(mot) for mot in self.sentiment_negatif)
            neutre_count = sum(texte.count(mot) for mot in self.sentiment_neutre)
            
            total = positif_count + negatif_count + neutre_count
            
            if total > 0:
                sentiments = {
                    'Positif': positif_count,
                    'Négatif': negatif_count,
                    'Neutre': neutre_count,
                    'Score': (positif_count - negatif_count) / total
                }
            else:
                sentiments = {
                    'Positif': 0,
                    'Négatif': 0,
                    'Neutre': 0,
                    'Score': 0
                }
            
            self.sentiments_par_parti[parti] = sentiments
            
            # Déterminer le ton général
            if sentiments['Score'] > 0.1:
                ton = "Positif (propositions/solutions)"
            elif sentiments['Score'] < -0.1:
                ton = "Négatif (critiques)"
            else:
                ton = "Neutre/Équilibré"
            
            print(f"\n{parti}:")
            print(f"  Positif: {sentiments['Positif']} | "
                  f"Négatif: {sentiments['Négatif']} | "
                  f"Neutre: {sentiments['Neutre']}")
            print(f"  Score global: {sentiments['Score']:.3f}")
            print(f"  Ton général: {ton}")
        
        print()

    def creer_tableau_synthese(self):
        """Création du tableau de synthèse comparatif"""
        print("=" * 80)
        print("ÉTAPE 5: TABLEAU DE SYNTHÈSE")
        print("=" * 80)
        
        # Récupérer tous les thèmes uniques
        tous_themes = set()
        for themes in self.themes_par_parti.values():
            tous_themes.update(themes.keys())
        
        # Créer le DataFrame
        data = []
        for parti in self.partis:
            row = {'Parti': parti}
            
            # Ajouter le nombre de textes (simplifié: 1 texte par parti)
            row['Nb_Textes'] = 1 if self.textes_bruts.get(parti, "") else 0
            
            # Top 3 thèmes
            themes = self.themes_par_parti.get(parti, {})
            top_themes = sorted(themes.items(), key=lambda x: x[1], reverse=True)[:3]
            row['Top_Themes'] = ', '.join([f"{t[0]}({t[1]})" for t in top_themes])
            
            # Sentiment
            sentiment = self.sentiments_par_parti.get(parti, {})
            if sentiment.get('Score', 0) > 0.1:
                row['Ton'] = "Positif"
            elif sentiment.get('Score', 0) < -0.1:
                row['Ton'] = "Négatif"
            else:
                row['Ton'] = "Neutre"
            
            row['Score_Sentiment'] = sentiment.get('Score', 0)
            
            data.append(row)
        
        df = pd.DataFrame(data)
        
        # Afficher le tableau
        print("\nTableau comparatif par parti:")
        print(df.to_string(index=False))
        
        # Sauvegarder en CSV et Excel
        df.to_csv('synthese_partis.csv', index=False, encoding='utf-8-sig')
        df.to_excel('synthese_partis.xlsx', index=False)
        print("\n[OK] Tableau sauvegarde: synthese_partis.csv et synthese_partis.xlsx")
        
        # Créer un tableau détaillé par thème
        themes_detail = []
        for theme in sorted(tous_themes):
            row = {'Theme': theme}
            for parti in self.partis:
                count = self.themes_par_parti.get(parti, {}).get(theme, 0)
                row[parti] = count
            themes_detail.append(row)
        
        df_themes = pd.DataFrame(themes_detail)
        df_themes.to_csv('themes_details.csv', index=False, encoding='utf-8-sig')
        df_themes.to_excel('themes_details.xlsx', index=False)
        print("[OK] Details des themes sauvegardes: themes_details.csv et themes_details.xlsx")
        
        print()
        return df, df_themes

    def visualiser_resultats(self):
        """Génération des visualisations"""
        print("=" * 80)
        print("ÉTAPE 6: VISUALISATIONS")
        print("=" * 80)
        
        # 1. Répartition des thèmes par parti
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('Répartition des Thèmes par Parti Politique', 
                     fontsize=16, fontweight='bold')
        
        for idx, parti in enumerate(self.partis):
            ax = axes[idx // 2, idx % 2]
            themes = self.themes_par_parti.get(parti, {})
            
            if themes:
                top_themes = dict(sorted(themes.items(), 
                                       key=lambda x: x[1], 
                                       reverse=True)[:8])
                
                colors = plt.cm.Set3(range(len(top_themes)))
                ax.barh(list(top_themes.keys()), list(top_themes.values()), 
                       color=colors)
                ax.set_xlabel('Nombre de mentions')
                ax.set_title(f'{parti}', fontweight='bold')
                ax.grid(axis='x', alpha=0.3)
            else:
                ax.text(0.5, 0.5, 'Pas de données', 
                       ha='center', va='center', fontsize=14)
                ax.set_title(f'{parti}', fontweight='bold')
        
        plt.tight_layout()
        plt.savefig('themes_par_parti.png', dpi=300, bbox_inches='tight')
        print("[OK] Graphique sauvegarde: themes_par_parti.png")
        
        # 2. Comparaison des sentiments
        fig, ax = plt.subplots(figsize=(12, 6))
        
        partis_valides = [p for p in self.partis if self.sentiments_par_parti.get(p)]
        scores = [self.sentiments_par_parti[p]['Score'] for p in partis_valides]
        colors = ['green' if s > 0.1 else 'red' if s < -0.1 else 'gray' 
                 for s in scores]
        
        ax.bar(partis_valides, scores, color=colors, alpha=0.7, edgecolor='black')
        ax.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
        ax.set_ylabel('Score de Sentiment', fontsize=12)
        ax.set_xlabel('Parti', fontsize=12)
        ax.set_title('Comparaison des Tons/Sentiments par Parti', 
                    fontsize=14, fontweight='bold')
        ax.grid(axis='y', alpha=0.3)
        
        # Légende
        from matplotlib.patches import Patch
        legend_elements = [
            Patch(facecolor='green', alpha=0.7, label='Positif (propositions)'),
            Patch(facecolor='gray', alpha=0.7, label='Neutre'),
            Patch(facecolor='red', alpha=0.7, label='Négatif (critiques)')
        ]
        ax.legend(handles=legend_elements, loc='upper right')
        
        plt.tight_layout()
        plt.savefig('sentiments_comparaison.png', dpi=300, bbox_inches='tight')
        print("[OK] Graphique sauvegarde: sentiments_comparaison.png")
        
        # 3. Nuages de mots par parti
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('Nuages de Mots par Parti', fontsize=16, fontweight='bold')
        
        for idx, parti in enumerate(self.partis):
            ax = axes[idx // 2, idx % 2]
            mots = self.textes_nettoyes.get(parti, [])
            
            if mots and len(mots) > 10:
                texte = ' '.join(mots)
                wordcloud = WordCloud(width=800, height=400, 
                                     background_color='white',
                                     colormap='viridis',
                                     max_words=50).generate(texte)
                
                ax.imshow(wordcloud, interpolation='bilinear')
                ax.set_title(f'{parti}', fontweight='bold')
                ax.axis('off')
            else:
                ax.text(0.5, 0.5, 'Données insuffisantes', 
                       ha='center', va='center', fontsize=14)
                ax.set_title(f'{parti}', fontweight='bold')
                ax.axis('off')
        
        plt.tight_layout()
        plt.savefig('nuages_mots.png', dpi=300, bbox_inches='tight')
        print("[OK] Graphique sauvegarde: nuages_mots.png")
        
        # 4. Heatmap des thèmes
        tous_themes = set()
        for themes in self.themes_par_parti.values():
            tous_themes.update(themes.keys())
        
        matrix_data = []
        for theme in sorted(tous_themes):
            row = [self.themes_par_parti.get(parti, {}).get(theme, 0) 
                   for parti in self.partis]
            matrix_data.append(row)
        
        if matrix_data:
            fig, ax = plt.subplots(figsize=(10, 12))
            im = ax.imshow(matrix_data, cmap='YlOrRd', aspect='auto')
            
            ax.set_xticks(range(len(self.partis)))
            ax.set_yticks(range(len(tous_themes)))
            ax.set_xticklabels(self.partis)
            ax.set_yticklabels(sorted(tous_themes))
            
            # Ajouter les valeurs dans les cellules
            for i in range(len(tous_themes)):
                for j in range(len(self.partis)):
                    text = ax.text(j, i, matrix_data[i][j],
                                 ha="center", va="center", color="black", fontsize=9)
            
            ax.set_title('Heatmap: Intensité des Thèmes par Parti', 
                        fontsize=14, fontweight='bold', pad=20)
            plt.colorbar(im, ax=ax, label='Nombre de mentions')
            plt.tight_layout()
            plt.savefig('heatmap_themes.png', dpi=300, bbox_inches='tight')
            print("[OK] Graphique sauvegarde: heatmap_themes.png")
        
        print()

    def analyser_cooccurrence(self):
        """Analyse de co-occurrence des thèmes"""
        print("=" * 80)
        print("ÉTAPE 7: ANALYSE DE CO-OCCURRENCE DES THÈMES")
        print("=" * 80)
        
        cooccurrences_par_parti = {}
        
        for parti, mots in self.textes_nettoyes.items():
            if not mots:
                continue
            
            texte = ' '.join(mots)
            
            # Détecter les thèmes présents dans des segments de texte
            # On découpe le texte en segments de 50 mots
            window_size = 50
            cooccurrences = defaultdict(int)
            
            # Parcourir le texte par fenêtres
            words = texte.split()
            for i in range(0, len(words), window_size // 2):  # Overlap de 50%
                segment = ' '.join(words[i:i+window_size])
                
                # Détecter quels thèmes sont dans ce segment
                themes_dans_segment = []
                for theme, keywords in self.themes_keywords.items():
                    if any(kw in segment for kw in keywords):
                        themes_dans_segment.append(theme)
                
                # Compter les co-occurrences
                if len(themes_dans_segment) >= 2:
                    for theme1, theme2 in combinations(sorted(themes_dans_segment), 2):
                        cooccurrences[(theme1, theme2)] += 1
            
            cooccurrences_par_parti[parti] = cooccurrences
        
        # Créer un DataFrame pour l'export
        cooccurrence_data = []
        for parti, cooccs in cooccurrences_par_parti.items():
            if cooccs:
                top_cooccs = sorted(cooccs.items(), key=lambda x: x[1], reverse=True)[:10]
                print(f"\n{parti} - Top co-occurrences:")
                for (theme1, theme2), count in top_cooccs:
                    print(f"  {theme1} <-> {theme2}: {count} fois")
                    cooccurrence_data.append({
                        'Parti': parti,
                        'Theme_1': theme1,
                        'Theme_2': theme2,
                        'Frequence': count
                    })
        
        if cooccurrence_data:
            df_coocc = pd.DataFrame(cooccurrence_data)
            df_coocc.to_csv('cooccurrences_themes.csv', index=False, encoding='utf-8-sig')
            df_coocc.to_excel('cooccurrences_themes.xlsx', index=False)
            print("\n[OK] Analyse de co-occurrence sauvegardee: cooccurrences_themes.csv/.xlsx")
        
        print()
        return cooccurrences_par_parti

    def visualiser_radar(self):
        """Crée un graphique radar comparant les 4 partis sur tous les thèmes"""
        print("=" * 80)
        print("ÉTAPE 8: GRAPHIQUE RADAR COMPARATIF")
        print("=" * 80)
        
        # Récupérer tous les thèmes
        tous_themes = set()
        for themes in self.themes_par_parti.values():
            tous_themes.update(themes.keys())
        
        if not tous_themes:
            print("[!] Pas de themes a visualiser")
            return
        
        # Limiter aux thèmes les plus importants pour la lisibilité
        theme_totaux = defaultdict(int)
        for parti_themes in self.themes_par_parti.values():
            for theme, count in parti_themes.items():
                theme_totaux[theme] += count
        
        # Prendre les 10 thèmes les plus mentionnés
        top_themes = sorted(theme_totaux.items(), key=lambda x: x[1], reverse=True)[:10]
        themes_a_afficher = [t[0] for t in top_themes]
        
        print(f"Themes affiches (top 10): {', '.join(themes_a_afficher)}")
        
        # Créer le graphique radar
        fig = plt.figure(figsize=(12, 12))
        ax = fig.add_subplot(111, projection='polar')
        
        # Nombre de thèmes
        num_themes = len(themes_a_afficher)
        angles = np.linspace(0, 2 * np.pi, num_themes, endpoint=False).tolist()
        
        # Fermer le cercle
        angles += angles[:1]
        
        # Couleurs pour chaque parti
        couleurs = {
            'PAM': '#1f77b4',  # Bleu
            'RNI': '#ff7f0e',  # Orange
            'PJD': '#2ca02c',  # Vert
            'PI': '#d62728'    # Rouge
        }
        
        # Tracer chaque parti
        for parti in self.partis:
            themes_parti = self.themes_par_parti.get(parti, {})
            if not themes_parti:
                continue
            
            # Normaliser les valeurs (0-100)
            max_val = max(theme_totaux.values())
            valeurs = [themes_parti.get(theme, 0) / max_val * 100 for theme in themes_a_afficher]
            valeurs += valeurs[:1]  # Fermer le cercle
            
            ax.plot(angles, valeurs, 'o-', linewidth=2, label=parti, 
                   color=couleurs.get(parti, 'gray'), markersize=6)
            ax.fill(angles, valeurs, alpha=0.15, color=couleurs.get(parti, 'gray'))
        
        # Configurer les labels
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(themes_a_afficher, size=10)
        ax.set_ylim(0, 100)
        
        # Ajouter une grille
        ax.grid(True, linestyle='--', alpha=0.7)
        
        # Titre et légende
        plt.title('Comparaison Radar des Thèmes par Parti\n(Valeurs normalisées sur 100)', 
                 size=14, fontweight='bold', pad=20)
        plt.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1), fontsize=11)
        
        plt.tight_layout()
        plt.savefig('graphique_radar.png', dpi=300, bbox_inches='tight')
        print("[OK] Graphique radar sauvegarde: graphique_radar.png")
        
        # Créer aussi un second radar avec tous les thèmes (si moins de 15)
        if len(tous_themes) <= 14:
            fig2 = plt.figure(figsize=(14, 14))
            ax2 = fig2.add_subplot(111, projection='polar')
            
            themes_complets = sorted(list(tous_themes))
            num_themes_complet = len(themes_complets)
            angles_complet = np.linspace(0, 2 * np.pi, num_themes_complet, endpoint=False).tolist()
            angles_complet += angles_complet[:1]
            
            for parti in self.partis:
                themes_parti = self.themes_par_parti.get(parti, {})
                if not themes_parti:
                    continue
                
                max_val = max(theme_totaux.values())
                valeurs = [themes_parti.get(theme, 0) / max_val * 100 for theme in themes_complets]
                valeurs += valeurs[:1]
                
                ax2.plot(angles_complet, valeurs, 'o-', linewidth=2, label=parti,
                        color=couleurs.get(parti, 'gray'), markersize=5)
                ax2.fill(angles_complet, valeurs, alpha=0.12, color=couleurs.get(parti, 'gray'))
            
            ax2.set_xticks(angles_complet[:-1])
            ax2.set_xticklabels(themes_complets, size=9)
            ax2.set_ylim(0, 100)
            ax2.grid(True, linestyle='--', alpha=0.7)
            
            plt.title('Comparaison Radar - Tous les Thèmes\n(Valeurs normalisées sur 100)',
                     size=14, fontweight='bold', pad=20)
            plt.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1), fontsize=11)
            
            plt.tight_layout()
            plt.savefig('graphique_radar_complet.png', dpi=300, bbox_inches='tight')
            print("[OK] Graphique radar complet sauvegarde: graphique_radar_complet.png")
        
        print()

    def generer_rapport(self):
        """Génère un rapport textuel détaillé"""
        print("=" * 80)
        print("ÉTAPE 9: GÉNÉRATION DU RAPPORT")
        print("=" * 80)
        
        rapport = []
        rapport.append("=" * 80)
        rapport.append("RAPPORT D'ANALYSE - TEXT MINING DES DISCOURS POLITIQUES MAROCAINS")
        rapport.append("=" * 80)
        rapport.append("")
        
        rapport.append("1. RÉSUMÉ EXÉCUTIF")
        rapport.append("-" * 80)
        for parti in self.partis:
            nb_mots = len(self.textes_nettoyes.get(parti, []))
            rapport.append(f"\n{parti}:")
            rapport.append(f"  • Nombre de mots analysés: {nb_mots}")
            
            themes = self.themes_par_parti.get(parti, {})
            if themes:
                top3 = sorted(themes.items(), key=lambda x: x[1], reverse=True)[:3]
                rapport.append(f"  • Thèmes principaux: {', '.join([t[0] for t in top3])}")
            
            sentiment = self.sentiments_par_parti.get(parti, {})
            score = sentiment.get('Score', 0)
            if score > 0.1:
                ton = "Positif - Focus sur les propositions et solutions"
            elif score < -0.1:
                ton = "Négatif - Focus sur les critiques et problèmes"
            else:
                ton = "Neutre/Équilibré"
            rapport.append(f"  • Ton général: {ton}")
        
        rapport.append("\n" + "=" * 80)
        rapport.append("2. ANALYSE COMPARATIVE DES PRIORITÉS")
        rapport.append("-" * 80)
        
        # Identifier les thèmes communs
        themes_par_nb_partis = defaultdict(list)
        tous_themes = set()
        for parti, themes in self.themes_par_parti.items():
            tous_themes.update(themes.keys())
        
        for theme in tous_themes:
            partis_concernes = [p for p in self.partis 
                              if theme in self.themes_par_parti.get(p, {})]
            themes_par_nb_partis[len(partis_concernes)].append(
                (theme, partis_concernes)
            )
        
        rapport.append("\nThèmes traités par tous les partis:")
        if 4 in themes_par_nb_partis or 3 in themes_par_nb_partis:
            communs = themes_par_nb_partis.get(4, []) + themes_par_nb_partis.get(3, [])
            for theme, partis in communs:
                rapport.append(f"  • {theme}: {', '.join(partis)}")
        else:
            rapport.append("  Aucun thème commun à tous les partis")
        
        rapport.append("\nThèmes spécifiques à certains partis:")
        if 1 in themes_par_nb_partis:
            for theme, partis in themes_par_nb_partis[1][:5]:
                rapport.append(f"  • {theme}: {partis[0]} uniquement")
        
        rapport.append("\n" + "=" * 80)
        rapport.append("3. ANALYSE DES OPINIONS/SENTIMENTS")
        rapport.append("-" * 80)
        
        for parti in self.partis:
            sentiment = self.sentiments_par_parti.get(parti, {})
            if sentiment:
                rapport.append(f"\n{parti}:")
                rapport.append(f"  Mots positifs: {sentiment['Positif']}")
                rapport.append(f"  Mots négatifs: {sentiment['Négatif']}")
                rapport.append(f"  Mots neutres: {sentiment['Neutre']}")
                rapport.append(f"  Score: {sentiment['Score']:.3f}")
                
                if sentiment['Score'] > 0.1:
                    rapport.append("  → Approche propositionnelle, focus sur les solutions")
                elif sentiment['Score'] < -0.1:
                    rapport.append("  → Approche critique, focus sur les problèmes")
                else:
                    rapport.append("  → Approche équilibrée")
        
        rapport.append("\n" + "=" * 80)
        rapport.append("4. CONCLUSIONS")
        rapport.append("-" * 80)
        rapport.append("\nObservations principales:")
        rapport.append("• Les partis abordent des thématiques variées reflétant leurs priorités")
        rapport.append("• Les tons varient entre propositions constructives et critiques")
        rapport.append("• Certains thèmes sont communs (développement, social, économie)")
        rapport.append("• D'autres thèmes sont spécifiques à chaque parti")
        
        rapport.append("\n" + "=" * 80)
        rapport.append("FIN DU RAPPORT")
        rapport.append("=" * 80)
        
        # Sauvegarder le rapport
        rapport_texte = '\n'.join(rapport)
        with open('rapport_analyse.txt', 'w', encoding='utf-8') as f:
            f.write(rapport_texte)
        
        print("[OK] Rapport detaille sauvegarde: rapport_analyse.txt")
        print()
        
        return rapport_texte

    def executer_analyse_complete(self):
        """Exécute toutes les étapes de l'analyse"""
        print("\n")
        print("=" * 80)
        print("    ANALYSE TEXT MINING - DISCOURS POLITIQUES MAROCAINS")
        print("=" * 80)
        print("\n")
        
        # Étapes de l'analyse
        self.charger_textes()
        self.pretraiter_textes()
        self.analyser_themes()
        self.analyser_sentiments()
        df_synthese, df_themes = self.creer_tableau_synthese()
        self.visualiser_resultats()
        self.analyser_cooccurrence()
        self.visualiser_radar()
        rapport = self.generer_rapport()
        
        print("=" * 80)
        print("ANALYSE TERMINÉE AVEC SUCCÈS!")
        print("=" * 80)
        print("\nFichiers generes:")
        print("  [TABLE] synthese_partis.csv / synthese_partis.xlsx")
        print("  [TABLE] themes_details.csv / themes_details.xlsx")
        print("  [TABLE] cooccurrences_themes.csv / cooccurrences_themes.xlsx [NOUVEAU]")
        print("  [GRAPH] themes_par_parti.png")
        print("  [GRAPH] sentiments_comparaison.png")
        print("  [GRAPH] nuages_mots.png")
        print("  [GRAPH] heatmap_themes.png")
        print("  [GRAPH] graphique_radar.png [NOUVEAU]")
        print("  [GRAPH] graphique_radar_complet.png [NOUVEAU]")
        print("  [TEXTE] rapport_analyse.txt")
        print("\n" + "=" * 80)
        print()


# Point d'entrée principal
if __name__ == "__main__":
    try:
        # Créer l'instance et lancer l'analyse
        analyseur = AnalyseTextMining(dossier=".")
        analyseur.executer_analyse_complete()
        
        print("[OK] Vous pouvez maintenant consulter les resultats!")
        print("   -> Ouvrez les fichiers Excel pour voir les tableaux")
        print("   -> Ouvrez les images PNG pour voir les visualisations")
        print("   -> Lisez le rapport_analyse.txt pour l'interpretation detaillee")
        
    except Exception as e:
        print(f"\n[ERREUR]: {e}")
        import traceback
        traceback.print_exc()

