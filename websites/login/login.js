    const form = document.getElementById('login-form');

    form.addEventListener('submit', (e) => {
        e.preventDefault();
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;

        fetch(`http://${ip_address}:5000/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({"email": email, "password":password })
        })
        .then(res => {
            if (!res.ok) {
                return res.json().then(errorData => {
                    throw new Error(errorData.message || 'Login failed');
                });
            }
            return res.json();
        })
        .then(data => {
            // Instead of storing tokens, redirect to a temporary page
            const redirectUrl = `http://${ip_address}/www/reg3/websites/redirect/redirect.html?token=${encodeURIComponent(data.access_token)}`; // Replace 3001 with your temporary page port
            window.location.href = redirectUrl;
            })
        .catch(err => {
            console.error('Login failed:', err);
            // Display error message to the user
            // alert("Login failed. Please check your credentials.");
        });
    });

    //Remove the makeProtectedRequest and refreshToken functions as they are no longer needed in this approach.