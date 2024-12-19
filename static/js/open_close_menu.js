document.addEventListener("DOMContentLoaded", function () {
    const menuToggle = document.querySelector(".menu-toggle");
    const dropdownMenu = document.querySelector(".dropdown-menu");

    if (menuToggle && dropdownMenu) {
        menuToggle.addEventListener("click", function () {
            dropdownMenu.classList.toggle("active");
        });
    }
});


//    // Cambia entre modo claro y oscuro
//    toggleTheme.addEventListener("click", function () {
//        document.body.classList.toggle("dark-theme"); // Añade o elimina la clase "dark-theme" al body
//        updateTheme(); // Actualiza el tema visual
//    });
//
//    // Verifica el estado actual del tema y lo aplica
//    function updateTheme() {
//        const isDarkTheme = document.body.classList.contains("dark-theme");
//
//        // Si está en tema oscuro, cambia el color de fondo y texto
//        if (isDarkTheme) {
//            document.body.style.backgroundColor = "#151E21";
//            document.body.style.color = "#7DDFEE";
//        } else {
//            document.body.style.backgroundColor = "#ffffff";
//            document.body.style.color = "#000000";
//        }
//    }
//
//    // Llama a la función para aplicar el tema al cargar la página
//    updateTheme();