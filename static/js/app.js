// SocrAItes - Modern Philosophy Chat Interface
class SocrAItesChat {
    constructor() {
        this.currentPhilosopher = 'socrates';
        this.isLoading = false;
        this.conversations = [];
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.showWelcomeScreen();
        this.updatePhilosopher();
    }

    setupEventListeners() {
        // Send button
        const sendButton = document.getElementById('sendMessage');
        const messageInput = document.getElementById('messageInput');
        
        if (sendButton && messageInput) {
            sendButton.addEventListener('click', () => this.sendMessage());
            
            // Enter key handling
            messageInput.addEventListener('keydown', (e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    this.sendMessage();
                }
            });

            // Auto-resize textarea
            messageInput.addEventListener('input', (e) => this.autoResizeTextarea(e));
        }
        
        // Philosopher selection
        const philosopherSelect = document.getElementById('philosopherSelect');
        if (philosopherSelect) {
            philosopherSelect.addEventListener('change', (e) => {
                this.currentPhilosopher = e.target.value;
                this.updatePhilosopher();
            });
        }
    }

    autoResizeTextarea(e) {
        const textarea = e.target;
        textarea.style.height = 'auto';
        textarea.style.height = Math.min(textarea.scrollHeight, 120) + 'px';
    }

    showWelcomeScreen() {
        const chatMessages = document.getElementById('chatMessages');
        if (!chatMessages) return;

        // Clear any existing content
        chatMessages.innerHTML = '';

        // Create welcome message
        const welcomeDiv = document.createElement('div');
        welcomeDiv.className = 'welcome-screen';
        welcomeDiv.innerHTML = `
            <div class="welcome-title">Welcome to SocrAItes</div>
            <div class="welcome-subtitle">
                Dive deep into philosophical wisdom with AI-powered conversations. 
                Explore life's biggest questions with history's greatest thinkers.
            </div>
            <div class="philosopher-cards">
                <div class="philosopher-card" onclick="window.socraitesChat.selectPhilosopher('camus')">
                    <div class="philosopher-name">Albert Camus</div>
                    <div class="philosopher-description">Explore the absurd nature of existence and the human condition</div>
                </div>
                <div class="philosopher-card" onclick="window.socraitesChat.selectPhilosopher('nietzsche')">
                    <div class="philosopher-name">Friedrich Nietzsche</div>
                    <div class="philosopher-description">Challenge conventional morality and embrace radical thinking</div>
                </div>
                <div class="philosopher-card" onclick="window.socraitesChat.selectPhilosopher('dostoevsky')">
                    <div class="philosopher-name">Fyodor Dostoevsky</div>
                    <div class="philosopher-description">Delve into psychological depths and spiritual questioning</div>
                </div>
                <div class="philosopher-card" onclick="window.socraitesChat.selectPhilosopher('socrates')">
                    <div class="philosopher-name">Socrates</div>
                    <div class="philosopher-description">Question everything and discover wisdom through dialogue</div>
                </div>
                <div class="philosopher-card" onclick="window.socraitesChat.selectPhilosopher('kafka')">
                    <div class="philosopher-name">Franz Kafka</div>
                    <div class="philosopher-description">Navigate the absurd bureaucracy of modern existence</div>
                </div>
                <div class="philosopher-card" onclick="window.socraitesChat.selectPhilosopher('cioran')">
                    <div class="philosopher-name">Emil Cioran</div>
                    <div class="philosopher-description">Embrace pessimistic wisdom and lucid despair</div>
                </div>
            </div>
        `;
        
        chatMessages.appendChild(welcomeDiv);
    }

    selectPhilosopher(philosopher) {
        this.currentPhilosopher = philosopher;
        
        // Update dropdown
        const philosopherSelect = document.getElementById('philosopherSelect');
        if (philosopherSelect) {
            philosopherSelect.value = philosopher;
        }
        
        this.updatePhilosopher();
        this.startConversation();
    }

    startConversation() {
        const chatMessages = document.getElementById('chatMessages');
        if (!chatMessages) return;

        // Clear welcome screen
        chatMessages.innerHTML = '';

        // Add initial message from philosopher
        const welcomeText = this.getPhilosopherWelcome();
        this.addAIMessage(welcomeText, this.getPhilosopherName());
        
        // Focus input
        const messageInput = document.getElementById('messageInput');
        if (messageInput) {
            messageInput.focus();
        }
    }

    getPhilosopherWelcome() {
        const welcomes = {
            'camus': 'Ah, another soul searching for meaning in this absurd existence. I am Camus, and I invite you to explore the fundamental questions of human life with me. What weighs on your mind today?',
            'nietzsche': 'Welcome, fellow seeker of truth! I am Nietzsche, here to challenge your assumptions and push beyond conventional thinking. What sacred cows shall we examine today?',
            'dostoevsky': 'Greetings, dear friend. I am Dostoevsky, and I sense the deep currents of human nature that flow within you. Let us explore the mysteries of the soul together. What troubles your spirit?',
            'socrates': 'Welcome, my friend! I am Socrates, and I must confess - I know nothing. But through questioning together, perhaps we can discover some wisdom. What is it that you think you know, and how might we examine it?'
        };
        return welcomes[this.currentPhilosopher] || 'Hello! I\'m here to discuss philosophy with you. What would you like to explore?';
    }

    updatePhilosopher() {
        const philosophers = {
            'camus': {
                name: 'Albert Camus',
                description: 'Existentialist & Absurdist',
                avatar: 'AC'
            },
            'nietzsche': {
                name: 'Friedrich Nietzsche',
                description: 'Bold & Provocative',
                avatar: 'FN'
            },
            'dostoevsky': {
                name: 'Fyodor Dostoevsky',
                description: 'Psychological & Spiritual',
                avatar: 'FD'
            },
            'socrates': {
                name: 'Socrates',
                description: 'Questioner & Seeker',
                avatar: 'S'
            }
        };

        const philosopher = philosophers[this.currentPhilosopher];
        if (philosopher) {
            console.log(`Switched to ${philosopher.name}`);
        }
    }

    async sendMessage() {
        const input = document.getElementById('messageInput');
        const sendButton = document.getElementById('sendMessage');
        
        if (!input || !sendButton) {
            console.error('Input elements not found');
            return;
        }

        const message = input.value.trim();

        if (!message || this.isLoading) return;

        // Disable input
        this.isLoading = true;
        input.disabled = true;
        sendButton.disabled = true;

        // Add user message
        this.addUserMessage(message);
        input.value = '';
        input.style.height = 'auto';

        // Show typing indicator
        const typingIndicator = this.showTypingIndicator();

        try {
            // Create empty AI message for streaming
            const chatMessages = document.getElementById('chatMessages');
            const aiMessageElement = this.createMessage('ai', '', this.getPhilosopherName());
            const contentElement = aiMessageElement.querySelector('.message-content');
            
            // Remove typing indicator and add AI message
            if (typingIndicator && typingIndicator.parentNode) {
                typingIndicator.remove();
            }
            chatMessages.appendChild(aiMessageElement);
            this.scrollToBottom();

            // Start streaming
            const response = await fetch('/api/chat/stream', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    message: message,
                    philosopher: this.currentPhilosopher
                })
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            // Process streaming response
            const reader = response.body.getReader();
            const decoder = new TextDecoder();
            let buffer = '';

            while (true) {
                const { done, value } = await reader.read();
                
                if (done) break;
                
                buffer += decoder.decode(value, { stream: true });
                const lines = buffer.split('\n');
                buffer = lines.pop(); // Keep incomplete line in buffer
                
                for (const line of lines) {
                    if (line.startsWith('data: ')) {
                        try {
                            const data = JSON.parse(line.slice(6));
                            
                            if (data.type === 'content') {
                                // Update content with typing effect
                                contentElement.textContent = data.text;
                                this.scrollToBottom();
                            } else if (data.type === 'complete') {
                                // Final update
                                contentElement.textContent = data.text;
                                this.scrollToBottom();
                                break;
                            }
                        } catch (e) {
                            console.warn('Failed to parse streaming data:', e);
                        }
                    }
                }
            }

        } catch (error) {
            console.error('Error:', error);
            
            // Remove typing indicator if still present
            if (typingIndicator && typingIndicator.parentNode) {
                typingIndicator.remove();
            }
            
            // Try fallback to regular API
            try {
                const fallbackResponse = await fetch('/api/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        message: message,
                        philosopher: this.currentPhilosopher
                    })
                });
                
                if (fallbackResponse.ok) {
                    const data = await fallbackResponse.json();
                    this.addAIMessage(data.response, data.philosopher_name || this.getPhilosopherName());
                } else {
                    this.addAIMessage('I apologize, but I encountered an error while processing your question. Please try again.', 'Error');
                }
            } catch (fallbackError) {
                this.addAIMessage('I apologize, but I encountered an error while processing your question. Please try again.', 'Error');
            }
        } finally {
            // Re-enable input
            this.isLoading = false;
            input.disabled = false;
            sendButton.disabled = false;
            input.focus();
        }
    }

    addUserMessage(message) {
        const chatMessages = document.getElementById('chatMessages');
        if (!chatMessages) return;

        const messageElement = this.createMessage('user', message, 'You');
        chatMessages.appendChild(messageElement);
        this.scrollToBottom();
    }

    addAIMessage(message, philosopherName) {
        const chatMessages = document.getElementById('chatMessages');
        if (!chatMessages) return;

        const messageElement = this.createMessage('ai', message, philosopherName);
        chatMessages.appendChild(messageElement);
        this.scrollToBottom();
    }

    createMessage(type, text, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${type}`;

        const avatar = document.createElement('div');
        avatar.className = 'message-avatar';
        avatar.textContent = this.getAvatarText(type, sender);

        const content = document.createElement('div');
        content.className = 'message-content';

        const messageText = document.createElement('div');
        messageText.className = 'message-text';
        messageText.textContent = text;

        const meta = document.createElement('div');
        meta.className = 'message-meta';
        meta.textContent = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

        content.appendChild(messageText);
        content.appendChild(meta);
        messageDiv.appendChild(avatar);
        messageDiv.appendChild(content);

        return messageDiv;
    }

    getAvatarText(type, sender) {
        if (type === 'user') return 'You';
        
        const avatars = {
            'Albert Camus': 'AC',
            'Friedrich Nietzsche': 'FN',
            'Fyodor Dostoevsky': 'FD',
            'AI Guide': 'AI'
        };
        
        return avatars[sender] || sender.substring(0, 2).toUpperCase();
    }

    getPhilosopherName() {
        const names = {
            'camus': 'Albert Camus',
            'nietzsche': 'Friedrich Nietzsche',
            'dostoevsky': 'Fyodor Dostoevsky',
            'socrates': 'Socrates',
            'kafka': 'Franz Kafka',
            'cioran': 'Emil Cioran'
        };
        return names[this.currentPhilosopher] || 'Philosophy Guide';
    }

    showTypingIndicator() {
        const chatMessages = document.getElementById('chatMessages');
        if (!chatMessages) return null;

        const typingDiv = document.createElement('div');
        typingDiv.className = 'message ai typing-indicator';
        typingDiv.innerHTML = `
            <div class="message-avatar">
                ${this.getAvatarText('ai', this.getPhilosopherName())}
            </div>
            <div class="message-content">
                <div class="typing-dots">
                    <div class="typing-dot"></div>
                    <div class="typing-dot"></div>
                    <div class="typing-dot"></div>
                </div>
            </div>
        `;
        chatMessages.appendChild(typingDiv);
        this.scrollToBottom();
        return typingDiv;
    }

    scrollToBottom() {
        const chatMessages = document.getElementById('chatMessages');
        if (chatMessages) {
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }
    }
}

// Initialize the chat when the page loads
document.addEventListener('DOMContentLoaded', () => {
    window.socraitesChat = new SocrAItesChat();
});