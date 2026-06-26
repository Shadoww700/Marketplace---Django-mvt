/**
 * NEO•CORE - SECURITY IDENTITY VERIFICATION CONTROLLER
 * UI Script Identity: Multi-Cell OTP Splitter & Auto-Tab Engine
 */

document.addEventListener("DOMContentLoaded", () => {
    console.log("🔑 [SECURITY MODULE] Identity verification layer standing by.");

    // 1. МАТРИЧНЫЙ ТЕКСТ ЗАГОЛОВКА
    const charset = "0123456789X█▓▒░@#$";
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

    // 2. УПРАВЛЕНИЕ МНОГОЯЧЕЕЧНЫМ ВВОДОМ (Multi-cell OTP UX)
    const cells = document.querySelectorAll(".code-cell");
    const hiddenInput = document.getElementById("code");
    const form = document.getElementById("verification-form");

    if (cells.length > 0 && hiddenInput && form) {
        
        // Фокусируемся на первой ячейке сразу при загрузке
        cells[0].focus();

        cells.forEach((cell, index) => {
            // Обработка ввода символа
            cell.addEventListener("input", (e) => {
                // Разрешаем только цифры
                cell.value = cell.value.replace(/[^0-9]/g, "");

                if (cell.value.length === 1 && index < cells.length - 1) {
                    // Переходим к следующей ячейке, если текущая заполнена
                    cells[index + 1].focus();
                }
                updateHiddenValue();
            });

            // Обработка стирания (Backspace) и навигации стрелками
            cell.addEventListener("keydown", (e) => {
                if (e.key === "Backspace" && cell.value.length === 0 && index > 0) {
                    // Возвращаемся назад при Backspace, если поле пустое
                    cells[index - 1].focus();
                } else if (e.key === "ArrowLeft" && index > 0) {
                    cells[index - 1].focus();
                } else if (e.key === "ArrowRight" && index < cells.length - 1) {
                    cells[index + 1].focus();
                }
            });

            // Поддержка вставки всего кода целиком (Paste Event, например "123456")
            cell.addEventListener("paste", (e) => {
                e.preventDefault();
                const pasteData = (e.clipboardData || window.clipboardData).getData("text").trim();
                
                if (/^\d{6}$/.test(pasteData)) { // Если в буфере ровно 6 цифр
                    pasteData.split("").forEach((char, i) => {
                        if (cells[i]) cells[i].value = char;
                    });
                    cells[cells.length - 1].focus();
                    updateHiddenValue();
                }
            });
        });

        // Функция сбора данных из ячеек в один скрытый input
        function updateHiddenValue() {
            let combinedCode = "";
            cells.forEach(cell => combinedCode += cell.value);
            hiddenInput.value = combinedCode;
        }

        // Валидация перед отправкой
        form.addEventListener("submit", (e) => {
            updateHiddenValue();
            if (hiddenInput.value.length !== 6) {
                e.preventDefault();
                console.error("⛔ [SECURITY ERROR] Code block incomplete.");
                // Трясем форму, если код неполный
                form.classList.add("shake-animation");
                setTimeout(() => form.classList.remove("shake-animation"), 400);
            }
        });
    }
});