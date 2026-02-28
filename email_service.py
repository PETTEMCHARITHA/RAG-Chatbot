"""
Email Service Module - Handles all email operations for the RAG Chatbot
Supports both instant notifications and periodic newsletters
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import json
import os
from typing import List, Dict
from email_templates import (
    get_instant_email_template,
    get_weekly_digest_template,
    get_concept_update_template
)

class EmailService:
    def __init__(self, smtp_config: Dict = None):
        """
        Initialize email service with SMTP configuration
        
        Args:
            smtp_config: Dictionary with keys:
                - smtp_server: SMTP server address
                - smtp_port: SMTP port
                - sender_email: Sender email address
                - sender_password: Sender email password
                - sender_name: Display name for sender
        """
        # Default to Gmail SMTP (update these with your credentials)
        self.smtp_server = smtp_config.get('smtp_server', 'smtp.gmail.com') if smtp_config else 'smtp.gmail.com'
        self.smtp_port = smtp_config.get('smtp_port', 587) if smtp_config else 587
        self.sender_email = smtp_config.get('sender_email', 'your-email@gmail.com') if smtp_config else 'your-email@gmail.com'
        self.sender_password = smtp_config.get('sender_password', 'your-app-password') if smtp_config else 'your-app-password'
        self.sender_name = smtp_config.get('sender_name', 'RAG Chatbot') if smtp_config else 'RAG Chatbot'
        
    def send_email(self, recipient_email: str, subject: str, html_body: str, plain_text: str = None) -> bool:
        """
        Send email using SMTP
        
        Args:
            recipient_email: Recipient email address
            subject: Email subject
            html_body: HTML content of email
            plain_text: Plain text version (for fallback)
        
        Returns:
            True if email sent successfully, False otherwise
        """
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = f"{self.sender_name} <{self.sender_email}>"
            msg['To'] = recipient_email
            
            # Attach plain text and HTML versions
            if plain_text:
                msg.attach(MIMEText(plain_text, 'plain', 'utf-8'))
            msg.attach(MIMEText(html_body, 'html', 'utf-8'))
            
            # Send email via SMTP
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()  # Secure connection
                server.login(self.sender_email, self.sender_password)
                server.send_message(msg)
            
            print(f"✅ Email sent successfully to {recipient_email}")
            return True
            
        except smtplib.SMTPAuthenticationError:
            print(f"❌ Email authentication failed. Check your credentials.")
            return False
        except smtplib.SMTPException as e:
            print(f"❌ SMTP error while sending email: {str(e)}")
            return False
        except Exception as e:
            print(f"❌ Error sending email: {str(e)}")
            return False

    def send_instant_notification(self, username: str, email: str, query: str, response: str, 
                                  sources: List[Dict] = None) -> bool:
        """
        Send instant email notification after user query
        
        Args:
            username: Username
            email: User email address
            query: User's question/query
            response: AI-generated response
            sources: List of source documents with metadata
                Example: [{'filename': 'doc.pdf', 'page': 5, 'excerpt': '...'}]
        
        Returns:
            True if sent successfully
        """
        if sources is None:
            sources = []
        
        # Generate HTML email
        html_body = get_instant_email_template(
            username=username,
            query=query,
            response=response,
            sources=sources,
            timestamp=datetime.now()
        )
        
        subject = f"Your Query Results: {query[:30]}... - {datetime.now().strftime('%b %d, %Y')}"
        
        return self.send_email(email, subject, html_body)

    def send_weekly_digest(self, username: str, email: str, digest_data: Dict) -> bool:
        """
        Send weekly digest email with personalized updates
        
        Args:
            username: Username
            email: User email address
            digest_data: Dictionary containing:
                - search_count: Number of searches this week
                - top_concepts: List of top concepts searched
                - documents_read: Count of documents
                - recent_queries: List of recent queries
                - trending_topics: List of trending topics
                - recommendations: List of recommended documents
        
        Returns:
            True if sent successfully
        """
        # Generate HTML email
        html_body = get_weekly_digest_template(
            username=username,
            search_count=digest_data.get('search_count', 0),
            top_concepts=digest_data.get('top_concepts', []),
            documents_read=digest_data.get('documents_read', 0),
            recent_queries=digest_data.get('recent_queries', []),
            trending_topics=digest_data.get('trending_topics', []),
            recommendations=digest_data.get('recommendations', []),
            timestamp=datetime.now()
        )
        
        subject = f"Your Weekly Learning Update - {datetime.now().strftime('%B %d, %Y')}"
        
        return self.send_email(email, subject, html_body)

    def send_concept_update(self, username: str, email: str, concept: str, 
                           new_documents: List[Dict], insights: str = "") -> bool:
        """
        Send concept-based update when new documents match user interests
        
        Args:
            username: Username
            email: User email address
            concept: Concept/topic name
            new_documents: List of new documents related to concept
                Example: [{'title': 'doc.pdf', 'description': '...'}, ...]
            insights: Additional insights about the concept
        
        Returns:
            True if sent successfully
        """
        # Generate HTML email
        html_body = get_concept_update_template(
            username=username,
            concept=concept,
            new_documents=new_documents,
            insights=insights,
            timestamp=datetime.now()
        )
        
        subject = f"New Content Available: {concept} - {datetime.now().strftime('%b %d, %Y')}"
        
        return self.send_email(email, subject, html_body)


# Global email service instance
_email_service = None

def initialize_email_service(smtp_config: Dict = None) -> EmailService:
    """
    Initialize the global email service
    
    Args:
        smtp_config: SMTP configuration dictionary
    
    Returns:
        EmailService instance
    """
    global _email_service
    _email_service = EmailService(smtp_config)
    return _email_service

def get_email_service() -> EmailService:
    """Get the global email service instance"""
    global _email_service
    if _email_service is None:
        _email_service = EmailService()
    return _email_service

def should_send_email(users_data: Dict, username: str, email_type: str = 'instant') -> bool:
    """
    Check if user has enabled notifications for this email type
    
    Args:
        users_data: Users data dictionary
        username: Username
        email_type: Type of email ('instant', 'weekly_digest', 'concept_update')
    
    Returns:
        True if email should be sent
    """
    if username not in users_data:
        return False
    
    user = users_data[username]
    
    # Get email preferences, default to enabled
    preferences = user.get('email_preferences', {})
    
    if email_type == 'instant':
        return preferences.get('instant_notification', True)
    elif email_type == 'weekly_digest':
        return preferences.get('weekly_digest', True)
    elif email_type == 'concept_update':
        return preferences.get('concept_updates', True)
    
    return True
