// Connect to the WebSocket server
const ws = new WebSocket('ws://localhost:8080');

// Connection opened
ws.onopen = () => {
    status.textContent = 'Connected to server';
    status.style.color = 'green';
};

// Listen for messages
ws.onmessage = (event) => {
    const message = document.createElement('div');
    message.className = 'message';
    message.textContent = event.data;
    messages.appendChild(message);
    messages.scrollTop = messages.scrollHeight;
};

// Handle errors
ws.onerror = (error) => {
    status.textContent = 'Error: ' + error.message;
    status.style.color = 'red';
};

// Handle connection close
ws.onclose = () => {
    status.textContent = 'Disconnected from server';
    status.style.color = 'red';
};

// Function to send a message
function sendMessage() {
    const message = messageInput.value.trim();
    if (message) {
    ws.send(message);
    messageInput.value = '';
    }
}

// Send message on Enter key
// messageInput.addEventListener('keypress', (e) => {
//     if (e.key === 'Enter') {
//     sendMessage();
//     }
// });