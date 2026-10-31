TOUR DE MAGIE DES CINQ CARTES

1. Décompressez le projet.
2. Placez vos 52 images PNG dans le dossier cartes_png.
   Les noms doivent être de la forme AT.png, 10C.png, RP.png, etc.
3. Ouvrez un terminal dans le dossier du projet.
4. Installez les dépendances :
       pip install -r requirements.txt
5. Lancez l'application :
       streamlit run app.py

L'application utilise votre algorithme de choix des quatre cartes.
Le spectateur sélectionne cinq cartes en cliquant sur les cartes du jeu.
Les quatre cartes sont révélées une à une, puis la carte cachée est dévoilée.
