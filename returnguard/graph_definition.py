"""Shared workflow topology: source for graph implementation and JSON export."""
# The same declaration is the source for the JSON topology export.
NODES = ("lookup_order", "policy_check", "draft_response", "compliance_check")
EDGES = (
    ("__start__", "lookup_order"),
    ("lookup_order", "policy_check"),
    ("policy_check", "draft_response"),
    ("draft_response", "compliance_check"),
    ("compliance_check", "__end__"),
)

