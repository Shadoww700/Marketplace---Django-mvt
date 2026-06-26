document.addEventListener("DOMContentLoaded", () => {
    // Декодер текста заголовка
    const charset = "0123456789ABCDEFΩΨ█";
    const titleObj = document.querySelector("[data-decode]");
    if (titleObj) {
        const orig = titleObj.innerText;
        let iter = 0;
        let inter = setInterval(() => {
            titleObj.innerText = orig.split("").map((let, i) => {
                if (i < iter) return orig[i];
                return charset[Math.floor(Math.random() * charset.length)];
            }).join("");
            if (iter >= orig.length) { clearInterval(inter); titleObj.innerText = orig; }
            iter += 1/2;
        }, 30);
    }

    // Логика переключения панелей
    const terminalScreen = document.getElementById("terminal-screen");
    const formScreen = document.getElementById("form-screen");
    const activateBtn = document.getElementById("activate-register-btn");
    const backBtn = document.getElementById("back-to-terminal");

    if (activateBtn && backBtn && terminalScreen && formScreen) {
        // Переход К форме регистрации
        activateBtn.addEventListener("click", () => {
            terminalScreen.classList.remove("active");
            formScreen.classList.add("active");
        });

        // Возврат ИЗ формы регистрации обратно к логам
        backBtn.addEventListener("click", (e) => {
            e.preventDefault();
            formScreen.classList.remove("active");
            terminalScreen.classList.add("active");
        });
    }

    // Если сервер вернул ошибку, сразу открываем экран с формой
    if (document.querySelector(".cyber-alert-box")) {
        if (terminalScreen && formScreen) {
            terminalScreen.classList.remove("active");
            formScreen.classList.add("active");
        }
    }
});