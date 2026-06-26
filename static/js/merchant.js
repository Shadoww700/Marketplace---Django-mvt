/**
 * NEO•CORE - MERCHANT APPLICATION CONTROLLER
 * UI Script Identity: Form Integrity Scan & Matrix Text Effects
 */

document.addEventListener("DOMContentLoaded", () => {
    console.log("📡 [SYSTEM] Merchant application uplink established.");

    // 1. ДЕКОДИРОВАНИЕ ЗАГОЛОВКА
    const charset = "ABCDEFGHIKLMNOPQRSTUVWXYZZ0123456789#!@$%*";
    const titleObj = document.querySelector("[data-decode]");
    if (titleObj) {
        const origText = titleObj.innerText;
        let iter = 0;
        let inter = setInterval(() => {
            titleObj.innerText = origText.split("").map((let, i) => {
                if (i < iter) return origText[i];
                return charset[Math.floor(Math.random() * charset.length)];
            }).join("");
            if (iter >= origText.length) { clearInterval(inter); titleObj.innerText = origText; }
            iter += 1/2;
        }, 30);
    }

    // 2. ИНТЕРАКТИВНЫЙ ИНДИКАТОР ПЛОТНОСТИ ДАННЫХ (Data Density Scanner)
    const messageArea = document.getElementById("message");
    const progressBar = document.getElementById("scan-progress-fill");
    const progressText = document.getElementById("scan-percentage");

    if (messageArea && progressBar && progressText) {
        messageArea.addEventListener("input", () => {
            const textLength = messageArea.value.length;
            
            // Считаем прогресс: 150 символов = 100% заполнения "Траста лога"
            let percentage = Math.min(Math.round((textLength / 150) * 100), 100);
            
            // Обновляем ширину прогресс-бара и текст
            progressBar.style.width = `${percentage}%`;
            progressText.innerText = `${percentage}%`;

            // Динамически меняем цвета шкалы в зависимости от заполнения
            if (percentage < 30) {
                progressBar.style.background = "var(--neon-orange)";
                progressText.style.color = "var(--neon-orange)";
            } else if (percentage < 70) {
                progressBar.style.background = "var(--neon-purple)";
                progressText.style.color = "var(--neon-purple)";
            } else {
                progressBar.style.background = "var(--neon-cyan)";
                progressText.style.color = "var(--neon-cyan)";
                progressBar.style.boxShadow = "0 0 10px var(--neon-cyan)";
            }
        });
    }
});