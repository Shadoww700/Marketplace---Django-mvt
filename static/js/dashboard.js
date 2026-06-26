/**
 * NEO•CORE - INTERACTIVE DASHBOARD SYSTEM BRAIN
 * UI Script Identity: Matrix Glitch Decoding & Interactive Cyber Particles
 */

document.addEventListener("DOMContentLoaded", () => {
    console.log("🔒 [SYSTEM] Dashboard neural interface initialized.");

    // 1. МАТРИЧНЫЙ ЭФФЕКТ ДЕКОДИРОВАНИЯ ЗАГОЛОВКОВ (Glitch Text Decoding)
    const charset = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@#$%&*_+?";
    const decodeElements = document.querySelectorAll("[data-decode]");

    decodeElements.forEach(element => {
        const originalText = element.innerText;
        let iteration = 0;
        let interval = null;

        // Функция запускается один раз при инициализации интерфейса
        interval = setInterval(() => {
            element.innerText = originalText
                .split("")
                .map((letter, index) => {
                    if (index < iteration) {
                        return originalText[index];
                    }
                    return charset[Math.floor(Math.random() * charset.length)];
                })
                .join("");

            if (iteration >= originalText.length) {
                clearInterval(interval);
                element.innerText = originalText; // Возвращаем финальный чистый текст
            }
            iteration += 1 / 2;
        }, 25);
    });

    // 2. КАСКАДНОЕ ПОЯВЛЕНИЕ СТРОК С ЭФФЕКТОМ КВАНТОВОГО СМЕЩЕНИЯ
    const logRows = document.querySelectorAll(".dashboard-log-row");
    logRows.forEach((row, index) => {
        row.style.opacity = "0";
        row.style.transform = "perspective(500px) rotateX(10deg) translateY(15px)";
        row.style.transition = "all 0.4s cubic-bezier(0.16, 1, 0.3, 1)";

        setTimeout(() => {
            row.style.opacity = "1";
            row.style.transform = "perspective(500px) rotateX(0deg) translateY(0)";
        }, 100 + index * 35); // Каждая следующая строка плавно вылетает за предыдущей
    });

    // 3. НЕОНОВЫЕ ИСКРЫ (MouseMove Sparkles) внутри строк логов
    logRows.forEach(row => {
        row.addEventListener("mousemove", (e) => {
            const rect = row.getBoundingClientRect();
            const x = e.clientX - rect.left; // Получаем координаты мыши внутри строки
            const y = e.clientY - rect.top;

            // Динамически передаем координаты в CSS-переменные для подсветки
            row.style.setProperty("--mouse-x", `${x}px`);
            row.style.setProperty("--mouse-y", `${y}px`);
        });
    });
});