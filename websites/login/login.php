<!DOCTYPE html>

<?php include "../../components\\navbar\\navbar.html";?>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login</title>
    <link rel="stylesheet" href="login.css">
</head>
<body>
    <div class="container">
        <script src="../../components\\darkmod\\dark.js">
        </script>
        <h1>Login</h1>
        <form id="login-form">
            <label for="email">Email:</label>
            <input type="email" id="email" name="email">
            <p id="validationEmail"></p><br><br>
            <label for="password">Password:</label>
            <input type="password" id="password" name="password"><br><br>
            <button type="submit">Login</button>
        </form>
    </div>
    <script src="\www\reg3\components\get_ip\get_ip.js"></script>
    <script src="email-check.js"></script>
    <script src="login.js"></script>

</body>
</html>
