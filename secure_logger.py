import json
import hashlib
import time
import secrets
import os

LOG_FILE = "secure_audit_log.json"

# --- Terminal Colors for nice output ---
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
RESET = '\033[0m'

def calculate_hash(index, timestamp, event_type, description, previous_hash, nonce):
    """Creates a SHA-256 hash of the log data."""
    data_string = f"{index}{timestamp}{event_type}{description}{previous_hash}{nonce}"
    return hashlib.sha256(data_string.encode('utf-8')).hexdigest()

def load_logs():
    """Loads existing logs from the JSON file."""
    if not os.path.exists(LOG_FILE):
        return []
    try:
        with open(LOG_FILE, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        print(f"{RED}[ERROR] Log file is corrupted (invalid JSON).{RESET}")
        return []

def save_logs(logs):
    """Saves logs to the JSON file with nice formatting."""
    with open(LOG_FILE, 'w') as f:
        json.dump(logs, f, indent=4)

def add_log(event_type, description):
    """Adds a new cryptographically sealed log entry."""
    logs = load_logs()
    
    # Determine the previous hash (Genesis block starts with 64 zeros)
    previous_hash = "0" * 64
    index = 0
    if len(logs) > 0:
        last_log = logs[-1]
        index = last_log['index']
        previous_hash = last_log['current_hash']

    # Build the new log entry
    new_index = index + 1
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    nonce = secrets.token_hex(16) # Cryptographically secure random string
    
    # Calculate the seal
    current_hash = calculate_hash(new_index, timestamp, event_type, description, previous_hash, nonce)

    new_entry = {
        "index": new_index,
        "timestamp": timestamp,
        "event_type": event_type,
        "description": description,
        "previous_hash": previous_hash,
        "nonce": nonce,
        "current_hash": current_hash
    }

    logs.append(new_entry)
    save_logs(logs)
    print(f"{GREEN}[+]{RESET} Log #{new_index} added securely. | Hash: {current_hash[:20]}...")

def verify_chain():
    """Verifies the entire log history to detect ANY tampering."""
    logs = load_logs()
    
    if not logs:
        print(f"{YELLOW}[*]{RESET} No logs found to verify.")
        return True

    print(f"{YELLOW}[*]{RESET} Initiating Audit Check on {len(logs)} log entries...")

    for i in range(len(logs)):
        current = logs[i]
        
        # CHECK 1: Are we missing a log? (Catches deletions/reordering)
        if current['index'] != i + 1:
            print(f"{RED}[!!!] TAMPERING DETECTED:{RESET} Log index mismatch! Expected {i+1}, found {current['index']}. (Log deleted or rearranged)")
            return False

        # CHECK 2: Is the chain broken? (Catches modifications to previous logs)
        expected_prev_hash = "0" * 64 if i == 0 else logs[i-1]['current_hash']
        if current['previous_hash'] != expected_prev_hash:
            print(f"{RED}[!!!] TAMPERING DETECTED:{RESET} Chain broken at Log #{current['index']}. Previous log was altered or deleted.")
            return False

        # CHECK 3: Is the current seal valid? (Catches in-place editing of this specific log)
        recalculated_hash = calculate_hash(
            current['index'], 
            current['timestamp'], 
            current['event_type'], 
            current['description'], 
            current['previous_hash'], 
            current['nonce']
        )
        
        if recalculated_hash != current['current_hash']:
            print(f"{RED}[!!!] TAMPERING DETECTED:{RESET} Log #{current['index']} was modified in-place!")
            return False

    print(f"{GREEN}[+] AUDIT COMPLETE: Log integrity is 100% intact. No tampering found.{RESET}")
    return True

if __name__ == "__main__":
    print("--- 1. GENERATING SECURE LOGS ---")
    add_log("LOGIN_SUCCESS", "User 'admin' logged in from 192.168.1.50")
    add_log("FILE_ACCESS", "User 'admin' read /etc/passwd")
    add_log("LOGIN_FAILURE", "Failed login for 'root' from 10.0.0.99")
    
    print("\n--- 2. RUNNING VER
