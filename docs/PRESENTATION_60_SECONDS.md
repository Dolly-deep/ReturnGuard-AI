# Pitch atelier — 60 secondes

« Notre cas d'usage s'appelle ReturnGuard AI. Un service client doit traiter des demandes de retour, mais une réponse rédigée par IA peut être incorrecte ou annoncer un remboursement non autorisé.

Nous avons construit un workflow LangGraph avec quatre nœuds : recherche d'une commande simulée, application de règles métier, génération d'une réponse, puis contrôle automatique de sa conformité. Les cas incertains sont dirigés vers un examen humain.

Nous avons une suite de plus de vingt cas de test couvrant les délais, les catégories exclues, les anomalies et les réponses trompeuses. Les dépendances externes sont simulées pour que les tests fonctionnent sans clé API.

À chaque push GitHub, notre pipeline installe les dépendances, exécute la suite de tests et publie un rapport. Le badge vert atteste que les vérifications passent sur la version actuelle du dépôt.

Notre démonstration montre qu'une IA peut aider à rédiger, tandis que la conformité reste contrôlée par du code et des tests reproductibles. »
