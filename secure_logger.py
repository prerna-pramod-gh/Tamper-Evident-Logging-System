import json
import hashlib
import time
import random
import os
import string

LOG_FILE = "secure_audit_log.json"

GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
RESET = '\033[0m'

def generate_nonce(length=32):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def calculate_hash(index, timestamp, event_type, description, previous_hash, nonce):
    data_string = f"{index}{timestamp}{event_type}{description}{previous_hash}{nonce}"
    return hashlib.sha256(data_string.encode('utf-8')).hexdigest()

def load_logs():
    if not os.path.exists(LOG_FILE):
        return []
    try:
        with open(LOG_FILE, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        print(f"{RED}[ERROR] Log file corrupted.{RESET}")
        return []

def save_logs(logs):
    with open(LOG_FILE, 'w') as f:
        json.dump(logs, f, indent=4)

def add_log(event_type, description):
    logs = load_logs()
    
    previous_hash = "0" * 64
    index = 0
    if len(logs) > 0:
        last_log = logs[-1]
        index = last_log['index']
        previous_hash = last_log['current_hash']

    new_index = index + 1
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    nonce = generate_nonce()
    
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
    print(f"{GREEN}[+]{RESET} Log #{new_index} added. Hash: {current_hash[:20]}...")

def verify_chain():
    logs = load_logs()
    
    if not logs:
        print(f"{YELLOW}[*]{RESET} No logs found.")
        return True

    print(f"{YELLOW}[*]{RESET} Initiating Audit Check...")

    for i in range(len(logs)):
        current = logs[i]
        
        if current['index'] != i + 1:
            print(f"{RED}[!!!] TAMPERING DETECTED:{RESET} Log missing!")
            return False

        expected_prev_hash = "0" * 64 if i == 0 else logs[i-1]['current_hash']
        if current['previous_hash'] != expected_prev_hash:
            print(f"{RED}[!!!] TAMPERING DETECTED:{RESET} Chain broken!")
            return False

        recalculated_hash = calculate_hash(
            current['index'], 
            current['timestamp'], 
            current['event_type'], 
            current['description'], 
            current['previous_hash'], 
            current['nonce']
        )
        
        if recalculated_hash != current['current_hash']:
            print(f"{RED}[!!!] TAMPERING DETECTED:{RESET} Log modified!")
            return False

    print(f"{GREEN}[+] AUDIT COMPLETE: 100% intact.{RESET}")
    return True

if __name__ == "__main__":
    print("--- 1. GENERATING LOGS ---")
    add_log("LOGIN_SUCCESS", "User admin logged in")
    add_log("FILE_ACCESS", "User admin read /etc/passwd")
    add_log("LOGIN_FAILURE", "Failed login for root")
    
    print("\n--- 2. VERIFYING LOGS ---")
    verify_chain()
    
    print("\n" + "="*50)
    print("Open secure_audit_log.json")
    print("Change admin to HACKER, save, and run again.")
    print("="*50 + "\n")
