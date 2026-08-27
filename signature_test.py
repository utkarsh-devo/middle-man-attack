# signature_test.py - Detect and test signature protection
from mitmproxy import http

def request(flow: http.HTTPFlow) -> None:
    if "w.3pati.in" in flow.request.pretty_host:
        signature_params = ["sign", "signature", "sig", "hash", "hmac", "token", "auth"]
        found_signatures = []
        for param in signature_params:
            if param in flow.request.query:
                found_signatures.append(param)
                print(f"[SIGNATURE FOUND] Parameter: {param} = {flow.request.query[param]}")
        
        if found_signatures and "st3=" in flow.request.url:
            original_st3 = flow.request.query.get("st3", "")
            flow.request.query["st3"] = "9999999"
            print(f"[SIGNATURE TEST] Changed st3 from {original_st3} to 9999999 without updating signature")

def response(flow: http.HTTPFlow) -> None:
    if "w.3pati.in" in flow.request.pretty_host:
        if flow.response.status_code == 403 or flow.response.status_code == 400:
            print("  ✅ Signature protection detected!")
        elif flow.response.status_code == 200:
            print("  ⚠️ Server accepted request without proper signature!")