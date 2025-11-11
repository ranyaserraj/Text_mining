# 📚 TECHNIQUES DE TEXT MINING UTILISÉES

## Vue d'Ensemble

Ce projet utilise **5 grandes familles de techniques** de text mining pour analyser les discours politiques.

---

## 1️⃣ PRÉTRAITEMENT (NLP - Natural Language Processing)

### **a) Tokenisation**
**Quoi :** Découper le texte en unités individuelles (mots)
```python
"L'emploi est prioritaire" → ["L'", "emploi", "est", "prioritaire"]
```

**Pourquoi :** Pour analyser chaque mot séparément

---

### **b) Normalisation**
**Quoi :** Mettre tout en minuscules
```python
"EMPLOI" → "emploi"
"Emploi" → "emploi"
```

**Pourquoi :** Pour que "Emploi" et "emploi" soient considérés comme le même mot

---

### **c) Nettoyage**
**Quoi :** Supprimer les éléments inutiles
- Ponctuation : `. , ! ? ; :`
- Chiffres : `2021, 1500, 67`
- Caractères spéciaux

**Pourquoi :** Ces éléments n'apportent pas de sens pour l'analyse thématique

---

### **d) Suppression des Stopwords**
**Quoi :** Retirer les mots vides qui n'ont pas de signification
```python
Stopwords : le, la, les, un, une, de, du, et, ou, dans, pour...
```

**Exemple :**
```
AVANT : "le parti propose une solution pour l'emploi"
APRÈS : "parti propose solution emploi"
```

**Pourquoi :** Se concentrer sur les mots porteurs de sens

---

## 2️⃣ ANALYSE THÉMATIQUE (Topic Detection)

### **a) Classification par Mots-Clés**
**Quoi :** Identifier les thèmes en cherchant des mots-clés spécifiques

**Exemple - Thème "Emploi" :**
```python
mots_clés = ["emploi", "travail", "chômage", "recrutement", "stage"]
```

**Comment ça marche :**
1. Pour chaque thème, on a une liste de mots-clés
2. On compte combien de fois ces mots apparaissent dans le texte
3. On classe les thèmes par nombre d'occurrences

**Résultat :**
```
PAM : Emploi (29 mentions) → Thème principal
```

---

### **b) Extraction de Fréquences**
**Quoi :** Compter la fréquence d'apparition de chaque thème

**Formule simple :**
```
Fréquence(Thème) = Σ occurrences de tous les mots-clés du thème
```

**Exemple :**
```
Thème Santé pour PAM:
- "santé" : 8 fois
- "médical" : 3 fois
- "hôpital" : 5 fois
→ Total : 16 mentions
```

---

## 3️⃣ ANALYSE DE SENTIMENT (Sentiment Analysis)

### **a) Classification Lexicale**
**Quoi :** Classer les mots selon leur connotation

**3 catégories :**

**Positif :**
```python
["améliorer", "renforcer", "développer", "garantir", "créer", "succès"]
```

**Négatif :**
```python
["crise", "échec", "corruption", "problème", "déficit", "pauvreté"]
```

**Neutre :**
```python
["analyser", "observer", "constater", "identifier", "évaluer"]
```

---

### **b) Calcul de Score**
**Formule :**
```python
Score = (Positifs - Négatifs) / (Positifs + Négatifs + Neutres)
```

**Exemple PAM :**
```
Positifs : 30
Négatifs : 3
Neutres : 1
Score = (30 - 3) / (30 + 3 + 1) = 27/34 = 0.79
```

**Interprétation :**
- Score > 0.1 → Ton **Positif** (propositions)
- Score -0.1 à 0.1 → Ton **Neutre**
- Score < -0.1 → Ton **Négatif** (critiques)

---

## 4️⃣ ANALYSE DE CO-OCCURRENCE (Co-occurrence Analysis)

### **Quoi :** Identifier quels thèmes sont mentionnés ensemble

### **Comment ça marche :**

**Étape 1 :** Découper en segments
```
Texte = "...emploi...social...développement..."
→ Segment 1 (50 mots) : emploi + social + économie
→ Segment 2 (50 mots) : social + santé + éducation
```

**Étape 2 :** Détecter les thèmes dans chaque segment
```
Segment 1 contient : [Emploi, Social, Économie]
```

**Étape 3 :** Compter les paires
```
(Emploi, Social) → +1
(Emploi, Économie) → +1
(Social, Économie) → +1
```

**Résultat :**
```
PAM : Emploi ↔ Social = 13 co-occurrences
→ Ces deux thèmes sont souvent mentionnés ensemble
```

---

### **Paramètres utilisés :**
- **Taille de fenêtre :** 50 mots
- **Overlap :** 50% (25 mots se chevauchent entre segments)

**Pourquoi l'overlap ?**
Pour ne pas "couper" des liens entre thèmes qui sont à cheval sur 2 segments

---

## 5️⃣ VISUALISATION DE DONNÉES (Data Visualization)

### **a) Graphiques à Barres**
**Technique :** Matplotlib Bar Chart
**Usage :** Comparer l'importance de chaque thème par parti

---

### **b) Heatmap (Carte de Chaleur)**
**Technique :** Seaborn Heatmap
**Usage :** Visualiser l'intensité de tous les thèmes pour tous les partis simultanément

**Principe :**
- Couleur claire → Faible mention
- Couleur foncée → Forte mention

---

### **c) Nuage de Mots (Word Cloud)**
**Technique :** WordCloud Algorithm
**Usage :** Visualiser les mots les plus fréquents

**Principe :**
- Taille du mot ∝ Fréquence d'apparition
- Les mots les plus grands = les plus importants

---

### **d) Graphique Radar/Spider**
**Technique :** Polar Projection Chart
**Usage :** Comparer plusieurs partis sur plusieurs dimensions

**Principe :**
1. Chaque axe = un thème
2. Distance du centre = intensité (0-100)
3. Relier les points → forme géométrique
4. Surface de la forme = complétude thématique

**Lecture :**
- Grande surface → Discours complet
- Forme ronde → Équilibre
- Pics marqués → Spécialisation

---

## 🔬 TECHNIQUES STATISTIQUES UTILISÉES

### **1. Normalisation**
**Formule :**
```python
Valeur_normalisée = (Valeur / Max) × 100
```

**Pourquoi :** Pour comparer des partis avec des longueurs de discours différentes

**Exemple :**
```
PI : 141 mentions d'Économie (max absolu)
PAM : 14 mentions d'Économie
Normalisé : PAM = (14/141) × 100 = 10/100
```

---

### **2. Comptage de Fréquences**
**Technique :** Bag of Words (BoW) simplifié

**Principe :**
- On ignore l'ordre des mots
- On compte juste combien de fois chaque mot apparaît

**Exemple :**
```
"emploi emploi santé emploi" → {"emploi": 3, "santé": 1}
```

---

### **3. Filtrage par Seuil**
**Technique :** Threshold Filtering

**Principe :** Garder uniquement ce qui est significatif

**Critères appliqués :**
- Mots de longueur > 2 caractères
- Thèmes avec au moins 1 mention
- Top 10 pour les visualisations

---

## 📊 MÉTRIQUES CALCULÉES

### **1. Densité Thématique**
```
Densité = Nombre de mentions / Nombre total de mots
```

**Exemple PAM :**
```
Emploi : 29 mentions / 556 mots = 5.2%
```

---

### **2. Ratio Positif/Négatif**
```
Ratio = Mots_Positifs / Mots_Négatifs
```

**Exemple PAM :**
```
30 / 3 = 10:1 (très positif)
```

---

### **3. Taux de Couverture Thématique**
```
Couverture = Nombre de thèmes traités / Total thèmes possibles
```

**Exemple PI :**
```
13 thèmes / 14 possibles = 92.9%
```

---

## 🎯 ALGORITHMES UTILISÉS

### **1. Recherche de Motifs (Pattern Matching)**
**Algorithme :** Substring Search
**Complexité :** O(n×m) où n=longueur texte, m=longueur mot-clé

---

### **2. Fenêtre Glissante (Sliding Window)**
**Usage :** Pour l'analyse de co-occurrence
```python
for i in range(0, len(mots), step):
    segment = mots[i:i+window_size]
    analyser(segment)
```

---

### **3. Agrégation de Données (Data Aggregation)**
**Technique :** GroupBy + Count
```python
themes_par_parti = {
    'PAM': {'Emploi': 29, 'Social': 26},
    'PI': {'Économie': 141, 'Social': 79}
}
```

---

## 📐 FORMULES MATHÉMATIQUES CLÉS

### **1. Score de Sentiment**
```
S = (P - N) / (P + N + U)
```
où P=Positif, N=Négatif, U=Neutre

---

### **2. Normalisation Min-Max**
```
X_norm = (X - X_min) / (X_max - X_min) × 100
```

---

### **3. Fréquence Relative**
```
F_rel = (Occurrences_thème / Total_mots) × 1000
```

---

## 🛠️ OUTILS ET BIBLIOTHÈQUES

### **Python 3.12**
Langage de programmation

### **Pandas**
- Manipulation de données tabulaires
- DataFrames pour organiser les résultats

### **NumPy**
- Calculs mathématiques
- Normalisation des valeurs

### **Matplotlib**
- Graphiques à barres
- Graphiques radar

### **Seaborn**
- Heatmap
- Styling des graphiques

### **WordCloud**
- Génération des nuages de mots

### **Collections (defaultdict, Counter)**
- Comptage efficace
- Stockage de fréquences

### **Itertools (combinations)**
- Génération de paires pour co-occurrence

### **Re (Regular Expressions)**
- Nettoyage du texte
- Recherche de motifs

---

## 🎓 CONCEPTS CLÉS DU TEXT MINING

### **1. Corpus**
L'ensemble des textes analysés (4 discours)

### **2. Document**
Un texte individuel (1 discours par parti)

### **3. Token**
Une unité de texte (un mot après tokenisation)

### **4. Vocabulaire**
L'ensemble unique de tous les mots

### **5. TF (Term Frequency)**
Fréquence d'un terme dans un document

### **6. Feature**
Une caractéristique mesurable (ex: nombre de mots positifs)

---

## 📈 PIPELINE D'ANALYSE

```
Texte brut
    ↓
1. PRÉTRAITEMENT
   - Tokenisation
   - Normalisation
   - Nettoyage
   - Stopwords
    ↓
2. EXTRACTION
   - Thèmes
   - Sentiments
   - Co-occurrences
    ↓
3. AGRÉGATION
   - Comptages
   - Calculs de scores
   - Normalisation
    ↓
4. VISUALISATION
   - Graphiques
   - Tableaux
   - Rapports
    ↓
Résultats finaux
```

---

## 💡 POURQUOI CES TECHNIQUES ?

### **Prétraitement**
✅ Nécessaire pour que l'ordinateur "comprenne" le texte
✅ Réduit le bruit et se concentre sur l'essentiel

### **Analyse Thématique**
✅ Identifie automatiquement les priorités
✅ Permet la comparaison objective

### **Analyse de Sentiment**
✅ Mesure le ton (positif/négatif)
✅ Révèle l'approche (critique vs propositif)

### **Co-occurrence**
✅ Révèle les liens conceptuels
✅ Montre comment les thèmes s'articulent

### **Visualisation**
✅ Rend les données compréhensibles
✅ Facilite la comparaison

---

## 🎯 AVANTAGES DE CETTE APPROCHE

### ✅ **Objectivité**
Pas d'interprétation subjective, juste des chiffres

### ✅ **Reproductibilité**
Même analyse = mêmes résultats

### ✅ **Scalabilité**
Fonctionne avec 4 textes ou 400

### ✅ **Exhaustivité**
Analyse tout le texte, pas juste des extraits

### ✅ **Rapidité**
4 secondes vs plusieurs heures manuellement

---

## 📚 LIMITATIONS

### ⚠️ **Contexte**
Les mots isolés perdent parfois leur contexte

### ⚠️ **Nuances**
L'ironie ou le sarcasme sont difficiles à détecter

### ⚠️ **Mots-clés**
Dépend de la qualité de la liste de mots-clés

### ⚠️ **Langue**
Optimisé pour le français, nécessite adaptation pour d'autres langues

---

## 🚀 AMÉLIORATIONS POSSIBLES

### **1. TF-IDF**
Pondérer les mots par leur rareté
```
TF-IDF = Fréquence × log(N_documents / N_documents_contenant_mot)
```

### **2. N-grams**
Analyser des groupes de mots (bi-grams, tri-grams)
```
"nouveau modèle" = 1 token au lieu de 2
```

### **3. Word Embeddings**
Utiliser des vecteurs de mots (Word2Vec, GloVe)

### **4. Machine Learning**
Entraîner des modèles de classification automatiques

### **5. Named Entity Recognition (NER)**
Extraire automatiquement les noms (personnes, lieux, organisations)

---

## 📊 RÉSUMÉ DES TECHNIQUES

| Technique | Objectif | Complexité |
|-----------|----------|------------|
| Tokenisation | Découper en mots | Faible |
| Stopwords | Filtrer mots vides | Faible |
| Fréquences | Compter occurrences | Moyenne |
| Sentiment | Mesurer le ton | Moyenne |
| Co-occurrence | Trouver liens | Élevée |
| Visualisation | Présenter résultats | Moyenne |

---

## 🎓 CONCEPTS AVANCÉS APPLIQUÉS

### **Sliding Window avec Overlap**
Améliore la détection de co-occurrence aux frontières

### **Normalisation Multi-échelle**
Permet la comparaison de textes de longueurs différentes

### **Projection Polaire**
Visualisation radar pour comparaisons multidimensionnelles

### **Agrégation Hiérarchique**
Organisation des résultats par parti → thème → sous-thème

---

## 💻 COMPLEXITÉ ALGORITHMIQUE

### **Prétraitement**
O(n) où n = nombre de mots

### **Analyse Thématique**
O(n × m) où m = nombre de mots-clés par thème

### **Co-occurrence**
O(w × t²) où w = nombre de fenêtres, t = nombre de thèmes

### **Visualisation**
O(p × t) où p = nombre de partis

**Complexité totale :** O(n × m) dominante

---

## 🎯 EN RÉSUMÉ

Ce projet utilise **5 techniques principales** :

1. **Prétraitement NLP** → Nettoyer et préparer
2. **Analyse Thématique** → Identifier les sujets
3. **Analyse de Sentiment** → Mesurer le ton
4. **Co-occurrence** → Trouver les liens
5. **Visualisation** → Présenter les résultats

**Toutes ces techniques ensemble** permettent une analyse **complète, objective et visuelle** des discours politiques !

---

**Temps d'exécution total :** ~4 secondes
**Lignes de code :** 774 lignes Python
**Résultats :** 14 fichiers générés

🎉 **Une analyse qui prendrait des jours manuellement, réalisée en quelques secondes !**

