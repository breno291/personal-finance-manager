// ================================================== BASE ==================================================

// ==================================================
// INICIALIZAÇÃO
// ==================================================

lucide.createIcons();


// ==================================================
// ELEMENTOS - SIDEBAR
// ==================================================

const app = document.querySelector(".app");
const menuButton = document.querySelector("#menu-button");
const menuIcon = document.querySelector("#menu-icon");


// ==================================================
// EVENTOS - SIDEBAR
// ==================================================

menuButton.addEventListener("click", function () {
    app.classList.toggle("sidebar-collapsed");

    const collapsed = app.classList.contains("sidebar-collapsed");
    menuIcon.setAttribute("data-lucide", collapsed ? "panel-left-open" : "panel-left-close");
    menuButton.setAttribute("aria-label", collapsed ? "Abrir menu" : "Fechar menu");

    lucide.createIcons();
});



// ================================================== UTILITÁRIOS ==================================================

// ==================================================
// FUNÇÕES - MOEDA
// ==================================================

function formatCurrencyInput(input) {
    let value = input.value.replace(/\D/g, "");

    if (!value) {
        input.value = "";
        return;
    }

    input.value = formatCurrency(Number(value));
}


function formatCurrency(valueInCents) {
    return (valueInCents / 100).toLocaleString("pt-BR",{style: "currency", currency: "BRL"});
}


function getCurrencyValueInCents(input) {
    const value = input.value.replace(/\D/g, "");

    return Number(value) || 0;
}


// ==================================================
// FUNÇÕES - DATAS
// ==================================================

function formatDateValue(year, month, day) {
    return [year,String(month).padStart(2, "0"),String(day).padStart(2, "0")].join("-");
}


function formatDateDisplay(dateValue) {
    const [year, month, day] = dateValue.split("-");

    return `${day}/${month}/${year}`;
}


function getValidDayForMonth(year, month, day) {
    const lastDay = new Date(year, month, 0).getDate();

    return Math.min(day,lastDay);
}


function addMonthsToDate(dateValue, monthsToAdd) {
    const [year, month, day] = dateValue.split("-").map(Number);
    const targetMonthIndex = month - 1 + monthsToAdd;
    const targetYear = year + Math.floor(targetMonthIndex / 12);
    const targetMonth = ((targetMonthIndex % 12) + 12) % 12 + 1;
    const targetDay = getValidDayForMonth(targetYear, targetMonth, day);

    return formatDateValue(targetYear, targetMonth, targetDay);
}


