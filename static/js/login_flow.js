/**
 * NEO•CORE - ENTITY LOGIN CONTROLLER
 * UI Script Identity: Matrix Core Decryption & Live Crypto Input Feedback
 */

document.addEventListener("DOMContentLoaded", () => {
    console.log("🔒 [SYSTEM] Authentication gateway module deployed.");

    // 1. МАТРИЧНОЕ ДЕКОДИРОВАНИЕ ЗАГОЛОВКА
    const charset = "0123456789ABCDEFΩΨ█#@$";
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

    // 2. ИНТЕРАКТИВНЫЙ МОНИТОР ПАРОЛЯ (Live Crypto Status)
    const passwordInput = document.getElementById("password");
    const cryptoDot = document.querySelector(".crypto-dot");
    const cryptoText = document.getElementById("crypto-text");

    if (passwordInput && cryptoDot && cryptoText) {
        passwordInput.addEventListener("input", () => {
            const passLength = passwordInput.value.length;

            if (passLength > 0) {
                // Включаем активное состояние генерации хеша
                cryptoDot.classList.add("crypto-active");
                cryptoText.innerText = `Uplink Status: Hashing Dynamic Key [len: ${passLength}]...`;
                cryptoText.style.color = "var(--neon-cyan)";
            } else {
                // Возвращаем дефолтный режим ожидания
                cryptoDot.classList.remove("crypto-active");
                cryptoText.innerText = "Uplink Status: Encrypted Pipeline Standby";
                cryptoText.style.color = "var(--text-muted)";
            }
        });
    }
});