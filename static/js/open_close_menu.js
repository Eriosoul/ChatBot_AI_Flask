document.addEventListener("DOMContentLoaded", function () {
    const userAvatar = document.getElementById("user-avatar");
    const dropdownMenu = document.getElementById("dropdown-menu");
    const toggleTheme = document.getElementById("toggle-theme");

    // abrir y cerrar el menu con el evento del clic
    userAvatar.addEventListener("click", function (e) {
        e.stopPropagation(); // Evita que el evento se propague al documento
        dropdownMenu.classList.toggle("show");
    });
    // cerrar el menu si haces clic fuera de el
    document.addEventListener("click", function () {
        dropdownMenu.classList.remove("show");
    });

    // Cambia entre modo claro y oscuro
    toggleTheme.addEventListener("click", function () {
        document.body.classList.toggle("dark-theme"); // Añade o elimina la clase "dark-theme" al body
        updateTheme(); // Actualiza el tema visual
    });

    // Verifica el estado actual del tema y lo aplica
    function updateTheme() {
        const isDarkTheme = document.body.classList.contains("dark-theme");

        // Si está en tema oscuro, cambia el color de fondo y texto
        if (isDarkTheme) {
            document.body.style.backgroundColor = "#151E21";
            document.body.style.color = "#7DDFEE";
        } else {
            document.body.style.backgroundColor = "#ffffff";
            document.body.style.color = "#000000";
        }
    }

    // Llama a la función para aplicar el tema al cargar la página
    updateTheme();
});