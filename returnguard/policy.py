"""Deterministic, fictional 30-day e-commerce returns policy.

It is illustrative workshop policy, NOT statutory consumer-rights advice.
Only orders with delivered status, standard goods, valid delivery ages, and no
reported defect are eligible for a *return request*, never an issued refund.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ORDERS_PATH = Path(__file__).resolve().parent.parent / "mocks" / "orders.json"
REVIEW_KEYWORDS = (
    "cassé", "casse", "endommag", "abîmé", "abime", "défectueux",
    "defectueux", "damaged", "broken", "defective", "wrong item",
    "mauvais produit", "colis perdu", "not received", "non reçu", "non recu",
)
RESTRICTED_CATEGORIES = {"hygiene", "digital"}


def load_mock_order(order_id: str) -> dict[str, Any] | None:
    """Find an order in an immutable simulated database. Never calls the network."""
    with ORDERS_PATH.open("r", encoding="utf-8") as f:
        orders = json.load(f)
    return orders.get(order_id)


def evaluate_policy(order: dict[str, Any] | None, message: str) -> dict[str, str]:
    """Enforce rules, returning a structured reason code and decision."""
    if order is None:
        return {"decision": "HUMAN_REVIEW", "reason_code": "ORDER_NOT_FOUND",
                "reason": "Commande introuvable dans la base de démonstration."}
    if not isinstance(message, str) or not message.strip():
        return {"decision": "HUMAN_REVIEW", "reason_code": "MESSAGE_MISSING",
                "reason": "Demande client absente ou vide."}
    if any(k in message.casefold() for k in REVIEW_KEYWORDS):
        return {"decision": "HUMAN_REVIEW", "reason_code": "EXCEPTION_REPORTED",
                "reason": "Problème produit ou livraison nécessitant une vérification humaine."}
    if order.get("status") != "delivered":
        return {"decision": "HUMAN_REVIEW", "reason_code": "NOT_DELIVERED",
                "reason": "La commande n'est pas confirmée comme livrée."}
    days = order.get("days_since_delivery")
    if isinstance(days, bool) or not isinstance(days, int) or days < 0:
        return {"decision": "HUMAN_REVIEW", "reason_code": "INVALID_ORDER_DATA",
                "reason": "Données de date de livraison manquantes ou invalides."}
    category = order.get("category")
    if category in RESTRICTED_CATEGORIES:
        return {"decision": "NOT_ELIGIBLE", "reason_code": "RESTRICTED_CATEGORY",
                "reason": "Catégorie exclue par la politique fictive de cet atelier."}
    if category != "standard":
        return {"decision": "HUMAN_REVIEW", "reason_code": "UNKNOWN_CATEGORY",
                "reason": "Catégorie non reconnue : une validation humaine est requise."}
    if days > 30:
        return {"decision": "NOT_ELIGIBLE", "reason_code": "WINDOW_EXPIRED",
                "reason": "Délai fictif de 30 jours dépassé."}
    return {"decision": "ELIGIBLE", "reason_code": "WITHIN_WINDOW",
            "reason": "La demande de retour respecte la politique fictive de 30 jours."}
