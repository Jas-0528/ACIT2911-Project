document.getElementById("nav-burger").addEventListener("click", (event) => {
  event.preventDefault();
  var navLinks = document.getElementById("nav-links");
  if (navLinks.style.display === "none" || navLinks.style.display === "") {
    navLinks.style.display = "block";
  } else {
    navLinks.style.display = "none";
  }
});
