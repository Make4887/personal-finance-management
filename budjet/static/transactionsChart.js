const dataTransactionsChart = document.currentScript.dataset;
let balance_change = dataTransactionsChart.balanceChange;
let changing_date = dataTransactionsChart.changingDate;
console.log(balance_change);
console.log(changing_date);
balance_change = JSON.parse(balance_change);
changing_date = JSON.parse(changing_date);
console.log(balance_change);
console.log(changing_date);

let transactionsChart = document.getElementById("transactionsChart");
console.log(balance_change);
console.log(changing_date);

let transactionsData = {
  labels: changing_date,
  datasets: [
  {
    label: 'Изменение баланса по дням',
    data: balance_change,
    fill: false,
    borderColor: 'rgb(75, 192, 192)',
    tension: 0.1
  }]
};

let lineTransactionsChart = new Chart(transactionsChart, {
  type: 'line',
  data: transactionsData
});