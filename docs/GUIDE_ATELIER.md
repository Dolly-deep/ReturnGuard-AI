# Guide animateur — Atelier pratique (90 minutes)

## Résultat attendu

Montrer que la validation de réponses IA ne repose pas sur le prompt : règles métier en Python, tests unitaires, tests d'intégration LangGraph, contrôle de conformité et pipeline CI.

| Étape | Durée | Action | Preuve |
|---|---:|---|---|
| 1. Workflow | 25 min | Montrer `workflow.py` et exécuter les scénarios `demo.py` | 3 sorties structurées différentes |
| 2. Tests | 25 min | Exécuter `python -m pytest tests -v --junitxml=reports/results.xml` | plus de 20 tests PASS |
| 3. CI | 20 min | Pousser le projet sur GitHub, ouvrir Actions → Business Tests | run vert, rapport téléchargé |
| 4. Livrables | 20 min | Vérifier export JSON, rapport HTML, README et mocks | badge vert + fichiers du dépôt |

## Trois démonstrations à faire en direct

**Cas A : retour éligible**

```bash
python demo.py CMD-1001 "Je veux retourner ma commande."
```

Attendu : `ELIGIBLE`, `WITHIN_WINDOW`, `compliant=true`.

**Cas B : délai dépassé**

```bash
python demo.py CMD-1003 "Je veux retourner ma commande."
```

Attendu : `NOT_ELIGIBLE`, `WINDOW_EXPIRED`, `compliant=true`.

**Cas C : incident, escalade**

```bash
python demo.py CMD-1001 "Le produit est cassé."
```

Attendu : `HUMAN_REVIEW`, `EXCEPTION_REPORTED`, `compliant=true`.

## Instructions GitHub simples

1. Décompresser l'archive.
2. Ouvrir le dossier dans VS Code/Codex.
3. Installer les packages (`python -m pip install -r requirements.txt`).
4. Exécuter `python -m pytest tests -v --junitxml=reports/results.xml`.
5. Créer le dépôt GitHub et importer le dossier en conservant `.github/workflows/ci.yml`.
6. Ouvrir l'onglet **Actions**, cliquer sur le premier run, voir le statut.
7. Ajouter le vrai chemin du dépôt au badge dans `README.md`.

## Captures à montrer

- Sortie console des 3 démos.
- Rapport des 20+ tests (`reports/report.html`).
- Job **Business Tests** validé dans l'onglet Actions.
- Badge vert affiché dans le README, après vérification du run.

## Message clé

> « Le modèle peut rédiger, mais ne décide pas de la politique. Les tests métier et le validateur sont déterministes, réexécutés automatiquement à chaque modification du code. »

## Limites de l'export JSON

`workflow_export.json` prouve l'architecture et les règles, mais le fichier n'est pas un workflow AgenticAI ré-importable. Le moteur exécutable est Python + LangGraph. Cette distinction doit être dite clairement si l'animateur demande un export natif d'une plateforme no-code.
