const internationalPhoneNumberRegex = /\d{4} \d{3} \d{4}/;

function isValidPhoneNumberInternational(phoneNumber) {
  return internationalPhoneNumberRegex.test(phoneNumber);
}

const phoneNumberInput = document.getElementById("phoneNumber");
const phonevalidationMessage = document.getElementById("validationphoneNumber");
var isPhoneValid = false;
phoneNumberInput.addEventListener("blur", () => {
  if (isValidPhoneNumberInternational(phoneNumberInput.value)) {
    phonevalidationMessage.textContent = "Valid phone number";
    phonevalidationMessage.style.color = "green";
    isPhoneValid = true;
  } else {
    phonevalidationMessage.textContent = "Invalid phone number";
    phonevalidationMessage.style.color = "red";
    isPhoneValid = false;
  }
});
