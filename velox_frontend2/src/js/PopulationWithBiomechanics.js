export const PopulationWithBiomechanics=(propsData)=>{
  if (propsData != undefined) {
    var temp = [];
    propsData.forEach(propsData => {
      temp.push({
        'horse_type':propsData.horse_type,
        'counts' : propsData.counts
      });
    });
  }
  else 
  {
    return;
  }
    return {
      type: "pie",
      data: {
        labels:temp.map(item => item.horse_type),
        datasets: [
          {
            data: temp.map(item => item.counts),
            backgroundColor: ['#bbdeea','#a0cad8','#c9e5ee', '#bbe6f4', '#c8f4ff', '#d6ffff', '#bbdeea', '#c9e5ee'],
          },
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
        }
      },
    }
}