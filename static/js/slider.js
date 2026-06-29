/* ==========================================================================
   PRODUCT IMAGE SLIDER
   Листает фотки внутри карточки товара стрелками
   ========================================================================== */

document.addEventListener('DOMContentLoaded', () => {

    document.querySelectorAll('.product-card').forEach(card => {
        const wrapper = card.querySelector('.product-image-wrapper');
        if (!wrapper) return;

        const imgs = wrapper.querySelectorAll('.product-image');
        if (imgs.length <= 1) return; // одна фотка — слайдер не нужен

        let current = 0;

        // Прячем все кроме первой
        imgs.forEach((img, i) => {
            img.style.display = i === 0 ? 'block' : 'none';
        });

        // Счётчик "1 / 3"
        const counter = document.createElement('div');
        counter.className = 'slider-counter';
        counter.textContent = `1 / ${imgs.length}`;
        wrapper.appendChild(counter);

        // Кнопка назад
        const btnPrev = document.createElement('button');
        btnPrev.className = 'slider-btn slider-btn-prev';
        btnPrev.innerHTML = '&#8249;'; // ‹
        wrapper.appendChild(btnPrev);

        // Кнопка вперёд
        const btnNext = document.createElement('button');
        btnNext.className = 'slider-btn slider-btn-next';
        btnNext.innerHTML = '&#8250;'; // ›
        wrapper.appendChild(btnNext);

        // Точки-индикаторы
        const dots = document.createElement('div');
        dots.className = 'slider-dots';
        imgs.forEach((_, i) => {
            const dot = document.createElement('span');
            dot.className = 'slider-dot' + (i === 0 ? ' active' : '');
            dot.addEventListener('click', () => goTo(i));
            dots.appendChild(dot);
        });
        wrapper.appendChild(dots);

        function goTo(index) {
            imgs[current].style.display = 'none';
            dots.children[current].classList.remove('active');
            current = (index + imgs.length) % imgs.length;
            imgs[current].style.display = 'block';
            dots.children[current].classList.add('active');
            counter.textContent = `${current + 1} / ${imgs.length}`;
        }

        btnPrev.addEventListener('click', (e) => {
            e.preventDefault();
            e.stopPropagation();
            goTo(current - 1);
        });

        btnNext.addEventListener('click', (e) => {
            e.preventDefault();
            e.stopPropagation();
            goTo(current + 1);
        });
    });

});