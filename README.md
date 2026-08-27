# MitmCertSaver — MITMProxy Security Testing Toolkit
 
> A lightweight Python-based security-testing toolkit built on [MITMProxy](https://www.mitmproxy.org/) for intercepting HTTP traffic, managing CA certificates, modifying request parameters, and testing application behaviour against manipulated traffic.
 
---
 
## ⚠️ Disclaimer
 
This project is intended **only for authorized security testing, cybersecurity labs, CTFs, and applications or networks that you own or have explicit permission to test.**
 
Do not use this project to intercept, modify, or inspect traffic belonging to other users or systems without authorization.
 
---
 
## Table of Contents
 
- [Overview](#overview)
- [Project Goals](#project-goals)
- [How It Works](#how-it-works)
- [Features](#features)
- [Testing Framework](#testing-framework)
- [Response Analysis](#response-analysis)
- [Project Structure](#project-structure)
- [Technology Stack](#technology-stack)
- [Installation](#installation)
- [Running Security Tests](#running-security-tests)
- [Security Considerations](#security-considerations)
- [Current Limitations](#current-limitations)
- [Future Scope](#future-scope)
- [Contributing](#contributing)
- [License](#license)
- [Author](#author)
---
 
## Overview
 
**MitmCertSaver** addresses a practical problem encountered while working with MITMProxy: obtaining the generated CA certificate can be inconvenient through the standard browser-based `mitm.it` workflow.
 
The project automatically searches for the MITMProxy CA certificate at:
 
```
~/.mitmproxy/mitmproxy-ca-cert.pem
```
 
and copies it into the project directory as `mitmproxy_certificate.pem`.
 
Alongside certificate handling, the project includes several MITMProxy-based scripts that demonstrate how intercepted HTTP requests can be inspected, logged, modified, fuzzed, and evaluated.
 
---
 
## Project Goals
 
- Automate MITMProxy certificate extraction
- Intercept HTTP requests and responses
- Observe and log request parameters
- Test whether request parameters can be manipulated
- Test application behaviour against unexpected input
- Perform basic fuzz testing
- Record and store security test results
- Detect suspicious or unexpected server responses
- Provide a reusable environment for authorized security testing
---
 
## How It Works
 
The basic request/response lifecycle through the proxy is:
 
```
Client
  │
  ▼
MITMProxy
  │
  ▼
Python Script
  ├── Inspect request
  ├── Modify parameters
  ├── Log request
  └── Forward request
          │
          ▼
     Target Server
          │
          ▼
       Response
          │
          ▼
      MITMProxy
          │
          ▼
        Client
```
 
### Certificate Automation
 
MITMProxy generates its CA certificate in the user's home directory. This project automatically locates:
 
```
~/.mitmproxy/mitmproxy-ca-cert.pem
```
 
and copies it to:
 
```
./mitmproxy_certificate.pem
```
 
This is handled using Python's `os` and `pathlib` modules.
 
---
 
## Features
 
### 1. Automatic Certificate Extraction
 
Automatically locates and copies the MITMProxy CA certificate, eliminating the need to manually navigate to the MITMProxy certificate page.
 
**Output:** `mitmproxy_certificate.pem`
 
---
 
### 2. HTTP Request Interception
 
The main interceptor inspects HTTP requests and responses passing through MITMProxy, logging output in the form:
 
```
[REQUEST] GET <URL>
[RESPONSE] 200 <URL>
```
 
---
 
### 3. Request Parameter Manipulation
 
The testing scripts can modify selected request parameters before forwarding the request. For example, the test suite demonstrates modifications to parameters such as `st3`, `uid`, and `n`, and can inject additional parameters to evaluate how the target application handles unexpected input.
 
---
 
### 4. Security Test Automation
 
The security testing script automates and records the following categories of tests:
 
| Test Category | Description |
|---|---|
| Parameter Modification | Attempts different values for selected parameters |
| Event Manipulation | Tests whether event-related parameters can be changed |
| Parameter Pollution | Adds extra parameters to evaluate server-side handling |
| Extra Parameter Injection | Injects unexpected parameters into requests |
| Special Character / Path Input | Tests special and path-like input against request handling |
| Response Inspection | Evaluates server responses to manipulated requests |
 
Each recorded result includes: **Attack Type · Original Request · Modified Request · Result · Timestamp**
 
---
 
## Testing Framework
 
The repository contains multiple independent test scripts, each targeting a specific testing scenario.
 
### `combined_test.py`
 
Runs multiple security tests through a single MITMProxy interceptor.
 
**Included tests:**
- `st3` parameter modification
- UID manipulation
- Additional parameter injection
- Event name manipulation
- Response checking
**Test flow:**
 
```
Original Request → Modify Parameter → Forward Request → Inspect Response → Determine Result
```
 
---
 
### `security_test.py`
 
A broader security-testing framework that maintains a collection of test results and logs each test with its attack type, request details, and outcome.
 
---
 
### `fuzz_test.py`
 
Tests how the application responds to unexpected and extreme input values.
 
**Test data categories:**
 
- Very large numbers
- Negative values
- Floating-point values
- Special characters
- Long strings
- Unicode characters
- Malformed input
- SQL-like strings
- HTML / script-like strings
- Path-like strings
---
 
## Response Analysis
 
All test scripts inspect server responses and HTTP status codes to determine how the application reacted to manipulated requests.
 
| Status Code | Interpretation |
|---|---|
| `200` | Request accepted |
| `400–499` | Request rejected / client-side error |
| `500+` | Server-side error |
 
The scripts also scan response content for keywords such as `error` and `success` to further classify results.
 
---
 
## Project Structure
 
```
middle-man-attack/
│
├── .vscode/
├── __pycache__/
│
├── script.py               # Main MITMProxy interceptor
├── combined_test.py        # Combined multi-test interceptor
├── security_test.py        # Broader security testing framework
├── fuzz_test.py            # Fuzz testing script
├── replay_test.py          # Request replay testing
├── signature_test.py       # Signature/integrity testing
├── uid_test.py             # UID-specific testing
│
├── json_logger.py          # JSON-based result logging
├── test_logger.py          # General test logging utility
│
├── results.json            # Stored test results
├── requirements.txt        # Python dependencies
├── README.md
│
├── .gitattributes
└── tempCodeRunnerFile.py
```
 
---
 
## Technology Stack
 
| Technology | Purpose |
|---|---|
| Python 3 | Core implementation |
| MITMProxy | HTTP traffic interception |
| JSON | Test result storage |
| `pathlib` | File and path handling |
| `os` | Certificate file operations |
| `datetime` | Test timestamps |
| `random` | Randomized test inputs |
| `urllib.parse` | URL and query parameter handling |
 
---
 
## Installation
 
### Prerequisites
 
- Python 3
- MITMProxy — install from [mitmproxy.org](https://www.mitmproxy.org/)
### Steps
 
**1. Clone the repository**
 
```bash
git clone https://github.com/utkarsh-devo/middle-man-attack.git
cd middle-man-attack
```
 
**2. Install Python dependencies**
 
```bash
pip install -r requirements.txt
```
 
**3. Start MITMProxy once to generate the CA certificate**
 
```bash
mitmweb
```
 
This creates the certificate directory at `~/.mitmproxy/`.
 
**4. Run the main interceptor**
 
```bash
mitmweb -s script.py
```
 
---
 
## Running Security Tests
 
Run any individual test script by passing it to MITMProxy with the `-s` flag.
 
```bash
# Security tests
mitmweb -s security_test.py
 
# Combined tests
mitmweb -s combined_test.py
 
# Fuzz tests
mitmweb -s fuzz_test.py
```
 
> ⚠️ Run these tests **only against systems you own or are explicitly authorized to test.**
 
---
 
## Security Considerations
 
This project is an educational and security-testing tool — not a production proxy or defensive product.
 
- Use only on authorized targets
- Do not intercept traffic belonging to other users
- Do not install certificates on systems you do not control
- Do not use the scripts against third-party services without permission
- Test in an isolated lab environment whenever possible
- Remove generated certificates from systems where they are no longer needed
---
 
## Current Limitations
 
The current implementation is focused on experimentation and authorized testing. Planned improvements include:
 
- Better structured logging
- Centralized test configuration
- HTML test reports
- Automatic result summarization
- More robust certificate management
- Configurable target selection (currently requires manual editing)
- Test-case configuration through JSON or YAML
- Improved response analysis
- Automated regression testing
- Safer isolated laboratory configuration
---
 
## Future Scope
 
The project can be extended into a more complete security-testing framework:
 
```
Traffic Capture
      ↓
Request Classification
      ↓
Automated Test Generation
      ↓
Request Mutation
      ↓
Response Analysis
      ↓
Vulnerability Indicators
      ↓
Report Generation
```
 
---
 
## Contributing
 
Contributions are welcome for:
 
- New security test modules
- Improved logging
- Better documentation
- Additional response analysis
- Test automation improvements
- Bug fixes
- Lab and demo configuration improvements
Please test all changes in an authorized environment before submitting a pull request.
 
---
 
## License
 
*License not yet specified. Update this section before treating the repository as a public open-source project.*
 
---
 
## Author
 
**Utkarsh**
 
GitHub: [utkarsh-devo](https://github.com/utkarsh-devo)
 
---
 
*Built for learning, experimentation, and authorized security testing.*
