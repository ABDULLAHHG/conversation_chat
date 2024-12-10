<!DOCTYPE html>
<html lang="en">
<?php include "../../components\\navbar\\navbar.html";?>

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Registration</title>
    <link rel="stylesheet" href="register.css">
</head>
<body>
    <div class="container">
<script src="../../components\\darkmod\\dark.js">
</script>
        <h1>Registration</h1>
        <form id="register-form">
            
            <label for="name">Name:</label>
            <input type="text" id="name" name="name" placeholder="Enter your name">
            <p id="validationName"></p><br><br>
            
            <label for="number" >Number:</label>
            <input type="text" id="phoneNumber" name="number"  placeholder="+964 xxxx-xxx-xxxx" >
            <p id="validationphoneNumber"></p><br><br>
            
            <label for="email">Email:</label>
            <input type="email" id="email" name="email"  placeholder="enter your email eg. example@example.com" >
            <p id="validationEmail"></p><br><br>

            <label for="password">Password:</label>
            <input type="password" id="password" name="password" placeholder="Enter your password">
            <p id="validationPassword"></p><br><br>

            <label for="password">Confirm Password:</label>
            <input type="password" id="confirmPassword" name="password" placeholder="comfirm your password">
            <p id="validationConfrim-password"></p><br><br>

            <button type="submit">Register</button>
            <p id="vaildationSubmit"></p><br><br>

        </form>
    </div>

    <script src="\www\reg3\components\get_ip\get_ip.js"></script>
    <script src="password-check.js" defer></script>
    <script src="phone-check.js" defer></script>
    <script src="name-check.js" defer></script>
    <script src="email-check.js" defer></script>
    <script src="Confirmpassword-check.js" defer></script>
    <script src="submit.js" defer></script>

    <script>

</script>


</body>
</html>
