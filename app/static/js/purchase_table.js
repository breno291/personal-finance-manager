// ==================================================
// PURCHASE TABLE
// ==================================================

const purchasesTable = new DataTable("#purchases-table", {
    pageLength: 20,
    lengthChange: false,
    order: [],

    layout: {topStart: null, topEnd: null},
    language: {
        info: "Mostrando _START_–_END_ de _TOTAL_ compras",
        infoEmpty: "Nenhuma compra encontrada",
        zeroRecords: "",
        emptyTable: "",
        paginate: {previous: "‹", next: "›"}
    }
});


// ==================================================
// FILTER ELEMENTS
// ==================================================

const searchInput = document.getElementById("purchases-search");
const paymentMethodFilter = document.getElementById("payment-method-filter");
const purchaseMonthFilter = document.getElementById("purchase-month-filter");
const clearFiltersButton = document.getElementById("clear-filters");


// ==================================================
// PAYMENT METHOD FILTER
// ==================================================

purchasesTable.column(4).data().unique().sort().each(function (value) {
    const option = document.createElement("option");

    option.value = value;
    option.textContent = value;

    paymentMethodFilter.appendChild(option);
});


// ==================================================
// PURCHASE MONTH FILTER
// ==================================================

purchasesTable.column(0).data().unique().sort().each(function (value) {
    const month = value.substring(3);

    const optionExists = Array.from(
        purchaseMonthFilter.options
    ).some(function (option) {
        return option.value === month;
    });

    if (optionExists) {
        return;
    }

    const option = document.createElement("option");

    option.value = month;
    option.textContent = month;

    purchaseMonthFilter.appendChild(option);
});


// ==================================================
// FILTER EVENTS
// ==================================================

searchInput.addEventListener("input", function () {
    purchasesTable.search(this.value).draw();
});

paymentMethodFilter.addEventListener("change", function () {
    purchasesTable.column(4).search(this.value, { exact: true }).draw();
});

purchaseMonthFilter.addEventListener("change", function () {
    purchasesTable.column(0).search(this.value).draw();
});

clearFiltersButton.addEventListener("click", function () {
    searchInput.value = "";
    paymentMethodFilter.value = "";
    purchaseMonthFilter.value = "";

    purchasesTable.search("");
    purchasesTable.column(4).search("");
    purchasesTable.column(0).search("");

    purchasesTable.draw();
});


// ==================================================
// TABLE EVENTS
// ==================================================

const purchasesTableElement = document.getElementById("purchases-table");

purchasesTableElement.addEventListener("click", function (event) {
    const row = event.target.closest("tbody tr");

    if (!row) {
        return;
    }

    openEditPurchaseModal(
        row.dataset.purchaseId
    );
});

