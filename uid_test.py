# uid_test.py - Test for broken authentication
from mitmproxy import http

def request(flow: http.HTTPFlow) -> None:
    if "w.3pati.in" in flow.request.pretty_host and "uid=" in flow.request.url:
        original_uid = flow.request.query.get("uid", "unknown")
        test_uids = ["12345678", "99999999", "11111111", "00000000"]
        new_uid = test_uids[hash(flow.request.url) % len(test_uids)]
        flow.request.query["uid"] = new_uid
        print(f"[UID TEST] Changed from {original_uid} to {new_uid}")

def response(flow: http.HTTPFlow) -> None:
    if "w.3pati.in" in flow.request.pretty_host:
        print(f"[UID TEST RESPONSE] Status: {flow.response.status_code}")