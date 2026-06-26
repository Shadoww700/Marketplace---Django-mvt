/**
 * NEO•CORE - ADMIN PANEL SYSTEMS CONTROL
 * UI Script Identity: Tactical Glow Manipulation & Decryption Streams
 */

document.addEventListener("DOMContentLoaded", () => {
    console.log("🛡️ [SECURITY RECON] Core Admin Interface active and secured.");

    // 1. МАТРИЧНОЕ ДЕКОДИРОВАНИЕ ТЕКСТА КЛАССА ДАННЫХ
    const matrixChars = "0101XYZΩΨ█▓▒░@#$§€";
    const decryptables = document.querySelectorAll("[data-decode]");

    decryptables.forEach(target => {
        const targetString = target.innerText;
        let counter = 0;
        let loop = setInterval(() => {
            target.innerText = targetString.split("").map((char, index) => {
                if (index < counter) return targetString[index];
                return matrixChars[Math.floor(Math.random() * matrixChars.length)];
            }).join("");
            
            if (counter >= targetString.length) {
                clearInterval(loop);
                target.innerText = targetString;
            }
            counter += 1 / 2;
        }, 20);
    });

    // 2. ИНТЕЛЛЕКТУАЛЬНАЯ ПОДСВЕТКА КАРТОЧЕК ЗАЯВОК (Tactical Status Hover)
    const applicationRows = document.querySelectorAll(".admin-application-row");

    applicationRows.forEach(row => {
        const approveBtn = row.querySelector(".btn-approve-core");
        const rejectBtn = row.querySelector(".btn-reject-core");

        if (approveBtn && rejectBtn) {
            // При наведении на одобрение - карточка становится зеленоватой
            approveBtn.addEventListener("mouseenter", () => {
                row.style.borderColor = "var(--neon-emerald)";
                row.style.boxShadow = "0 0 20px rgba(16, 185, 129, 0.15)";
                row.style.background = "rgba(4, 30, 20, 0.4)";
            });

            // При наведении на отказ - карточка становится красной
            rejectBtn.addEventListener("mouseenter", () => {
                row.style.borderColor = "#ef4444";
                row.style.boxShadow = "0 0 20px rgba(239, 68, 68, 0.15)";
                row.style.background = "rgba(45, 10, 10, 0.4)";
            });

            // Возврат в исходное дефолтное состояние
            const resetState = () => {
                row.style.borderColor = "var(--glass-border)";
                row.style.boxShadow = "none";
                row.style.background = "rgba(7, 11, 22, 0.45)";
            };

            approveBtn.addEventListener("mouseleave", resetState);
            rejectBtn.addEventListener("mouseleave", resetState);
        }
    });
});