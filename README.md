## 🛡️ Tamper-Evident Logging System
Traditional log files rely on trust. If a rogue insider alters a .txt or .csv log, the change is invisible. This project eliminates trust by using cryptographic chaining (SHA-256) to ensure that if a single byte of a log entry is changed, the tampering is instantly detected.

### 🎯 Key Features
Cryptographic Chaining: Every log entry contains the SHA-256 hash of the previous entry.
Collision Resistance: Utilizes a randomized nonce to prevent hash collisions on identical events.
Comprehensive Detection: Catches in-place modifications, deleted entries, and rearranged logs.
Zero False Positives: Verification relies on pure mathematics, ensuring absolute trust in the audit trail.

### 📄 Deep-Dive Technical Whitepaper
For the system architecture, threat modeling, and edge-case analysis, read the full technical document: https://docs.google.com/document/d/1ishEfiZe0uBRfICslhmTV6NcydIcrfwtOXPhQ0z5Tqw/edit?tab=t.0

