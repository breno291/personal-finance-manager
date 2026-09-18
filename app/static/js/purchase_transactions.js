// ==================================================
// TRANSACTION ELEMENTS
// ==================================================

const transactionsSection = document.getElementById("transactions-section");
const installmentGroups = document.getElementById("installment-groups");
const personOptionsTemplate = document.getElementById("person-options-template");


// ==================================================
// INSTALLMENT VALUES
// ==================================================

function calculateInstallmentValues() {
    const purchaseValueInCents = getCurrencyValueInCents(purchaseValue);
    const installmentCount = Number(purchaseInstallments.value);
    const baseValue = Math.floor(purchaseValueInCents / installmentCount);
    const remainder = purchaseValueInCents % installmentCount;
    const installmentValues = [];

    for (let index = 0; index < installmentCount; index++) {
        const extraCent = index < remainder ? 1 : 0;

        installmentValues.push(baseValue + extraCent);
    }

    return installmentValues;
}


// ==================================================
// DUE DATE
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
    const dueDay = Number(selectedOption.dataset.dueDay);
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
// TRANSACTION VISIBILITY
// ==================================================

function updateTransactionsVisibility() {
    const purchaseComplete = isPurchaseDataComplete();
    const dueDate = getFirstDueDate();

    const shouldShow = purchaseComplete && dueDate !== "";

    transactionsSection.classList.toggle("hidden", !shouldShow);
}


// ==================================================
// TRANSACTION RESET
// ==================================================

function resetPurchaseTransactions() {
    transactionsSection.classList.add("hidden");
    installmentGroups.innerHTML = "";
}


// ==================================================
// INSTALLMENT GROUPS
// ==================================================

function updateInstallmentGroups() {
    updateDueDateField();
    updateTransactionsVisibility();

    if (!isPurchaseDataComplete()) {
        installmentGroups.innerHTML = "";
        return;
    }

    const firstDueDate = getFirstDueDate();

    if (!firstDueDate) {
        installmentGroups.innerHTML = "";
        return;
    }

    const installmentValues = calculateInstallmentValues();

    installmentGroups.innerHTML = "";

    installmentValues.forEach(function (value, index) {
        const installmentNumber = index + 1;
        const dueDate = addMonthsToDate(firstDueDate, index);
        const group = createInstallmentGroup(installmentNumber, value, dueDate);

        addTransactionRow(group, {value: value, removable: false});

        installmentGroups.appendChild(group);
    });

    lucide.createIcons();
}

function createInstallmentGroup(installmentNumber, installmentValue, dueDate) {
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

    const addPersonButton = group.querySelector(".add-person-transaction-button");

    addPersonButton.addEventListener("click", function () {
        addTransactionRow(group, {value: 0, removable: true});
        lucide.createIcons();
    });

    return group;
}


// ==================================================
// EXISTING TRANSACTIONS
// ==================================================

function loadExistingTransactions(transactions) {
    resetPurchaseTransactions();

    const transactionsByInstallment = groupTransactionsByInstallment(transactions);

    Object.entries(transactionsByInstallment).forEach(
        function ([installmentNumber, transactions]) {
            const installmentValue = calculateTransactionsTotal(transactions);

            const dueDate = transactions[0].due_date;

            const group = createInstallmentGroup(Number(installmentNumber), installmentValue, dueDate);

            transactions.forEach(function (transaction, index) {
                addTransactionRow(group, {
                        transactionId: transaction.id,
                        personId: transaction.person_id,
                        value: transaction.value,
                        removable: index > 0
                    }
                );
            });

            installmentGroups.appendChild(group);
        }
    );

    transactionsSection.classList.remove("hidden");

    lucide.createIcons();
}

function groupTransactionsByInstallment(transactions) {
    const groupedTransactions = {};

    transactions.forEach(function (transaction) {
        const installmentNumber = transaction.installment;

        if (!groupedTransactions[installmentNumber]) {
            groupedTransactions[installmentNumber] = [];
        }

        groupedTransactions[installmentNumber].push(transaction);
    });

    return groupedTransactions;
}

function calculateTransactionsTotal(transactions) {
    return transactions.reduce(
        function (total, transaction) {
            return total + transaction.value;
        },
        0
    );
}


// ==================================================
// TRANSACTION ROWS
// ==================================================

function addTransactionRow(group, {transactionId = "", personId = "", value = 0, removable = false}) {
    const installmentNumber = group.dataset.installment;
    const dueDate = group.dataset.dueDate;
    const row = createTransactionRow(installmentNumber, dueDate, removable);

    row.querySelector('input[name="transaction_id"]').value = transactionId;
    row.querySelector(".transaction-person").value = personId;

    const amountInput = row.querySelector(".transaction-amount");
    amountInput.value = value > 0 ? formatCurrency(value) : "";

    const rows = group.querySelector(".transaction-rows");
    rows.appendChild(row);

    updatePersonOptions(group);
    updateInstallmentBalance(group);
}

function createTransactionRow(installmentNumber, dueDate, removable) {
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
            <input type="text" name="amount" class="transaction-amount" placeholder="R$ 0,00" inputmode="numeric" required>
        </div>

        ${removable ? `
            <button class="transaction-remove" type="button" aria-label="Remover pessoa">
                <i data-lucide="trash-2"></i>
            </button>
        ` : ""}
    `;

    bindTransactionRowEvents(row, removable);

    return row;
}

function bindTransactionRowEvents(row, removable) {
    const personSelect = row.querySelector(".transaction-person");

    const amountInput = row.querySelector(".transaction-amount");

    personSelect.addEventListener("change", function () {
        const group = row.closest(".installment-group");

        updatePersonOptions(group);
    });

    amountInput.addEventListener("input", function () {
        formatCurrencyInput(this);

        const group = row.closest(".installment-group");

        updateInstallmentBalance(group);
    });

    if (!removable) {
        return;
    }

    const removeButton = row.querySelector(".transaction-remove");

    removeButton.addEventListener("click", function () {
        const group = row.closest(".installment-group");

        row.remove();

        updatePersonOptions(group);
        updateInstallmentBalance(group);
    });
}


// ==================================================
// PERSON OPTIONS
// ==================================================

function updatePersonOptions(group) {
    const selects = group.querySelectorAll(".transaction-person");

    const selectedPeople = Array.from(selects)
        .map(function (select) {
            return select.value;
        })
        .filter(function (value) {
            return value !== "";
        });

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
// INSTALLMENT BALANCE
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
        balance.textContent = `Excedeu: ${formatCurrency(Math.abs(difference))}`;

        return;
    }

    balance.classList.add("complete");
    balance.textContent = "Distribuído corretamente ✓";
}


// ==================================================
// TRANSACTION VALIDATION
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

            if (person === "" || amount <= 0) {
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
