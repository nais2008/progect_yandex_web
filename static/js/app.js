// параллакс на странице с информацией о товаре
document.addEventListener("mousemove", function (e) {
    Object.assign(document.documentElement, {
        style: `
            --move-x: ${(e.clientX - window.innerWidth / 2) * 0.007}deg;
            --move-y: ${(e.clientY - window.innerHeight / 2) * -0.01}deg;
        `
    });
});

// интересная фича
let docTitle = document.title;
window.addEventListener("blur", function () {
    document.title = "Давай обратно😥";
});
window.addEventListener("focus", function () {
    document.title = docTitle;
});