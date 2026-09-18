// ==================================================
// ELEMENTS - CONFIRMATION
// ==================================================

const confirmationModal = document.getElementById("confirmation-modal");
const confirmationModalForm = document.getElementById("modal-form");
const confirmationNo = document.getElementById("confirmation-no");


// ==================================================
// FUNCTIONS - CONFIRMATION
// ==================================================

function openConfirmationModal(action) {
    confirmationModalForm.action = action;
    confirmationModal.classList.add("open");
}

function closeConfirmationModal() {
    confirmationModal.classList.remove("open");
}


// ==================================================
// EVENTS - CONFIRMATION
// ==================================================

confirmationNo.addEventListener("click", closeConfirmationModal);