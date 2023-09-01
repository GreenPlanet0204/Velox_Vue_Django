<template>
  <div class="row">
    <div class="col-lg-1"></div>
    <div class="col-lg-10">
      <h5 class="text-center">
        Conformation Score
        <span
          ><b
            >{{ sum ? sum + " samples" : "" }} - ({{
              allelite +
                " Elite - " +
                allnonelites +
                " Non-Elite - " +
                percentageelite +
                "% Elite Percent"
            }})</b
          ></span
        >
      </h5>
      <canvas id="conformation_score_by_age"></canvas>
      <div class="chart1">
        <div class="row text-center">
          <div class="col-lg-12">
            <table class="table table-borderless percantage_all">
              <thead>
                <tr>
                  <th scope="col">% of All</th>
                  <th
                    scope="col"
                    v-for="(per, index_2) in percentageArrAll"
                    :key="index_2"
                  >
                    {{ per.percentage + "%" }}
                  </th>
                </tr>
                <tr>
                  <th scope="col">% of Elite in Group</th>
                  <th
                    scope="col"
                    v-for="(per, index_3) in percentageArrElite"
                    :key="index_3"
                  >
                    {{ per.percentage + "%" }}
                  </th>
                </tr>
                <tr>
                  <th scope="col">% of Elite of all Elite</th>
                  <th
                    scope="col"
                    v-for="(per, index_4) in percentageArrEliteofElite"
                    :key="index_4"
                  >
                    {{ per.perc + "%" }}
                  </th>
                </tr>
                <tr>
                  <th scope="col">Odds Ratio</th>
                  <th
                    scope="col"
                    v-for="(per, index_5) in ratio"
                    :key="index_5"
                  >
                    {{ per.percentage }}
                  </th>
                </tr>
              </thead>
              <tbody></tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
    <div class="col-lg-1"></div>
  </div>
</template>

<script>
import Chart from "chart.js";
import { ConformationScoreByAge } from "../js/ConformationScoreByAge.js";

export default {
  name: "ConformationScoreByAge",
  props: {
    result1: []
  },
  data() {
    return {
      ConformationScoreByAge: ConformationScoreByAge,
      type: "",
      result: "",
      temp1: [],
      sum: "",
      percentageArrAll: [],
      percentageArrElite: [],
      percentageArrEliteofElite: [],
      ratio: [],
      allelite: [],
      allnonelites: [],
      percentageelite: ""
    };
  },
  async mounted() {
    this.result = this.result1;
    const ctx = document.getElementById("conformation_score_by_age");
    if (window.bar41 != undefined) {
      window.bar41.destroy();
    }
    const chartData = this.ConformationScoreByAge(
      this.result?.data?.conformation?.age
    );
    window.bar41 = new Chart(ctx, chartData);
    this.chart_type();
    this.temp1 = this.result?.data?.conformation?.age.map(item => item.counts);
    if (this.temp1 != undefined) {
      this.sum = this.temp1.reduce((partialSum, a) => partialSum + a, 0);
    }
  },
  methods: {
    async chart_type() {
      let temp,
        data = [];
      temp = this.result?.data?.conformation?.age;

      temp?.forEach(element => {
        data.push({
          score: element.score,
          elite: element.elite,
          counts: element.counts
        });
        this.temp1 = data.map(item => item.counts);
        if (this.temp1 != undefined) {
          this.sum = this.temp1.reduce((partialSum, a) => partialSum + a, 0);
        }
      });

      const ctx = document.getElementById("conformation_score_by_age");
      if (window.bar41 != undefined) {
        window.bar41.destroy();
      }
      const chart_type_data = this.ConformationScoreByAge(data);
      this.getPercentage(chart_type_data);
      window.bar41 = new Chart(ctx, chart_type_data);
    },
    async getPercentage(chartData) {
      this.allelite = chartData.data.datasets[1].data.reduce(
        (partialSum, a) => partialSum + a,
        0
      );
      this.allnonelites = chartData.data.datasets[0].data.reduce(
        (partialSum, a) => partialSum + a,
        0
      );
      this.percentageelite = ((this.allelite / this.sum) * 100).toFixed(2);
      this.percentageArrAll = [];
      this.percentageArrElite = [];
      this.percentageArrEliteofElite = [];
      var eliteArr = [];
      var eliteSum = 0;
      this.ratio = [];
      chartData.data.labels.forEach((e, i) => {
        const label = chartData.data.labels[i];

        /* calculate for step 1 start*/
        const labelViseArr = chartData.filteredArrData.filter(
          x => x.score == label
        );
        const labelSum = labelViseArr.reduce(
          (partialSum, a) => partialSum + a.sum,
          0
        );
        const percentage = ((labelSum * 100) / this.sum).toFixed(2);
        this.percentageArrAll.push({ score: label, percentage: percentage });
        /* calculate for step 1 end*/

        /* calculate for step 2 start*/
        const labelViseArr1 = chartData.filteredArrData.filter(
          x => x.score == label && x.elite == "Yes"
        );
        const labelSum1 = labelViseArr1.reduce(
          (partialSum, a) => partialSum + a.sum,
          0
        );
        const labelViseArr2 = chartData.filteredArrData.filter(
          x => x.score == label
        );
        const labelSum2 = labelViseArr2.reduce(
          (partialSum, a) => partialSum + a.sum,
          0
        );
        if (labelSum1 != 0 || labelSum2 != 0) {
          var percentage1 = ((labelSum1 * 100) / labelSum2).toFixed(2);
        } else {
          var percentage1 = 0;
        }
        this.percentageArrElite.push({ score: label, percentage: percentage1 });
        /* calculate for step 2 end*/

        /* calculate for step 3 start*/
        const labelViseArr3 = chartData.filteredArrData.filter(
          x => x.score == label && x.elite == "Yes"
        );
        eliteArr.push(labelViseArr3[0]);

        /* calculate for step 4 start*/
        const labelViseArr4 = chartData.filteredArrData.filter(
          x => x.score == label && x.elite == "Yes"
        );
        const labelSum3 = labelViseArr4.reduce(
          (partialSum, a) => partialSum + a.sum,
          0
        );
        const labelViseArr5 = chartData.filteredArrData.filter(
          x => x.score == label && x.elite == "No"
        );
        const labelSum4 = labelViseArr5.reduce(
          (partialSum, a) => partialSum + a.sum,
          0
        );
        if (
          labelSum3 == 0 ||
          labelSum4 == 0 ||
          labelSum3 == "" ||
          labelSum4 == "" ||
          isNaN(labelSum3) ||
          isNaN(labelSum4)
        ) {
          var percentage2 = 0;
        } else {
          var percentage2 = (
            labelSum3 /
            labelSum4 /
            (labelSum4 / labelSum3)
          ).toFixed(2);
        }
        this.ratio.push({ score: label, percentage: percentage2 });
        /* calculate for step 4 end*/
      });
      eliteSum = eliteArr.reduce((partialSum, a) => partialSum + a.sum, 0);
      eliteArr = eliteArr.map(x => {
        const perc = ((x.sum * 100) / eliteSum).toFixed(2);
        return { ...x, perc: perc };
      });
      this.percentageArrEliteofElite = eliteArr;
      /* calculate for step 3 end*/
    }
  }
};
</script>
<style>
.chart label {
  margin-right: 10px;
}
.chart input[type="radio"] {
  margin-right: 5px;
}
.chart1 {
  margin-top: 10px;
}
.percantage_all th:first-child {
  width: 13%;
}
.percantage_all th {
  width: 15%;
  font-size: 12.8px;
  text-align: left !important;
  padding-left: 0px;
  padding-right: 0px;
  font-weight: 400;
}
</style>
