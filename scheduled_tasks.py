"""
Scheduled Tasks Module - Handle periodic email jobs (weekly digest, newsletters)
Uses APScheduler for background task scheduling
"""

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime, timedelta
import json
import os
from email_service import get_email_service
import config


class ScheduledTaskManager:
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.users_file = 'users.json'
    
    def start(self):
        """Start the scheduler"""
        if not self.scheduler.running:
            self.scheduler.start()
            print("✅ Scheduler started - Background tasks enabled")
            
            # Schedule weekly digest (every Sunday at 9 AM)
            self.scheduler.add_job(
                self.send_weekly_digests,
                CronTrigger(day_of_week='sun', hour=9, minute=0),
                id='weekly_digest',
                name='Weekly Digest Email',
                replace_existing=True
            )
            print("📅 Scheduled: Weekly Digest - Every Sunday at 9:00 AM")
    
    def stop(self):
        """Stop the scheduler"""
        if self.scheduler.running:
            self.scheduler.shutdown()
            print("⛔ Scheduler stopped")
    
    def load_users(self):
        """Load users from JSON file"""
        try:
            if os.path.exists(self.users_file):
                with open(self.users_file, 'r') as f:
                    return json.load(f)
        except Exception as e:
            print(f"❌ Error loading users: {str(e)}")
        return {}
    
    def send_weekly_digests(self):
        """Send weekly digest emails to all users who want them"""
        print("\n" + "="*60)
        print("📊 WEEKLY DIGEST JOB STARTED")
        print("="*60)
        
        try:
            users = self.load_users()
            email_service = get_email_service()
            
            digest_count = 0
            skip_count = 0
            
            for username, user_data in users.items():
                try:
                    # Check if user wants weekly digest
                    preferences = user_data.get('email_preferences', config.DEFAULT_EMAIL_PREFERENCES)
                    if not preferences.get('weekly_digest', True):
                        skip_count += 1
                        continue
                    
                    user_email = user_data.get('email', '')
                    if not user_email:
                        print(f"⚠️  {username}: No email address found, skipping")
                        skip_count += 1
                        continue
                    
                    # Gather digest data
                    search_history = user_data.get('search_history', [])
                    interests = user_data.get('interests', [])
                    
                    # Count searches this week (last 7 days)
                    this_week_searches = 0
                    this_week_queries = []
                    one_week_ago = datetime.now() - timedelta(days=7)
                    
                    for search in search_history:
                        search_time = datetime.fromisoformat(search.get('timestamp', ''))
                        if search_time > one_week_ago:
                            this_week_searches += 1
                            query = search.get('query', '')
                            if query:
                                this_week_queries.append(query)
                    
                    digest_data = {
                        'search_count': this_week_searches,
                        'top_concepts': interests[-10:],  # Latest 10 interests
                        'documents_read': this_week_searches,  # Approximate
                        'recent_queries': this_week_queries[-5:],  # Last 5 queries
                        'trending_topics': ['Machine Learning', 'Data Science', 'AI'],  # Static for now
                        'recommendations': [
                            {
                                'title': 'Advanced Analytics Guide.pdf',
                                'description': 'Based on your recent searches'
                            },
                            {
                                'title': 'Deep Learning Fundamentals.pdf',
                                'description': 'Popular among users like you'
                            }
                        ]
                    }
                    
                    # Send email
                    if email_service.send_weekly_digest(username, user_email, digest_data):
                        digest_count += 1
                        print(f"✅ {username}: Weekly digest sent to {user_email}")
                    else:
                        print(f"❌ {username}: Failed to send weekly digest")
                        
                except Exception as e:
                    print(f"❌ {username}: Error sending digest - {str(e)}")
            
            print(f"\n📊 RESULT: {digest_count} digests sent, {skip_count} users skipped")
            print("="*60 + "\n")
            
        except Exception as e:
            print(f"❌ CRITICAL ERROR in weekly digest job: {str(e)}")
            print("="*60 + "\n")
    
    def send_concept_update_emails(self, concept: str, documents: list):
        """
        Send concept update emails to users interested in a topic
        
        Args:
            concept: The concept/topic name
            documents: List of new documents related to concept
        """
        print(f"\n📧 Sending concept update emails for: {concept}")
        
        try:
            users = self.load_users()
            email_service = get_email_service()
            
            sent_count = 0
            for username, user_data in users.items():
                try:
                    preferences = user_data.get('email_preferences', config.DEFAULT_EMAIL_PREFERENCES)
                    if not preferences.get('concept_updates', True):
                        continue
                    
                    # Check if user is interested in this concept
                    interests = user_data.get('interests', [])
                    if not any(keyword in concept.lower() for keyword in interests):
                        continue
                    
                    user_email = user_data.get('email', '')
                    if not user_email:
                        continue
                    
                    if email_service.send_concept_update(username, user_email, concept, documents):
                        sent_count += 1
                        print(f"  ✅ Sent to {username}")
                
                except Exception as e:
                    print(f"  ❌ Error sending to {username}: {str(e)}")
            
            print(f"📊 Concept update emails sent: {sent_count}\n")
            
        except Exception as e:
            print(f"❌ Error in concept update job: {str(e)}\n")


# Global scheduler instance
_scheduler = None

def initialize_scheduler() -> ScheduledTaskManager:
    """Initialize and start the global scheduler"""
    global _scheduler
    _scheduler = ScheduledTaskManager()
    _scheduler.start()
    return _scheduler

def get_scheduler() -> ScheduledTaskManager:
    """Get the global scheduler instance"""
    global _scheduler
    if _scheduler is None:
        _scheduler = ScheduledTaskManager()
    return _scheduler

def stop_scheduler():
    """Stop the global scheduler"""
    global _scheduler
    if _scheduler:
        _scheduler.stop()
