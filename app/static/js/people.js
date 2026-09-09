// ==================================================
// ELEMENTOS - PESSOA
// ==================================================

const personModal = document.getElementById("person-modal");
const personForm = document.getElementById("person-form");
const personModalTitle = document.getElementById("person-modal-title");

const addPersonButton = document.getElementById("add-person-button");
const closePersonModalButton = document.getElementById("close-person-modal");
const cancelPersonModal = document.getElementById("cancel-person-modal");
const deletePersonButton = document.getElementById("delete-person-button");

const personCards = document.querySelectorAll(".person-card");

const personId = document.getElementById("person-id");
const personName = document.getElementById("person-name");
const personEmail = document.getElementById("person-email");
const personPhone = document.getElementById("person-phone");


// ==================================================
// ELEMENTOS - CONFIRMAÇÃO
// ==================================================

const confirmationModal = document.getElementById("confirmation-modal");
const confirmationModalForm = document.getElementById("modal-form");
const confirmationNo = document.getElementById("confirmation-no");
const confirmationYes = document.getElementById("confirmation-yes");


// ==================================================
// FUNÇÕES - PESSOA
// ==================================================

function openPersonModal() {
    personModalTitle.textContent = "Adicionar Pessoa";

    personId.value = "";
    personName.value = "";
    personEmail.value = "";
    personPhone.value = "";

    personForm.action = "/people";

    deletePersonButton.classList.remove("visible");
    personModal.classList.add("open");
}

function closePersonModal() {
    personModal.classList.remove("open");
}


// ==================================================
// EVENTOS - PESSOA
// ==================================================

addPersonButton.addEventListener("click", openPersonModal);
closePersonModalButton.addEventListener("click", closePersonModal);
cancelPersonModal.addEventListener("click", closePersonModal);

personModal.addEventListener("click", function (event) {
    if (event.target === personModal) {
        closePersonModal();
    }
});

personCards.forEach(function (card) {
    card.addEventListener("click", function () {
        personModalTitle.textContent = "Editar Pessoa";

        personId.value = card.dataset.personId;
        personName.value = card.dataset.personName;
        personEmail.value = card.dataset.personEmail;
        personPhone.value = card.dataset.personPhone;

        personForm.action = `/people/${personId.value}/edit`;

        deletePersonButton.classList.add("visible");
        personModal.classList.add("open");
    });
});


// ==================================================
// EVENTOS - TELEFONE
// ==================================================

personPhone.addEventListener("input", function () {
    let phone = this.value.replace(/\D/g, "");

    phone = phone.slice(0, 11);

    if (phone.length > 10) {
        phone = phone.replace(
            /^(\d{2})(\d{5})(\d{0,4}).*/,
            "($1) $2-$3"
        );
    } else if (phone.length > 6) {
        phone = phone.replace(
            /^(\d{2})(\d{4})(\d{0,4}).*/,
            "($1) $2-$3"
        );
    } else if (phone.length > 2) {
        phone = phone.replace(
            /^(\d{2})(\d{0,5})/,
            "($1) $2"
        );
    } else if (phone.length > 0) {
        phone = phone.replace(
            /^(\d{0,2})/,
            "($1"
        );
    }

    this.value = phone;
});


// ==================================================
// EVENTOS - CONFIRMAÇÃO
// ==================================================

deletePersonButton.addEventListener("click", function () {
    confirmationModal.classList.add("open");
});

confirmationNo.addEventListener("click", function () {
    confirmationModal.classList.remove("open");
});

confirmationYes.addEventListener("click", function () {
	// confirmationModal.classList.remove("open");
    confirmationModalForm.action = `/people/${personId.value}/remove`; 
});