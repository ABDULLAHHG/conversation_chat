
// token is global , sender_username is global , message is getting from the input 
function sendMessage() {
    const messageInput = document.getElementById('messageInput');
    const messageText = messageInput.value.trim();

    if (messageText !== '') {
        
        
        // Send message to the server using AJAX
        const xhr = new XMLHttpRequest();
        xhr.open('POST', `http://${ip_address}:5000/sendmessage`, true);
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.setRequestHeader('Authorization', accessToken); // Set the Authorization header
        xhr.onreadystatechange = function () {

            if (xhr.readyState === XMLHttpRequest.DONE) {
                if (xhr.status === 200) {
                    
                    console.log('Message sent successfully');
                    // addSentMessage(messageText, true); // Add sent message to the chat
                    messageInput.value = ''; // Clear input
                } else {
                    console.error('Error sending message:', xhr.statusText);
                }
            }
        };
        console.log('Current conversation_id:', conversation_id);
        xhr.send(JSON.stringify({
            "conversation_id": conversation_id, // Ensure conversation_id is defined in your scope
            sender_username: currentChatUser,
            message: messageText
        }));
    }
}

// Function to receive messages
function receiveMessages() {
    const xhr = new XMLHttpRequest();
    xhr.open('GET', `http://${ip_address}:5000/receivedmessage?conversation_id=${conversation_id}`, true);
    xhr.setRequestHeader('Authorization', accessToken); // Set the Authorization header
    xhr.onreadystatechange = function () {
        if (xhr.readyState === XMLHttpRequest.DONE) {
            if (xhr.status === 200) {
                const messages = JSON.parse(xhr.responseText);
                messages.forEach(message => {
                    addReceivedMessage(message, false); // Add received message to the 
                    conversation_id = conversation_id;
                });
            } else {
                console.error('Error receiving messages:', xhr.statusText);
            }
        }
    };
    xhr.send();
}




function addSentMessage(message, isSent) {
    const chatMessages = document.getElementById('chatMessages');
    const messageElement = document.createElement('div');
    messageElement.classList.add('message', isSent ? 'sent' : 'received');
    messageElement.textContent = message;
    chatMessages.appendChild(messageElement);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function addReceivedMessage(message) {
    if (displayedMessageIds.has(message.message_id)) {
        return; // If the message ID has already been displayed, do nothing
    }

    displayedMessageIds.add(message.message_id); // Add the message ID to the set

    const chatMessages = document.getElementById('chatMessages');
    const messageElement = document.createElement('div');

    // Check if the message sender is the current user
    const isSent = message.sender_id === message.current_user_id;

    // Add the appropriate class based on whether the message is sent or received
    messageElement.classList.add('message', isSent ? 'sent' : 'received');
    messageElement.textContent = message.message; // Assuming message has a 'message' property
    chatMessages.appendChild(messageElement);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}