const burgerMenuBlock = document.querySelector(".hamburger");
const burgerMenuTogle = document.querySelector(".hamburger--line");
const burgerMenuNavigation = document.querySelector(".burger-navigation");

burgerMenuBlock.addEventListener("click", function(){
  burgerMenuTogle.classList.toggle("hamburger--line__x");
  body.classList.toggle("lock");
  burgerMenuNavigation.classList.toggle("active");
});