# ============================================================================
# PARTIE 3 : TÉLÉCHARGEMENT DEPUIS GOOGLE DRIVE
# ============================================================================
"""
📂 EXPLICATION PARTIE 3 (VERSION GOOGLE DRIVE) :
Au lieu d'uploader manuellement les fichiers, on les télécharge directement 
depuis Google Drive en utilisant les liens partagés.

✅ Avantages :
   - Plus rapide (pas besoin d'uploader à chaque fois)
   - Les fichiers restent sur votre Drive
   - Code réutilisable

⏱️ Temps d'exécution : ~10-30 secondes (selon taille des fichiers)
💡 Les fichiers doivent être en mode "Accessible à toute personne disposant du lien"
"""

# Installation de gdown (pour télécharger depuis Google Drive)
!pip install gdown -q

import gdown
import os

print("=" * 80)
print("📂 TÉLÉCHARGEMENT DES FICHIERS DEPUIS GOOGLE DRIVE")
print("=" * 80)
print()

# Dictionnaire des fichiers avec leurs IDs Google Drive
fichiers_drive = {
    'PAM_Discours.txt': '1SJhMpOXzRaT0xCgWwvzOoarmA-XgG8Qk',
    'PI_Discours.txt': '12HkfJcto1AZIQi1iUrALgrUlaJ8STGLU',
    'PJD_Discours.txt': '1oHdyS0SdPcrHxoJhtZGyKEZlCftspU-X',
    'RNI_Discours.txt': '14mgRIS-zjKxNKUQ3tTHP1oOGNXFRbJPt'
}

# Télécharger chaque fichier
fichiers_telecharges = 0
for nom_fichier, file_id in fichiers_drive.items():
    try:
        print(f"⏳ Téléchargement de {nom_fichier}...")
        url = f'https://drive.google.com/uc?id={file_id}'
        gdown.download(url, nom_fichier, quiet=False)
        
        # Vérifier que le fichier existe et n'est pas vide
        if os.path.exists(nom_fichier):
            taille = os.path.getsize(nom_fichier)
            print(f"✅ {nom_fichier} téléchargé avec succès ({taille} octets)")
            fichiers_telecharges += 1
        else:
            print(f"❌ Erreur : {nom_fichier} non téléchargé")
    except Exception as e:
        print(f"❌ Erreur lors du téléchargement de {nom_fichier}: {e}")
    print()

print("=" * 80)
if fichiers_telecharges == 4:
    print(f"✅ SUCCÈS ! Les 4 fichiers ont été téléchargés avec succès !")
else:
    print(f"⚠️ ATTENTION ! Seulement {fichiers_telecharges}/4 fichiers téléchargés")
print("=" * 80)
print()

# Afficher la liste des fichiers téléchargés
print("📋 Fichiers présents dans le répertoire :")
for nom_fichier in fichiers_drive.keys():
    if os.path.exists(nom_fichier):
        taille = os.path.getsize(nom_fichier)
        nb_mots = len(open(nom_fichier, 'r', encoding='utf-8').read().split())
        print(f"   ✅ {nom_fichier} - {taille} octets - {nb_mots} mots")
    else:
        print(f"   ❌ {nom_fichier} - NON TROUVÉ")
print()

