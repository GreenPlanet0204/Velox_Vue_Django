export const CardioScoreByCluster = (propsData) => {
    if(propsData != undefined)
    {
        var temp = [];
        var temp_2 = [];
        var temp_3 = [];
        var finArr = [];

        finArr = [
            { score: 'A+', elite: "Yes", sum: null },
            { score: 'A+', elite: "No", sum: null },
            { score: 'A', elite: "Yes", sum: null },
            { score: 'A', elite: "No", sum: null },
            { score: 'B+', elite: "Yes", sum: null },
            { score: 'B+', elite: "No", sum: null },
            { score: 'B', elite: "Yes", sum: null },
            { score: 'B', elite: "No", sum: null },
            { score: 'C', elite: "Yes", sum: null },
            { score: 'C', elite: "No", sum: null },
            { score: 'D', elite: "Yes", sum: null },
            { score: 'D', elite: "No", sum: null },
        ]
        //@ Filter data sum
        const dataTotal = (arr, type) => {
            arr.forEach(element => {
                if (element.length != 0) {
                    const sum1 = element.reduce((accumulator, object) => {
                        return accumulator + object['counts']
                    }, 0);
                    for (const obj of finArr) {
                        if (obj.score == element[0].score && obj.elite == type) {
                            obj.sum = sum1;
                            break;
                        }
                    }
                }
            });
        }
        //@ Filter Elite Data
        const filterEliteData = (data, type, condition) => {
            if (type == 'Yes') {
                temp_2.push(data.filter(item => item.elite == type && item.score == condition));
            } else {
                temp_3.push(data.filter(item => item.elite == type && item.score == condition));
            }
        }
        propsData.forEach(element => {
            temp.push(element.score);
        });

        let uniqueItems = [...new Set(temp)]

        uniqueItems.forEach(element => {
            filterEliteData(propsData, 'Yes', element)
            filterEliteData(propsData, 'No', element)

        });
        dataTotal(temp_2, 'Yes')
        dataTotal(temp_3, 'No')
    }
    else
    {
        return;
    }
    

    return {
        type: "bar",
        filteredArrData:finArr,
        data: {
            labels: [...new Set(finArr.map(item => item.score))],
            datasets: [
                {
                    label: "Non-Elite",
                    data: finArr.filter(item => item.elite == 'No').map(item => item.sum),
                    backgroundColor: "#a0cad8",
                },
                {
                    label: "Elite",
                    data: finArr.filter(item => item.elite == 'Yes').map(item => item.sum),
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
                        display: false
                    },
                    stacked: true
                }],
                yAxes: [{
                    gridLines: {
                        display: true
                    },
                    ticks: {
                        beginAtZero: true
                    },
                    stacked: true
                }]
            },
        }
    }
}

