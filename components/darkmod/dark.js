(function() {
    function toggleDarkMode() {
        document.body.classList.toggle("dark-mode");
        try {
            localStorage.setItem('darkMode', document.body.classList.contains('dark-mode'));
        } catch (error) {
            console.error("Error setting dark mode in localStorage:", error);
        }
    }

    try {
        if (localStorage.getItem('darkMode') === 'true') {
            document.body.classList.add('dark-mode');
        }
    } catch (error) {
        console.error("Error retrieving dark mode from localStorage:", error);
    }

    const button = document.createElement('button');
    button.classList.add('toggle-button');
    button.textContent = 'Toggle Dark Mode';
    button.addEventListener('click', toggleDarkMode);

    const style = document.createElement('style');
    style.textContent = `
        body {
            font-family: sans-serif;
            transition: background-color 0.3s ease, color 0.3s ease;
        }

        body.dark-mode {
            background-color: #222;
            color: #eee;
        }

        body.dark-mode label,
        body.dark-mode input,
        body.dark-mode select,
        body.dark-mode textarea {
            color: #eee;
        }

        body.dark-mode input[type="text"],
        body.dark-mode input[type="email"],
        body.dark-mode input[type="password"],
        body.dark-mode textarea {
            background-color: #444;
            border: 1px solid #555;
        }

        body.dark-mode button {
            background-color: #45a049; 
            color: white;
        }
        dark-mode input::selection {
  
        }
        .dark-mode .message.received {
            background-color: #555;
            align-self: flex-start;
        }
            

        body.dark-mode a {
            color: #888;
        }
        body.dark-mode nav {   
        background-color: #333; 
        color: white;
        padding: 10px 0;
        text-align: center; 
    }
        .container {
            width: 50%;
            height: 50%;
            margin: 50% auto;
            padding: 20px;
            background-color: #fff;
            border: 1px solid #ddd;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }

        .dark-mode .container {
            background-color: #444;
            border-color: #555;
            box-shadow: 0 0 10px rgba(255, 255, 255, 0.1);
            color : #eee;
        }
	.dark-mode h1{
         color: #eee;
        }
    .dark-mode button[type="submit"]:hover {
    background-color: #45a049;
}


        .toggle-button {
            position: fixed;
            bottom: 1%;
            right: 20px;
            padding: 10px 15px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            background-color: #4CAF50;
            color: white;
            transition: background-color 0.3s ease;
        }

        .toggle-button:hover {
            background-color: #45a049;
        }



        @media (max-width: 768px) {
            .toggle-button {
                bottom: 1%;
                right: 10px;
                padding: 8px 12px;
            }
        }
    `;

    document.body.appendChild(button);
    document.head.appendChild(style);
})();

