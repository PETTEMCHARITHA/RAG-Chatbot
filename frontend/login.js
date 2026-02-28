document.getElementById('loginForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const errorMessage = document.getElementById('errorMessage');
    
    // Hide previous error
    errorMessage.classList.remove('show');
    errorMessage.textContent = '';
    
    try {
        console.log(`Attempting login for user: ${username}`);
        const response = await fetch('/api/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username, password }),
        });
        
        console.log(`Login response status: ${response.status}`);
        const data = await response.json();
        
        if (data.success) {
            console.log(`Login successful! Token: ${data.token.substring(0, 10)}...`);
            // Store token in localStorage
            localStorage.setItem('authToken', data.token);
            localStorage.setItem('username', data.username);
            // Redirect to chat page
            window.location.href = '/chat';
        } else {
            // Show error message
            errorMessage.textContent = data.message;
            errorMessage.classList.add('show');
        }
    } catch (error) {
        console.error('Login error:', error);
        errorMessage.textContent = 'An error occurred. Please try again.';
        errorMessage.classList.add('show');
    }
});
