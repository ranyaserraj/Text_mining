# Projet Text Mining - Analyse des Discours Politiques Marocains

## 📋 Objectif du Projet

Analyser les discours de 4 partis politiques marocains (PAM, PI, PJD, RNI) pour identifier:
- **Les sujets** traités (éducation, santé, économie, etc.)
- **Les opinions/sentiments** exprimés (positif, négatif, neutre)

## 📁 Structure du Projet

```
TM/
├── PAM_Discours.txt        # Discours du PAM
├── PI_Discours.txt         # Discours du PI
├── PJD_Discours.txt        # Discours du PJD
├── RNI_Discours.txt        # Discours du RNI
├── analyse_text_mining.py  # Script principal
├── requirements.txt        # Dépendances Python
└── README.md              # Ce fichier
```

## 🔧 Installation

### 1. Installer Python (si nécessaire)
- Téléchargez Python 3.8+ depuis [python.org](https://www.python.org/)

### 2. Installer les bibliothèques
```bash
pip install -r requirements.txt
```

Ou installer manuellement:
```bash
pip install pandas numpy matplotlib seaborn wordcloud openpyxl spacy
python -m spacy download fr_core_news_sm
```

**Note importante** : Le modèle spaCy `fr_core_news_sm` est nécessaire pour la lemmatisation (technique avancée de NLP)

## 🚀 Utilisation

### Lancer l'analyse complète:
```bash
python analyse_text_mining.py
```

Le script va automatiquement:
1. ✅ Charger les 4 fichiers texte
2. ✅ Nettoyer et prétraiter les textes
3. ✅ Identifier les thèmes (14 catégories)
4. ✅ Analyser les sentiments
5. ✅ Créer des tableaux comparatifs
6. ✅ Générer des visualisations
7. ✅ Produire un rapport détaillé

## 📊 Résultats Générés

### Fichiers Excel/CSV
- `synthese_partis.xlsx` - Tableau comparatif par parti
- `themes_details.xlsx` - Détails des mentions par thème

### Visualisations (PNG)
- `themes_par_parti.png` - Graphiques à barres des thèmes par parti
- `sentiments_comparaison.png` - Comparaison des tons (positif/négatif)
- `nuages_mots.png` - Nuages de mots pour chaque parti
- `heatmap_themes.png` - Carte de chaleur des thèmes

### Rapport
- `rapport_analyse.txt` - Rapport textuel détaillé avec interprétations

## 📈 Méthodologie

### 1. Prétraitement ⚡ **Avec Lemmatisation (Technique Avancée)**
- **Lemmatisation** : Réduction de chaque mot à sa forme de base (ex: `développons` → `développer`)
- Suppression des éléments inutiles (ponctuation, chiffres)
- Tokenisation intelligente avec spaCy
- Suppression des stopwords (mots vides)
- **Résultat** : ~50% de réduction du volume tout en conservant le sens

💡 **Avantage** : La lemmatisation regroupe les variantes d'un même mot (`développer`, `développement`, `développons` → `développer`), rendant l'analyse beaucoup plus précise et professionnelle.

### 2. Analyse Thématique
14 thèmes identifiés automatiquement:
- Éducation, Santé, Emploi, Économie
- Logement, Justice, Social, Environnement
- Gouvernance, Agriculture, Tourisme
- Droits des femmes, Jeunesse, Infrastructure

### 3. Analyse de Sentiment
Classification en 3 catégories:
- **Positif** → Propositions, solutions
- **Négatif** → Critiques, problèmes
- **Neutre** → Constat, analyse

### 4. Visualisation
- Graphiques comparatifs
- Nuages de mots
- Heatmap thématique

## 🎯 Thèmes Analysés

| Thème | Mots-clés exemples |
|-------|-------------------|
| Éducation | école, enseignement, formation, université |
| Santé | santé, hôpital, médecin, AMO |
| Emploi | emploi, travail, chômage, recrutement |
| Économie | économie, croissance, investissement |
| Social | pauvreté, inégalités, solidarité |
| Environnement | eau, énergie, climat, durabilité |
| Justice | droit, loi, corruption, équité |
| ... | ... |

## 📝 Interprétation des Résultats

### Score de Sentiment
- **Score > 0.1** → Ton positif (propositions)
- **Score -0.1 à 0.1** → Ton neutre/équilibré
- **Score < -0.1** → Ton négatif (critiques)

### Nombre de Mentions
Plus un thème est mentionné, plus il est prioritaire pour le parti

## 🔍 Exemple de Résultats

```
PAM:
  Top Thèmes: Éducation(45), Santé(38), Emploi(32)
  Ton: Positif (propositions/solutions)
  Score: 0.245

PI:
  Top Thèmes: Justice(67), Économie(54), Social(48)
  Ton: Neutre/Équilibré
  Score: 0.023
```

## 💡 Conseils d'Utilisation

1. **Vérifiez les données**: Assurez-vous que les 4 fichiers .txt sont présents
2. **Analysez les graphiques**: Les visualisations facilitent la comparaison
3. **Lisez le rapport**: Le fichier `rapport_analyse.txt` contient les conclusions
4. **Personnalisez**: Vous pouvez modifier les mots-clés dans le script

## 🛠️ Personnalisation

Pour ajouter des thèmes ou modifier les mots-clés, éditez dans `analyse_text_mining.py`:

```python
self.themes_keywords = {
    'Votre_Theme': ['mot1', 'mot2', 'mot3'],
    ...
}
```

## ❓ Résolution de Problèmes

### Erreur: Module not found
```bash
pip install [nom_du_module]
```

### Fichier texte vide (RNI)
Le script gère automatiquement les fichiers vides et continue l'analyse

### Caractères spéciaux non affichés
Les graphiques utilisent DejaVu Sans pour supporter les accents français

## 📧 Support

Pour toute question sur le projet ou l'analyse, consultez le code commenté dans `analyse_text_mining.py`

## 📄 Licence

Projet académique - Text Mining des discours politiques marocains

---

**Dernière mise à jour**: Novembre 2025

