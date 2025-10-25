#!/usr/bin/env python3
"""
Email configuration setup for the Task Scheduler
"""

import json
import os
import getpass

def setup_gmail():
    """Setup Gmail configuration"""
    print("📧 Gmail Setup")
    print("=" * 30)
    print("To use Gmail, you need to:")
    print("1. Enable 2-Factor Authentication on your Google account")
    print("2. Generate an 'App Password' for this application")
    print("3. Use the App Password (not your regular password)")
    print()
    print("📖 How to get Gmail App Password:")
    print("1. Go to https://myaccount.google.com/security")
    print("2. Click 'App passwords' (you need 2FA enabled)")
    print("3. Select 'Mail' and 'Windows Computer'")
    print("4. Copy the 16-character password")
    print()
    
    email = input("Enter your Gmail address: ")
    print("Enter your Gmail App Password (16 characters, no spaces):")
    password = getpass.getpass("App Password: ")
    
    return {
        "smtp_server": "smtp.gmail.com",
        "smtp_port": 587,
        "sender_email": email,
        "sender_password": password,
        "sender_name": "Task Scheduler"
    }

def setup_outlook():
    """Setup Outlook/Hotmail configuration"""
    print("📧 Outlook/Hotmail Setup")
    print("=" * 30)
    
    email = input("Enter your Outlook/Hotmail address: ")
    password = getpass.getpass("Enter your password: ")
    
    return {
        "smtp_server": "smtp-mail.outlook.com",
        "smtp_port": 587,
        "sender_email": email,
        "sender_password": password,
        "sender_name": "Task Scheduler"
    }

def setup_custom():
    """Setup custom SMTP configuration"""
    print("📧 Custom SMTP Setup")
    print("=" * 30)
    
    smtp_server = input("SMTP Server (e.g., smtp.example.com): ")
    smtp_port = int(input("SMTP Port (usually 587 or 465): "))
    email = input("Your email address: ")
    password = getpass.getpass("Your email password: ")
    sender_name = input("Sender name (optional): ") or "Task Scheduler"
    
    return {
        "smtp_server": smtp_server,
        "smtp_port": smtp_port,
        "sender_email": email,
        "sender_password": password,
        "sender_name": sender_name
    }

def save_config(config):
    """Save email configuration to file"""
    # Update the email_sender.py file
    with open("email_sender.py", "r") as f:
        content = f.read()
    
    # Replace the EMAIL_CONFIG section
    config_str = f"""EMAIL_CONFIG = {{
    "smtp_server": "{config['smtp_server']}",
    "smtp_port": {config['smtp_port']},
    "sender_email": "{config['sender_email']}",
    "sender_password": "{config['sender_password']}",
    "sender_name": "{config['sender_name']}"
}}"""
    
    # Find and replace the EMAIL_CONFIG
    start = content.find("EMAIL_CONFIG = {")
    end = content.find("}", start) + 1
    
    if start != -1 and end != -1:
        new_content = content[:start] + config_str + content[end:]
        
        with open("email_sender.py", "w") as f:
            f.write(new_content)
        
        print("✅ Email configuration saved!")
        return True
    else:
        print("❌ Could not update configuration file")
        return False

def test_email_config():
    """Test the email configuration"""
    print("\n🧪 Testing Email Configuration...")
    
    recipient = input("Enter test recipient email: ")
    
    # Import and test
    try:
        import email_sender
        success = email_sender.send_email(
            recipient,
            "Test Email from Task Scheduler",
            "This is a test email to verify your email configuration is working correctly.\n\nIf you receive this, your setup is successful!"
        )
        
        if success:
            print("✅ Test email sent successfully!")
            print("Check the recipient's inbox (and spam folder)")
        else:
            print("❌ Test email failed. Please check your configuration.")
            
    except Exception as e:
        print(f"❌ Error testing email: {e}")

def main():
    """Main setup function"""
    print("📧 Email Setup for Task Scheduler")
    print("=" * 40)
    print("Choose your email provider:")
    print("1. Gmail")
    print("2. Outlook/Hotmail")
    print("3. Custom SMTP")
    print("4. Test current configuration")
    
    choice = input("\nEnter your choice (1-4): ")
    
    if choice == "1":
        config = setup_gmail()
        if save_config(config):
            test_choice = input("\nWould you like to send a test email? (y/n): ")
            if test_choice.lower() == 'y':
                test_email_config()
    
    elif choice == "2":
        config = setup_outlook()
        if save_config(config):
            test_choice = input("\nWould you like to send a test email? (y/n): ")
            if test_choice.lower() == 'y':
                test_email_config()
    
    elif choice == "3":
        config = setup_custom()
        if save_config(config):
            test_choice = input("\nWould you like to send a test email? (y/n): ")
            if test_choice.lower() == 'y':
                test_email_config()
    
    elif choice == "4":
        test_email_config()
    
    else:
        print("Invalid choice")

if __name__ == "__main__":
    main()