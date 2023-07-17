const data = document.currentScript.dataset;
let chart_amount = data.chartAmount;
chart_amount = JSON.parse(chart_amount);
let moneyChart = document.getElementById("moneyChart");
console.log(chart_amount);

Chart.defaults.global.defaultFontFamily = "Lato";
Chart.defaults.global.defaultFontSize = 18;

let moneyData = {
  labels: [
    "Расход",
    "Доход",
    "Перевод со счета",
    "Перевод на счет",
  ],
  datasets: [
  {
    data: chart_amount,
    backgroundColor: [
      "#FF6384",
      "#63FF84",
      "#611304",
      "#FBCEB1",
    ]
  }]
};

let pieChart = new Chart(moneyChart, {
  type: 'pie',
  data: moneyData,
  options: {
    legend: {
      position: 'bottom'
    }
  }
});
