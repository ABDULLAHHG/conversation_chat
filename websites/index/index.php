<!DOCTYPE html>

<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Conversation App</title>
    <style>

        body {
            font-family: sans-serif;
            margin: 0;
            background-color: #f4f4f4; 
            display: flex;
            flex-direction: column;
            min-height: 100vh; 
        }

      
        .container {
            flex: 1; 
            padding: 20px;
            display: flex;
            justify-content: center;
            align-items: center; 
        }

        h1 {
            color: #333; 
            text-align: center;
            margin: 10vh;

        }

        
        @media (max-width: 600px) {
            nav button {
                display: block; 
                margin: 10px auto;
                width: 80%; 
            }
        }
    </style>
</head>
<body>
<?php include "../../components\\navbar\\navbar.html";?>
    <div class="">
        <h1>Conversation App</h1>
    </div>
    <script src="../../components\\darkmod\\dark.js"></script> </body>
</html>