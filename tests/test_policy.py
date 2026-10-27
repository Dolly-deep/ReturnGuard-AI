"""Thirty-plus independent business scenarios, tested without external services."""
import pytest
from returnguard.policy import evaluate_policy, load_mock_order

# Case matrix includes order states, deadline boundaries and defect escalation.
CASES = [
    ("CMD-1001", "Je souhaite un retour", "ELIGIBLE", "WITHIN_WINDOW"),
    ("CMD-1001", "Please return my item", "ELIGIBLE", "WITHIN_WINDOW"),
    ("CMD-1001", "Produit non adapté", "ELIGIBLE", "WITHIN_WINDOW"),
    ("CMD-1001", "Le produit ne me convient pas", "ELIGIBLE", "WITHIN_WINDOW"),
    ("CMD-1002", "Je veux retourner mon achat", "ELIGIBLE", "WITHIN_WINDOW"),
    ("CMD-1002", "Retour au 30e jour", "ELIGIBLE", "WITHIN_WINDOW"),
    ("CMD-1003", "Retour demandé", "NOT_ELIGIBLE", "WINDOW_EXPIRED"),
    ("CMD-1003", "Produit en retard", "NOT_ELIGIBLE", "WINDOW_EXPIRED"),
    ("CMD-1004", "Retour d'une commande envoyée", "HUMAN_REVIEW", "NOT_DELIVERED"),
    ("CMD-1005", "Demande de retour", "NOT_ELIGIBLE", "RESTRICTED_CATEGORY"),
    ("CMD-1005", "Return please", "NOT_ELIGIBLE", "RESTRICTED_CATEGORY"),
    ("CMD-1006", "Je souhaite renvoyer", "NOT_ELIGIBLE", "RESTRICTED_CATEGORY"),
    ("CMD-1007", "Retour le jour de livraison", "ELIGIBLE", "WITHIN_WINDOW"),
    ("CMD-1008", "Je voudrais retourner", "HUMAN_REVIEW", "NOT_DELIVERED"),
    ("CMD-1009", "Demande ordinaire", "ELIGIBLE", "WITHIN_WINDOW"),
    ("CMD-1010", "Retour d'article de toilette", "NOT_ELIGIBLE", "RESTRICTED_CATEGORY"),
    ("CMD-1011", "Retour d'un produit", "HUMAN_REVIEW", "INVALID_ORDER_DATA"),
    ("CMD-1012", "Retour d'une commande annulée", "HUMAN_REVIEW", "NOT_DELIVERED"),
    ("CMD-1013", "Retour d'une catégorie inconnue", "HUMAN_REVIEW", "UNKNOWN_CATEGORY"),
    ("CMD-9999", "Où est ma commande ?", "HUMAN_REVIEW", "ORDER_NOT_FOUND"),
    ("CMD-1001", "Le produit est cassé", "HUMAN_REVIEW", "EXCEPTION_REPORTED"),
    ("CMD-1001", "Le produit est endommagé", "HUMAN_REVIEW", "EXCEPTION_REPORTED"),
    ("CMD-1001", "Article défectueux", "HUMAN_REVIEW", "EXCEPTION_REPORTED"),
    ("CMD-1001", "My item is broken", "HUMAN_REVIEW", "EXCEPTION_REPORTED"),
    ("CMD-1001", "My item is damaged", "HUMAN_REVIEW", "EXCEPTION_REPORTED"),
    ("CMD-1001", "I received the wrong item", "HUMAN_REVIEW", "EXCEPTION_REPORTED"),
    ("CMD-1001", "J'ai reçu un mauvais produit", "HUMAN_REVIEW", "EXCEPTION_REPORTED"),
    ("CMD-1003", "Le produit est cassé et date de 31 jours", "HUMAN_REVIEW", "EXCEPTION_REPORTED"),
    ("CMD-1005", "Je l'ai reçu défectueux", "HUMAN_REVIEW", "EXCEPTION_REPORTED"),
    ("CMD-1001", "", "HUMAN_REVIEW", "MESSAGE_MISSING"),
    ("CMD-1001", "   ", "HUMAN_REVIEW", "MESSAGE_MISSING"),
    ("CMD-1001", "Colis perdu", "HUMAN_REVIEW", "EXCEPTION_REPORTED"),
    ("CMD-1001", "Package not received", "HUMAN_REVIEW", "EXCEPTION_REPORTED"),
]

@pytest.mark.parametrize("order_id,message,decision,reason", CASES,
                         ids=[f"business_case_{i:02d}" for i in range(1, len(CASES) + 1)])
def test_business_case(order_id, message, decision, reason):
    result = evaluate_policy(load_mock_order(order_id), message)
    assert result["decision"] == decision
    assert result["reason_code"] == reason
    assert result["reason"]

@pytest.mark.parametrize("days,expected", [
    (0, "ELIGIBLE"), (1, "ELIGIBLE"), (29, "ELIGIBLE"),
    (30, "ELIGIBLE"), (31, "NOT_ELIGIBLE"), (365, "NOT_ELIGIBLE"),
    (-1, "HUMAN_REVIEW"), (None, "HUMAN_REVIEW"),
    (True, "HUMAN_REVIEW"), ("10", "HUMAN_REVIEW"),
])
def test_day_boundaries(days, expected):
    order = {"status": "delivered", "days_since_delivery": days, "category": "standard"}
    assert evaluate_policy(order, "Je souhaite retourner")["decision"] == expected


def test_mock_data_exists():
    assert load_mock_order("CMD-1001")["status"] == "delivered"


def test_order_missing_from_mock():
    assert load_mock_order("NO_SUCH_ORDER") is None


def test_no_message_does_not_auto_approve():
    order = load_mock_order("CMD-1001")
    assert evaluate_policy(order, None)["decision"] == "HUMAN_REVIEW"
