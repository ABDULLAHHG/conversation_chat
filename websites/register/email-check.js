// Regular expression for email validation.  This is a more robust regex than simpler ones.
const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

function isValidEmail(email) {
  return emailRegex.test(email);
}

const emailInput = document.getElementById("email");
const emailvalidationMessage = document.getElementById("validationEmail");
var isEmailValid = false;

emailInput.addEventListener("blur", () => {
  const email = emailInput.value.trim();

  if (isValidEmail(email)) {
    emailvalidationMessage.textContent = "Valid email address";
    emailvalidationMessage.style.color = "green";
    isEmailValid = true;
  } else {
    emailvalidationMessage.textContent = "Invalid email address";
    emailvalidationMessage.style.color = "red";
    isEmailValid = false;
  }
});