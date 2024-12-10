// Retrieve the access token from session storage
const accessToken = sessionStorage.getItem('token');

if (accessToken) {
    // Send the user to the protected route with the access token in the header
    fetch(`http://${ip_address}:5000/username`, { // Your protected route
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${accessToken}`
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        // Check if username is present in the response
        if (data) {
            const username = data.username
            console.log(username)
            document.getElementById("username").textContent = username;
        } else {
            console.error('Username not found in the response.');
            window.location.href = '/www/reg3/websites/redirect/redirect.html'; // Replace with your actual protected website URL
            alert("Unexpected response from the server.");
        }
    })
    .catch(error => {
        console.error('Error accessing protected route:', error);
        window.location.href = '/www/reg3/websites/redirect/redirect.html'; // Replace with your actual protected website URL
        alert("Error accessing protected route. Please try again later.");
    });
} else {
    window.location.href = '/www/reg3/websites/redirect/redirect.html'; // Replace with your actual protected website URL
    console.error('Access token not found.');
    alert("Error: Access token not found.");
}