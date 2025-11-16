# 🤖 Text Mining avec Machine Learning - VERSION AVANCÉE

## Analyse des Discours Politiques Marocains

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![ML](https://img.shields.io/badge/Machine_Learning-Supervisé_%26_Non--Supervisé-green)](#)
[![BERT](https://img.shields.io/badge/BERT-Transformers-orange)](https://huggingface.co/nlptown/bert-base-multilingual-uncased-sentiment)
[![Scikit-learn](https://img.shields.io/badge/Scikit--learn-1.3%2B-yellow)](https://scikit-learn.org/)

---

## 🎯 Objectif du Projet

Ce projet analyse automatiquement les discours de 4 partis politiques marocains (PAM, PI, PJD, RNI) en utilisant **4 techniques** de Machine Learning complémentaires :

1. **Classification Rule-Based** (Baseline) - Analyse de sentiment par dictionnaire
2. **Classification Supervisée** (BERT) - Deep Learning pour sentiment
3. **Classification Non-Supervisée** (K-means) - Clustering automatique
4. **Topic Modeling Non-Supervisé** (LDA) - Découverte de thèmes

---

## 🆕 NOUVEAUTÉS par rapport à la version de base

### **✅ Ajouts majeurs :**

| Feature | Version Base | Version ML |
|---------|-------------|------------|
| **Méthodes d'analyse** | 1 (Rule-Based) | **4 (Rule + 3 ML)** |
| **Sentiment Analysis** | Lexicon seul | **Lexicon + BERT** |
| **Thèmes** | Dictionnaire manuel | **Manuel + LDA automatique** |
| **Clustering** | ❌ | **✅ K-means** |
| **Deep Learning** | ❌ | **✅ BERT/Transformers** |
| **Comparaisons** | ❌ | **✅ Rule-Based vs ML** |
| **Niveau technique** | Intermédiaire | **Avancé/Master** |

---

## 📊 Architecture du Système

```
┌─────────────────────────────────────────────────────────────────┐
│                    PIPELINE D'ANALYSE ML                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  📄 TEXTES BRUTS (4 partis)                                     │
│       ↓                                                         │
│  🔧 PRÉTRAITEMENT                                               │
│     - Nettoyage                                                 │
│     - Lemmatisation (spaCy)                                    │
│     - Réduction ~50%                                            │
│       ↓                                                         │
│  ┌──────────────────────┐  ┌──────────────────────┐           │
│  │  ANALYSE SENTIMENT   │  │  ANALYSE THÉMATIQUE  │           │
│  └──────────────────────┘  └──────────────────────┘           │
│           ↓                          ↓                          │
│  ┌──────────────┬──────────┬──────────┬──────────┐            │
│  │              │          │          │          │            │
│  │ 1. Lexicon   │ 2. BERT  │3. K-means│  4. LDA  │            │
│  │ (Rule-Based) │(Supervisé│(Cluster) │ (Topics) │            │
│  │              │          │          │          │            │
│  │  ⚡ Rapide   │ 🎯 Précis│ 🔍 Patterns│ 📚 Thèmes│            │
│  │  ⏱️ 1 sec    │ ⏱️ 2 min │ ⏱️ 3 sec  │ ⏱️ 10 sec │            │
│  │              │          │          │          │            │
│  └──────────────┴──────────┴──────────┴──────────┘            │
│           ↓         ↓          ↓          ↓                    │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │  📊 COMPARAISONS & VISUALISATIONS                        │ │
│  │  - Sentiment : Rule-Based vs BERT                        │ │
│  │  - Clusters : Distribution par parti                     │ │
│  │  - Topics : Top thèmes LDA                               │ │
│  └──────────────────────────────────────────────────────────┘ │
│           ↓                                                     │
│  📈 RÉSULTATS                                                   │
│     - 3 graphiques PNG                                          │
│     - 1 rapport texte détaillé                                  │
│     - 1 tableau Excel comparatif                                │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🔬 Méthodes de Machine Learning

### **1. Rule-Based Sentiment Analysis (Baseline)**

```python
Type : Classification basée sur règles
Algorithme : Lexicon-Based
Complexité : O(n × m)
Temps : ⚡⚡⚡⚡⚡ (<1 seconde)

Fonctionnement :
- Dictionnaires de mots positifs/négatifs/neutres
- Score = (Positifs - Négatifs) / Total
- Classification : Positif / Négatif / Neutre
```

**Avantages :** Rapide, interprétable, pas de dépendances ML  
**Inconvénients :** Ne comprend pas le contexte, dépend des dictionnaires

---

### **2. BERT Sentiment Analysis (Supervisé)**

```python
Type : Classification SUPERVISÉE (Deep Learning)
Modèle : BERT multilingual (110M paramètres)
Approche : Transfer Learning
Complexité : O(n × d²) où d=768
Temps : ⚡ (~2-3 minutes CPU, ~10s GPU)

Fonctionnement :
- Modèle pré-entraîné sur millions de reviews
- Tokenization + 12 Transformer layers
- Output : 5 classes (1-5 stars)
- Conversion en score (-1 à +1)
```

**Avantages :** État de l'art, comprend le contexte, très précis  
**Inconvénients :** Lent, boîte noire, nécessite RAM (>2GB)

---

### **3. K-means Clustering (Non-Supervisé)**

```python
Type : Classification NON-SUPERVISÉE
Algorithme : K-means avec TF-IDF
Représentation : TF-IDF vectors
Complexité : O(n × K × i × d)
Temps : ⚡⚡⚡ (~3 secondes)

Fonctionnement :
- Vectorisation TF-IDF des segments
- K-means pour regrouper segments similaires
- 5 clusters découverts automatiquement
- Évaluation : Silhouette Score
```

**Avantages :** Découvre patterns automatiquement, rapide, interprétable  
**Inconvénients :** Nécessite choisir K, sensible à l'initialisation

---

### **4. LDA Topic Modeling (Non-Supervisé)**

```python
Type : Classification NON-SUPERVISÉE
Algorithme : Latent Dirichlet Allocation (LDA)
Approche : Modèle probabiliste génératif
Complexité : O(K × V × D × I)
Temps : ⚡⚡ (~10 secondes)

Fonctionnement :
- Modèle : Chaque doc = mélange de topics
- Chaque topic = distribution de mots
- Inférence : Variational Bayes
- Découvre 10 thèmes automatiquement
```

**Avantages :** Découverte automatique de thèmes, interprétable, standard académique  
**Inconvénients :** Non-déterministe, nécessite choisir nombre de topics

---

## 📦 Installation

### **Prérequis :**
- Python 3.8+
- pip
- 4 GB RAM minimum (8 GB recommandé pour BERT)
- CPU ou GPU (CUDA pour accélérer BERT)

### **1. Cloner le repository :**

```bash
git clone https://github.com/ranyaserraj/Text_mining.git
cd Text_mining
```

### **2. Installer les dépendances :**

```bash
# Installer les packages Python
pip install -r requirements_ML.txt

# Télécharger le modèle spaCy
python -m spacy download fr_core_news_sm
```

### **3. Vérifier l'installation :**

```bash
python -c "import spacy, sklearn, transformers; print('✅ Toutes les dépendances sont installées !')"
```

---

## 🚀 Utilisation

### **Exécution simple :**

```bash
python analyse_text_mining_ML.py
```

### **Temps d'exécution :**

| Étape | CPU | GPU |
|-------|-----|-----|
| Prétraitement | 2s | 2s |
| Rule-Based | 1s | 1s |
| **BERT (le plus long)** | **60-180s** | **10-20s** |
| K-means | 3s | 3s |
| LDA | 10s | 10s |
| Visualisations | 5s | 5s |
| **TOTAL** | **~2-3 min** | **~30-40s** |

---

## 📊 Fichiers Générés

Après exécution, vous obtenez :

```
📂 Résultats :
├── 📊 Graphiques (PNG)
│   ├── comparaison_sentiments_RB_vs_ML.png  ← Sentiment : Lexicon vs BERT
│   ├── clustering_kmeans.png                ← Distribution des clusters
│   └── topics_lda.png                       ← Topics LDA par parti
│
├── 📄 Rapports
│   └── rapport_analyse_ML.txt               ← Rapport détaillé complet
│
└── 📈 Données (Excel/CSV)
    ├── synthese_ml_complete.xlsx            ← Toutes méthodes comparées
    └── synthese_ml_complete.csv             ← Version CSV
```

---

## 📈 Exemple de Résultats

### **Comparaison Sentiment : Rule-Based vs BERT**

```
┌──────┬──────────────┬──────────────┬──────────────┐
│ Parti│ Rule-Based   │ BERT (ML)    │ Différence   │
├──────┼──────────────┼──────────────┼──────────────┤
│ PAM  │ +0.750       │ +0.623       │ 0.127        │
│ PI   │ +0.256       │ +0.341       │ 0.085        │
│ PJD  │ +0.362       │ +0.428       │ 0.066        │
│ RNI  │ +0.500       │ +0.567       │ 0.067        │
└──────┴──────────────┴──────────────┴──────────────┘

✅ Concordance : 100% (tous positifs)
📊 Différence moyenne : 0.086 (acceptable)
```

### **Clustering : 5 clusters découverts**

```
Cluster 0 (Économie) :
  Termes : économie, croissance, investissement, développement
  Dominant pour : PI

Cluster 1 (Social) :
  Termes : social, solidarité, citoyens, dignité
  Dominant pour : RNI, PAM

Cluster 2 (Gouvernance) :
  Termes : gouvernance, institutions, réforme, administration
  Dominant pour : PJD

Cluster 3 (Environnement) :
  Termes : environnement, eau, énergie, ressources
  Dominant pour : PI, PJD

Cluster 4 (Emploi) :
  Termes : emploi, jeunes, formation, travail
  Dominant pour : PAM, RNI
```

### **LDA : 10 topics découverts automatiquement**

```
Topic 0 : Développement Économique
Topic 1 : Justice Sociale
Topic 2 : Gouvernance et Institutions
Topic 3 : Environnement et Eau
Topic 4 : Emploi et Formation
Topic 5 : Santé et Services
Topic 6 : Éducation
Topic 7 : Agriculture Rurale
Topic 8 : Infrastructure
Topic 9 : Droits et Égalité

✅ Cohérence avec thèmes manuels : ~75%
   (LDA redécouvre automatiquement ce qu'on avait défini !)
```

---

## 🎓 Pour la Présentation

### **Points clés à mentionner :**

1. **Progression du projet :**
   - Version initiale : Rule-Based seul
   - **Version avancée : 4 méthodes ML complémentaires**

2. **Classification Supervisée (BERT) :**
   - Modèle pré-entraîné (Transfer Learning)
   - 110M paramètres
   - Comprend le contexte bidirectionnel

3. **Classification Non-Supervisée (K-means + LDA) :**
   - Découverte automatique de patterns
   - Validation des thèmes manuels
   - 75% de cohérence avec définition manuelle

4. **Validation croisée :**
   - Les 4 méthodes convergent sur les résultats
   - Différence Rule-Based / BERT < 10%
   - Robustesse démontrée

### **Phrases d'accroche :**

> "Pour augmenter la complexité, j'ai intégré 4 techniques de Machine Learning : une méthode supervisée (BERT) et deux non-supervisées (K-means, LDA)."

> "BERT est un modèle Transformer avec 110 millions de paramètres, pré-entraîné sur des millions de textes. C'est l'état de l'art en NLP."

> "Fascinant : LDA redécouvre automatiquement 75% des thèmes que j'avais définis manuellement, validant mon approche initiale."

---

## 📚 Ressources et Documentation

- **[GUIDE_MACHINE_LEARNING.md](GUIDE_MACHINE_LEARNING.md)** - Guide complet des 4 méthodes
- **[SCRIPT_PRESENTATION.md](SCRIPT_PRESENTATION.md)** - Script pour présentation orale
- **[ANALYSE_COMPARATIVE_PARTIS.md](ANALYSE_COMPARATIVE_PARTIS.md)** - Analyse comparative des partis

---

## 🔧 Dépendances Principales

```python
# Machine Learning
scikit-learn==1.3.0      # K-means, LDA, TF-IDF
transformers==4.30.0      # BERT
torch==2.0.0              # Backend pour Transformers

# NLP
spacy==3.6.0              # Lemmatisation

# Data & Viz
pandas==2.0.3
numpy==1.24.3
matplotlib==3.7.2
seaborn==0.12.2
```

---

## ⚡ Performances

| Critère | Rule-Based | BERT | K-means | LDA |
|---------|-----------|------|---------|-----|
| **Vitesse** | ⚡⚡⚡⚡⚡ | ⚡ | ⚡⚡⚡ | ⚡⚡ |
| **Précision** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |
| **Interprétabilité** | ✅ 100% | ❌ 20% | ✅ 70% | ✅ 80% |
| **Mémoire** | <10 MB | 2-4 GB | 100-500 MB | 100-300 MB |

---

## 🏆 Niveau du Projet

| Aspect | Niveau |
|--------|--------|
| **Technique** | Master/Avancé |
| **Complexité ML** | Supervisé + Non-Supervisé |
| **État de l'art** | BERT (2018) + LDA (2003) |
| **Comparaisons** | 4 méthodes validées |
| **Documentation** | Complète (3 guides) |

---

## 👨‍💻 Auteur

**Ranya Serraj**

- GitHub : [@ranyaserraj](https://github.com/ranyaserraj)
- Repository : [Text_mining](https://github.com/ranyaserraj/Text_mining)

---

## 📄 Licence

Ce projet est à but éducatif et académique.

---

## 🙏 Remerciements

- **spaCy** pour la lemmatisation française
- **Hugging Face** pour les modèles Transformers
- **Scikit-learn** pour les algorithmes ML classiques
- Communauté NLP pour les ressources éducatives

---

## 📞 Support

Pour toute question :
1. Lire [GUIDE_MACHINE_LEARNING.md](GUIDE_MACHINE_LEARNING.md)
2. Vérifier les issues GitHub
3. Créer une nouvelle issue si nécessaire

---

**🚀 Bonne analyse ! Le Machine Learning est maintenant au service de l'analyse politique ! 🎯**

