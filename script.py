# -*- coding: utf-8 -*-
import os
from pathlib import Path

from mitmproxy import http

def request(flow: http.HTTPFlow) -> None:
    if "SourceChips" in flow.request.url:
        print(f"\n[!] Chips request intercepted!")
        original_url = flow.request.url
        print(f"[*] Original: {original_url}")
        
        

def response(flow: http.HTTPFlow) -> None:
    if "SourceChips" in flow.request.url:
        print(f"[*] Response status: {flow.response.status_code}")
        print("-" * 50)

BASE_DIR = Path(__file__).parent

# -------------------------------
# Save the mitmproxy certificate
# -------------------------------
def save_mitmproxy_cert():
    try:
        home = os.path.expanduser("~/.mitmproxy")
        ca_cert = os.path.join(home, "mitmproxy-ca-cert.pem")
        output_file = BASE_DIR / "mitmproxy_certificate.pem"

        if os.path.exists(ca_cert):
            with open(ca_cert, "rb") as src, open(output_file, "wb") as dst:
                dst.write(src.read())
            print(f"[CERT] Certificate copied to: {output_file}")
        else:
            print("[CERT] CA file not found in ~/.mitmproxy")
    except Exception as e:
        print(f"[CERT ERROR] {e}")

save_mitmproxy_cert()

# -------------------------------
# Empty / minimal interceptor
# -------------------------------
class SimpleInterceptor:
    def request(self, flow: http.HTTPFlow):
        print(f"[REQUEST] {flow.request.method} {flow.request.pretty_url}")

    def response(self, flow: http.HTTPFlow):
        print(f"[RESPONSE] {flow.response.status_code} {flow.request.pretty_url}")

addons = [
    SimpleInterceptor()
]
