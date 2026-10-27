"""Exports the executable graph's declared topology and policy metadata.

LangGraph has no native re-importable AgenticAI-style project JSON here.
This is a documentation/topology JSON export. Python code is the executable.
"""
import json
from pathlib import Path
from returnguard.graph_definition import EDGES, NODES

export = {
    "project": "ReturnGuard AI",
    "framework": "LangGraph (Python)",
    "export_type": "topology_and_policy_metadata_not_reimportable",
    "implementation": "returnguard/workflow.py",
    "nodes": [{"id": name, "type": "python_function"} for name in NODES],
    "edges": [{"source": source, "target": target} for source, target in EDGES],
    "policy": {"return_window_days_inclusive": 30, "eligible_category": "standard",
               "excluded_categories": ["digital", "hygiene"],
               "possible_decisions": ["ELIGIBLE", "NOT_ELIGIBLE", "HUMAN_REVIEW"]},
    "mocks": ["mocks/orders.json", "Mock AI writer injected in tests"],
    "checks": ["order_id presence", "expected decision wording", "forbidden refund claims"]
}
path = Path(__file__).resolve().parent / "workflow_export.json"
path.write_text(json.dumps(export, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"Export generated: {path}")
