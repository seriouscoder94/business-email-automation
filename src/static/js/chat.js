// Chat UI state
let chatVisible = true;
let messageHistory = [];

// Toggle chat visibility
function toggleChat() {
    const chat = document.getElementById('ai-chat');
    chatVisible = !chatVisible;
    chat.style.display = chatVisible ? 'block' : 'none';
}

// Add a message to the chat
function addMessage(message, isUser = false) {
    const messagesDiv = document.getElementById('chat-messages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `flex ${isUser ? 'justify-end' : 'justify-start'}`;
    
    messageDiv.innerHTML = `
        <div class="${isUser ? 'bg-blue-600 text-white' : 'bg-gray-100 text-gray-800'} 
                    rounded-lg px-4 py-2 max-w-[80%] break-words">
            ${message}
        </div>
    `;
    
    messagesDiv.appendChild(messageDiv);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
    
    // Save to history
    messageHistory.push({
        content: message,
        isUser: isUser,
        timestamp: new Date().toISOString()
    });
}

// Send a message to the AI
async function sendMessage() {
    const input = document.getElementById('chat-input');
    const message = input.value.trim();
    
    if (message) {
        // Add user message to chat
        addMessage(message, true);
        input.value = '';
        
        try {
            // Send to backend
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    message: message,
                    history: messageHistory
                })
            });
            
            if (response.ok) {
                const data = await response.json();
                // Add AI response to chat
                addMessage(data.response);
                
                // Handle any actions
                if (data.actions) {
                    handleActions(data.actions);
                }
            } else {
                addMessage('Sorry, I encountered an error. Please try again.');
            }
        } catch (error) {
            console.error('Error:', error);
            addMessage('Sorry, I encountered an error. Please try again.');
        }
    }
}

// Handle quick actions
async function quickAction(action) {
    let message = '';
    switch (action) {
        case 'analyze':
            message = 'Could you analyze my business and provide recommendations?';
            break;
        case 'template':
            message = 'Can you help me create an email template?';
            break;
        case 'insights':
            message = 'What insights do you have about my business performance?';
            break;
    }
    
    if (message) {
        document.getElementById('chat-input').value = message;
        await sendMessage();
    }
}

// Handle AI actions
function handleActions(actions) {
    actions.forEach(action => {
        switch (action.type) {
            case 'analyze':
                // Trigger business analysis
                analyzeBusiness(action.data);
                break;
            case 'template':
                // Load template editor
                loadTemplate(action.data);
                break;
            case 'insight':
                // Display insights
                displayInsights(action.data);
                break;
        }
    });
}

// Initialize chat
document.addEventListener('DOMContentLoaded', () => {
    // Add welcome message
    addMessage('Hello! I'm your AI assistant. How can I help you today? You can ask me to:
1. Analyze your business
2. Create email templates
3. Get performance insights');
    
    // Set up enter key handling
    document.getElementById('chat-input').addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });
});
