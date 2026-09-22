// ==================================================
// TRANSACTIONS TABLE
// ==================================================

const transactionsTable = new DataTable("#transactions-table", {
    pageLength: 20,
    lengthChange: false,
    order: [],

    layout: {topStart: null, topEnd: null},

    language: {
        info: "Mostrando _START_–_END_ de _TOTAL_ lançamentos",
        infoEmpty: "Nenhum lançamento encontrado",
        zeroRecords: "",
        emptyTable: "",
        paginate: {previous: "‹", next: "›"}
    }
});


// ==================================================
// FILTER ELEMENTS
// ==================================================

const searchInput = document.getElementById("transactions-search");
const personFilter = document.getElementById("person-filter");
const paymentMethodFilter = document.getElementById("payment-method-filter");
const purchaseMonthFilter = document.getElementById("purchase-month-filter");
const dueMonthFilter = document.getElementById("due-month-filter");
const clearFiltersButton = document.getElementById("clear-filters");


// ==================================================
// PERSON FILTER
// ==================================================

transactionsTable.column(3).data().unique().sort().each(function (value) {
    const option = document.createElement("option");

    option.value = value;
    option.textContent = value;

    personFilter.appendChild(option);
});


// ==================================================
// PAYMENT METHOD FILTER
// ==================================================

transactionsTable.column(2).data().unique().sort().each(function (value) {
    const option = document.createElement("option");

    option.value = value;
    option.textContent = value;

    paymentMethodFilter.appendChild(option);
});


// ==================================================
// PURCHASE MONTH FILTER
// ==================================================

transactionsTable.column(0).data().unique().sort().each(function (value) {
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
// DUE MONTH FILTER
// ==================================================

transactionsTable.column(6).data().unique().sort().each(function (value) {
    const month = value.substring(3);

    const optionExists = Array.from(
        dueMonthFilter.options
    ).some(function (option) {
        return option.value === month;
    });

    if (optionExists) {
        return;
    }

    const option = document.createElement("option");

    option.value = month;
    option.textContent = month;

    dueMonthFilter.appendChild(option);
});


// ==================================================
// FILTER EVENTS
// ==================================================

searchInput.addEventListener("input", function () {
    transactionsTable.search(this.value).draw();
});

personFilter.addEventListener("change", function () {
    transactionsTable.column(3).search(this.value, {exact: true}).draw();
});

paymentMethodFilter.addEventListener("change", function () {
    transactionsTable.column(2).search(this.value, {exact: true}).draw();
});

purchaseMonthFilter.addEventListener("change", function () {
    transactionsTable.column(0).search(this.value).draw();
});

dueMonthFilter.addEventListener("change", function () {
    transactionsTable.column(6).search(this.value).draw();
});

clearFiltersButton.addEventListener("click", function () {
    searchInput.value = "";
    personFilter.value = "";
    paymentMethodFilter.value = "";
    purchaseMonthFilter.value = "";
    dueMonthFilter.value = "";

    transactionsTable.search("");

    transactionsTable.column(3).search("");
    transactionsTable.column(2).search("");
    transactionsTable.column(0).search("");
    transactionsTable.column(6).search("");

    transactionsTable.draw();
});

// ==================================================
// TRANSACTION STATUS
// ==================================================

document.getElementById("transactions-table").addEventListener("change", async function (event) {
    if (!event.target.classList.contains("transaction-status")) {
        return;
    }

    const select = event.target;
    const transactionId = select.dataset.transactionId;

    const formData = new FormData();
    formData.append("status", select.value);

    const response = await fetch(`/transactions/${transactionId}/status`, {method: "POST", body: formData});

    if (!response.ok) {
        return;
    }

    const data = await response.json();

    const row = select.closest("tr");
    const paymentDateCell = row.querySelector(".transaction-payment-date");

    paymentDateCell.textContent = data.payment_date || "-";
    updateTransactionStatusRows();
});

function updateTransactionStatusRows() {
    const today = new Date().toISOString().split("T")[0];

    document.querySelectorAll(".transaction-status").forEach(function (select) {
        const row = select.closest("tr");
        const dueDate = row.cells[6].dataset.order;

        row.classList.remove(
            "transaction-paid",
            "transaction-separated",
            "transaction-overdue"
        );

        if (select.value === "1") {
            row.classList.add("transaction-paid");
        } else if (dueDate < today) {
            row.classList.add("transaction-overdue");
        } else if (select.value === "2") {
            row.classList.add("transaction-separated");
        }
    });
}

updateTransactionStatusRows();

transactionsTable.on("draw", function () {
    updateTransactionStatusRows();
});
