let conversation_id; // Declare at the top of your script

async function searchUser() {
    const searchInput = document.getElementById('searchInput');
    const searchTerm = searchInput.value.trim();
    const searchResults = document.getElementById('search-results');
    searchResults.innerHTML = '';

    if (searchTerm === '') {
        const li = document.createElement('li');
        li.textContent = 'Please enter a username.';
        searchResults.appendChild(li);
        return;
    }

    try {
        const accessToken = sessionStorage.getItem('token') || ''; // Simplified token retrieval
        
        const response = await fetch(`http://${ip_address}:5000/search_user/${encodeURIComponent(searchTerm)}`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${accessToken}` // Sending token in headers
            }
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const result = await response.json();

        if (result.exists) {
            startChat(searchTerm); // Open chat if username exists
            // const li = document.createElement('li');
            // li.textContent = `Conversation created with "${searchTerm}". ID: ${result.conversation_id}`;
            conversation_id = result.conversation_id;
        } else {
            const li = document.createElement('li');
            li.textContent = `User "${searchTerm}" does not exist.`;
            searchResults.appendChild(li);
        }
    } catch (error) {
        console.error('Error checking username:', error);
        const li = document.createElement('li');
        li.textContent = 'An error occurred while checking the username.';
        searchResults.appendChild(li);
    }
}
