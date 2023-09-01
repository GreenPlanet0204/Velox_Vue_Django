export const ImageScoreByAge = {
    type: "bar",
    data: {
        labels: [ 'A+', 'A', 'B+', 'B', 'C', 'D'],
        datasets: [
        {
            label: "Image Score by Age",
            data: [5, 10, 8, 9, 5, 2],
            backgroundColor: "#bbdeea",
        }
        ]
    },
    options: {
      responsive: true,
      legend: {
        position: 'bottom',
        labels: {
            usePointStyle: true,
            boxWidth: 6
          }
      },
      scales: {
            xAxes: [{
                gridLines: {
                    display:false
                }
            }],
            yAxes: [{
                gridLines: {
                    display:true
                },
                ticks: {
                    beginAtZero: true,
                },    
            }]
        },
    }
  };
  
  export default ImageScoreByAge;