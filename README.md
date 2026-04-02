🛡️ Tamper-Evident Logging System
Traditional log files (.txt, .csv) are fundamentally flawed in high-security environments: a rogue insider with file-system access can easily alter, delete, or rearrange entries to cover their tracks.

This project simulates a real-world Secure Audit Logging System. It uses cryptographic chaining (similar to a blockchain) to ensure that if a single byte of a log entry is changed, the entire chain of custody is broken and the tampering is instantly detected.

🎯 Key Features
Cryptographic Chaining: Every log entry contains the SHA-256 hash of the previous entry.
Collision Resistance: Utilizes a randomized nonce for every entry to prevent hash collisions on identical events.
Comprehensive Detection: Catches in-place modifications, deleted entries, and rearranged logs.
Zero False Positives: Verification relies on pure mathematics, ensuring absolute trust in the audit trail.
🏗️ How It Works
Instead of just writing text to a file, the system creates a JSON object for every event:

Ingest: System receives event data (Timestamp, Event Type, Description).
Link: It looks up the current_hash of the most recent log and assigns it as the new entry's previous_hash.
Salting (Nonce): Generates a random string to ensure unique hashing.
Seal: Hashes all combined data (Index + Timestamp + Event + Previous Hash + Nonce) using SHA-256 to create the current_hash.
Store: Appends the sealed JSON object to secure_audit_log.json.
[ Log 1 ]             [ Log 2 ]             [ Log 3 ]Prev: 0000...         Prev: Hash(1)         Prev: Hash(2)Data: "Login..."      Data: "File Access"   Data: "Logout..."Hash: abc123...  ---> Hash: def456...  ---> Hash: ghi789...
If "File Access" is changed to "Deleted File", Hash(2) becomes xyz999. The system sees Hash(2) != def456 and triggers a TAMPER ALERT.

🎬 Proof of Concept
1. Adding Logs & Verifying Integrity
[Insert a 5-to-10 second GIF here showing you running the script, logs being added, and the "Audit Complete: Log integrity is 100% intact" message]

2. Catching Tampering In-Action
[Insert a screenshot here showing you manually editing the JSON file (e.g., changing a username from "admin" to "hacker"), saving it, running the verify script, and showing the "TAMPERING DETECTED" output]

⚡ Quick Start
Prerequisites: Python 3.6+ installed.
# 1. Clone the repository
git clone https://github.com/[YourUsername]/Tamper-Evident-Logger.git
cd Tamper-Evident-Logger

# 2. Run the logger to generate sample logs
python secure_logger.py

# 3. Verify the logs are secure
# (Try modifying secure_audit_log.json manually before running this!)
python secure_logger.py --verify


📄 Documentation & Threat Model
As part of the cybersecurity assessment, a comprehensive 2500-word report was written detailing the design decisions, algorithm logic, edge-case handling, and limitations of this system.


🛠️ Tech Stack
Language: Python 3
Cryptography: hashlib (SHA-256)
Data Structure: JSON
