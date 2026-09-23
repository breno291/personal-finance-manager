// ==================================================
// ELEMENTS - CONFIRMATION
// ==================================================

const confirmationModal = document.getElementById("confirmation-modal");
const confirmationModalForm = document.getElementById("modal-form");
const confirmationTitle = document.getElementById("confirmation-title");
const confirmationMessage = document.getElementById("confirmation-message");
const confirmationNo = document.getElementById("confirmation-no");


// ==================================================
// FUNCTIONS - CONFIRMATION
// ==================================================

function openConfirmationModal(action, title, message) {
    confirmationModalForm.action = action;
    confirmationTitle.textContent = title;
    confirmationMessage.textContent = message;

    confirmationModal.classList.add("open");
}

function closeConfirmationModal() {
    confirmationModal.classList.remove("open");
}


// ==================================================
// EVENTS - CONFIRMATION
// ==================================================

confirmationNo.addEventListener("click", closeConfirmationModal);
