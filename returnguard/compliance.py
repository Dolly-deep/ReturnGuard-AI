"""Response validator: automatic correction if a draft violates constraints."""
from __future__ import annotations

from typing import Any
from .response import REQUIRED_PHRASE, safe_template

FORBIDDEN_PHRASES = (
    "remboursement effectué", "remboursement est effectué", "refund issued",
    "refund completed", "refund guaranteed", "guaranteed refund",
    "we have issued your refund", "your refund is processed",
    "remboursement garanti", "remboursement a été traité",
)


def compliance_issues(state: dict[str, Any], draft: str) -> list[str]:
    issues: list[str] = []
    if not isinstance(draft, str) or not draft.strip():
        return ["EMPTY_RESPONSE"]
    response = draft.casefold()
    if state["order_id"].casefold() not in response:
        issues.append("MISSING_ORDER_REFERENCE")
    expected = REQUIRED_PHRASE[state["decision"]]
    if expected.casefold() not in response:
        issues.append("MISSING_DECISION_PHRASE")
    decision = state["decision"]
    # A model must not reverse the policy decision while including mandatory words.
    if ((decision == "ELIGIBLE" and "non éligible au retour" in response)
            or (decision == "NOT_ELIGIBLE" and "votre demande est éligible au retour" in response)
            or (decision == "HUMAN_REVIEW" and "éligible au retour" in response)):
        issues.append("CONTRADICTORY_DECISION")
    if any(phrase in response for phrase in FORBIDDEN_PHRASES):
        issues.append("UNAUTHORIZED_REFUND_CLAIM")
    return issues


def validate_or_correct(state: dict[str, Any], draft: str) -> dict[str, Any]:
    issues = compliance_issues(state, draft)
    response = safe_template(state) if issues else draft
    # A fallback must also be subject to the same validator.
    fallback_issues = compliance_issues(state, response)
    return {
        "response": response,
        "compliant": not fallback_issues,
        "corrected": bool(issues),
        "compliance_issues": issues + fallback_issues,
    }
