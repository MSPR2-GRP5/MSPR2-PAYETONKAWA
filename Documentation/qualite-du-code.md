# Qualité du code

Afin de pouvoir s’assurer de la qualité des livrables, nous avons mis en place plusieurs outils.
Ces derniers analysent le code et relèvent les inconsistences de format, les erreurs de type et autres problèmes d'optimisations.

Tous ces outils sont exécutés lors des pull-requests et bloquent le merge lorsque des erreurs sont détectées, forçant leur correction.

Afin d'améliorer l'expérience developpeur, ces outils peuvent également être lancés localement, via la console ou une intégration à l'IDE.


## [Ruff](https://docs.astral.sh/ruff/) (linter)

Un linter et formateur de code extrémement rapide, écris en Rust.

```bash
ruff check paye_ton_kawa/
ruff format paye_ton_kawa/
```

**Intégrations :**
* [VS Code](https://docs.astral.sh/ruff/integrations/#vs-code-official)
* [PyCharm](https://docs.astral.sh/ruff/integrations/#pycharm-external-tool)


## [MyPy](https://mypy.readthedocs.io/en/latest/index.html) (type check)

Vérificateur statique de type.

```bash
mypy --strict --config-file=paye_ton_kawa/mypy.ini --exclude paye_ton_kawa/manage.py paye_ton_kawa/
```

MyPy peut généralement inférer les types de variables automatiquement et aucune modification du code est nécessaire. Dans les cas où ça n'est pas le cas, pour les fonctions ou les listes vides, référez-vous à la [cheat sheet](https://mypy.readthedocs.io/en/latest/cheat_sheet_py3.html#).
