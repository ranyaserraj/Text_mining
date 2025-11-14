# 🔬 Lemmatisation : Technique Avancée de Text Mining

## 📌 Qu'est-ce que la Lemmatisation ?

La **lemmatisation** est une technique de normalisation linguistique qui réduit chaque mot à sa **forme canonique** (ou lemme), c'est-à-dire sa forme de base telle qu'elle apparaît dans un dictionnaire.

### Exemples concrets :
| Mot original | Lemme |
|-------------|-------|
| `développons` | `développer` |
| `développement` | `développement` |
| `développé` | `développer` |
| `politique` | `politique` |
| `politiques` | `politique` |
| `gouvernemental` | `gouvernemental` |
| `gouverner` | `gouverner` |

---

## 🆚 Différence avec la **Stemming** (Racinisation)

| Technique | Méthode | Résultat | Exemple |
|-----------|---------|----------|---------|
| **Stemming** | Coupe la fin des mots selon des règles | Racine approximative (pas toujours un vrai mot) | `développement` → `develop` |
| **Lemmatisation** | Analyse morphologique avec dictionnaire | Lemme valide (vrai mot) | `développement` → `développement` |

### Pourquoi la lemmatisation est meilleure ?
- ✅ **Précision linguistique** : Produit des vrais mots
- ✅ **Contexte grammatical** : Tient compte du rôle du mot (verbe, nom, etc.)
- ✅ **Qualité d'analyse** : Résultats plus pertinents et interprétables

---

## 🚀 Implémentation dans notre projet

### Bibliothèque utilisée : **spaCy**
[spaCy](https://spacy.io/) est une bibliothèque NLP (Natural Language Processing) moderne et performante.

**Modèle utilisé** : `fr_core_news_sm` (français)
- Modèle pré-entraîné sur des textes d'actualité français
- Contient un dictionnaire de lemmes et des règles grammaticales

### Installation :
```bash
pip install spacy
python -m spacy download fr_core_news_sm
```

---

## 📊 Impact sur notre analyse

### Résultats de la réduction :

| Parti | Mots bruts | Lemmes extraits | Réduction |
|-------|-----------|----------------|-----------|
| **PAM** | 1,067 | **535** | 50% |
| **PI** | 5,370 | **2,492** | 54% |
| **PJD** | 1,605 | **746** | 54% |
| **RNI** | 1,688 | **858** | 49% |

**Moyenne : 52% de réduction** → *Concentration sur les concepts clés*

---

## 🎯 Avantages pour l'analyse thématique

### Avant la lemmatisation :
```
développer (10 fois)
développement (8 fois)
développons (3 fois)
→ 3 entrées distinctes = analyse fragmentée
```

### Après la lemmatisation :
```
développer (21 fois)
→ 1 seule entrée = vision unifiée du concept
```

---

## 🔍 Processus de lemmatisation dans le code

```python
# Chargement du modèle français
nlp = spacy.load("fr_core_news_sm")

# Traitement du texte
doc = nlp(texte)

# Extraction des lemmes
for token in doc:
    if not token.is_stop and len(token.lemma_) > 2:
        lemmes.append(token.lemma_.lower())
```

### Filtres appliqués :
1. **Suppression des stopwords** (mots vides : `le, la, de, un, etc.`)
2. **Suppression de la ponctuation**
3. **Longueur minimale** : 3 caractères
4. **Normalisation** : minuscules

---

## 📈 Amélioration de la qualité

### 1. Nuages de mots plus cohérents
Sans lemmatisation : `développer`, `développement`, `développé` apparaissent séparément

Avec lemmatisation : Un seul concept `développer` avec une taille proportionnelle à l'importance réelle

### 2. Analyse de co-occurrence plus précise
Les thèmes sont mieux identifiés car les variantes d'un même mot sont regroupées

### 3. Résultats plus professionnels
L'analyse reflète vraiment les **concepts abordés**, pas juste les mots utilisés

---

## 🛠️ Techniques complémentaires appliquées

| Technique | Objectif | Outil utilisé |
|-----------|----------|---------------|
| **Tokenisation** | Découper le texte en mots | spaCy |
| **Nettoyage** | Supprimer chiffres et ponctuation | Regex (`re`) |
| **Stopwords** | Éliminer mots vides | spaCy (liste intégrée) |
| **Lemmatisation** | Réduire aux formes de base | spaCy NLP |

---

## 🌟 Résultat final

La **lemmatisation** transforme une analyse basique en une **étude linguistique professionnelle**, donnant des résultats :
- ✅ Plus précis
- ✅ Plus compacts
- ✅ Plus interprétables
- ✅ Plus fiables pour la prise de décision

---

## 📚 Références

- [Documentation spaCy](https://spacy.io/)
- [Modèles français spaCy](https://spacy.io/models/fr)
- [Lemmatisation vs Stemming](https://nlp.stanford.edu/IR-book/html/htmledition/stemming-and-lemmatization-1.html)

