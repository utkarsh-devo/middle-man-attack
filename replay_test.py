# replay_test.py - Test for replay vulnerabilities
from mitmproxy import http
import time

captured_requests = []
replay_count = 0

def request(flow: http.HTTPFlow) -> None:
    global replay_count
    if "w.3pati.in" in flow.request.pretty_host:
        if "NoLimitBonus" in flow.request.url:
            captured_requests.append({
                "url": flow.request.url,
                "headers": dict(flow.request.headers),
                "timestamp": time.time()
            })
            print(f"[CAPTURED] Bonus request saved (#{len(captured_requests)})")

def response(flow: http.HTTPFlow) -> None:
    global replay_count
    if "w.3pati.in" in flow.request.pretty_host:
        if hasattr(flow.request, "is_replay") and flow.request.is_replay:
            replay_count += 1
            print(f"[REPLAY #{replay_count}] Status: {flow.response.status_code}")