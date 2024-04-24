// динамический поиск
document.addEventListener('DOMContentLoaded', function() {
  const searchForm = document.querySelector('.search-form');
  const searchInput = searchForm.querySelector('input[name="search"]');
  const productListContainer = document.querySelector('.product .giutar');

  searchForm.addEventListener('input', function(event) {
    const searchTerm = searchInput.value.trim(); // Получаем значение поискового запроса

    // Выполняем AJAX-запрос к маршруту /shop с использованием POST-запроса и передаем search_term
    fetch('/shop', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded' // Устанавливаем заголовок Content-Type
        },
        body: `search_term=${encodeURIComponent(searchTerm)}` // Передаем данные в формате x-www-form-urlencoded
    })
    .then(response => response.json()) // Преобразуем ответ в формат JSON
    .then(data => {
      // Очищаем контейнер с товарами
      productListContainer.innerHTML = '';

      // Обрабатываем результаты поиска и отображаем их на странице
      data.products.forEach(product => {
        const productElement = document.createElement('div');
        productElement.classList.add('item');
        productElement.innerHTML = `
          <div class="item item${product.id}">
            <img src="https://www.slapshop.ru/upload/iblock/806/k014nz3bcntldhvrgej0z1uvdbavhut6.jpg" alt="">
            <div class="text">
              <h3>${product.title}</h3>
              <p>${product.content}</p>
              <a href="/info_product/${product.id}" class="btn btn_info">Больше информации</a>
            </div>
          </div>
        `;
        productListContainer.appendChild(productElement);
      });
    })
    .catch(error => console.error('Ошибка:', error)); // Обрабатываем ошибки
  });
});

// кнопка вверх
const showOnPx = 100;
const backToTopButton = document.querySelector(".back-to-top")

const scrollContainer = () => {
  return document.documentElement || document.body;
};

document.addEventListener("scroll", () => {
  if (scrollContainer().scrollTop > showOnPx) {
    backToTopButton.style.opacity = "1";
    backToTopButton.style.outline = "3px solid #FFF0BB";
  } else {
    backToTopButton.style.opacity = "0";
    backToTopButton.style.outline = "none";
  }
})

const goToTop = () => {
	document.body.scrollIntoView({
    behavior: "smooth",
  });
};

backToTopButton.addEventListener("click", goToTop);