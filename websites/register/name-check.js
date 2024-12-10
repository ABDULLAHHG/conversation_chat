function isNameValidF(name) {
    return name.trim() !== ""; 
  }
  
  const nameInput = document.getElementById("name");
  const NamevalidationMessage = document.getElementById("validationName");
  var isNameValid = false;
  nameInput.addEventListener("blur", () => {
    if (isNameValidF(nameInput.value)) {
      NamevalidationMessage.textContent = "Valid name";
      NamevalidationMessage.style.color = "green";
      isNameValid = true;
    } else {
      NamevalidationMessage.textContent = "Name cannot be empty";
      NamevalidationMessage.style.color = "red";
      isNameValid = false;
    }
  });