function filterPlants() {
    const searchInput = document.getElementById("search").value.toLowerCase();
    const plantList = document.getElementById("plant-list");
    const plants = plantList.getElementsByTagName("li");

    for (let i = 0; i < plants.length; i++) {
        const plantName = plants[i].textContent || plants[i].innerText;
        if (plantName.toLowerCase().indexOf(searchInput) > -1) {
            plants[i].style.display = "";
        } else {
            plants[i].style.display = "none";
        }
    }
}

document.getElementById("profileForm").onsubmit = function(event) {
    event.preventDefault(); // Предотвращаем перезагрузку страницы
    const name = document.getElementById("name").value;
    const email = document.getElementById("email").value;

    // Сохраняем данные
    if (name) {
        document.getElementById("username").innerText = name;
        alert("Данные сохранены!");
    } else {
        alert("Пожалуйста, введите ваше имя.");
    }
};

document.getElementById("plantForm").onsubmit = function(event) {
    event.preventDefault(); // Предотвращаем перезагрузку страницы
    const plantName = document.getElementById("plantName").value;

    if (plantName) {
        addPlant(plantName);
        document.getElementById("plantName").value = ""; // Очищаем поле ввода
    } else {
        alert("Пожалуйста, введите название растения.");
    }
};

function addPlant(name) {
    const plantList = document.getElementById("plantList");
    const li = document.createElement("li");

    // Создаем ссылку на страницу растения
    let plantLink = '';
    switch (name.toLowerCase()) {
        case 'монстера':
            plantLink = '<a href="monstera.html">Монстера</a>';
            break;
        case 'фикус':
            plantLink = '<a href="fikus.html">Фикус</a>';
            break;
        case 'потос':
            plantLink = '<a href="pothos.html">Потос</a>';
            break;
        default:
            plantLink = name; // Если не найдено — просто показываем имя
            break;
    }

    li.innerHTML = `${plantLink} <button onclick="waterPlant(this)">Полить</button> <span> Полив: Never</span>`;
    plantList.appendChild(li);
}

function waterPlant(button) {
    const plantLi = button.parentNode;
    const wateringSpan = plantLi.querySelector("span");
    const currentDate = new Date().toLocaleDateString();
    wateringSpan.innerText = ` Полив: ${currentDate}`;
}
