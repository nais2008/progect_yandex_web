// интересная фича
let docTitle = document.title;
window.addEventListener("blur", function () {
    document.title = "Давай обратно😥";
});
window.addEventListener("focus", function () {
    document.title = docTitle;
});


const body = document.querySelector("body");

// модальное окно
try {
    const modal = document.querySelector(".modal");
    const overlay = document.querySelector(".overlay");
    const openModalBtn = document.querySelector(".btn-open");
    const closeModalBtn = document.querySelector(".btn-close");

    openModalBtn.addEventListener("click", function () {
        modal.classList.remove("hidden");
        overlay.classList.remove("hidden");
        body.classList.add("lock");
    });
    closeModalBtn.addEventListener("click", function () {
        modal.classList.add("hidden");
        overlay.classList.add("hidden");
        body.classList.remove("lock");
    });
    overlay.addEventListener("click",function () {
        modal.classList.add("hidden");
        overlay.classList.add("hidden");
        body.classList.remove("lock");
    });
} catch (e) {}

// Мобильная адаптация слайдера
const swiper_galary = document.querySelector(".mySwiper");


function updateSlidesPerView() {
    if (window.innerWidth < 895) {
        swiper_galary.setAttribute("slides-per-view", "1");
    } else if (window.innerWidth < 1335) {
        swiper_galary.setAttribute("slides-per-view", "2");
    } else {
        swiper_galary.setAttribute("slides-per-view", "3");
    }
}


updateSlidesPerView();
window.addEventListener("resize", updateSlidesPerView);