# Application de Vocabulaire Français-Allemand

Ceci est une application web simple construite avec Streamlit pour vous aider à apprendre et à pratiquer le vocabulaire français-allemand. Elle charge les données de vocabulaire à partir d'un fichier CSV (`data.csv`) et fournit une interface conviviale pour parcourir, filtrer et écouter les mots et les phrases.

## Fonctionnalités

- **Filtrer le vocabulaire :** Filtrez les mots et les phrases par catégorie et sous-catégorie.
- **Écouter la prononciation :** Écoutez la prononciation allemande de chaque mot ou expression à l'aide de la synthèse vocale.
- **Afficher/Masquer les colonnes :** Choisissez d'afficher les colonnes français, allemand ou les deux.
- **Contrôler le nombre de mots :** Utilisez un curseur pour ajuster le nombre d'éléments de vocabulaire affichés.

## Comment l'utiliser

1. **Installer Streamlit :** Si vous n'avez pas Streamlit installé, exécutez `pip install streamlit`.
2. **Fichier de données :** Assurez-vous d'avoir un fichier CSV nommé `data.csv` dans le même répertoire que le script de l'application (`app.py`). Le fichier CSV doit comporter les colonnes suivantes :
    - **Category :** La catégorie principale du vocabulaire.
    - **Subcategory :** Une sous-catégorie plus spécifique au sein de la catégorie principale.
    - **French :** Le mot ou l'expression en français.
    - **Allemand :** La traduction allemande du mot ou de l'expression en français.
3. **Exécuter l'application :** Ouvrez votre terminal, accédez au répertoire contenant `app.py` et exécutez `streamlit run app.py`.
4. **Utiliser les filtres :** Sélectionnez les catégories et sous-catégories souhaitées dans la barre latérale pour filtrer la liste de vocabulaire.
5. **Écouter et apprendre :** Cliquez sur le bouton de lecture dans la colonne "Listen" pour entendre la prononciation allemande de chaque mot ou expression.
6. **Personnaliser l'affichage :** Utilisez les cases à cocher pour afficher ou masquer les colonnes français et allemand. Ajustez le curseur pour contrôler le nombre de mots affichés.

## Format du fichier de données

Le fichier `data.csv` doit être un fichier de valeurs séparées par des virgules avec les colonnes suivantes :

| Category | Subcategory | French | Allemand |
|---|---|---|---|
| Salutations | Basique | Bonjour | Guten Tag |
| Salutations | Formel | Bonsoir | Guten Abend |
| ... | ... | ... | ... |

## Améliorations futures

- Ajouter plus de langues.
- Mettre en œuvre la répétition espacée pour un apprentissage plus efficace.
- Permettre aux utilisateurs de créer et d'enregistrer leurs propres listes de vocabulaire.
- Rendre l'application compatible avec les mobiles.
