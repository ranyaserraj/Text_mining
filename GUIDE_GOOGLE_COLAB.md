# 📘 GUIDE D'UTILISATION GOOGLE COLAB

## 🎯 Comment utiliser le code dans Google Colab

Ce guide explique comment diviser et exécuter le code dans Google Colab cellule par cellule.

---

## 📋 ÉTAPES PRÉLIMINAIRES

### 1. Ouvrir Google Colab
- Allez sur : https://colab.research.google.com/
- Créez un nouveau notebook : **Fichier → Nouveau notebook**

### 2. Préparer vos fichiers
Assurez-vous d'avoir vos 4 fichiers de discours prêts :
- `PAM_Discours.txt`
- `PI_Discours.txt`
- `PJD_Discours.txt`
- `RNI_Discours.txt`

---

## 🔢 DIVISION DU CODE EN 11 PARTIES

Le fichier `analyse_text_mining_COLAB.py` est déjà divisé en **11 parties**.
Chaque partie doit être copiée dans une **cellule séparée** de Google Colab.

---

## 📦 CELLULE 1 : Installation des bibliothèques

### Explication
Cette cellule installe toutes les bibliothèques nécessaires (spaCy, WordCloud, etc.)

### Code à copier dans la cellule 1
```python
# ============================================================================
# PARTIE 1 : INSTALLATION DES BIBLIOTHÈQUES
# ============================================================================

!pip install spacy wordcloud openpyxl -q
!python -m spacy download fr_core_news_sm -q

print("✅ Toutes les bibliothèques sont installées !")
```

### ⏱️ Temps : ~1-2 minutes
### 💡 N'exécutez qu'**une seule fois** au début

---

## 📚 CELLULE 2 : Importation des modules

### Explication
Import de tous les modules Python (pandas, matplotlib, spaCy...)

### Code à copier dans la cellule 2
```python
# ============================================================================
# PARTIE 2 : IMPORTATION DES MODULES
# ============================================================================

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

try:
    nlp = spacy.load("fr_core_news_sm")
    print("✅ Modèle spaCy français chargé avec succès")
except OSError:
    print("❌ Erreur : Modèle spaCy non trouvé")
    nlp = None

plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['figure.figsize'] = (14, 8)
sns.set_style("whitegrid")

print("✅ Tous les modules sont importés !")
```

### ⏱️ Temps : Quelques secondes

---

## 📂 CELLULE 3 : Upload des fichiers

### Explication
Upload de vos 4 fichiers de discours dans Colab

### Code à copier dans la cellule 3
```python
# ============================================================================
# PARTIE 3 : UPLOAD DES FICHIERS TEXTE
# ============================================================================

from google.colab import files

print("📁 Veuillez uploader vos 4 fichiers de discours (.txt)")
print("   Fichiers attendus : PAM_Discours.txt, PI_Discours.txt, PJD_Discours.txt, RNI_Discours.txt")
print()

uploaded = files.upload()

print()
print(f"✅ {len(uploaded)} fichier(s) uploadé(s) avec succès !")
for filename in uploaded.keys():
    print(f"   • {filename}")
```

### ⏱️ Temps : Variable selon taille des fichiers
### 💡 Après exécution, cliquez sur **"Choisir les fichiers"** et sélectionnez vos 4 fichiers

---

## 🏗️ CELLULE 4 : Définition de la classe (Configuration)

### Explication
Définition de la classe avec :
- Stopwords (mots vides)
- 14 thèmes avec mots-clés
- Dictionnaires de sentiment

### Code à copier dans la cellule 4
Copiez **toute la PARTIE 4** du fichier `analyse_text_mining_COLAB.py`
(Lignes avec la définition de la classe et les dictionnaires)

### ⏱️ Temps : Instantané

---

## 🔧 CELLULE 5 : Méthodes de chargement et prétraitement

### Explication
Ajout des méthodes pour :
- Charger les fichiers texte
- Lemmatisation (réduction des mots à leur forme de base)

### Code à copier dans la cellule 5
Copiez **toute la PARTIE 5** du fichier `analyse_text_mining_COLAB.py`

### ⏱️ Temps : Instantané

---

## 📊 CELLULE 6 : Méthodes d'analyse thématique et de sentiment

### Explication
Ajout des méthodes pour :
- Topic Mining (extraction de thèmes)
- Sentiment Analysis (analyse du ton)

### Code à copier dans la cellule 6
Copiez **toute la PARTIE 6** du fichier `analyse_text_mining_COLAB.py`

### ⏱️ Temps : Instantané

---

## 🔗 CELLULE 7 : Méthode d'analyse de co-occurrence

### Explication
Analyse des liens entre thèmes (Sliding Window)

### Code à copier dans la cellule 7
Copiez **toute la PARTIE 7** du fichier `analyse_text_mining_COLAB.py`

### ⏱️ Temps : Instantané

---

## 📋 CELLULE 8 : Méthode de création de tableaux

### Explication
Création des tableaux de synthèse (CSV et Excel)

### Code à copier dans la cellule 8
Copiez **toute la PARTIE 8** du fichier `analyse_text_mining_COLAB.py`

### ⏱️ Temps : Instantané

---

## 📊 CELLULE 9 : Méthodes de visualisation

### Explication
Génération de tous les graphiques :
- Barres, Sentiments, Nuages de mots, Heatmap, Radar

### Code à copier dans la cellule 9
Copiez **toute la PARTIE 9** du fichier `analyse_text_mining_COLAB.py`

### ⏱️ Temps : Instantané

---

## 📝 CELLULE 10 : Méthode de génération de rapport

### Explication
Génération du rapport textuel détaillé

### Code à copier dans la cellule 10
Copiez **toute la PARTIE 10** du fichier `analyse_text_mining_COLAB.py`

### ⏱️ Temps : Instantané

---

## 🚀 CELLULE 11 : EXÉCUTION DE L'ANALYSE COMPLÈTE

### Explication
**C'EST ICI QUE L'ANALYSE SE LANCE !**
Cette cellule exécute toutes les étapes et génère tous les fichiers

### Code à copier dans la cellule 11
Copiez **toute la PARTIE 11** du fichier `analyse_text_mining_COLAB.py`

### ⏱️ Temps : ~30 secondes à 2 minutes
### 🎯 C'est la **dernière cellule** à exécuter !

---

## 📥 TÉLÉCHARGER LES RÉSULTATS

Après l'exécution de la cellule 11, vous aurez 10 fichiers générés.

### Pour télécharger un fichier
```python
# Dans une nouvelle cellule
from google.colab import files

# Télécharger un fichier spécifique
files.download('synthese_partis.xlsx')
files.download('themes_par_parti.png')
files.download('rapport_analyse.txt')

# OU télécharger tous les fichiers d'un coup
import os
for f in os.listdir('.'):
    if f.endswith(('.csv', '.xlsx', '.png', '.txt')) and not f.startswith('.'):
        files.download(f)
```

---

## 📁 FICHIERS GÉNÉRÉS

### 📊 Tableaux (3 fichiers)
- `synthese_partis.csv` / `.xlsx` → Comparaison par parti
- `themes_details.csv` / `.xlsx` → Détails par thème
- `cooccurrences_themes.csv` / `.xlsx` → Co-occurrences

### 📈 Graphiques (5-6 fichiers PNG)
- `themes_par_parti.png` → Barres par parti
- `sentiments_comparaison.png` → Comparaison des tons
- `nuages_mots.png` → Word clouds
- `heatmap_themes.png` → Carte de chaleur
- `graphique_radar.png` → Radar comparatif
- `graphique_radar_complet.png` → Radar complet (si ≤14 thèmes)

### 📝 Rapport (1 fichier)
- `rapport_analyse.txt` → Rapport détaillé

---

## 🎓 ORDRE D'EXÉCUTION RECOMMANDÉ

```
1️⃣ Cellule 1  → Installer bibliothèques
2️⃣ Cellule 2  → Importer modules
3️⃣ Cellule 3  → Uploader fichiers
4️⃣ Cellule 4  → Définir classe
5️⃣ Cellule 5  → Ajouter méthodes prétraitement
6️⃣ Cellule 6  → Ajouter méthodes analyse
7️⃣ Cellule 7  → Ajouter co-occurrence
8️⃣ Cellule 8  → Ajouter tableaux
9️⃣ Cellule 9  → Ajouter visualisations
🔟 Cellule 10 → Ajouter rapport
1️⃣1️⃣ Cellule 11 → LANCER L'ANALYSE 🚀
```

---

## ⚠️ POINTS IMPORTANTS

### 1. Exécution séquentielle
❗ **Exécutez les cellules dans l'ordre** (1 → 2 → 3 → ... → 11)
❗ Ne sautez aucune cellule

### 2. Temps d'attente
- Cellule 1 : ~1-2 minutes (installation)
- Cellule 3 : Variable (upload fichiers)
- Cellule 11 : ~30 sec à 2 min (analyse)
- Autres cellules : Instantané

### 3. Redémarrage du runtime
Si vous redémarrez le runtime Colab, vous devez **réexécuter toutes les cellules** depuis le début

### 4. Graphiques dans Colab
Les graphiques s'afficheront directement dans le notebook grâce à `plt.show()`

---

## 🆘 DÉPANNAGE

### Problème : "Module not found"
**Solution** : Réexécutez la cellule 1 (installation) puis la cellule 2 (import)

### Problème : "Modèle spaCy non trouvé"
**Solution** : Dans la cellule 1, exécutez :
```python
!python -m spacy download fr_core_news_sm
```

### Problème : "Fichiers non trouvés"
**Solution** : Vérifiez que vous avez bien uploadé les 4 fichiers dans la cellule 3

### Problème : "Class not defined"
**Solution** : Exécutez les cellules 4 à 10 dans l'ordre avant la cellule 11

---

## 💡 CONSEILS

### Renommer le notebook
Donnez un nom clair : `Analyse_Text_Mining_Discours_Politiques.ipynb`

### Sauvegarder régulièrement
Colab sauvegarde automatiquement, mais vous pouvez aussi :
**Fichier → Télécharger → Télécharger .ipynb**

### Ajouter des notes
Entre les cellules, ajoutez des cellules **Texte** (Markdown) pour vos propres notes

---

## 🎯 EXEMPLE DE STRUCTURE FINALE

```
📓 Votre notebook Google Colab
├─ 📝 [Texte] Titre du projet
├─ 💻 [Code] Cellule 1 - Installation
├─ 💻 [Code] Cellule 2 - Import
├─ 💻 [Code] Cellule 3 - Upload
├─ 📝 [Texte] "Définition de la classe"
├─ 💻 [Code] Cellule 4 - Classe
├─ 💻 [Code] Cellule 5 - Prétraitement
├─ 💻 [Code] Cellule 6 - Analyse
├─ 💻 [Code] Cellule 7 - Co-occurrence
├─ 💻 [Code] Cellule 8 - Tableaux
├─ 💻 [Code] Cellule 9 - Visualisations
├─ 💻 [Code] Cellule 10 - Rapport
├─ 📝 [Texte] "LANCEMENT DE L'ANALYSE"
├─ 💻 [Code] Cellule 11 - EXÉCUTION
└─ 💻 [Code] Cellule 12 - Téléchargement résultats
```

---

## ✅ CHECKLIST AVANT EXÉCUTION

- [ ] Google Colab ouvert
- [ ] Nouveau notebook créé
- [ ] 11 cellules de code créées
- [ ] Code copié dans chaque cellule
- [ ] 4 fichiers .txt prêts à uploader
- [ ] Cellules exécutées dans l'ordre
- [ ] Fichiers générés téléchargés

---

## 🎉 RÉSULTAT FINAL

Après l'exécution complète, vous aurez :
- ✅ 10 fichiers générés
- ✅ Graphiques affichés dans le notebook
- ✅ Tableaux de synthèse visibles
- ✅ Rapport détaillé complet

**Temps total : ~5-10 minutes** (selon taille des fichiers)

---

## 📚 RESSOURCES SUPPLÉMENTAIRES

- **Documentation Google Colab** : https://colab.research.google.com/notebooks/intro.ipynb
- **Documentation spaCy** : https://spacy.io/
- **Documentation pandas** : https://pandas.pydata.org/

---

**🎓 Bonne analyse avec Google Colab ! 🚀**

