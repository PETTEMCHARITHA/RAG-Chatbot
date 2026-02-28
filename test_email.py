"""
Email System Test Script
Run this to verify email configuration and send test emails
"""

import json
import os
import sys
from datetime import datetime
from email_service import initialize_email_service
import config


def load_users():
    """Load users from JSON"""
    if os.path.exists('users.json'):
        with open('users.json', 'r') as f:
            return json.load(f)
    return {}


def test_email_config():
    """Test if email configuration is valid"""
    print("\n" + "="*60)
    print("📧 EMAIL CONFIGURATION TEST")
    print("="*60)
    
    print("\n✓ Config loaded")
    print(f"  SMTP Server: {config.EMAIL_CONFIG['smtp_server']}")
    print(f"  SMTP Port: {config.EMAIL_CONFIG['smtp_port']}")
    print(f"  Sender Email: {config.EMAIL_CONFIG['sender_email']}")
    print(f"  Sender Name: {config.EMAIL_CONFIG['sender_name']}")
    
    # Check for default values
    if config.EMAIL_CONFIG['sender_email'] == 'your-email@gmail.com':
        print("\n⚠️  WARNING: Email not configured!")
        print("  Please update config.py with your Gmail address and app password")
        return False
    
    if config.EMAIL_CONFIG['sender_password'] == 'your-app-password':
        print("\n⚠️  WARNING: App password not set!")
        print("  Please update config.py with your Gmail app-specific password")
        return False
    
    print("\n✅ Configuration looks good!")
    return True


def send_test_email():
    """Send a test email to a user"""
    print("\n" + "="*60)
    print("📨 SEND TEST EMAIL")
    print("="*60)
    
    users = load_users()
    
    if not users:
        print("\n❌ No users found in users.json")
        print("  Register a user first using the chatbot signup page")
        return
    
    print("\n📋 Available users:")
    user_list = list(users.keys())
    for i, username in enumerate(user_list, 1):
        email = users[username].get('email', 'N/A')
        print(f"  {i}. {username} ({email})")
    
    try:
        choice = input("\nSelect user number (or press Enter to cancel): ").strip()
        if not choice:
            return
        
        idx = int(choice) - 1
        if idx < 0 or idx >= len(user_list):
            print("❌ Invalid selection")
            return
        
        username = user_list[idx]
        user_data = users[username]
        user_email = user_data.get('email', '')
        
        if not user_email:
            print(f"❌ {username} has no email address")
            return
        
        print(f"\n📧 Sending test email to {username} ({user_email})...")
        
        # Test instant notification
        email_service = initialize_email_service(config.EMAIL_CONFIG)
        
        result = email_service.send_instant_notification(
            username=username,
            email=user_email,
            query="What is Machine Learning?",
            response="Machine Learning is a subset of artificial intelligence that enables systems to learn and improve from experience. It focuses on developing algorithms that can analyze data and make decisions with minimal human intervention.",
            sources=[
                {'filename': 'ML_101.pdf', 'page': 5},
                {'filename': 'AI_Guide.pdf', 'page': 12}
            ]
        )
        
        if result:
            print("✅ Test email sent successfully!")
            print(f"   Email should arrive in {user_email} within a few seconds")
            print("   Check your spam folder if it doesn't appear in inbox")
        else:
            print("❌ Failed to send test email")
            print("   Check your email configuration in config.py")
    
    except ValueError:
        print("❌ Invalid input")
    except Exception as e:
        print(f"❌ Error: {str(e)}")


def test_user_preferences():
    """Check user email preferences"""
    print("\n" + "="*60)
    print("⚙️  USER EMAIL PREFERENCES")
    print("="*60)
    
    users = load_users()
    
    if not users:
        print("\n❌ No users found")
        return
    
    print("\n📋 User Email Settings:\n")
    
    for username, user_data in users.items():
        prefs = user_data.get('email_preferences', config.DEFAULT_EMAIL_PREFERENCES)
        print(f"👤 {username}")
        print(f"   Email: {user_data.get('email', 'N/A')}")
        print(f"   Instant Notifications: {'✅ ON' if prefs.get('instant_notification') else '❌ OFF'}")
        print(f"   Weekly Digest: {'✅ ON' if prefs.get('weekly_digest') else '❌ OFF'}")
        print(f"   Concept Updates: {'✅ ON' if prefs.get('concept_updates') else '❌ OFF'}")
        print(f"   Frequency: {prefs.get('frequency', 'weekly')}")
        print()


def test_search_history():
    """Display user search history"""
    print("\n" + "="*60)
    print("🔍 USER SEARCH HISTORY")
    print("="*60)
    
    users = load_users()
    
    if not users:
        print("\n❌ No users found")
        return
    
    print("\n📊 Search Statistics:\n")
    
    for username, user_data in users.items():
        searches = user_data.get('search_history', [])
        interests = user_data.get('interests', [])
        
        print(f"👤 {username}")
        print(f"   Total Searches: {len(searches)}")
        print(f"   Top Interests: {', '.join(interests[-5:]) if interests else 'None yet'}")
        
        if searches:
            print(f"   Last 3 Searches:")
            for search in searches[-3:]:
                query = search.get('query', '')
                timestamp = search.get('timestamp', '')
                print(f"     • {query}")
                print(f"       {timestamp}")
        
        print()


def main():
    """Main menu"""
    print("\n" + "="*70)
    print("🤖 RAG CHATBOT - EMAIL SYSTEM TEST UTILITY")
    print("="*70)
    
    while True:
        print("\nOptions:")
        print("  1. Test Email Configuration")
        print("  2. Send Test Email")
        print("  3. View User Email Preferences")
        print("  4. View Search History")
        print("  5. Show Default Preferences")
        print("  6. Exit")
        
        choice = input("\nSelect option (1-6): ").strip()
        
        if choice == '1':
            if test_email_config():
                print("\n✅ Next step: Configure your Gmail app password in config.py")
                print("   See EMAIL_SETUP.md for detailed instructions")
        
        elif choice == '2':
            if test_email_config():
                send_test_email()
        
        elif choice == '3':
            test_user_preferences()
        
        elif choice == '4':
            test_search_history()
        
        elif choice == '5':
            print("\n📋 Default Email Preferences (for new users):")
            print(json.dumps(config.DEFAULT_EMAIL_PREFERENCES, indent=2))
        
        elif choice == '6':
            print("\n👋 Goodbye!")
            break
        
        else:
            print("❌ Invalid option")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Exiting...")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
