# Guide de Contribution

Merci de votre intérêt pour contribuer à SGI ! Ce document fournit les directives et instructions pour contribuer au projet.

## Code de Conduite

Ce projet et tous ses contributeurs sont régis par notre [Code de Conduite](CODE_OF_CONDUCT.md). En participant, vous êtes censé respecter ce code.

## Comment Contribuer

### Signaler des Bugs

Avant de créer un rapport de bogue, veuillez vérifier la liste des problèmes, car vous pourriez découvrir que le bogue a déjà été signalé. Lors de la création un rapport de bug, incluez autant de détails que possible :

- **Utilisez un titre clairement descriptif**
- **Décrivez l'étape exacte qui reproduit le problème**
- **Fournissez des exemples précis pour démontrer les étapes**
- **Décrivez le comportement observé et pointez quel est le problème avec ce comportement**
- **Expliquez le comportement attendu**
- **Incluez des captures d'écran et des fichiers GIF animés si possible**

### Suggérer des Améliorations

Les améliorations peuvent inclure de nouvelles fonctionnalités, ou une approche entièrement nouvelle pour résoudre un problème existant.

Lors de la création d'une suggestion d'amélioration, veuillez inclure :

- **Utilisez un titre clairement descriptif**
- **Fournissez une description détaillée de la fonctionnalité suggérée**
- **Fournissez des exemples spécifiques pour démontrer le cas d'usage**
- **Décrivez le comportement actuel et le comportement proposé**

## Processus de Contribution

### Configuration de l'Environnement de Développement

1. **Forker le référentiel**
   ```bash
   git clone https://github.com/yourusername/sgi.git
   cd sgi
   ```

2. **Créer une branche pour votre fonctionnalité**
   ```bash
   git checkout -b feature/nom-de-votre-fonctionnalite
   ```

3. **Installer les dépendances**
   ```bash
   uv sync
   source .venv/bin/activate
   ```

### Développement

1. **Effectuer vos modifications**
   - Écrivez du code propre et lisible
   - Suivez les conventions PEP 8
   - Ajoutez des tests pour nouvelles fonctionnalités
   - Mettez à jour la documentation si nécessaire

2. **Exécuter les Vérifications de Qualité**
   ```bash
   # Linting
   ruff check app/ main.py
   ruff format app/ main.py
   
   # Type checking
   mypy app/ main.py
   
   # Tests
   pytest tests/
   
   # Sécurité
   pip-audit
   ```

3. **Valider les Changements**
   ```bash
   # Vérifier que le serveur peut démarrer
   python -m uvicorn main:app --reload
   
   # Exécuter les tests API
   python test_api_endpoints.py
   ```

### Soumettre une Pull Request

1. **Pousser votre branche**
   ```bash
   git push origin feature/nom-de-votre-fonctionnalite
   ```

2. **Créer une Pull Request**
   - Décrivez clairement ce que vous avez modifié
   - Référencez tout problème connexe (`Fixes #issue-number`)
   - Fournissez des détails sur les tests effectués
   - Assurez-vous que tous les contrôles CI/CD réussissent

3. **Répondre aux Commentaires**
   - Soyez réceptif aux commentaires
   - Effectuez les modifications demandées
   - Repousser les changements

## Conventions de Codage

### Style de Code
- Utiliser [PEP 8](https://pep8.org/)
- Ligne maximale : 100 caractères
- Utiliser 4 espaces pour l'indentation

### Nommage
- **Variables et fonctions** : snake_case (`my_variable`)
- **Classes** : PascalCase (`MyClass`)
- **Constantes** : UPPER_CASE (`MY_CONSTANT`)

### Documentation
- Utiliser des docstrings pour toutes les fonctions et classes
- Format : Google style docstrings
```python
def my_function(param: str) -> str:
    """Short description.
    
    Longer description if needed.
    
    Args:
        param: Description of param
        
    Returns:
        Description of return value
    """
```

### Imports
- Organiser les imports : standard > third-party > local
- Importer des modules complets, pas des objets isolés
- Une import par ligne

### Type Hints
- Ajouter des type hints à toutes les fonctions
- Utiliser les annotations de type Python modernes

## Tests

- **Obligatoire** pour toute nouvelle fonctionnalité
- **Recommandé** pour les corrections de bugs
- Utiliser `pytest` comme framework de test
- Mettre les tests dans le répertoire `tests/`

```bash
# Exécuter les tests
pytest tests/

# Avec couverture
pytest --cov=app tests/
```

## Documentation

- Mettez à jour le README si vous modifiez le comportement
- Mettez à jour l'API_DOCUMENTATION.md pour les changements d'API
- Ajoutez des entrées au CHANGELOG.md

## Processus de Révue

Les mainteneurs examinineront votre PR et pourront demander des changements. C'est normal ! Voici ce que nous cherchons :

- ✅ Le code fonctionne comme prévu
- ✅ Les tests réussissent
- ✅ La couverture de code n'a pas diminué
- ✅ Les lignes directrices de style sont suivies
- ✅ Les vérifications de sécurité passent
- ✅ La documentation est à jour

## Questions ?

- 📖 Lire la [documentation](README.md)
- 🐛 Vérifier les [issues existantes](https://github.com/yourusername/sgi/issues)
- 💬 Ouvrir une [discussion](https://github.com/yourusername/sgi/discussions)

## Merci !

Vos contributions rendent ce projet meilleur. Merci d'avoir contribué ! 🙏
