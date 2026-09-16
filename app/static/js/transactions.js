// ================================================== LANÇAMENTOS ==================================================

// ==================================================
// ELEMENTOS - LANÇAMENTOS
// ==================================================

const transactionsSection = document.getElementById("transactions-section");
const installmentGroups = document.getElementById("installment-groups");
const personOptionsTemplate = document.getElementById("person-options-template");


// ==================================================
// FUNÇÕES - VALORES DAS PARCELAS
// ==================================================

function calculateInstallmentValues() {
    const purchaseValueInCents = getCurrencyValueInCents(purchaseValue);
    const installmentCount = Number(purchaseInstallments.value);
    const baseValue = Math.floor(purchaseValueInCents / installmentCount);
    const remainder = purchaseValueInCents % installmentCount;
    const installmentValues = [];

    for (let index = 0; index < installmentCount; index++) {
        let installmentValue =
            baseValue;

        if (index < remainder) {
            installmentValue += 1;
        }

        installmentValues.push(installmentValue);
    }

    return installmentValues;
}


// ==================================================
// FUNÇÕES - VENCIMENTO
// ==================================================

function paymentMethodHasDueDate() {
    if (!purchasePaymentMethod.value) {
        return false;
    }

    const selectedOption = purchasePaymentMethod.selectedOptions[0];

    return (
        selectedOption.dataset.closingDay !== "" &&
        selectedOption.dataset.dueDay !== ""
    );
}


function calculateCardFirstDueDate() {
    const selectedOption = purchasePaymentMethod.selectedOptions[0];
    const closingDay = Number(selectedOption.dataset.closingDay);
    const dueDay =Number(selectedOption.dataset.dueDay);

    const [purchaseYear, purchaseMonth, purchaseDay] = purchaseDate.value.split("-").map(Number);
    const monthsUntilDue = purchaseDay >= closingDay ? 2 : 1;
    const targetMonthIndex = purchaseMonth - 1 + monthsUntilDue;

    const targetYear = purchaseYear + Math.floor(targetMonthIndex / 12);
    const targetMonth = ((targetMonthIndex % 12) + 12) % 12 + 1;
    const targetDay = getValidDayForMonth(targetYear, targetMonth, dueDay);

    return formatDateValue(targetYear, targetMonth, targetDay);
}


function updateDueDateField() {
    if (!purchasePaymentMethod.value) {
        firstDueDateField.classList.add("hidden");
        firstDueDate.required = false;

        return;
    }

    if (paymentMethodHasDueDate()) {
        firstDueDateField.classList.add("hidden");
        firstDueDate.required = false;
        firstDueDate.value = "";

        return;
    }

    firstDueDateField.classList.remove("hidden");
    firstDueDate.required = true;
}


function getFirstDueDate() {
    if (!purchasePaymentMethod.value) {
        return "";
    }

    if (paymentMethodHasDueDate()) {
        if (!purchaseDate.value) {
            return "";
        }

        return calculateCardFirstDueDate();
    }

    return firstDueDate.value;
}


// ==================================================
// FUNÇÕES - VISIBILIDADE
// ==================================================

function updateTransactionsVisibility() {
    if (!isPurchaseDataComplete()) {
        transactionsSection.classList.add("hidden");

        return;
    }

    const dueDate = getFirstDueDate();

    if (!dueDate) {
        transactionsSection.classList.add("hidden");

        return;
    }

    transactionsSection.classList.remove("hidden");
}


// ==================================================
// FUNÇÕES - GRUPOS DE PARCELAS
// ==================================================

function updateInstallmentGroups() {
    updateDueDateField();
    updateTransactionsVisibility();

    if (!isPurchaseDataComplete()) {
        installmentGroups.innerHTML = "";
        return;
    }

    const firstInstallmentDueDate = getFirstDueDate();

    if (!firstInstallmentDueDate) {
        installmentGroups.innerHTML = "";
        return;
    }

    const installmentValues = calculateInstallmentValues();

    installmentGroups.innerHTML = "";

    installmentValues.forEach(
        function (installmentValue, index) {
            const installmentNumber = index + 1;
            const dueDate = addMonthsToDate(firstInstallmentDueDate, index);
            const group = createInstallmentGroup(installmentNumber, installmentValue, dueDate);

            installmentGroups.appendChild(group);
        }
    );

    lucide.createIcons();
}


function createInstallmentGroup(installmentNumber, installmentValue, dueDate) {
    const group = document.createElement("div");

    group.classList.add("installment-group");
    group.dataset.installment =installmentNumber;
    group.dataset.value =installmentValue;
    group.dataset.dueDate =dueDate;

    group.innerHTML = `
        <div class="installment-header">
            <h4>Parcela ${installmentNumber} - vencimento: ${formatDateDisplay(dueDate)}</h4>
            <span class="installment-total">${formatCurrency(installmentValue)}</span>
        </div>

        <div class="transaction-rows"></div>
        <button class="add-person-transaction-button" type="button"><i data-lucide="plus"></i>Adicionar pessoa</button>
        <div class="installment-balance"></div>
    `;

    const rows = group.querySelector(".transaction-rows");
    rows.appendChild(createTransactionRow(installmentNumber, false, installmentValue, dueDate));

    const addPersonButton = group.querySelector(".add-person-transaction-button");

    addPersonButton.addEventListener("click", function () {
        rows.appendChild(createTransactionRow(installmentNumber,true,0,dueDate));

        updatePersonOptions(group);
        updateInstallmentBalance(group);

        lucide.createIcons();
    });

    updateInstallmentBalance(group);

    return group;
}


// ==================================================
// FUNÇÕES - CARREGAR LANÇAMENTOS
// ==================================================

function loadExistingTransactions(transactions) {
    installmentGroups.innerHTML = "";

    const transactionsByInstallment = {};

    transactions.forEach(function (transaction) {
        if (!transactionsByInstallment[transaction.installment]) {
            transactionsByInstallment[transaction.installment] = [];
        }

        transactionsByInstallment[transaction.installment].push(transaction);
    });

    Object.entries(transactionsByInstallment).forEach(
        function ([installmentNumber, installmentTransactions]) {
            const installmentValue = installmentTransactions.reduce(function (total, transaction) { return total + transaction.value; }, 0);
            const dueDate = installmentTransactions[0].due_date;
            const group = createExistingInstallmentGroup(Number(installmentNumber), installmentValue, dueDate, installmentTransactions);

            installmentGroups.appendChild(group);
        }
    );

    transactionsSection.classList.remove("hidden");

    lucide.createIcons();
}


function createExistingInstallmentGroup(installmentNumber, installmentValue, dueDate, transactions) {
    const group = document.createElement("div");

    group.classList.add("installment-group");
    group.dataset.installment = installmentNumber;
    group.dataset.value = installmentValue;
    group.dataset.dueDate = dueDate;

    group.innerHTML = `
        <div class="installment-header">
            <h4>
                Parcela ${installmentNumber} -
                vencimento: ${formatDateDisplay(dueDate)}
            </h4>

            <span class="installment-total">
                ${formatCurrency(installmentValue)}
            </span>
        </div>

        <div class="transaction-rows"></div>

        <button class="add-person-transaction-button" type="button">
            <i data-lucide="plus"></i>Adicionar pessoa
        </button>

        <div class="installment-balance"></div>
    `;

    const rows = group.querySelector(".transaction-rows");

    transactions.forEach(function (transaction, index) {
        const row = createTransactionRow(installmentNumber, index > 0, transaction.value, dueDate);

        row.querySelector('input[name="transaction_id"]').value = transaction.id;
        row.querySelector(".transaction-person").value =transaction.person_id;
        rows.appendChild(row);
    });

    const addPersonButton = group.querySelector(".add-person-transaction-button");

    addPersonButton.addEventListener("click", function () {
        rows.appendChild(createTransactionRow(installmentNumber, true, 0, dueDate));

        updatePersonOptions(group);
        updateInstallmentBalance(group);

        lucide.createIcons();
    });

    updatePersonOptions(group);
    updateInstallmentBalance(group);

    return group;
}


// ==================================================
// FUNÇÕES - LANÇAMENTO
// ==================================================

function createTransactionRow(installmentNumber, removable, initialValue, dueDate) {
    const row = document.createElement("div");

    row.classList.add("transaction-row");

    row.innerHTML = `
        <input type="hidden" name="installment_number" value="${installmentNumber}">
		<input type="hidden" name="transaction_id" value="">
        <input type="hidden" name="due_date" value="${dueDate}">

        <div class="form-field">
            <label>Pessoa</label>
            <select name="person_id" class="transaction-person" required>
                ${personOptionsTemplate.innerHTML}
            </select>
        </div>

        <div class="form-field">
            <label>Valor</label>
            <input type="text" name="amount" class="transaction-amount" 
                value="${initialValue > 0 ? formatCurrency(initialValue) : ""}"
                placeholder="R$ 0,00" inputmode="numeric" required
            >
        </div>

        ${removable ? `
                    <button class="transaction-remove" type="button" aria-label="Remover pessoa">
                        <i data-lucide="trash-2"></i>
                    </button>
                ` : ""}
    `;

    const person = row.querySelector(".transaction-person");

    const amount = row.querySelector(".transaction-amount");

    person.addEventListener("change", function () {
        const group = row.closest(".installment-group");
        updatePersonOptions(group);
    });

    amount.addEventListener("input", function () {
        formatCurrencyInput(this);

        const group = row.closest(".installment-group");

        updateInstallmentBalance(group);
    });

    if (removable) {
        const removeButton = row.querySelector(".transaction-remove");
        removeButton.addEventListener("click", function () {
            const group = row.closest(".installment-group");

            row.remove();

            updatePersonOptions(group);
            updateInstallmentBalance(group);
        });
    }

    return row;
}


// ==================================================
// FUNÇÕES - PESSOAS
// ==================================================

function updatePersonOptions(group) {
    const selects = group.querySelectorAll(".transaction-person");
    const selectedPeople = Array.from(selects).map(select => select.value).filter(value => value !== "");

    selects.forEach(function (select) {
        const currentValue = select.value;

        Array.from(select.options).forEach(function (option) {
            if (option.value === "") {
                return;
            }

            option.disabled = option.value !== currentValue && selectedPeople.includes(option.value);
        });
    });
}


// ==================================================
// FUNÇÕES - SALDO
// ==================================================

function updateInstallmentBalance(group) {
    const installmentValue = Number(group.dataset.value);
    const amountInputs = group.querySelectorAll(".transaction-amount");
    let distributedValue = 0;

    amountInputs.forEach(function (input) {
        distributedValue += getCurrencyValueInCents(input);
    });

    const difference = installmentValue - distributedValue;
    const balance = group.querySelector(".installment-balance");

    balance.classList.remove("remaining", "exceeded", "complete");

    if (difference > 0) {
        balance.classList.add("remaining");
        balance.textContent = `Falta distribuir: ${formatCurrency(difference)}`;

        return;
    }

    if (difference < 0) {
        balance.classList.add("exceeded");
        balance.textContent =`Excedeu: ${formatCurrency(Math.abs(difference))}`;

        return;
    }

    balance.classList.add("complete");
    balance.textContent ="Distribuído corretamente ✓";
}


// ==================================================
// VALIDAÇÕES - LANÇAMENTOS
// ==================================================

function areTransactionsValid() {
    const groups = installmentGroups.querySelectorAll(".installment-group");

    if (groups.length === 0) {
        return false;
    }

    for (const group of groups) {
        const installmentValue = Number(group.dataset.value);
        const rows = group.querySelectorAll(".transaction-row");
        let distributedValue = 0;

        for (const row of rows) {
            const person = row.querySelector(".transaction-person").value;
            const amount = getCurrencyValueInCents(row.querySelector(".transaction-amount"));

            if ( person === "" || amount <= 0) {
                return false;
            }

            distributedValue += amount;
        }

        if (distributedValue !== installmentValue) {
            return false;
        }
    }

    return true;
}

