# Documentation des mocks — ReturnGuard AI

## Pourquoi simuler les dépendances ?

L'atelier doit produire des tests répétables, rapides et **indépendants des APIs tierces**. Les simulations permettent de vérifier les règles métier même en l'absence de clé OpenAI, de réseau et d'une véritable base commerciale.

## Mock n°1 : base de commandes

- **Source** : `mocks/orders.json` ; **mode d'accès** : lecture locale (`returnguard/policy.py`).
- **Nature** : dictionnaire JSON inventé ; aucune donnée personnelle ni vraie transaction.
- **Champs** : `status` (delivered, shipped, pending, cancelled), `days_since_delivery` (int/null), `category` (standard, hygiene, digital, other).
- **Cas présents** : `CMD-1001` à `CMD-1013` ; `CMD-9999` simulé comme absent.
- **Défaillances simulées** : commande introuvable, livraison non confirmée, données temporelles invalides, catégorie inconnue.
- **Restrictions fictives** : 30 jours inclus, catégories hygiene et digital exclues pour le seul atelier.

## Mock n°2 : générateur de réponse IA

- **Production facultative** : `optional_openai_writer()` dans `returnguard/response.py`, utilise OpenAI seulement si `OPENAI_API_KEY` est définie.
- **Mode sans réseau** : `safe_template(state)` renvoie une réponse contrôlée et reproductible.
- **Injection des tests** : `build_graph(writer=lambda state: ...)` remplace la fonction de génération ; l'interface est une fonction `(state: dict) -> str`.
- **Scénarios testés** : rédaction insuffisante, référence manquante, phrase de décision absente, promesse de remboursement, décision contradictoire, panne du modèle.
- **Sortie garantie** : le validateur inspecte le brouillon puis remplace les réponses incorrectes par un template revalidé.

## Limites et sécurité

Les tests avec mocks **ne prouvent pas** la qualité générale d'un vrai LLM ; ils vérifient que notre logique reste stable lorsque le modèle reçoit ou retourne certaines valeurs. Aucune requête de paiement, de remboursement ou de logistique réelle n'est émise.
