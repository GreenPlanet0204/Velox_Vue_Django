export const DNACardioBiomechanicsScoreByType = (propsData) => {
    if(propsData != undefined)
    {
        var temp = [];
        var temp_2 = [];
        var temp_3 = [];
        var finArr = [];

        finArr = [
            { score: 'A+', type: "Flat", sum: null },
            { score: 'A+', type: "National Hunt", sum: null },
            { score: 'A', type: "Flat", sum: null },
            { score: 'A', type: "National Hunt", sum: null },
            { score: 'B+', type: "Flat", sum: null },
            { score: 'B+', type: "National Hunt", sum: null },
            { score: 'B', type: "Flat", sum: null },
            { score: 'B', type: "National Hunt", sum: null },
            { score: 'C', type: "Flat", sum: null },
            { score: 'C', type: "National Hunt", sum: null },
            { score: 'D', type: "Flat", sum: null },
            { score: 'D', type: "National Hunt", sum: null },
        ]
        //@ Filter data sum
        const dataTotal = (arr, type) => {
            arr.forEach(element => {
                if (element.length != 0) {
                    const sum1 = element.reduce((accumulator, object) => {
                        return accumulator + object['counts']
                    }, 0);
                    for (const obj of finArr) {
                        if (obj.score == element[0].score && obj.type == type) {
                            obj.sum = sum1;
                            break;
                        }
                    }
                }
            });
        }
        //@ Filter Elite Data
        const filterEliteData = (data, type, condition) => {
            if (type == 'Flat') {
                temp_2.push(data.filter(item => item.type == type && item.score == condition));
            } else {
                temp_3.push(data.filter(item => item.type == type && item.score == condition));
            }
        }
        propsData.forEach(element => {
            temp.push(element.score);
        });
        let uniqueItems = [...new Set(temp)]

        uniqueItems.forEach(element => {
            filterEliteData(propsData, 'Flat', element)
            filterEliteData(propsData, 'National Hunt', element)

        });
        dataTotal(temp_2, 'Flat')
        dataTotal(temp_3, 'National Hunt')
    }
    else 
    {
        return;
    }

    return {
        type: "bar",
        data: {
            labels: [...new Set(finArr.map(item => item.score))],
            datasets: [
            {
                label: "Flat",
                data: finArr.filter(item => item.type == 'Flat').map(item => item.sum),
                backgroundColor: "#bbdeea",
            },
            {
                label: "National Hunt",
                data: finArr.filter(item => item.type == 'National Hunt').map(item => item.sum),
                backgroundColor: "#a0cad8",
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
                        beginAtZero: true
                    }   
                }]
            },
        }
    }
}