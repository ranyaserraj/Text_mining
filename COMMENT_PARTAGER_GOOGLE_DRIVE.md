# 📂 COMMENT METTRE VOS FICHIERS GOOGLE DRIVE EN MODE PUBLIC

## 🎯 Objectif
Rendre vos 4 fichiers de discours accessibles publiquement pour que Google Colab puisse les télécharger automatiquement.

---

## 📋 MÉTHODE 1 : PARTAGE FICHIER PAR FICHIER (Recommandée)

### **Étape 1 : Ouvrir Google Drive**
1. Allez sur : https://drive.google.com/
2. Connectez-vous avec votre compte Google

### **Étape 2 : Localiser vos fichiers**
Trouvez vos 4 fichiers :
- `PAM_Discours.txt`
- `PI_Discours.txt`
- `PJD_Discours.txt`
- `RNI_Discours.txt`

### **Étape 3 : Clic droit sur le premier fichier**
```
┌─────────────────────────────────────┐
│  PAM_Discours.txt                   │
│                                     │
│  [Clic droit sur le fichier]       │
│                                     │
│  ▼ Menu contextuel s'ouvre         │
│    • Ouvrir avec                   │
│    • Partager              ← ICI ! │
│    • Obtenir le lien              │
│    • Déplacer vers                 │
│    • Supprimer                     │
│    • ...                           │
└─────────────────────────────────────┘
```

### **Étape 4 : Cliquez sur "Partager"**
Une fenêtre s'ouvre :

```
╔═══════════════════════════════════════════════════════════╗
║  Partager "PAM_Discours.txt"                              ║
╠═══════════════════════════════════════════════════════════╣
║                                                           ║
║  🔒 Accès limité                           [Modifier ▼]  ║  ← CLIQUEZ ICI !
║      Seules les personnes autorisées peuvent accéder     ║
║                                                           ║
║  ┌─────────────────────────────────────────────────┐     ║
║  │ Ajouter des personnes ou des groupes           │     ║
║  └─────────────────────────────────────────────────┘     ║
║                                                           ║
║  [Copier le lien]                          [Terminé]     ║
╚═══════════════════════════════════════════════════════════╝
```

### **Étape 5 : Cliquez sur "Modifier" (à côté de "Accès limité")**
Un menu déroulant apparaît :

```
╔═══════════════════════════════════════════════════════╗
║  Accès général                                        ║
╠═══════════════════════════════════════════════════════╣
║                                                       ║
║  ○ Accès limité                                       ║
║     Seules les personnes autorisées peuvent accéder   ║
║                                                       ║
║  ● Toute personne disposant du lien        ← CHOISIR ! ║
║     Toute personne disposant du lien peut accéder     ║
║                                                       ║
╚═══════════════════════════════════════════════════════╝
```

### **Étape 6 : Sélectionnez "Toute personne disposant du lien"**
La fenêtre change :

```
╔═══════════════════════════════════════════════════════════╗
║  Partager "PAM_Discours.txt"                              ║
╠═══════════════════════════════════════════════════════════╣
║                                                           ║
║  🌐 Toute personne disposant du lien      [Modifier ▼]   ║
║      Toute personne sur Internet disposant du lien       ║
║      peut consulter ce fichier                           ║
║                                                           ║
║      Rôle : Lecteur ▼                    ← VÉRIFIER !    ║
║                                                           ║
║  [Copier le lien]                          [Terminé]     ║
╚═══════════════════════════════════════════════════════════╝
```

### **Étape 7 : Vérifier le rôle = "Lecteur"**
Cliquez sur le menu déroulant "Rôle" pour vérifier :

```
Rôle :
  ● Lecteur        ← DOIT ÊTRE SÉLECTIONNÉ
  ○ Commentateur
  ○ Éditeur
```

**Important** : Laissez sur **"Lecteur"** (c'est suffisant et plus sécurisé)

### **Étape 8 : Cliquez sur "Terminé"**
✅ Le fichier est maintenant public !

### **Étape 9 : Répéter pour les 3 autres fichiers**
Recommencez les étapes 3 à 8 pour :
- `PI_Discours.txt`
- `PJD_Discours.txt`
- `RNI_Discours.txt`

---

## 📋 MÉTHODE 2 : PARTAGE MULTIPLE (Plus rapide)

Si vos fichiers sont dans le même dossier :

### **Étape 1 : Sélectionner les 4 fichiers**
- Maintenez **Ctrl** (Windows) ou **Cmd** (Mac)
- Cliquez sur chaque fichier
- Les 4 fichiers sont maintenant sélectionnés

```
✓ PAM_Discours.txt   (sélectionné)
✓ PI_Discours.txt    (sélectionné)
✓ PJD_Discours.txt   (sélectionné)
✓ RNI_Discours.txt   (sélectionné)
```

### **Étape 2 : Clic droit → Partager**
Le même menu s'ouvre pour les 4 fichiers

### **Étape 3 : Suivre les étapes 4-8 ci-dessus**
Les modifications s'appliquent aux 4 fichiers en même temps !

---

## ✅ VÉRIFICATION QUE LE PARTAGE FONCTIONNE

### Méthode 1 : Vérifier visuellement
Regardez l'icône à côté du nom du fichier dans Google Drive :

```
Sans partage :   📄 PAM_Discours.txt
Avec partage :   🌐 PAM_Discours.txt   ← Icône de lien/globe
```

### Méthode 2 : Tester le lien
1. Clic droit sur le fichier → **"Copier le lien"**
2. Ouvrez une **fenêtre de navigation privée** (Ctrl+Shift+N dans Chrome)
3. Collez le lien
4. Si vous pouvez voir le fichier **sans vous connecter** → ✅ C'est bon !

### Méthode 3 : Vérifier dans les paramètres
1. Clic droit sur le fichier → **"Partager"**
2. Vous devez voir :
   ```
   🌐 Toute personne disposant du lien
   ```
   (et non "🔒 Accès limité")

---

## 🖼️ GUIDE VISUEL COMPLET EN IMAGES

### Vue d'ensemble du processus :

```
ÉTAPE 1                    ÉTAPE 2                    ÉTAPE 3
┌──────────────┐          ┌──────────────┐          ┌──────────────┐
│ Google Drive │          │ Clic droit   │          │   Partager   │
│              │   →      │ sur fichier  │   →      │              │
│ Vos fichiers │          │              │          │  [Modifier]  │
└──────────────┘          └──────────────┘          └──────────────┘

ÉTAPE 4                    ÉTAPE 5
┌──────────────────────┐  ┌──────────────┐
│ Toute personne       │  │   Terminé    │
│ disposant du lien    │→ │              │
│ Rôle: Lecteur        │  │   ✅ Fait    │
└──────────────────────┘  └──────────────┘
```

---

## 🎯 VOS FICHIERS APRÈS PARTAGE

Une fois partagés, vos liens ressemblent à ceci :

| Fichier | Statut | Lien |
|---------|--------|------|
| PAM_Discours.txt | ✅ Public | https://drive.google.com/file/d/1SJhMpOXzRaT0xCgWwvzOoarmA-XgG8Qk/view |
| PI_Discours.txt | ✅ Public | https://drive.google.com/file/d/12HkfJcto1AZIQi1iUrALgrUlaJ8STGLU/view |
| PJD_Discours.txt | ✅ Public | https://drive.google.com/file/d/1oHdyS0SdPcrHxoJhtZGyKEZlCftspU-X/view |
| RNI_Discours.txt | ✅ Public | https://drive.google.com/file/d/14mgRIS-zjKxNKUQ3tTHP1oOGNXFRbJPt/view |

---

## 🔐 SÉCURITÉ : EST-CE DANGEREUX ?

### ❓ Ma question
"Si je rends mes fichiers publics, tout le monde peut les voir ?"

### ✅ Réponse
**Oui**, mais seulement si quelqu'un a le lien !

### Ce que ça veut dire :
- ✅ Les fichiers ne sont **pas indexés** par Google
- ✅ Les fichiers ne sont **pas dans les résultats de recherche**
- ✅ Seules les personnes ayant le lien peuvent y accéder
- ✅ Personne ne peut les **modifier** (rôle = Lecteur)
- ✅ Personne ne peut les **supprimer**

### Si vous êtes inquiet :
Après avoir terminé votre projet, vous pouvez :
1. Remettre les fichiers en mode **"Accès limité"**
2. Ou les supprimer de Google Drive

---

## 🔄 COMMENT REVENIR EN MODE PRIVÉ

Si vous voulez rendre vos fichiers privés après :

### Étape 1 : Clic droit sur le fichier → Partager

### Étape 2 : Cliquez sur "Modifier" (à côté de "Toute personne disposant du lien")

### Étape 3 : Sélectionnez "Accès limité"

```
╔═══════════════════════════════════════════════════════╗
║  Accès général                                        ║
╠═══════════════════════════════════════════════════════╣
║                                                       ║
║  ● Accès limité                          ← CHOISIR   ║
║     Seules les personnes autorisées peuvent accéder   ║
║                                                       ║
║  ○ Toute personne disposant du lien                   ║
║     Toute personne disposant du lien peut accéder     ║
║                                                       ║
╚═══════════════════════════════════════════════════════╝
```

### Étape 4 : Cliquez sur "Terminé"
✅ Le fichier est de nouveau privé !

---

## 🆘 PROBLÈMES COURANTS

### Problème 1 : Je ne vois pas l'option "Partager"
**Cause** : Vous n'êtes pas le propriétaire du fichier
**Solution** : Contactez le propriétaire ou copiez les fichiers dans votre Drive

### Problème 2 : L'option "Toute personne disposant du lien" est grisée
**Cause** : Restrictions de votre organisation (compte professionnel/scolaire)
**Solution** : 
- Utilisez un compte Google personnel
- Ou demandez à l'administrateur de votre organisation

### Problème 3 : Le téléchargement dans Colab échoue toujours
**Cause** : Le partage n'est pas encore actif
**Solution** : 
- Attendez 1-2 minutes (propagation des changements)
- Videz le cache de Colab : `Runtime → Reset all runtimes`
- Vérifiez le lien dans une fenêtre de navigation privée

---

## 📸 CAPTURES D'ÉCRAN ALTERNATIVES

### Sur téléphone/tablette :

1. **Ouvrez l'app Google Drive**
2. **Appuyez sur les 3 points** (⋮) à côté du fichier
3. **Sélectionnez "Partager"**
4. **Appuyez sur "Modifier"** sous "Accès limité"
5. **Sélectionnez "Toute personne disposant du lien"**
6. **Vérifiez que "Lecteur" est sélectionné**
7. **Appuyez sur "Terminé"**

---

## ✅ CHECKLIST FINALE

Avant de lancer Google Colab, vérifiez :

- [ ] Les 4 fichiers sont sur Google Drive
- [ ] Chaque fichier affiche 🌐 (icône de partage)
- [ ] En cliquant sur "Partager", je vois "Toute personne disposant du lien"
- [ ] Le rôle est "Lecteur"
- [ ] J'ai testé un lien dans une fenêtre de navigation privée
- [ ] Le téléchargement fonctionne (le fichier s'ouvre sans demander de connexion)

---

## 🎓 RÉSUMÉ RAPIDE

```
1. Google Drive → Localiser fichier
2. Clic droit → Partager
3. Modifier → Toute personne disposant du lien
4. Rôle = Lecteur
5. Terminé
6. Répéter pour les 4 fichiers

Total : 2 minutes ⏱️
```

---

## 🔗 LIENS UTILES

- **Google Drive** : https://drive.google.com/
- **Aide Google Drive** : https://support.google.com/drive/answer/2494822
- **Votre projet sur GitHub** : https://github.com/ranyaserraj/Text_mining.git

---

## 💡 ASTUCE BONUS

### Créer un dossier partagé pour tous vos fichiers :

1. Créez un nouveau dossier : `Discours_Politiques`
2. Mettez les 4 fichiers dedans
3. Clic droit sur le dossier → Partager
4. "Toute personne disposant du lien" + "Lecteur"
5. Tous les fichiers du dossier sont maintenant publics !

**Avantage** : Si vous ajoutez d'autres fichiers dans ce dossier, ils seront automatiquement publics.

---

**C'est fait ? Lancez Google Colab et testez la PARTIE 3 ! 🚀**

