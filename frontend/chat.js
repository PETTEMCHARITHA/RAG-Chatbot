// Elements
const documentsStatus = document.getElementById('documentsStatus');
const documentsList = document.getElementById('documentsList');
const chatMessages = document.getElementById('chatMessages');
const chatForm = document.getElementById('chatForm');
const messageInput = document.getElementById('messageInput');
const sendBtn = document.getElementById('sendBtn');
const logoutBtn = document.getElementById('logoutBtn');

// Get auth token from localStorage
function getAuthToken() {
    return localStorage.getItem('authToken');
}

// Helper function to make API requests with auth token
async function apiRequest(url, options = {}) {
    const token = getAuthToken();
    if (!token) {
        console.error('No auth token found');
        window.location.href = '/';
        return null;
    }
    
    const headers = options.headers || {};
    headers['Authorization'] = `Bearer ${token}`;
    
    const config = {
        ...options,
        headers
    };
    
    console.log(`API Request to ${url}`);
    return fetch(url, config);
}

// Check documents status
async function checkDocumentsStatus() {
    try {
        const response = await apiRequest('/api/documents-status');
        if (!response) return;
        
        const data = await response.json();
        console.log('Documents status:', data);
        
        if (data.success) {
            if (data.documents_loaded) {
                documentsStatus.innerHTML = `<p class="success">✅ ${data.document_count} document(s) loaded</p>`;
                
                // Display document names
                if (data.documents && data.documents.length > 0) {
                    documentsList.innerHTML = '';
                    data.documents.forEach(doc => {
                        const docItem = document.createElement('div');
                        docItem.className = 'document-item';
                        docItem.innerHTML = `<span class="doc-icon">📄</span> <span class="doc-name">${doc}</span>`;
                        documentsList.appendChild(docItem);
                    });
                }
            } else {
                documentsStatus.innerHTML = `<p class="error">⚠️ No documents loaded</p>`;
                documentsList.innerHTML = '<p class="info">Add PDF files to the documents folder and restart the server.</p>';
            }
        }
    } catch (error) {
        console.error('Error checking documents status:', error);
        documentsStatus.innerHTML = `<p class="error">❌ Error checking documents status</p>`;
    }
}

// Chat handling
chatForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const token = getAuthToken();
    if (!token) {
        addMessage('Session expired. Please login again.', 'assistant');
        window.location.href = '/';
        return;
    }
    
    const question = messageInput.value.trim();
    if (!question) return;
    
    // Display user message
    addMessage(question, 'user');
    messageInput.value = '';
    
    // Show loading indicator
    const loadingId = addLoadingMessage();
    
    // Disable input while processing
    messageInput.disabled = true;
    sendBtn.disabled = true;
    
    try {
        console.log(`Sending chat request: ${question}`);
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({ question }),
        });
        
        console.log(`Chat response status: ${response.status}`);
        
        if (!response.ok) {
            const errorData = await response.json().catch(() => ({ message: 'Chat failed' }));
            console.error('Chat error:', errorData);
            removeLoadingMessage(loadingId);
            addMessage(errorData.message || 'An error occurred', 'assistant');
        } else {
            const data = await response.json();
            console.log('Chat response:', data);
            
            // Remove loading indicator
            removeLoadingMessage(loadingId);
            
            if (data.success) {
                // Display assistant response
                addMessage(data.response, 'assistant');
            } else {
                addMessage(data.message, 'assistant');
            }
        }
    } catch (error) {
        console.error('Chat exception:', error);
        removeLoadingMessage(loadingId);
        addMessage('An error occurred: ' + error.message, 'assistant');
    } finally {
        // Re-enable input
        messageInput.disabled = false;
        sendBtn.disabled = false;
        messageInput.focus();
    }
});

function addMessage(content, role) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${role}`;
    messageDiv.textContent = content;
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function addLoadingMessage() {
    const loadingId = `loading-${Date.now()}`;
    const loadingDiv = document.createElement('div');
    loadingDiv.id = loadingId;
    loadingDiv.className = 'message loading';
    loadingDiv.innerHTML = `
        <div class="loading-dot"></div>
        <div class="loading-dot"></div>
        <div class="loading-dot"></div>
    `;
    chatMessages.appendChild(loadingDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
    return loadingId;
}

function removeLoadingMessage(loadingId) {
    const loadingDiv = document.getElementById(loadingId);
    if (loadingDiv) {
        loadingDiv.remove();
    }
}

// Logout handling
logoutBtn.addEventListener('click', async () => {
    const token = getAuthToken();
    if (!token) {
        window.location.href = '/';
        return;
    }
    
    try {
        const response = await fetch('/api/logout', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`
            },
        });
        
        const data = await response.json();
        
        if (data.success) {
            localStorage.removeItem('authToken');
            localStorage.removeItem('username');
            window.location.href = '/';
        }
    } catch (error) {
        console.error('Logout error:', error);
        // Redirect anyway
        localStorage.removeItem('authToken');
        localStorage.removeItem('username');
        window.location.href = '/';
    }
});

// Load chat history on page load
async function loadChatHistory() {
    const token = getAuthToken();
    if (!token) {
        window.location.href = '/';
        return;
    }
    
    try {
        const response = await fetch('/api/chat-history', {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        const data = await response.json();
        
        if (data.success && data.history.length > 0) {
            // Remove welcome message
            const welcomeMsg = document.querySelector('.welcome-message');
            if (welcomeMsg) {
                welcomeMsg.remove();
            }
            
            // Display history
            data.history.forEach(msg => {
                addMessage(msg.content, msg.role);
            });
        }
    } catch (error) {
        console.error('Error loading chat history:', error);
    }
}

// Initialize on page load
checkDocumentsStatus();
loadChatHistory();
