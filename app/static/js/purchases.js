// ================================================== COMPRAS - TELA ==================================================

// ==================================================
// TABELA - COMPRAS
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
// ELEMENTOS - FILTROS
// ==================================================

const searchInput = document.querySelector("#purchases-search");
const paymentMethodFilter = document.querySelector("#payment-method-filter");
const purchaseMonthFilter = document.querySelector("#purchase-month-filter");
const clearFiltersButton = document.querySelector("#clear-filters");


// ==================================================
// FILTRO - BUSCA
// ==================================================

searchInput.addEventListener("input", function () {
    purchasesTable.search(this.value).draw();
});


// ==================================================
// FILTRO - FORMA DE PAGAMENTO
// ==================================================

purchasesTable.column(4).data().unique().sort().each(function (value) {
    const option = document.createElement("option");

    option.value = value;
    option.textContent = value;

    paymentMethodFilter.appendChild(option);
});


paymentMethodFilter.addEventListener("change", function () {
    purchasesTable.column(4).search(this.value, {exact: true}).draw();
});


// ==================================================
// FILTRO - MÊS DA COMPRA
// ==================================================

purchasesTable.column(0).data().unique().sort().each(function (value) {
    const month = value.substring(3);

    const optionExists = Array.from(
        purchaseMonthFilter.options
    ).some(function (option) {
        return option.value === month;
    });

    if (!optionExists) {
        const option = document.createElement("option");

        option.value = month;
        option.textContent = month;

        purchaseMonthFilter.appendChild(option);
    }
});


purchaseMonthFilter.addEventListener("change", function () {
    purchasesTable.column(0).search(this.value).draw();
});


// ==================================================
// FILTROS - LIMPAR
// ==================================================

clearFiltersButton.addEventListener("click", function () {
    searchInput.value = "";
    paymentMethodFilter.value = "";
    purchaseMonthFilter.value = "";

    purchasesTable.search("");
    purchasesTable.column(4).search("");
    purchasesTable.column(0).search("");

    purchasesTable.draw();
});


// ================================================== ADICIONAR / EDITAR COMPRA - MODAL ==================================================

// ==================================================
// ELEMENTOS - COMPRA
// ==================================================

const purchasesTableElement = document.getElementById("purchases-table");

const purchaseModal = document.getElementById("purchase-modal");
const purchaseForm = document.getElementById("purchase-form");
const purchaseModalTitle = document.getElementById("purchase-modal-title");

const purchaseDescription = document.getElementById("purchase-description");
const purchaseDate = document.getElementById("purchase-date");
const purchaseValue = document.getElementById("purchase-value");
const purchaseInstallments = document.getElementById("purchase-installments");
const purchasePaymentMethod = document.getElementById("purchase-payment-method");
const purchaseCategory = document.getElementById("purchase-category");
const purchaseSubcategory = document.getElementById("purchase-subcategory");

const firstDueDateField = document.getElementById("first-due-date-field");
const firstDueDate = document.getElementById("first-due-date");

const addPurchaseButton = document.getElementById("add-purchase-button");
const closePurchaseModalButton = document.getElementById("close-purchase-modal");
const cancelPurchaseModal = document.getElementById("cancel-purchase-modal");
const deletePurchaseButton = document.getElementById("delete-purchase-button");

let selectedPurchaseId = null;


// ==================================================
// CONFIGURAÇÕES - COMPRA
// ==================================================

const today = new Date();

const todayLocal = [
    today.getFullYear(),
    String(today.getMonth() + 1).padStart(2, "0"),
    String(today.getDate()).padStart(2, "0")
].join("-");

purchaseDate.max = todayLocal;


// ==================================================
// FUNÇÕES - COMPRA
// ==================================================

function openPurchaseModal() {
    selectedPurchaseId = null;

    purchaseModalTitle.textContent = "Adicionar Compra";
    purchaseForm.action = "/purchases";

    purchaseForm.reset();

    deletePurchaseButton.classList.remove("visible");
    firstDueDateField.classList.add("hidden");
    transactionsSection.classList.add("hidden");

    installmentGroups.innerHTML = "";

    purchaseModal.classList.add("open");
}


async function openEditPurchaseModal(purchaseId) {
    const response = await fetch(
        `/purchases/${purchaseId}/edit-data`
    );

    if (!response.ok) {
        return;
    }

    const data = await response.json();

    selectedPurchaseId = purchaseId;

    purchaseModalTitle.textContent = "Editar Compra";
    purchaseForm.action = `/purchases/${purchaseId}/edit`;

    purchaseDescription.value = data.purchase.description;
    purchaseDate.value = data.purchase.purchase_date;

    purchaseValue.value = data.purchase.value;
    formatCurrencyInput(purchaseValue);

    purchaseInstallments.value =
        data.purchase.installment_count;

    purchasePaymentMethod.value =
        data.purchase.payment_method_id;

    purchaseCategory.value =
        data.purchase.category_id;

    purchaseSubcategory.value =
        data.purchase.subcategory_id;

    deletePurchaseButton.classList.add("visible");

    loadExistingTransactions(data.transactions);

    purchaseModal.classList.add("open");
}


function closePurchaseModal() {
    purchaseModal.classList.remove("open");
}


// ==================================================
// VALIDAÇÕES - COMPRA
// ==================================================

function isPurchaseDataComplete() {
    const purchaseValueInCents =
        getCurrencyValueInCents(purchaseValue);

    return (
        purchaseDescription.value.trim() !== "" &&
        purchaseDate.value !== "" &&
        purchaseValueInCents > 0 &&
        Number(purchaseInstallments.value) >= 1 &&
        purchasePaymentMethod.value !== "" &&
        purchaseCategory.value !== "" &&
        purchaseSubcategory.value !== ""
    );
}


// ==================================================
// EVENTOS - COMPRA
// ==================================================

addPurchaseButton.addEventListener(
    "click",
    openPurchaseModal
);

closePurchaseModalButton.addEventListener(
    "click",
    closePurchaseModal
);

cancelPurchaseModal.addEventListener(
    "click",
    closePurchaseModal
);


purchaseModal.addEventListener("click", function (event) {
    if (event.target === purchaseModal) {
        closePurchaseModal();
    }
});


purchasesTableElement.addEventListener(
    "click",
    function (event) {
        const row = event.target.closest("tbody tr");

        if (!row) {
            return;
        }

        openEditPurchaseModal(
            row.dataset.purchaseId
        );
    }
);


purchaseDescription.addEventListener(
    "input",
    updateInstallmentGroups
);

purchaseDate.addEventListener(
    "change",
    updateInstallmentGroups
);


purchaseValue.addEventListener("input", function () {
    formatCurrencyInput(this);
    updateInstallmentGroups();
});


purchaseInstallments.addEventListener("input", function () {
    this.value = this.value.replace(/\D/g, "");
    updateInstallmentGroups();
});


purchasePaymentMethod.addEventListener("change", function () {
    firstDueDate.value = "";
    updateInstallmentGroups();
});


purchaseCategory.addEventListener(
    "change",
    updateInstallmentGroups
);

purchaseSubcategory.addEventListener(
    "change",
    updateInstallmentGroups
);

firstDueDate.addEventListener(
    "change",
    updateInstallmentGroups
);


// ==================================================
// ELEMENTOS - CONFIRMAÇÃO
// ==================================================

const confirmationModal = document.getElementById("confirmation-modal");
const confirmationModalForm = document.getElementById("modal-form");
const confirmationNo = document.getElementById("confirmation-no");
const confirmationYes = document.getElementById("confirmation-yes");


// ==================================================
// EVENTOS - CONFIRMAÇÃO
// ==================================================

deletePurchaseButton.addEventListener("click", function () {
    confirmationModal.classList.add("open");
});


confirmationNo.addEventListener("click", function () {
    confirmationModal.classList.remove("open");
});


confirmationYes.addEventListener("click", function () {
    confirmationModalForm.action =
        `/purchases/${selectedPurchaseId}/remove`;
});


// ==================================================
// SALVAR - COMPRA E LANÇAMENTOS
// ==================================================

purchaseForm.addEventListener("submit", function (event) {
    if (!isPurchaseDataComplete()) {
        event.preventDefault();
        return;
    }

    if (!getFirstDueDate()) {
        event.preventDefault();
        return;
    }

    if (!areTransactionsValid()) {
        event.preventDefault();
    }
});