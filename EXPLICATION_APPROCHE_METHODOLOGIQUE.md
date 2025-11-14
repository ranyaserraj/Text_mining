# 🎓 EXPLICATION APPROCHE MÉTHODOLOGIQUE DU PROJET

## 📌 Type de Problème : **Topic Mining + Sentiment Analysis**

### Ce projet est principalement :
- ✅ **Topic Mining** (Extraction de thèmes/sujets)
- ✅ **Sentiment Analysis** (Analyse de sentiment)
- ✅ **Co-occurrence Analysis** (Analyse des associations de concepts)

### Ce projet N'EST PAS :
- ❌ **Classification supervisée** (pas d'entraînement de modèle ML)
- ❌ **Clustering** (pas de regroupement non supervisé de documents)
- ❌ **Topic Modeling probabiliste** (pas de LDA, LSA, NMF)

---

## 🔍 ANALYSE DÉTAILLÉE DE L'APPROCHE

### 1️⃣ **TOPIC MINING (Extraction de Thèmes)**

#### **Type d'approche : Rule-Based / Keyword-Based**

**Principe :**
- Définition **manuelle** d'une liste de mots-clés par thème
- Comptage des occurrences dans le texte
- Pas d'apprentissage automatique

**Code correspondant :**
```python
self.themes_keywords = {
    'Emploi': ['emploi', 'travail', 'chômage', 'recrutement', 'stage', ...],
    'Santé': ['santé', 'médical', 'hôpital', 'médecin', ...],
    'Économie': ['économie', 'croissance', 'investissement', ...],
    # ... 14 thèmes au total
}
```

**Algorithme utilisé :**
```
Pour chaque parti:
    Pour chaque thème:
        compteur = 0
        Pour chaque mot du texte:
            Si mot in mots_clés_du_thème:
                compteur += 1
        Sauvegarder (parti, thème, compteur)
```

**Complexité : O(n × m × k)**
- n = nombre de mots
- m = nombre de thèmes
- k = nombre de mots-clés par thème

---

### 2️⃣ **SENTIMENT ANALYSIS (Analyse de Sentiment)**

#### **Type d'approche : Lexicon-Based Sentiment Analysis**

**Principe :**
- Dictionnaires de mots pré-définis (positif, négatif, neutre)
- Comptage des occurrences
- Calcul d'un score de polarité

**Code correspondant :**
```python
self.mots_positifs = [
    'développer', 'améliorer', 'renforcer', 'garantir', 'créer',
    'succès', 'efficace', 'moderniser', ...
]

self.mots_negatifs = [
    'crise', 'problème', 'échec', 'corruption', 'pauvreté',
    'inégalité', 'déficit', ...
]

self.mots_neutres = [
    'analyser', 'observer', 'constater', 'identifier', ...
]
```

**Formule du score :**
```python
score = (positifs - négatifs) / (positifs + négatifs + neutres)
```

**Algorithme utilisé :**
```
Pour chaque parti:
    positifs = 0
    négatifs = 0
    neutres = 0
    
    Pour chaque mot du texte:
        Si mot in mots_positifs: positifs += 1
        Si mot in mots_négatifs: négatifs += 1
        Si mot in mots_neutres: neutres += 1
    
    score = (positifs - négatifs) / total
    
    Si score > 0.1: ton = "Positif"
    Si score < -0.1: ton = "Négatif"
    Sinon: ton = "Neutre"
```

**Complexité : O(n × (p + g + u))**
- n = nombre de mots
- p, g, u = taille des dictionnaires positif/négatif/neutre

---

### 3️⃣ **CO-OCCURRENCE ANALYSIS (Analyse des Associations)**

#### **Type d'approche : Sliding Window + Graph-Based**

**Principe :**
- Découper le texte en fenêtres de N mots
- Identifier les thèmes présents dans chaque fenêtre
- Compter les paires de thèmes qui apparaissent ensemble

**Code correspondant :**
```python
window_size = 50  # Taille de la fenêtre
overlap = 50%     # Chevauchement

for i in range(0, len(words), window_size // 2):
    segment = words[i:i+window_size]
    
    # Détecter thèmes dans ce segment
    themes_dans_segment = []
    for theme in themes:
        if any(keyword in segment for keyword in theme_keywords):
            themes_dans_segment.append(theme)
    
    # Compter co-occurrences
    for theme1, theme2 in combinations(themes_dans_segment, 2):
        cooccurrences[(theme1, theme2)] += 1
```

**Algorithme : Sliding Window**
```
┌─────────────────┐
│   Fenêtre 1     │ [mots 0-49]
└─────────────────┘
     ┌─────────────────┐
     │   Fenêtre 2     │ [mots 25-74] (overlap 50%)
     └─────────────────┘
          ┌─────────────────┐
          │   Fenêtre 3     │ [mots 50-99]
          └─────────────────┘
```

**Pourquoi l'overlap ?**
Pour ne pas "couper" des relations entre thèmes qui sont à cheval sur 2 fenêtres

**Complexité : O(w × t²)**
- w = nombre de fenêtres ≈ n / (window_size/2)
- t = nombre de thèmes présents par fenêtre

---

### 4️⃣ **LEMMATISATION (Prétraitement Linguistique)**

#### **Type d'approche : Morphological Analysis avec NLP**

**Principe :**
- Utilisation de spaCy avec modèle pré-entraîné `fr_core_news_sm`
- Analyse morphologique pour trouver la forme de base (lemme)

**Code correspondant :**
```python
nlp = spacy.load("fr_core_news_sm")  # Modèle pré-entraîné

doc = nlp(texte)  # Traitement du texte

for token in doc:
    if not token.is_stop and len(token.lemma_) > 2:
        lemmes.append(token.lemma_.lower())
```

**Ce que fait spaCy en interne :**
1. **Tokenisation** : Découpe en tokens
2. **POS Tagging** : Identification grammaticale (verbe, nom, adjectif...)
3. **Dependency Parsing** : Analyse syntaxique
4. **Lemmatisation** : Application de règles morphologiques

**Algorithme utilisé par spaCy :**
- **Look-up table** : Dictionnaire de lemmes
- **Règles morphologiques** : Pour les formes régulières
- **Machine Learning** : Modèle entraîné sur corpus français

**Exemple de transformation :**
```
"développons" (verbe, 1ère personne pluriel)
    ↓ [analyse morphologique]
"développer" (infinitif = lemme)
```

---

## 🎯 COMPARAISON AVEC D'AUTRES APPROCHES

### **Classification (Supervisée) ❌ PAS utilisée**

**Ce serait :**
```python
# Entraînement
model = NaiveBayes()
model.fit(X_train, y_train)  # Nécessite des données étiquetées

# Prédiction
y_pred = model.predict(X_test)
```

**Pourquoi pas utilisé :**
- Nécessite des données d'entraînement étiquetées
- Objectif différent (prédire une classe vs extraire des thèmes)

---

### **Clustering (Non-supervisé) ❌ PAS utilisé**

**Ce serait :**
```python
# K-Means par exemple
kmeans = KMeans(n_clusters=4)
clusters = kmeans.fit_predict(document_vectors)

# Résultat : groupe de documents similaires
```

**Pourquoi pas utilisé :**
- On a seulement 4 documents (trop peu)
- Objectif différent (grouper vs analyser le contenu)

---

### **Topic Modeling Probabiliste ❌ PAS utilisé**

**Ce serait (LDA - Latent Dirichlet Allocation) :**
```python
# LDA
lda = LatentDirichletAllocation(n_components=10)
lda.fit(document_term_matrix)

# Résultat : distribution de probabilité sur les topics
```

**Pourquoi pas utilisé :**
- LDA découvre des topics de manière non supervisée
- Notre approche utilise des thèmes prédéfinis (plus contrôlé)
- LDA nécessite plus de documents

---

## 📊 NOTRE APPROCHE : **RULE-BASED TEXT MINING**

### **Avantages ✅**

1. **Interprétabilité**
   - On sait exactement pourquoi un thème est détecté
   - Traçable : "Emploi détecté car 'travail' apparaît 10 fois"

2. **Contrôle total**
   - On définit les thèmes qui nous intéressent
   - On peut ajuster les mots-clés facilement

3. **Pas de données d'entraînement nécessaires**
   - Pas besoin de corpus étiqueté
   - Fonctionne immédiatement

4. **Reproductible**
   - Mêmes entrées → mêmes sorties
   - Pas de variabilité due à l'initialisation aléatoire

5. **Rapide**
   - Pas d'entraînement de modèle ML
   - Exécution en quelques secondes

### **Limitations ⚠️**

1. **Dépendance aux mots-clés**
   - Si un mot-clé manque, le thème est sous-estimé
   - Nécessite expertise du domaine

2. **Pas de sémantique profonde**
   - "banque" (finance) vs "banque" (siège) → même mot
   - Pas de compréhension du contexte avancée

3. **Mots hors vocabulaire**
   - Nouveaux termes non couverts par les dictionnaires

4. **Scalabilité limitée**
   - Pour des milliers de thèmes, approche manuelle difficile

---

## 🧠 ALGORITHMES ET STRUCTURES DE DONNÉES UTILISÉS

### **1. Bag of Words (BoW)**
```python
# Représentation simplifiée
texte = "emploi emploi santé emploi"
bow = {"emploi": 3, "santé": 1}
```

**Complexité :** O(n) pour construire le BoW

---

### **2. Pattern Matching (Recherche de motifs)**
```python
if keyword in text:
    count += 1
```

**Algorithme sous-jacent :** Boyer-Moore ou Knuth-Morris-Pratt (Python)
**Complexité moyenne :** O(n) par recherche

---

### **3. Counter (Comptage de fréquences)**
```python
from collections import Counter
word_freq = Counter(words)
# word_freq = {'emploi': 29, 'santé': 18, ...}
```

**Structure :** Hash table
**Complexité :** O(1) pour insertion, O(n) pour parcours

---

### **4. Sliding Window (Fenêtre glissante)**
```python
for i in range(0, len(words), step):
    window = words[i:i+window_size]
    process(window)
```

**Complexité :** O(n / step)

---

### **5. Combinations (Génération de paires)**
```python
from itertools import combinations
themes = ['A', 'B', 'C']
pairs = list(combinations(themes, 2))
# [(A,B), (A,C), (B,C)]
```

**Complexité :** O(n²) pour n thèmes dans une fenêtre

---

## 📐 FORMULES MATHÉMATIQUES DÉTAILLÉES

### **1. Score de Sentiment**
```
S = (P - N) / (P + N + U)

Où :
- P = nombre de mots positifs
- N = nombre de mots négatifs
- U = nombre de mots neutres
- S ∈ [-1, 1]
```

**Interprétation :**
- S > 0.1 → Discours positif/propositif
- S ∈ [-0.1, 0.1] → Neutre/équilibré
- S < -0.1 → Négatif/critique

---

### **2. Normalisation (pour graphique radar)**
```
Valeur_normalisée = (Valeur / Max_global) × 100

Exemple :
PI : 116 mentions Économie (max absolu)
PAM : 13 mentions Économie
Normalisé PAM = (13/116) × 100 = 11.2%
```

---

### **3. Fréquence relative (mentions par 1000 mots)**
```
Freq_relative = (Nb_mentions / Total_mots) × 1000

Exemple PAM :
Emploi : 23 mentions / 535 lemmes × 1000 = 43 mentions/1000 mots
```

---

### **4. Co-occurrence strength (force de co-occurrence)**
```
Strength(A, B) = Nb_fenêtres_contenant_(A et B)

Exemple :
Emploi ↔ Social : 20 co-occurrences
→ Ces thèmes apparaissent ensemble dans 20 fenêtres
```

---

## 🔬 PIPELINE ALGORITHMIQUE DÉTAILLÉ

```
┌──────────────────────────────────────────────────┐
│  1. CHARGEMENT                                   │
│     Algorithme : File I/O                        │
│     Complexité : O(n) où n = taille fichier     │
└──────────────────────────────────────────────────┘
                    ↓
┌──────────────────────────────────────────────────┐
│  2. PRÉTRAITEMENT                                │
│     a) Nettoyage (Regex)         O(n)           │
│     b) Lemmatisation (spaCy)     O(n)           │
│     c) Stopwords (HashSet)       O(n)           │
└──────────────────────────────────────────────────┘
                    ↓
┌──────────────────────────────────────────────────┐
│  3. EXTRACTION THÉMATIQUE                        │
│     Algorithme : Pattern Matching               │
│     Pour chaque thème × chaque mot              │
│     Complexité : O(n × m × k)                   │
│     n=mots, m=thèmes, k=keywords/thème          │
└──────────────────────────────────────────────────┘
                    ↓
┌──────────────────────────────────────────────────┐
│  4. SENTIMENT ANALYSIS                           │
│     Algorithme : Dictionary Lookup              │
│     Complexité : O(n × d)                       │
│     n=mots, d=taille dictionnaires              │
└──────────────────────────────────────────────────┘
                    ↓
┌──────────────────────────────────────────────────┐
│  5. CO-OCCURRENCE                                │
│     Algorithme : Sliding Window + Combinations  │
│     Complexité : O(w × t²)                      │
│     w=fenêtres, t=thèmes/fenêtre                │
└──────────────────────────────────────────────────┘
                    ↓
┌──────────────────────────────────────────────────┐
│  6. AGRÉGATION                                   │
│     Algorithme : GroupBy + Count                │
│     Complexité : O(n log n)                     │
└──────────────────────────────────────────────────┘
                    ↓
┌──────────────────────────────────────────────────┐
│  7. VISUALISATION                                │
│     Matplotlib/Seaborn rendering                │
│     Complexité : O(p × t)                       │
│     p=partis, t=thèmes                          │
└──────────────────────────────────────────────────┘
```

**Complexité totale : O(n × m × k) dominante**

---

## 🎯 CLASSIFICATION DU PROJET

### **Domaine académique :**
- 📚 **Natural Language Processing (NLP)**
- 📊 **Text Mining / Text Analytics**
- 🔍 **Information Extraction**

### **Sous-domaines spécifiques :**
- Topic Detection (Rule-Based)
- Sentiment Analysis (Lexicon-Based)
- Text Preprocessing (Lemmatization)
- Co-occurrence Analysis

### **Niveau de complexité :**
- 🎓 **Niveau universitaire** : Licence 3 / Master 1
- 💼 **Applications professionnelles** : Analyse de discours, veille stratégique

---

## 💡 POURQUOI CETTE APPROCHE POUR CE PROJET ?

### **Contexte :**
- 4 textes de discours politiques
- Objectif : Comparer les thématiques et le ton
- Besoin d'interprétabilité

### **Justification :**

✅ **Rule-Based convient car :**
1. Petit corpus (4 documents)
2. Thèmes bien définis (politique marocaine)
3. Besoin de contrôle et traçabilité
4. Pas de données d'entraînement disponibles
5. Exécution rapide nécessaire

❌ **ML/Deep Learning serait excessif car :**
1. Trop peu de données
2. Risque de surapprentissage
3. Complexité non nécessaire
4. Temps d'entraînement inutile
5. Perte d'interprétabilité

---

## 📈 COMPARAISON PERFORMANCE

### **Notre approche (Rule-Based) :**
- ⏱️ Temps d'exécution : **~4 secondes**
- 💾 Mémoire : **<100 MB**
- 🎯 Précision : **Dépend de la qualité des mots-clés**
- 🔄 Reproductibilité : **100%**

### **Approche ML (si on l'utilisait) :**
- ⏱️ Entraînement : **Minutes à heures**
- 💾 Mémoire : **Plusieurs GB**
- 🎯 Précision : **Potentiellement meilleure avec beaucoup de données**
- 🔄 Reproductibilité : **Variable (initialisation aléatoire)**

---

## 🎓 RÉSUMÉ ACADÉMIQUE

### **Type de problème :**
**Text Mining avec approche Rule-Based**

### **Techniques principales :**
1. **Topic Detection** : Keyword-based matching
2. **Sentiment Analysis** : Lexicon-based scoring
3. **Co-occurrence Analysis** : Sliding window + graph
4. **Lemmatization** : Morphological analysis (spaCy)

### **Algorithmes utilisés :**
1. Pattern Matching (O(n))
2. Bag of Words (O(n))
3. Sliding Window (O(n/step))
4. Dictionary Lookup (O(1) avg)
5. Combinations (O(t²))

### **Pas de Machine Learning supervisé**
- Pas d'entraînement de modèle
- Pas de classification automatique
- Pas de clustering

### **Avantage principal :**
✅ **Interprétabilité et contrôle total**

---

## 📚 POUR ALLER PLUS LOIN

### **Améliorations possibles avec ML :**

1. **Named Entity Recognition (NER)**
   - Extraire automatiquement les noms (personnes, lieux)
   - Bibliothèque : spaCy NER, BERT-NER

2. **Topic Modeling automatique**
   - LDA (Latent Dirichlet Allocation)
   - NMF (Non-negative Matrix Factorization)

3. **Sentiment Analysis avancé**
   - Modèles pré-entraînés (CamemBERT pour français)
   - Deep Learning (LSTM, Transformer)

4. **Word Embeddings**
   - Word2Vec, GloVe, FastText
   - Similarité sémantique

5. **Classification supervisée**
   - Si on avait beaucoup de discours étiquetés
   - SVM, Random Forest, Neural Networks

---

## 🎯 CONCLUSION

**Ce projet est un excellent exemple de :**
- ✅ **Text Mining Rule-Based** efficace et interprétable
- ✅ **Analyse de sentiment lexicale** avec dictionnaires
- ✅ **Extraction de thèmes** par mots-clés
- ✅ **Prétraitement NLP** avec lemmatisation

**Ce n'est PAS :**
- ❌ De la classification supervisée (pas de ML)
- ❌ Du clustering (pas de regroupement)
- ❌ Du topic modeling probabiliste (pas de LDA)

**Approche parfaitement adaptée** pour :
- Petit corpus
- Thèmes prédéfinis
- Besoin d'interprétabilité
- Exécution rapide

---

**En résumé : Une approche pragmatique et efficace pour l'analyse de discours politiques ! 🚀**

