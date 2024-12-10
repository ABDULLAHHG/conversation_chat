function arePasswordsMatching(password, confirmPassword) {
    return password === confirmPassword;
  }
  
  const confirmPasswordInput = document.getElementById("confirmPassword");
  const ConfirmPasswordvalidationMessage = document.getElementById("validationConfrim-password");
  var isConfirmPasswordValid = false;
  confirmPasswordInput.addEventListener("blur", () => {
    if (arePasswordsMatching(passwordInput.value, confirmPasswordInput.value)) {
      ConfirmPasswordvalidationMessage.textContent = "Passwords match";
      ConfirmPasswordvalidationMessage.style.color = "green";
      isConfirmPasswordValid = true;
    } else {
      ConfirmPasswordvalidationMessage.textContent = "Passwords do not match";
      ConfirmPasswordvalidationMessage.style.color = "red";
      isConfirmPasswordValid = false;
    }
  });