"use strict";

const options = {
    responsive: true
};

// Make donut chart of monthly budget 

let ctx_donut = $("#donutChart").get(0).getContext("2d");

var random_var = '{{ rand_var }}';
var random_var2 = '{{ user.other_debts}}';
var random_var3 = '{{ mo_salary_left }}';
var random_var4 = random_var3 - random_var2 - random_var

// var random_var = {{ mort_pay|tojson }}; 

// $.get("/monthly-budget.json", function (data) {
let myDonutChart = new Chart(ctx_donut, {
                                      type: 'doughnut',
                                      data: {
                                        labels: ["Remaining Monthly Income", "PITI", "Other Debts"],
                                        datasets: [
                                        {
                                        "data": [random_var4, random_var, random_var2],
                                        "backgroundColor": [
                                            "#FF6384",
                                            "#36A2EB",
                                            "#FFCE56"
                                        ]
                                        }
                                        ]
                                      },
                                      options: options
                                    });
$('#donutLegend').html(myDonutChart.generateLegend());
// });

let ctx_bar = $("#barChart").get(0).getContext("2d")

let myBarChart = new Chart(ctx_bar, {
                                type: 'bar',
                                data: {
                                    labels: ["Remaining Monthly Income", "PITI", "Other Debts"],
                                    datasets: [
                                        {
                                        "data": [random_var4, random_var, random_var2],
                                        "backgroundColor": [
                                            "#FF6384",
                                            "#36A2EB",
                                            "#FFCE56"
                                        ]
                                        }
                                        ]
                                      },
                                      options: options
                                    });
                                
$('#barLegend').html(myBarChart.generateLegend());

var another_var = '{{ mo_salary_left }}' * .64; 
var another_var2 = ('{{ mo_salary_left }}' * .36) - random_var2;

function updateChart() {
    myDonutChart.data.datasets[0].data = [another_var, another_var2, random_var2];
    myDonutChart.update();
    myBarChart.data.datasets[0].data = [another_var, another_var2, random_var2];
    myBarChart.update();
}

function revertChart() {
    myDonutChart.data.datasets[0].data = [random_var4, random_var, random_var2];
    myDonutChart.update();
    myBarChart.data.datasets[0].data = [random_var4, random_var, random_var2];
    myBarChart.update();
}

/* For first slider */ 
var slider = document.getElementById("myRange");
// var output = document.getElementById("demo");
var sliderNumber = document.getElementById("sliderNumber");
// output.innerHTML = slider.value; 
var moPay = document.getElementById("moPay"); 
// var debts = '{{ other_debts }}'; 



slider.onchange = function() {
    sliderNumber.innerHTML = this.value; 
    moPay.innerHTML = (slider.value * random_var3 / 100) - random_var2; 
}