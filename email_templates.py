"""
Email Templates Module - HTML templates for different email types
"""

from datetime import datetime
from typing import List, Dict

def get_instant_email_template(username: str, query: str, response: str, 
                               sources: List[Dict], timestamp: datetime) -> str:
    """Generate HTML template for instant notification email"""
    
    sources_html = ""
    if sources:
        sources_html = "<div style='margin: 15px 0; background: #f9f9f9; padding: 12px; border-left: 4px solid #4CAF50;'>"
        sources_html += "<strong>📄 Source Documents:</strong><ul style='margin: 10px 0; padding-left: 20px;'>"
        for source in sources:
            filename = source.get('filename', 'Unknown')
            page = source.get('page', 'N/A')
            sources_html += f"<li>{filename} (Page {page})</li>"
        sources_html += "</ul></div>"
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                line-height: 1.6;
                color: #333;
                background-color: #f5f5f5;
            }}
            .container {{
                max-width: 600px;
                margin: 0 auto;
                background-color: #ffffff;
                border-radius: 8px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                overflow: hidden;
            }}
            .header {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 30px;
                text-align: center;
            }}
            .content {{
                padding: 30px;
            }}
            .section {{
                margin-bottom: 25px;
            }}
            .section-title {{
                color: #667eea;
                font-size: 18px;
                font-weight: bold;
                margin-bottom: 12px;
                border-bottom: 2px solid #667eea;
                padding-bottom: 8px;
            }}
            .query-box {{
                background: #f0f4ff;
                border-left: 4px solid #667eea;
                padding: 15px;
                border-radius: 4px;
                margin-bottom: 15px;
            }}
            .response-box {{
                background: #f9f9f9;
                padding: 15px;
                border-radius: 4px;
                border-left: 4px solid #4CAF50;
            }}
            .cta-button {{
                display: inline-block;
                background: #667eea;
                color: white;
                padding: 12px 30px;
                text-decoration: none;
                border-radius: 4px;
                margin-top: 20px;
                font-weight: bold;
            }}
            .cta-button:hover {{
                background: #764ba2;
            }}
            .footer {{
                background-color: #f9f9f9;
                padding: 20px;
                text-align: center;
                font-size: 12px;
                color: #666;
                border-top: 1px solid #ddd;
            }}
            .hi {{
                color: #667eea;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🤖 RAG Chatbot Query Results</h1>
                <p>Your personalized learning update</p>
            </div>
            
            <div class="content">
                <p>Hello <strong class="hi">{username}</strong>,</p>
                <p>Great! We found answers to your query. Here's your personalized result:</p>
                
                <div class="section">
                    <div class="section-title">🎯 Your Query</div>
                    <div class="query-box">
                        <strong>Question:</strong><br>
                        {query}
                    </div>
                </div>
                
                <div class="section">
                    <div class="section-title">💡 Answer Summary</div>
                    <div class="response-box">
                        {response}
                    </div>
                </div>
                
                {sources_html}
                
                <div class="section">
                    <p><strong>📅 Generated on:</strong> {timestamp.strftime('%B %d, %Y at %I:%M %p')}</p>
                </div>
                
                <a href="http://localhost:5000/chat" class="cta-button">Continue Learning →</a>
            </div>
            
            <div class="footer">
                <p>You're receiving this email because you have notifications enabled. 
                <a href="http://localhost:5000/chat" style="color: #667eea; text-decoration: none;">Manage preferences</a></p>
                <p>&copy; 2026 RAG Chatbot. All rights reserved.</p>
            </div>
        </div>
    </body>
    </html>
    """
    return html

def get_weekly_digest_template(username: str, search_count: int, top_concepts: List[str],
                               documents_read: int, recent_queries: List[str],
                               trending_topics: List[str], recommendations: List[Dict],
                               timestamp: datetime) -> str:
    """Generate HTML template for weekly digest email"""
    
    top_concepts_html = ""
    if top_concepts:
        top_concepts_html = "<ul style='margin: 10px 0; padding-left: 20px;'>"
        for i, concept in enumerate(top_concepts[:5], 1):
            top_concepts_html += f"<li>{i}. <strong>{concept}</strong></li>"
        top_concepts_html += "</ul>"
    
    recent_queries_html = ""
    if recent_queries:
        recent_queries_html = "<ul style='margin: 10px 0; padding-left: 20px;'>"
        for query in recent_queries[:5]:
            recent_queries_html += f"<li>• {query}</li>"
        recent_queries_html += "</ul>"
    
    trending_html = ""
    if trending_topics:
        trending_html = "<ul style='margin: 10px 0; padding-left: 20px;'>"
        for i, topic in enumerate(trending_topics[:5], 1):
            trending_html += f"<li>{i}. <strong>{topic}</strong> - Trending this week</li>"
        trending_html += "</ul>"
    
    recommendations_html = ""
    if recommendations:
        recommendations_html = "<ul style='margin: 10px 0; padding-left: 20px;'>"
        for rec in recommendations[:3]:
            recommendations_html += f"<li><strong>{rec.get('title', 'Document')}</strong><br><span style='color: #666; font-size: 13px;'>{rec.get('description', '')}</span></li>"
        recommendations_html += "</ul>"
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                line-height: 1.6;
                color: #333;
                background-color: #f5f5f5;
            }}
            .container {{
                max-width: 600px;
                margin: 0 auto;
                background-color: #ffffff;
                border-radius: 8px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                overflow: hidden;
            }}
            .header {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 30px;
                text-align: center;
            }}
            .content {{
                padding: 30px;
            }}
            .section {{
                margin-bottom: 25px;
                background: #f9f9f9;
                padding: 15px;
                border-radius: 6px;
                border-left: 4px solid #667eea;
            }}
            .section-title {{
                color: #667eea;
                font-size: 16px;
                font-weight: bold;
                margin-bottom: 12px;
            }}
            .stat-box {{
                display: inline-block;
                background: white;
                padding: 12px 20px;
                margin: 8px 8px 8px 0;
                border-radius: 4px;
                border: 1px solid #ddd;
                text-align: center;
            }}
            .stat-value {{
                font-size: 24px;
                font-weight: bold;
                color: #667eea;
            }}
            .stat-label {{
                font-size: 11px;
                color: #666;
                margin-top: 4px;
            }}
            .cta-button {{
                display: inline-block;
                background: #667eea;
                color: white;
                padding: 12px 30px;
                text-decoration: none;
                border-radius: 4px;
                margin-top: 20px;
                font-weight: bold;
            }}
            .cta-button:hover {{
                background: #764ba2;
            }}
            .footer {{
                background-color: #f9f9f9;
                padding: 20px;
                text-align: center;
                font-size: 12px;
                color: #666;
                border-top: 1px solid #ddd;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>📊 Weekly Learning Update</h1>
                <p>Your personalized learning summary</p>
            </div>
            
            <div class="content">
                <p>Hello <strong>{username}</strong>,</p>
                <p>Here's your learning progress for the week of {timestamp.strftime('%B %d, %Y')}:</p>
                
                <div style='text-align: center; margin: 20px 0;'>
                    <div class="stat-box">
                        <div class="stat-value">{search_count}</div>
                        <div class="stat-label">Searches</div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-value">{documents_read}</div>
                        <div class="stat-label">Documents</div>
                    </div>
                </div>
                
                <div class="section">
                    <div class="section-title">🎯 Your Top Concepts</div>
                    {top_concepts_html if top_concepts_html else '<p>No searches yet this week.</p>'}
                </div>
                
                <div class="section">
                    <div class="section-title">🔍 Recent Queries</div>
                    {recent_queries_html if recent_queries_html else '<p>No queries recorded.</p>'}
                </div>
                
                <div class="section">
                    <div class="section-title">🔥 Trending Topics</div>
                    {trending_html if trending_html else '<p>No trending topics this week.</p>'}
                </div>
                
                <div class="section">
                    <div class="section-title">💡 Recommended for You</div>
                    {recommendations_html if recommendations_html else '<p>No recommendations available.</p>'}
                </div>
                
                <a href="http://localhost:5000/chat" class="cta-button">Continue Your Learning →</a>
            </div>
            
            <div class="footer">
                <p>This is your weekly digest. Manage your email preferences in your account settings.</p>
                <p>&copy; 2026 RAG Chatbot. All rights reserved.</p>
            </div>
        </div>
    </body>
    </html>
    """
    return html

def get_concept_update_template(username: str, concept: str, new_documents: List[Dict],
                                insights: str, timestamp: datetime) -> str:
    """Generate HTML template for concept update email"""
    
    documents_html = ""
    if new_documents:
        documents_html = "<ul style='margin: 10px 0; padding-left: 20px;'>"
        for doc in new_documents[:5]:
            title = doc.get('title', 'Document')
            desc = doc.get('description', '')
            documents_html += f"<li><strong>{title}</strong><br><span style='color: #666; font-size: 13px;'>{desc}</span></li>"
        documents_html += "</ul>"
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                line-height: 1.6;
                color: #333;
                background-color: #f5f5f5;
            }}
            .container {{
                max-width: 600px;
                margin: 0 auto;
                background-color: #ffffff;
                border-radius: 8px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                overflow: hidden;
            }}
            .header {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 30px;
                text-align: center;
            }}
            .content {{
                padding: 30px;
            }}
            .section {{
                margin-bottom: 25px;
                background: #f9f9f9;
                padding: 15px;
                border-radius: 6px;
                border-left: 4px solid #667eea;
            }}
            .section-title {{
                color: #667eea;
                font-size: 16px;
                font-weight: bold;
                margin-bottom: 12px;
            }}
            .concept-highlight {{
                background: #fff3cd;
                border: 1px solid #ffc107;
                padding: 15px;
                border-radius: 4px;
                margin-bottom: 15px;
                color: #856404;
            }}
            .cta-button {{
                display: inline-block;
                background: #667eea;
                color: white;
                padding: 12px 30px;
                text-decoration: none;
                border-radius: 4px;
                margin-top: 20px;
                font-weight: bold;
            }}
            .cta-button:hover {{
                background: #764ba2;
            }}
            .footer {{
                background-color: #f9f9f9;
                padding: 20px;
                text-align: center;
                font-size: 12px;
                color: #666;
                border-top: 1px solid #ddd;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>📚 New Content Alert</h1>
                <p>Topics matching your interests</p>
            </div>
            
            <div class="content">
                <p>Hello <strong>{username}</strong>,</p>
                <p>We found new content related to <strong>"{concept}"</strong> - a topic you've been learning about!</p>
                
                <div class="concept-highlight">
                    <strong>📌 {concept}</strong><br>
                    <p>{insights if insights else 'Check out these new resources to deepen your knowledge.'}</p>
                </div>
                
                <div class="section">
                    <div class="section-title">🆕 New Documents Available</div>
                    {documents_html if documents_html else '<p>No new documents at this time.</p>'}
                </div>
                
                <a href="http://localhost:5000/chat" class="cta-button">Explore Content →</a>
            </div>
            
            <div class="footer">
                <p>You're receiving this because you've shown interest in this topic. Manage preferences anytime.</p>
                <p>&copy; 2026 RAG Chatbot. All rights reserved.</p>
            </div>
        </div>
    </body>
    </html>
    """
    return html
