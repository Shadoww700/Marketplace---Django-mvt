/**
 * NEO•CORE — QUANTUM MARKETPLACE SCRIPT ENGINE
 * UI Control: Real-time Sector Filtering & AI Terminal Decryption
 */

document.addEventListener("DOMContentLoaded", () => {
    console.log("📡 [SYSTEM] Quantum Marketplace UI core operational.");

    // 1. ЭФФЕКТ ПЕЧАТНОЙ МАШИНКИ ДЛЯ ТЕРМИНАЛА AI
    const typingContainer = document.querySelector(".ai-typing-target");
    
    if (typingContainer) {
        const rawText = typingContainer.getAttribute("data-raw-text") || "";
        let currentIndex = 0;
        typingContainer.innerText = ""; // Очищаем контейнер перед симуляцией

        function typeCharacter() {
            if (currentIndex < rawText.length) {
                typingContainer.innerText += rawText.charAt(currentIndex);
                currentIndex++;
                // Случайный интервал задержки для имитации живого терминала
                setTimeout(typeCharacter, Math.random() * 15 + 10);
            }
        }
        
        // Запуск протокола вывода через 400мс после загрузки зоны
        setTimeout(typeCharacter, 400);
    }

    // 2. ИНТЕРАКТИВНАЯ ФИЛЬТРАЦИЯ СЕКТОРОВ (КАТЕГОРИЙ) БЕЗ ПЕРЕЗАГРУЗКИ
    const categoryChips = document.querySelectorAll(".category-chip");
    const productCards = document.querySelectorAll(".product-card");

    categoryChips.forEach(chip => {
        chip.addEventListener("click", () => {
            // Переключаем активный чип
            categoryChips.forEach(c => c.classList.remove("active"));
            chip.classList.add("active");

            const selectedSector = chip.getAttribute("data-category");

            productCards.forEach(card => {
                const cardSector = card.getAttribute("data-product-sector");
                if (selectedSector === "all" || cardSector === selectedSector) {
                    card.style.display = "block";
                } else {
                    card.style.display = "none";
                }
            });
        });
    });
});

document.addEventListener('DOMContentLoaded', () => {
    const lightbox = document.getElementById('lightbox');
    const fullImg = document.getElementById('full-img');
    const images = document.querySelectorAll('.product-image');

    images.forEach(img => {
        img.addEventListener('click', () => {
            lightbox.style.display = 'flex';
            fullImg.src = img.src;
        });
    });

    // Закрытие при клике
    lightbox.addEventListener('click', () => {
        lightbox.style.display = 'none';
    });
});