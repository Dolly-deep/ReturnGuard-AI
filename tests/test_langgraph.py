"""Real end-to-end LangGraph tests (run when dependency is available, including CI)."""
import pytest
pytest.importorskip("langgraph", reason="Install requirements to execute LangGraph integration tests")
from returnguard.workflow import run_request, build_graph, NODES, EDGES

@pytest.mark.parametrize("order_id,message,expected", [
    ("CMD-1001", "Je veux retourner", "ELIGIBLE"),
    ("CMD-1003", "Je veux retourner", "NOT_ELIGIBLE"),
    ("CMD-1005", "Je veux retourner", "NOT_ELIGIBLE"),
    ("CMD-1001", "Mon article est cassé", "HUMAN_REVIEW"),
    ("CMD-9999", "Je veux retourner", "HUMAN_REVIEW"),
])
def test_graph_end_to_end(order_id, message, expected):
    result = run_request(order_id, message, writer=lambda state: "bad draft")
    assert result["decision"] == expected
    assert result["compliant"] is True
    assert result["corrected"] is True
    assert order_id in result["response"]


def test_adversarial_writer_cannot_issue_refund():
    result = run_request("CMD-1001", "Retour", writer=lambda s: (
        "CMD-1001 éligible au retour. We have issued your refund"))
    assert result["corrected"] is True
    assert "issued your refund" not in result["response"].lower()


def test_writer_exception_fails_safe():
    def crash(_state):
        raise RuntimeError("mock LLM timeout")
    result = run_request("CMD-1001", "Retour", writer=crash)
    assert result["compliant"] is True
    assert result["response"]


def test_graph_contains_expected_nodes():
    graph = build_graph(writer=lambda s: "")
    actual = set(graph.get_graph().nodes.keys())
    assert set(NODES).issubset(actual)
    assert len(EDGES) == 5
