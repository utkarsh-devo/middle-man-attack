# json_logger.py - Log all requests to JSON file
from mitmproxy import http
import json
import os
from datetime import datetime
from pathlib import Path

# Set up the log file path
LOG_FILE = "request_log.json"
RESULTS_FILE = "test_results.json"

def ensure_file_exists():
    """Create JSON file if it doesn't exist"""
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'w') as f:
            json.dump({"requests": [], "total_count": 0}, f, indent=2)

def log_request(flow: http.HTTPFlow):
    """Log request details to JSON file"""
    try:
        ensure_file_exists()
        
        # Load existing log
        with open(LOG_FILE, 'r') as f:
            data = json.load(f)
        
        # Extract query parameters
        query_params = {}
        for key, value in flow.request.query.items():
            query_params[key] = value
        
        # Create log entry
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "url": flow.request.url,
            "method": flow.request.method,
            "host": flow.request.pretty_host,
            "path": flow.request.path,
            "headers": dict(flow.request.headers),
            "query_params": query_params,
            "response_status": None,
            "response_size": 0
        }
        
        # Add to log
        data["requests"].append(log_entry)
        data["total_count"] = len(data["requests"])
        
        # Save
        with open(LOG_FILE, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"[LOGGED] #{data['total_count']}: {flow.request.url}")
        
    except Exception as e:
        print(f"[ERROR] Failed to log: {e}")

def log_response(flow: http.HTTPFlow):
    """Update log with response details"""
    try:
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, 'r') as f:
                data = json.load(f)
            
            if data["requests"]:
                # Update the last request with response data
                last_request = data["requests"][-1]
                if last_request["url"] == flow.request.url:
                    last_request["response_status"] = flow.response.status_code
                    last_request["response_size"] = len(flow.response.text) if flow.response.text else 0
            
            with open(LOG_FILE, 'w') as f:
                json.dump(data, f, indent=2)
    except Exception as e:
        print(f"[ERROR] Failed to log response: {e}")

def request(flow: http.HTTPFlow) -> None:
    """Called when a request is intercepted"""
    # Only log w.3pati.in requests
    if "w.3pati.in" in flow.request.pretty_host:
        log_request(flow)

def response(flow: http.HTTPFlow) -> None:
    """Called when a response is received"""
    if "w.3pati.in" in flow.request.pretty_host:
        log_response(flow)
                                                                                                                                      