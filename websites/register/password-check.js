const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$/;

function isValidPassword(password) {
  return passwordRegex.test(password);
}

const passwordInput = document.getElementById("password");
const passwordvalidationMessage = document.getElementById("validationPassword");
var isPasswordValid = false;
passwordInput.addEventListener("blur", () => {
  if (isValidPassword(passwordInput.value)) {
    passwordvalidationMessage.textContent = "Valid password";
    passwordvalidationMessage.style.color = "green";
    isPasswordValid = true;
  } else {
    passwordvalidationMessage.textContent = "Invalid password. Password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, and one number.";
    passwordvalidationMessage.style.color = "red";
    isPasswordValid = false;
  }
});


