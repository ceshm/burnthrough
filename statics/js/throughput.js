var vue = new Vue({
  el: '#app',
  delimiters: ["[[", "]]"],
  data: {},
});


const chart = new frappe.Chart("#weeklytp", {  // or a DOM element,
                                               // new Chart() in case of ES6 module with above usage
  title: "Weekly Histogram",
  data: {
    labels: ["w2-February", "w3-February", "w4-February", "w1-March", "w2-March", "w2-March", "w3-March", "w4-March", "w1-April", "w2-April", "w3-April"],
    datasets: [
      {
        name: "Prog Hrs", type: "area",
        values: [22, 25, 30, 35, 30, 32, 17, 22, 25, 23, 27]
      },
      {
        name: "Misc Hrs", type: "area",
        values: [11, 9, 20, 25, 22, 19, 22, 10, 12, 10, 12]
      },
    ]
  },
  type: 'axis-mixed', // or 'bar', 'line', 'scatter', 'pie', 'percentage'
  height: 250,
  //colors: ['#00a7e0', '#1e00e0','#00e038']
  colors: ['#00a7e0', '#e00052', '#e0b700']
});

const data = {
  labels: ["12am-3am", "3am-6pm", "6am-9am", "9am-12am",
    "12pm-3pm", "3pm-6pm", "6pm-9pm", "9am-12am"
  ],
  datasets: [
    {
      name: "Some Data", type: "bar",
      values: [25, 40, 30, 35, 8, 52, 17, -4]
    },
    {
      name: "Another Set", type: "line",
      values: [25, 50, -10, 15, 18, 32, 27, 14]
    },
    {
      name: "Trianother Set", type: "line",
      values: [20, 20, -10, 5, -5, 12, 37, 28]
    }
  ]
};
const chart2 = new frappe.Chart("#chartz", {  // or a DOM element,
                                              // new Chart() in case of ES6 module with above usage
  title: "",
  data: data,
  type: 'axis-mixed', // or 'bar', 'line', 'scatter', 'pie', 'percentage'
  height: 250,
  //colors: ['#00a7e0', '#1e00e0','#00e038']
  colors: ['#00a7e0', '#e00052', '#e0b700']
})

