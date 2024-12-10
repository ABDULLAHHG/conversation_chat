
function fetchContacts(token) {
    return fetch(`http://${ip_address}:5000/get_contacts`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json', // Good practice
            'Authorization': `Bearer ${token}` // Ensure this is correct
        },
        // Leave body out if not needed
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json(); // Parse JSON response
    })
    .then(data => {
        console.log(data); // Handle the response data
        return data; // Consider returning data for further use
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

const chatOutput = document.getElementById('chat-output');



function displayContacts(contacts) {
    const contactList = document.getElementById('contact-list');
    contactList.innerHTML = ''; // Clear existing contacts

    // Check if contacts is an array and has elements
    if (!Array.isArray(contacts) || contacts.length === 0) {
        contactList.innerHTML += '<p>No contacts found.</p>';
        return;
    }

    // If contacts contains only one object, handle it directly
    if (contacts.length === 1) {
        const contact = contacts[0]; // Access the single contact

        // Log the contact for debugging
        console.log(contact); 

        const li = document.createElement('li');
        li.textContent = contact.username; // Display the username
        li.addEventListener('click', () => startChat(contact.username, contact.conversation_id)); // Pass conversation_id
        contactList.appendChild(li); // Append the list item to the contact list
    } else {
        // Loop through contacts if there are multiple
        for (let i = 0; i < contacts.length; i++) {
            const contact = contacts[i]; // Access the current contact

            // Log the contact for debugging
            console.log(contact); 

            const li = document.createElement('li');
            li.textContent = contact.username; // Display the username
            li.addEventListener('click', () => startChat(contact.username, contact.conversation_id)); // Pass conversation_id
            contactList.appendChild(li); // Append the list item to the contact list
        }
    }
}