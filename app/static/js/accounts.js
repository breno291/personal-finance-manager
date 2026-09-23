// ==================================================
// ACCOUNT ELEMENTS
// ==================================================

const accountCards = document.querySelectorAll(".account-card");


// ==================================================
// ACCOUNT FUNCTIONS
// ==================================================

function loadAccount(card, month) {
    const paymentMethodId = card.dataset.paymentMethodId;

    fetch(`/accounts/payment-method/${paymentMethodId}?month=${month}`)
        .then(function (response) {
            return response.json();
        })
        .then(function (data) {
            renderAccount(card, data);
        });
}

function renderAccount(card, data) {
    const description = card.querySelector(".account-method-description");
    const content = card.querySelector(".account-content");
    const count = card.querySelector(".account-count");
    const paidButton = card.querySelector(".account-paid-button");

    description.textContent = data.payment_method.description;

    count.textContent = `${data.purchases.length} compras neste mês`;
    paidButton.disabled = data.purchases.length === 0;

    if (data.purchases.length === 0) {
        content.innerHTML = `
            <div class="account-empty">
                <i data-lucide="file"></i>

                <strong>Sem compras no mês</strong>
                <span>
                    Não há compras neste período nesta forma de pagamento.
                </span>
            </div>
        `;

        lucide.createIcons();

        return;
    }

    const peopleHeaders = data.people.map(function (person) {return `<th>${person.name}</th>`;}).join("");

    const purchasesRows = data.purchases
        .map(function (purchase) {
            let statusClass = "";

            if (purchase.status === 1) {
                statusClass = "account-row-paid";
            } else if (purchase.status === 2) {
                statusClass = "account-row-separated";
            }

            const peopleValues = data.people
                .map(function (person) {
                    const value = purchase.people[person.id];

                    if (value === undefined) {
                        return "<td></td>";
                    }

                    return `<td>${formatCurrency(value)}</td>`;
                })
                .join("");

            return `
                <tr data-purchase-id="${purchase.id}" class="${statusClass}">
                    <td class="account-purchase-column">${purchase.description}</td>
                    ${peopleValues}
                    <td class="account-total-column">${formatCurrency(purchase.total)}</td>
                </tr>
            `;
        })
        .join("");

    const peopleTotals = data.people
        .map(function (person) {
            return `<td>${formatCurrency(person.total)}</td>`;
        })
        .join("");

    content.innerHTML = `
        <div class="account-table-wrapper">
            <table class="account-table">
                <thead>
                    <tr>
                        <th class="account-purchase-column">Compra</th>
                        ${peopleHeaders}
                        <th class="account-total-column">Total</th>
                    </tr>
                </thead>

                <tbody>
                    ${purchasesRows}
                </tbody>

                <tfoot>
                    <tr>
                        <th class="account-purchase-column">Total</th>
                        ${peopleTotals}
                        <td class="account-total-column">${formatCurrency(data.total)}</td>
                    </tr>
                </tfoot>
            </table>
        </div>
    `;
}

function changeAccountMonth(calendar, offset) {
    const currentDate = calendar.selectedDates[0];
    const newDate = new Date(currentDate.getFullYear(), currentDate.getMonth() + offset, 1);

    calendar.setDate(newDate, true);
}


// ==================================================
// ACCOUNT EVENTS
// ==================================================

accountCards.forEach(function (card) {
    const month = card.querySelector(".account-month");
    const monthInput = month.querySelector(".account-month-input");
    const previousMonthButton = month.querySelector(".account-month-previous");
    const nextMonthButton = month.querySelector(".account-month-next");

    const calendar = flatpickr(monthInput, {
        plugins: [
            new monthSelectPlugin({shorthand: false, dateFormat: "Y-m", altFormat: "F/Y",}),
        ],
        altInput: true,

        onChange: function (_, dateString) {loadAccount(card, dateString);},
    });

    previousMonthButton.addEventListener("click", function () {
        changeAccountMonth(calendar, -1);
    });

    nextMonthButton.addEventListener("click", function () {
        changeAccountMonth(calendar, 1);
    });
});

