document.getElementById('register-form').addEventListener('submit', function(event) {
    // Prevent default form submission behavior
    event.preventDefault();
    const submitvalidation = document.getElementById("vaildationSubmit");
    console.log(JSON.stringify({ Name : nameInput.value,Number:  phoneNumberInput.value, Email:emailInput.value, Password:passwordInput.value }))
    // Check if all fields are valid
    if (isNameValid && isEmailValid && isPhoneValid && isPasswordValid && isConfirmPasswordValid) {
      // Submit the form (replace with your actual submission logic)
      
      
      fetch(`http://${ip_address}:5000/register`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        // user data
        body: JSON.stringify({
            Name: nameInput.value,
            Number: phoneNumberInput.value,
            Email: emailInput.value,
            Password: passwordInput.value
        })
    })
    .then(response => {
        if (!response.ok) {
            // Handle errors based on HTTP status code
            if (response.status === 500) {  // Server-side error
                return response.json().then(data => {
                    // Assuming data.errors is the dictionary of errors
                    let errorMessages = [];
                    for (const [field, message] of Object.entries(data.errors)) {
                        var ValidationMessage = document.getElementById(`${field}`);
                        ValidationMessage.textContent = `${message}`;
                        ValidationMessage.style.color = "red";
                                            }
                    throw new Error(errorMessages.join('\n')); // Throw a custom error
                });
            } else {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
        }
        return response.json(); // Parse successful response
    })
    .then(data => {
        // Handle successful login
        if (data.success) { // Assuming your server returns a success flag
            sessionStorage.setItem('username', username.value);
            window.location.href = '../booking/booking.html';
        } else {
            submitvalidation.textContent = data.message || 'Login failed. Please try again.';
            submitvalidation.style.color = "red";
        }
    })

    .catch(error => {
        // Handle errors
        console.error('Registration failed:', error);
    });
    } else {
      // Display an error message (customize as needed)
      submitvalidation.textContent = "Missing information";
      submitvalidation.style.color = "red";


    }
  });



  
  // a@gmail.com 
  // 0770 585 6142 
  // aass12AASS