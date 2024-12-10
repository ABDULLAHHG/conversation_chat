let currentChatUser = null;
let pollingInterval;
const displayedMessageIds = new Set();

// Navigation
const pages = document.querySelectorAll('.page');
const navLinks = document.querySelectorAll('nav a');
navLinks.forEach(link => {
    link.addEventListener('click', (e) => {
        e.preventDefault();
        showPage(link.getAttribute('href').substring(1));
    });
});

function showPage(pageId) {
    displayedMessageIds.clear();
    pages.forEach(page => page.classList.remove('active'));
    document.getElementById(pageId).classList.add('active');

    if (pageId === 'contacts') {
        displayedMessageIds.clear();
        stopPolling();
        fetchContacts(accessToken).then(contacts => {
            displayContacts(contacts);
        });
    } else if (pageId === 'chat') {
        displayedMessageIds.clear();
        receiveMessages();
        startPolling();
    } else if (pageId === 'search') {
        displayedMessageIds.clear();
    } else if (pageId === 'communication') {
        displayedMessageIds.clear();
        updateCommunicationHistory();
    }
}

// Function to stop polling
function stopPolling() {
    if (pollingInterval) {
        clearInterval(pollingInterval);
        pollingInterval = null;
        console.log('Stopped polling for new messages');
    }
}

function startPolling() {
    if (!pollingInterval) {
        pollingInterval = setInterval(receiveMessages, 2000);
        console.log('Started polling for new messages');
    }
}

function startChat(user , conversationId = null) {
    if(conversationId){
        conversation_id = conversationId;
    }
    
    currentChatUser = user;
    const chatHeader = document.getElementById('chat-header');
    chatHeader.textContent = `Chat with ${currentChatUser}`;
    showPage('chat');
    document.getElementById('chatMessages').innerHTML = '';
    // Add a received message when the chat starts
}

// Function to fetch and update communication history
async function updateCommunicationHistory() {
    const communicationHistory = document.getElementById('communicationHistory');
    communicationHistory.innerHTML = ''; // Clear existing history

    try {
        const response = await fetch(`http://${ip_address}:5000/get_communication_history`, {
            headers: {
                'Authorization': `Bearer ${accessToken}` // Replace accessToken with your actual token
            }
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();

        data.forEach(item => {
            const entry = document.createElement('div');
            entry.classList.add('contact-entry');
            entry.innerHTML = `
                <div class="contact-name">${item.username}</div>
                <div class="last-message">${item.message} (${item.timestamp})</div>
            `;
            entry.addEventListener('click', () => startChat(item.username, item.conversation_id));
            communicationHistory.appendChild(entry);
        });
    } catch (error) {
        console.error('Error fetching communication history:', error);
        // Handle error appropriately, e.g., display an error message to the user.
    }
}


showPage('search');


