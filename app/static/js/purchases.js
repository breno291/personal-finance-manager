// ==================================================
// PURCHASE ELEMENTS
// ==================================================

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
// PURCHASE CONFIGURATION
// ==================================================

const today = new Date();

purchaseDate.max = formatDateValue(today.getFullYear(), today.getMonth() + 1, today.getDate());


// ==================================================
// PURCHASE MODAL
// ==================================================

function openPurchaseModal() {
    selectedPurchaseId = null;

    purchaseForm.reset();
    purchaseForm.action = "/purchases";

    purchaseModalTitle.textContent = "Adicionar Compra";

    deletePurchaseButton.classList.remove("visible");
    firstDueDateField.classList.add("hidden");

    resetPurchaseTransactions();

    purchaseModal.classList.add("open");
}

async function openEditPurchaseModal(purchaseId) {
    const response = await fetch(`/purchases/${purchaseId}/edit-data`);

    if (!response.ok) {
        return;
    }

    const data = await response.json();

    selectedPurchaseId = purchaseId;

    purchaseForm.action =`/purchases/${purchaseId}/edit`;
    purchaseModalTitle.textContent ="Editar Compra";

    fillPurchaseForm(data.purchase);

    deletePurchaseButton.classList.add("visible");

    loadExistingTransactions(data.transactions);

    purchaseModal.classList.add("open");
}

function closePurchaseModal() {
    purchaseModal.classList.remove("open");
}

function fillPurchaseForm(purchase) {
    purchaseDescription.value = purchase.description;
    purchaseDate.value = purchase.purchase_date;
    purchaseValue.value = purchase.value;

    formatCurrencyInput(purchaseValue);

    purchaseInstallments.value = purchase.installment_count;
    purchasePaymentMethod.value = purchase.payment_method_id;
    purchaseCategory.value = purchase.category_id;
    purchaseSubcategory.value = purchase.subcategory_id;
}


// ==================================================
// PURCHASE VALIDATION
// ==================================================

function isPurchaseDataComplete() {
    return (
        purchaseDescription.value.trim() !== "" &&
        purchaseDate.value !== "" &&
        getCurrencyValueInCents(purchaseValue) > 0 &&
        Number(purchaseInstallments.value) >= 1 &&
        purchasePaymentMethod.value !== "" &&
        purchaseCategory.value !== "" &&
        purchaseSubcategory.value !== ""
    );
}


// ==================================================
// PURCHASE FIELD EVENTS
// ==================================================

const purchaseFields = [purchaseDescription, purchaseDate, purchaseCategory, purchaseSubcategory, firstDueDate];

purchaseFields.forEach(function (field) {
    field.addEventListener("input", updateInstallmentGroups);
});

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


// ==================================================
// PURCHASE MODAL EVENTS
// ==================================================

addPurchaseButton.addEventListener("click", openPurchaseModal);
closePurchaseModalButton.addEventListener("click", closePurchaseModal);
cancelPurchaseModal.addEventListener("click", closePurchaseModal);

purchaseModal.addEventListener("click", function (event) {
    if (event.target === purchaseModal) {
        closePurchaseModal();
    }
});

deletePurchaseButton.addEventListener("click", function () {
    openConfirmationModal(`/purchases/${selectedPurchaseId}/remove`);
});


// ==================================================
// PURCHASE SUBMIT
// ==================================================

purchaseForm.addEventListener("submit", function (event) {
    if (!isPurchaseDataComplete() || !getFirstDueDate() || !areTransactionsValid()) {
        event.preventDefault();
    }
});
