document.addEventListener("input", function(e) {
  if (e.target.matches("input[required]")) {
    const help = e.target.nextElementSibling;
    if (help && help.classList.contains("helptext")) {
      if (!e.target.checkValidity()) {
        help.style.color = "red";   // 🚨 invalid input
      } else {
        help.style.color = "#666";  // ✅ valid input
      }
    }
  }
});
