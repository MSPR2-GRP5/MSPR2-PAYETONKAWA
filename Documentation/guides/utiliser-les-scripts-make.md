# Utiliser les scripts Make

Un certain nombre de tâches sont souvent répétées et demande parfois plusieurs longues commandes.
*Make* permet de combiner ces commandes et de les appeler à l'aide d'une seule commande de seulement deux mots.

## Prérequis

Avoir Make d'installé sur son ordinateur.

### Linux

Make fait partis des outils GNU et est donc de base dans la plupart des distributions.

### Windows

Make est à l'origine une commande GNU et n'est donc pas disponible par défaut sous Windows, il faut l'installer.
Pour ce faire, plusieurs méthodes existent :

1. L'installer depuis [Make for Windows](https://gnuwin32.sourceforge.net/packages/make.htm)
2. Utiliser [Chocolatey](https://chocolatey.org/install):
    ```bash
    choco install make
    ```
3. Utiliser [Windows Subsystem for Linux](https://learn.microsoft.com/en-us/windows/wsl/install). Make devrait alors
   être disponible.

## Utiliser les scripts

Pour lancer la commande, se place à la racine du projet Django, au même niveau que le **manage.py**, et
utiliser `make <commande>`.

- `make pip-install`
  Installe les dépendances du projet
- `make mypy`
  Lance le type checker MyPy avec les mêmes paramètres que la CI
- `make ruff`
  Lance le linter Ruff avec les mêmes paramètres que la CI
- `make test`
  Lance tous les tests unitaires
- `make check`
  Lance les trois commandes précédentes. Recrée les vérifications de la CI
- `make clean`
  Reformatte le code. **Attention** : cela affecte ***tous*** les fichiers du projet, pas seulement les derniers
  modifiés.
  Utilisez cette commande après avoir corrigé toutes les erreurs liées aux tests et à MyPy, juste avant de créer votre
  PR ou au fur et à mesure de votre développement.
- `make server`
  Exécute les migrations et lance le serveur Django
- `make checkmigrations`
  Vérifie s'il faut créer des migrations en cas de modification des modèles
- `make migrations`
  Génère et applique les migrations après un changement de modèle

L'intégralité des commandes et leurs actions exactes sont visibles dans le fichier **Makefile**.
