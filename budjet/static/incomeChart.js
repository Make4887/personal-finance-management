const dataIncomeChart = document.currentScript.dataset;
let income_category = dataIncomeChart.incomeCategory;
let income_amount = dataIncomeChart.incomeAmount;
console.log(income_amount);
console.log(income_category);
income_category = JSON.parse(income_category);
income_amount = JSON.parse(income_amount);
console.log(income_amount);
console.log(income_category);

let incomeChart = document.getElementById("incomeChart");
console.log(income_amount);
console.log(income_category);

Chart.defaults.global.defaultFontFamily = "Lato";
Chart.defaults.global.defaultFontSize = 18;

let incomeData = {
    labels: income_category,
    datasets: [
        {
            data: income_amount,
            backgroundColor: [
                "#FF6384",
                "#63FF84",
                "#611304",
                "#FBCEB1",
            ]
        }]
};

let pieIncomeChart = new Chart(incomeChart, {
  type: 'pie',
  data: incomeData,
  options: {
    legend: {
        position: 'bottom'
        }
    }
});



