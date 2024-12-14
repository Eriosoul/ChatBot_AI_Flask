const toggleButton = document.getElementById("toggle-theme");
const userPrefersDark = window.matchMedia("(prefers-color-scheme: dark)");

function setTheme(theme) {
    if (theme === "dark") {
        document.documentElement.setAttribute("data-theme", "dark");
    } else {
        document.documentElement.setAttribute("data-theme", "light");
    }
}

// Establecer el tema inicial
setTheme(userPrefersDark.matches ? "dark" : "light");

// Cambiar tema al presionar el botón
toggleButton.addEventListener("click", () => {
    const currentTheme = document.documentElement.getAttribute("data-theme");
    setTheme(currentTheme === "dark" ? "light" : "dark");
});