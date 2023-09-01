export const ImageScoreByType = {
    type: "bar",
    data: {
        labels: [ 'A+', 'A', 'B+', 'B', 'C', 'D'],
        datasets: [
        {
            label: "Image Score by Type",
            data: [9, 7, 10, 5, 8, 3],
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
  
  export default ImageScoreByType;