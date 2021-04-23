// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#292b2c';

// Pie Chart Example
var ctx = document.getElementById("PieChart");
var myPieChart = new Chart(ctx, {
  type: 'pie',
  data: {
    labels: [ "已流失客户", "易流失客户", "安全客户"],
    datasets: [{
      data: [20.37,3.95,75.68],
      backgroundColor: [ '#dc3545', '#ffc107', '#28a745'],
    }],
  },
});
