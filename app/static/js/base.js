lucide.createIcons();

const app = document.querySelector(".app");
const menuButton = document.querySelector("#menu-button");

menuButton.addEventListener("click", () => {
    app.classList.toggle("sidebar-collapsed");

    const collapsed = app.classList.contains("sidebar-collapsed");
    const menuIcon = document.querySelector("#menu-icon");

    menuIcon.setAttribute(
        "data-lucide",
        collapsed ? "panel-left-open" : "panel-left-close"
    );

    menuButton.setAttribute(
        "aria-label",
        collapsed ? "Abrir menu" : "Fechar menu"
    );

    lucide.createIcons();
});