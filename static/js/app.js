// AI Philosophy Chatbot JavaScript

class PhilosophyChat {
    constructor() {
        this.currentPhilosopher = 'neutral';
        this.philosophers = {};
        this.isLoading = false;
        this.init();
    }

    async init() {
        await this.loadPhilosophers();
        await this.loadTopics();
        this.setupEventListeners();
        this.updatePhilosopherInfo();
    }

    async loadPhilosophers() {
        try {
            const response = await fetch('/api/philosophers');
            this.philosophers = await response.json();
        } catch (error) {
            console.error('Error loading philosophers:', error);
        }
    }

    async loadTopics() {
        try {
            const response = await fetch('/api/topics');
            const topics = await response.json();
            this.displayTopics(topics);
        } catch (error) {
            console.error('Error loading topics:', error);
        }
    }

    displayTopics(topics) {
        const container = document.getElementById('topicSuggestions');
        container.innerHTML = '';
        
        topics.slice(0, 5).forEach(topic => {
            const button = document.createElement('button');
            button.className = 'btn topic-btn';
            button.textContent = topic;
            button.onclick = () => this.sendTopicMessage(topic);
            container.appendChild(button);
        });
    }

    setupEventListeners() {
        // Philosopher selection
        document.getElementById('philosopherSelect').addEventListener('change', (e) => {
            this.currentPhilosopher = e.target.value;
            this.updatePhilosopherInfo();
        });

        // Send message button
        document.getElementById('sendMessage').addEventListener('click', () => {
            this.sendMessage();
        });

        // Enter key in input
        document.getElementById('messageInput').addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });

        // Clear conversation
        document.getElementById('clearConversation').addEventListener('click', () => {
            this.clearConversation();
        });
    }

    updatePhilosopherInfo() {
        const philosopher = this.philosophers[this.currentPhilosopher];
        if (philosopher) {
            document.getElementById('philosopherName').textContent = philosopher.name;
            document.getElementById('philosopherDescription').textContent = philosopher.description;
            document.getElementById('philosopherPeriod').textContent = philosopher.period;
            document.getElementById('currentPhilosopher').textContent = philosopher.name;
            
            // Update visual styling
            const infoDiv = document.getElementById('philosopherInfo');
            infoDiv.className = `mb-4 p-3 bg-secondary rounded philosopher-${this.currentPhilosopher}`;
        }
    }

    async sendMessage() {
        const input = document.getElementById('messageInput');
        const message = input.value.trim();
        
        if (!message || this.isLoading) return;

        // Clear input and disable sending
        input.value = '';
        this.setLoading(true);

        // Add user message to chat
        this.addMessage(message, 'user');

        // Show typing indicator
        this.showTypingIndicator();

        try {
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    message: message,
                    philosopher: this.currentPhilosopher
                })
            });

            const data = await response.json();
            
            if (response.ok) {
                this.hideTypingIndicator();
                this.addMessage(data.response, 'bot', data.sources);
            } else {
                throw new Error(data.error || 'Something went wrong');
            }
        } catch (error) {
            this.hideTypingIndicator();
            this.addMessage('I apologize, but I encountered an error. Please try again.', 'bot');
            console.error('Chat error:', error);
        } finally {
            this.setLoading(false);
        }
    }

    sendTopicMessage(topic) {
        document.getElementById('messageInput').value = topic;
        this.sendMessage();
    }

    addMessage(content, sender, sources = []) {
        const chatMessages = document.getElementById('chatMessages');
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message`;

        const philosopherName = sender === 'bot' 
            ? this.philosophers[this.currentPhilosopher]?.name || 'Philosophy Guide'
            : 'You';

        let sourcesHtml = '';
        if (sources && sources.length > 0) {
            sourcesHtml = '<div class="sources"><small class="text-muted">Sources:</small>';
            sources.forEach(source => {
                sourcesHtml += `<div class="source-item">${source.text}</div>`;
            });
            sourcesHtml += '</div>';
        }

        messageDiv.innerHTML = `
            <div class="message-content">
                ${sender === 'bot' ? `<strong>${philosopherName}:</strong> ` : ''}
                ${content}
                ${sourcesHtml}
            </div>
        `;

        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    showTypingIndicator() {
        const chatMessages = document.getElementById('chatMessages');
        const typingDiv = document.createElement('div');
        typingDiv.id = 'typingIndicator';
        typingDiv.innerHTML = `
            <div class="typing-indicator">
                <span></span>
                <span></span>
                <span></span>
            </div>
        `;
        chatMessages.appendChild(typingDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    hideTypingIndicator() {
        const typingIndicator = document.getElementById('typingIndicator');
        if (typingIndicator) {
            typingIndicator.remove();
        }
    }

    setLoading(loading) {
        this.isLoading = loading;
        const sendButton = document.getElementById('sendMessage');
        const messageInput = document.getElementById('messageInput');
        
        sendButton.disabled = loading;
        messageInput.disabled = loading;
        
        if (loading) {
            sendButton.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
        } else {
            sendButton.innerHTML = '<i class="fas fa-paper-plane"></i>';
        }
    }

    async clearConversation() {
        try {
            await fetch('/api/clear_conversation', { method: 'POST' });
            
            // Clear chat messages except welcome message
            const chatMessages = document.getElementById('chatMessages');
            chatMessages.innerHTML = `
                <div class="message bot-message">
                    <div class="message-content">
                        <strong>Philosophy Guide:</strong> Welcome! I'm here to discuss philosophical questions with you. 
                        Choose a philosopher from the sidebar to chat with their persona, or stick with me for general philosophical exploration.
                        What would you like to discuss today?
                    </div>
                </div>
            `;
        } catch (error) {
            console.error('Error clearing conversation:', error);
        }
    }
}

// Initialize the chat application when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new PhilosophyChat();
});
