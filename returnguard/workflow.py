"""Four-node executable LangGraph with mockable response generation."""
from __future__ import annotations

from typing import Any, Callable, TypedDict
from langgraph.graph import StateGraph, START, END

from .policy import evaluate_policy, load_mock_order
from .response import optional_openai_writer, safe_template
from .compliance import validate_or_correct

from .graph_definition import NODES, EDGES

class ReturnState(TypedDict, total=False):
    order_id: str
    message: str
    order: dict[str, Any] | None
    decision: str
    reason_code: str
    reason: str
    draft_response: str
    response: str
    compliant: bool
    corrected: bool
    compliance_issues: list[str]


def build_graph(writer: Callable[[dict[str, Any]], str] | None = None):
    """Provide writer injection to test bad AI output without contacting an API."""
    chosen_writer = writer or optional_openai_writer

    def lookup(state: ReturnState) -> dict[str, Any]:
        return {"order": load_mock_order(state["order_id"])}

    def decide(state: ReturnState) -> dict[str, Any]:
        return evaluate_policy(state.get("order"), state.get("message", ""))

    def draft(state: ReturnState) -> dict[str, Any]:
        try:
            text = chosen_writer(state)
        except Exception:
            # Fail-safe: a writer exception must never bypass compliance checks.
            text = safe_template(state)
        return {"draft_response": text}

    def guard(state: ReturnState) -> dict[str, Any]:
        return validate_or_correct(state, state.get("draft_response", ""))

    builder = StateGraph(ReturnState)
    builder.add_node("lookup_order", lookup)
    builder.add_node("policy_check", decide)
    builder.add_node("draft_response", draft)
    builder.add_node("compliance_check", guard)
    builder.add_edge(START, "lookup_order")
    builder.add_edge("lookup_order", "policy_check")
    builder.add_edge("policy_check", "draft_response")
    builder.add_edge("draft_response", "compliance_check")
    builder.add_edge("compliance_check", END)
    return builder.compile()


def run_request(order_id: str, message: str, *, writer=None) -> ReturnState:
    graph = build_graph(writer=writer)
    return graph.invoke({"order_id": order_id, "message": message})
