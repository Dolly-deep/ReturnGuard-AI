"""Run with: python demo.py [ORDER_ID] [MESSAGE]"""
import json
import sys
from returnguard.workflow import run_request

order_id = sys.argv[1] if len(sys.argv) > 1 else "CMD-1001"
message = sys.argv[2] if len(sys.argv) > 2 else "Bonjour, je souhaite retourner mon produit."
result = run_request(order_id, message)
output_fields = ("order_id", "decision", "reason_code", "reason", "response", "compliant", "corrected", "compliance_issues")
print(json.dumps({key: result.get(key) for key in output_fields}, ensure_ascii=False, indent=2))
