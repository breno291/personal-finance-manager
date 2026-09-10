// ==================================================
// ELEMENTOS - FORMA DE PAGAMENTO
// ==================================================

const paymentMethodModal = document.getElementById("payment-method-modal");
const paymentMethodForm = document.getElementById("payment-method-form");
const paymentMethodModalTitle = document.getElementById("payment-method-modal-title");

const addPaymentMethodButton = document.getElementById("add-payment-method-button");
const closePaymentMethodModalButton = document.getElementById("close-payment-method-modal");
const cancelPaymentMethodModal = document.getElementById("cancel-payment-method-modal");
const deletePaymentMethodButton = document.getElementById("delete-payment-method-button");

const paymentMethodCards = document.querySelectorAll(".payment-method-card");

const paymentMethodId = document.getElementById("payment-method-id");
const paymentMethodDescription = document.getElementById("payment-method-description");
const paymentMethodType = document.getElementById("payment-method-type");
const paymentMethodClosingDay = document.getElementById("payment-method-closing-day");
const paymentMethodDueDay = document.getElementById("payment-method-due-day");


// ==================================================
// ELEMENTOS - CONFIRMAÇÃO
// ==================================================

const confirmationModal = document.getElementById("confirmation-modal");
const confirmationModalForm = document.getElementById("modal-form");
const confirmationNo = document.getElementById("confirmation-no");
const confirmationYes = document.getElementById("confirmation-yes");


// ==================================================
// FUNÇÕES - FORMA DE PAGAMENTO
// ==================================================

function openPaymentMethodModal() {
    paymentMethodModalTitle.textContent = "Adicionar Forma de Pagamento";

    paymentMethodId.value = "";
    paymentMethodDescription.value = "";
    paymentMethodType.value = "";
    paymentMethodClosingDay.value = "";
    paymentMethodDueDay.value = "";

    paymentMethodForm.action = "/payment-methods";

	updatePaymentDaysRequirement();

    deletePaymentMethodButton.classList.remove("visible");
    paymentMethodModal.classList.add("open");
}

function closePaymentMethodModal() {
    paymentMethodModal.classList.remove("open");
}

function updatePaymentDaysRequirement() {
    const isCredit = paymentMethodType.value === "2";

    paymentMethodClosingDay.required = isCredit;
    paymentMethodDueDay.required = isCredit;
}


// ==================================================
// EVENTOS - FORMA DE PAGAMENTO
// ==================================================

addPaymentMethodButton.addEventListener("click", openPaymentMethodModal);
closePaymentMethodModalButton.addEventListener("click", closePaymentMethodModal);
cancelPaymentMethodModal.addEventListener("click", closePaymentMethodModal);

paymentMethodModal.addEventListener("click", function (event) {
    if (event.target === paymentMethodModal) {
        closePaymentMethodModal();
    }
});

paymentMethodCards.forEach(function (card) {
    card.addEventListener("click", function () {
        paymentMethodModalTitle.textContent = "Editar Forma de Pagamento";

        paymentMethodId.value = card.dataset.paymentMethodId;
        paymentMethodDescription.value = card.dataset.paymentMethodDescription;
        paymentMethodType.value = card.dataset.paymentMethodType;
        paymentMethodClosingDay.value = card.dataset.paymentMethodClosingDay;
        paymentMethodDueDay.value = card.dataset.paymentMethodDueDay;

		updatePaymentDaysRequirement();

        paymentMethodForm.action = `/payment-methods/${paymentMethodId.value}/edit`;

        deletePaymentMethodButton.classList.add("visible");
        paymentMethodModal.classList.add("open");
    });
});


// ==================================================
// EVENTOS - CONFIRMAÇÃO
// ==================================================

deletePaymentMethodButton.addEventListener("click", function () {
    confirmationModal.classList.add("open");
});

confirmationNo.addEventListener("click", function () {
    confirmationModal.classList.remove("open");
});

confirmationYes.addEventListener("click", function () {
    confirmationModalForm.action = `/payment-methods/${paymentMethodId.value}/remove`;
});


// ==================================================
// EVENTOS - TIPO DE PAGAMENTO
// ==================================================

paymentMethodType.addEventListener("change", function () {
    updatePaymentDaysRequirement();
});