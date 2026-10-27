"""Response conformity checks, including incorrect/mock model answers."""
import pytest
from returnguard.compliance import compliance_issues, validate_or_correct
from returnguard.response import safe_template

@pytest.fixture
def base_state():
    return {"order_id": "CMD-1001", "message": "Retour svp",
            "decision": "ELIGIBLE", "reason": "Dans les 30 jours"}


def test_safe_eligible_template_is_valid(base_state):
    response = safe_template(base_state)
    assert compliance_issues(base_state, response) == []


@pytest.mark.parametrize("decision", ["ELIGIBLE", "NOT_ELIGIBLE", "HUMAN_REVIEW"])
def test_safe_templates_all_decisions(base_state, decision):
    base_state["decision"] = decision
    assert compliance_issues(base_state, safe_template(base_state)) == []


@pytest.mark.parametrize("draft,expected_issue", [
    ("Salut", "MISSING_ORDER_REFERENCE"),
    ("CMD-1001 bonjour", "MISSING_DECISION_PHRASE"),
    ("", "EMPTY_RESPONSE"),
    ("CMD-1001 éligible au retour. Your refund issued!", "UNAUTHORIZED_REFUND_CLAIM"),
    ("CMD-1001 éligible au retour. remboursement garanti", "UNAUTHORIZED_REFUND_CLAIM"),
    ("CMD-1001 éligible au retour. guaranteed refund", "UNAUTHORIZED_REFUND_CLAIM"),
])
def test_detect_noncompliance(base_state, draft, expected_issue):
    assert expected_issue in compliance_issues(base_state, draft)


def test_validator_repairs_bad_response(base_state):
    result = validate_or_correct(base_state, "Your refund issued!")
    assert result["corrected"] is True
    assert result["compliant"] is True
    assert "éligible au retour" in result["response"]
    assert "UNAUTHORIZED_REFUND_CLAIM" in result["compliance_issues"]


def test_validator_preserves_valid_response(base_state):
    original = safe_template(base_state)
    result = validate_or_correct(base_state, original)
    assert result["response"] == original
    assert result["corrected"] is False
    assert result["compliant"] is True


@pytest.mark.parametrize("decision,draft", [
    ("ELIGIBLE", "CMD-1001 non éligible au retour malgré la décision"),
    ("NOT_ELIGIBLE", "CMD-1001 non éligible au retour, mais votre demande est éligible au retour"),
    ("HUMAN_REVIEW", "CMD-1001 examen humain, mais éligible au retour"),
])
def test_reject_contradictory_decision(base_state, decision, draft):
    base_state["decision"] = decision
    assert "CONTRADICTORY_DECISION" in compliance_issues(base_state, draft)
    result = validate_or_correct(base_state, draft)
    assert result["corrected"] and result["compliant"]
