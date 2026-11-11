CodeAlpha Cloud Computing Internship
Task 2: Detecting Data Leaks Using SQL Injection (Secure Cloud Auth)

A double-layer security cloud authentication system designed to protect user credentials against SQL injection attacks and secure sensitive data at rest using AES-256 encryption.

---

Features
-Double-Layer Security Protocol:
-Combines secure input parameterization with AES-256 encryption to prevent data leaks.
-AES-256 Encryption:
-Encrypts user credentials and sensitive info at rest using a 32-byte cryptographic key and CBC mode.
-SQL Injection Neutralization:
-Parameterized queries completely block malicious evaluation vectors (such as `' OR '1'='1`).
-Lightweight Architecture:
-Accessible and operable over local or cloud environments without heavy dependencies beyond standard libraries and the `cryptography` package.

---

Project Structure
```text
CodeAlpha_SQLInjectionSecuritySystem/
│
├── App.py             Main authentication and security script
├── secure_cloud.db    Local SQLite database (auto-generated on first run)
└── README.md          Project documentation
