export const ImageScoreByCluster = {
    type: "bar",
    data: {
        labels: [ 'A+', 'A', 'B+', 'B', 'C', 'D'],
        datasets: [
        {
            label: "Image Score by Cluster",
            data: [8, 2, 10, 4, 7, 6],
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
  
  export default ImageScoreByCluster;