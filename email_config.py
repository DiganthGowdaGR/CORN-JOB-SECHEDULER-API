#!/usr/bin/env python3
"""
Email Configuration Manager
Stores and manages email credentials securely
"""

import json
import os

CONFIG_FILE = "email_config.json"

def save_email_config(email, password, smtp_server="smtp.gmail.com", smtp_port=587):
    """Save email configuration"""
    config = {
        "email": email,
        "password": password,
        "smtp_server": smtp_server,
        "smtp_port": smtp_port
    }
    
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)
    
    return True

def load_email_config():
    """Load email configuration"""
    if not os.path.exists(CONFIG_FILE):
        return None
    
    try:
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    except:
        return None

def is_email_configured():
    """Check if email is configured"""
    config = load_email_config()
    return config is not None and 'email' in config and 'password' in config
