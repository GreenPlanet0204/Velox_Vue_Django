<template>
  <div>
    <canvas id="conformation_score_by_type"></canvas>
  </div>
</template>

<script>
import Chart from "chart.js";
import { ConformationScoreByType } from "../js/ConformationScoreByType.js";

export default {
  name: "ConformationScoreByType",
  props: {
    result1: []
  },
  data() {
    return {
      ConformationScoreByType: ConformationScoreByType,
      result: ""
    };
  },
  async mounted() {
    this.result = this.result1;
    const ctx = document.getElementById("conformation_score_by_type");
    if (window.bar42 != undefined) {
      window.bar42.destroy();
    }
    new Chart(ctx, this.ConformationScoreByType);
    window.bar42 = new Chart(
      ctx,
      this.ConformationScoreByType(this.result?.data?.conformation?.type)
    );
  }
};
</script>
