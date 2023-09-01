<template>
  <div class="row">
    <div class="col-lg-1"></div>
      <div class="col-lg-10">
        <h5 class="text-center">Cardio Score by Horse Type</h5>
        <canvas id="cardio_score_by_type"></canvas>
      </div>
      <div class="col-lg-1"></div>
  </div>
</template>

<script>
import Chart from 'chart.js'
import {CardioScoreByType} from '../js/CardioScoreByType.js'

export default {
  name: 'CardioScoreByType',
  props: {
		result1:[],
	},
   data() {
    return {
      CardioScoreByType: CardioScoreByType,
      result:"",
    }
  },
  async mounted() {
    this.result = this.result1;
    const ctx = document.getElementById('cardio_score_by_type');
    if (window.bar8 != undefined) {
      window.bar8.destroy();
    }
    window.bar8 = new Chart(ctx, this.CardioScoreByType(this.result?.data?.cardio?.type));
  }
}
</script>