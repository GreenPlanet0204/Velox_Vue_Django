<template>
  <div>
    <canvas id="biomechanics_score_by_type"></canvas>
  </div>
</template>

<script>
import Chart from 'chart.js'
import {BiomechanicsScoreByType} from '../js/BiomechanicsScoreByType.js'

export default {
  name: 'BiomechanicsScoreByType',
  props: {
		result1:[],
	},
   data() {
    return {
      BiomechanicsScoreByType: BiomechanicsScoreByType,
      result:"",
    }
  },
  async mounted() {
    this.result = this.result1;
    const ctx = document.getElementById('biomechanics_score_by_type');
    if (window.bar10 != undefined) {
      window.bar10.destroy();
    }
    new Chart(ctx, this.BiomechanicsScoreByType);
    window.bar10 = new Chart(ctx, this.BiomechanicsScoreByType(this.result?.data?.biomechanics?.type));
  }
}
</script>