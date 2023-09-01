export const BiomechanicsModelEvalution = (propsData) =>{
    if(propsData != undefined)
    {
        var temp = [];
        Object.keys(propsData).forEach(key => {
            temp.push({
                'keys':key,
                'values' : propsData[key],
                'backgroundcolor' : '#bbdeea'
              });
          });
          temp.sort((a, b) => (a.values < b.values) ? 1 : -1)
    }
    else
    {
        return;
    }

    return {
        type: "horizontalBar",
        data: {
            labels: temp.map(item => item.keys),
            datasets: [
                {
                    data: temp.map(item => item.values),
                    backgroundColor: temp.map(item => item.backgroundcolor),
                }
            ]
        },
        options: {
            tooltips: {
                enabled: true
            },
            responsive: true,
            legend: {
                display: false,
                position: 'bottom',
                fullWidth: true,
                labels: {
                    boxWidth: 10,
                    padding: 50
                }
            },
            scales: {
                yAxes: [{
                    barPercentage: 0.75,
                    gridLines: {
                        display: true,
                        drawTicks: false,
                        drawOnChartArea: false
                    },
                    ticks: {
                        fontColor: '#555759',
                        fontFamily: 'Lato',
                        fontSize: 15
                    }
    
                }],
                xAxes: [{
                    gridLines: {
                        display: true,
                        drawTicks: false,
                        tickMarkLength: 5,
                        drawBorder: false
                    },
                    ticks: {
                        padding: 5,
                        beginAtZero: true,
                        fontColor: '#555759',
                        fontFamily: 'Lato',
                        fontSize: 15,
                        callback: function (label, index, labels) {
                            return label/1000;
                        }
    
                    },
                    scaleLabel: {
                        display: true,
                        padding: 10,
                        fontFamily: 'Lato',
                        fontColor: '#555759',
                        fontSize: 16,
                        fontStyle: 700,
                        labelString: 'Feature Attribution',

                    },
    
                }]
            }
        }
    }
}