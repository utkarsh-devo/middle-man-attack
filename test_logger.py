# test_logger.py - Log test results to JSON
from mitmproxy import http
import json
import os
from datetime import datetime

RESULTS_FILE = "test_results.json"

def load_results():
    """Load existing results or create new"""
    if os.path.exists(RESULTS_FILE):
        with open(RESULTS_FILE, 'r') as f:
            return json.load(f)
    else:
        return {
            "test_session": {
                "start_time": datetime.now().isoformat(),
                "game": "Unity Game (w.3pati.in)",
                "domain": "w.3pati.in",
                "tester": "Security Analyst"
            },
            "summary": {
                "total_tests": 0,
                "vulnerabilities": 0,
                "safe": 0,
                "pending": 0
            },
            "tests": [],
            "findings": []
        }

def save_results(data):
    """Save results to JSON file"""
    with open(RESULTS_FILE, 'w') as f:
        json.dump(data, f, indent=2)
    print(f"[✓] Results saved to {RESULTS_FILE}")

def log_test_result(test_name, category, status, result, is_vulnerable=False, notes=""):
    """Log a test result"""
    data = load_results()
    
    test_entry = {
        "test_id": len(data["tests"]) + 1,
        "test_name": test_name,
        "category": category,
        "status": status,  # "PENDING", "PASS", "FAIL", "VULNERABLE"
        "result": result,
        "is_vulnerable": is_vulnerable,
        "notes": notes,
        "timestamp": datetime.now().isoformat()
    }
    
    data["tests"].append(test_entry)
    
    # Update summary
    data["summary"]["total_tests"] += 1
    if status == "VULNERABLE":
        data["summary"]["vulnerabilities"] += 1
    elif status == "PASS":
        data["summary"]["safe"] += 1
    else:
        data["summary"]["pending"] += 1
    
    save_results(data)
    print(f"[✓] Logged test: {test_name} ({status})")

# Example of using this in your interception script
def request(flow: http.HTTPFlow) -> None:
    if "w.3pati.in" in flow.request.pretty_host and "SourceChips" in flow.request.url:
        # Check if we modified st3
        if flow.request.query.get("st3") == "9999999":
            log_test_result(
                "st3_modification",
                "Parameter Tampering",
                "PENDING",
                "Modified st3 to 9999999, waiting for response",
                False
            )

def response(flow: http.HTTPFlow) -> None:
    if "w.3pati.in" in flow.request.pretty_host:
        # Check response for modifications
        if flow.request.query.get("st3") == "9999999":
            if "9999999" in flow.response.text:
                log_test_result(
                    "st3_modification",
                    "Parameter Tampering",
                    "VULNERABLE",
                    "Server returned modified value 9999999!",
                    True,
                    "Server accepted client-provided st3 value"
                )
            else:
                log_test_result(
                    "st3_modification",
                    "Parameter Tampering",
                    "PASS",
                    "Server ignored modified value",
                    False,
                    "Server maintains own value - secure"
                )