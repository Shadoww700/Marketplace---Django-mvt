/**
 * NEO•CORE - ADD PRODUCT FORM CONTROLLER
 * UI Script Identity: Image Processing Preview & Glitch Validation
 */

document.addEventListener("DOMContentLoaded", () => {
    console.log("🛠️ [SYSTEM] Product injection deployment module online.");

    // 1. ХАКЕРСКИЙ ЭФФЕКТ ДЕКОДИРОВАНИЯ ДЛЯ ЗАГОЛОВКА ФОРМЫ
    const charset = "XYZ0123456789#@$%&*?";
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

    // 2. ЖИВОЙ ПРЕВЬЮ ИНТЕРФЕЙС КАРТИНКИ (Neural Image Live Preview)
    const fileInput = document.getElementById("image");
    const fileText = document.getElementById("file-upload-text");
    const previewZone = document.getElementById("image-preview-zone");
    const previewImg = document.getElementById("image-preview-target");

    if (fileInput) {
        fileInput.addEventListener("change", function() {
            const file = this.files[0];
            if (file) {
                // Меняем текст кнопки загрузки
                fileText.innerText = `Selected: ${file.name.substring(0, 20)}...`;
                fileText.style.color = "var(--neon-cyan)";
                
                // Считываем картинку через FileReader
                const reader = new FileReader();
                reader.addEventListener("load", function() {
                    previewImg.setAttribute("src", this.result);
                    previewZone.classList.remove("hidden-preview");
                    previewZone.classList.add("active-preview");
                });
                reader.readAsDataURL(file);
            } else {
                fileText.innerText = "Upload Neural Spec Image";
                previewZone.classList.add("hidden-preview");
                previewZone.classList.remove("active-preview");
            }
        });
    }
});