document.addEventListener('DOMContentLoaded', () => {
    console.log('⚡ NEO•CORE Matrix Engine initialized.');

    // Интерактивный интерактив для чипсов категорий
    const chips = document.querySelectorAll('.category-chip');
    chips.forEach(chip => {
        chip.addEventListener('click', () => {
            chips.forEach(c => c.classList.remove('active'));
            chip.classList.add('active');
            
            // Здесь в будущем можно сделать AJAX фильтрацию товаров без перезагрузки страницы
            const categoryId = chip.dataset.category;
            console.log(`Filtering matrix items by category ID: ${categoryId}`);
        });
    });

    // Эффект динамической подсветки карточек при движении мыши (3D Глоу эффект)
    const cards = document.querySelectorAll('.product-card');
    cards.forEach(card => {
        card.addEventListener('mousemove', (e) => {
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            
            // Задаем CSS переменные координат мыши внутри карточки
            card.style.setProperty('--mouse-x', `${x}px`);
            card.style.setProperty('--mouse-y', `${y}px`);
        });
    });
});