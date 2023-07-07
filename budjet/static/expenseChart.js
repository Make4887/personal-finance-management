const dataExpenseChart = document.currentScript.dataset;
let expense_category = dataExpenseChart.expenseCategory;
let expense_amount = dataExpenseChart.expenseAmount;
console.log(expense_amount);
console.log(expense_category);
expense_category = JSON.parse(expense_category);
expense_amount = JSON.parse(expense_amount);
console.log(expense_amount);
console.log(expense_category);

let expenseChart = document.getElementById("ExpenseChart");
console.log(expense_amount);
console.log(expense_category);

Chart.defaults.global.defaultFontFamily = "Lato";
Chart.defaults.global.defaultFontSize = 18;

let expenseData = {
    labels: expense_category,
    datasets: [
        {
            data: expense_amount,
            backgroundColor: [
                "#FF6384",
                "#63FF84",
                "#611304",
                "#FBCEB1",
            ]
        }]
};

let pieExpenseChart = new Chart(expenseChart, {
  type: 'pie',
  data: expenseData
});



