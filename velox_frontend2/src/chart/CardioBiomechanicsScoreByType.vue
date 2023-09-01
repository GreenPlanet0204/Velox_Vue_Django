<template>
  <div>
    <canvas id="cardio_biomechanics_score_by_type"></canvas>
  </div>
</template>

<script>
import Chart from 'chart.js'
import {CardioBiomechanicsScoreByType} from '../js/CardioBiomechanicsScoreByType.js'

export default {
  name: 'CardioBiomechanicsScoreByType',
  props: {
		result1:[],
	},
   data() {
    return {
      CardioBiomechanicsScoreByType: CardioBiomechanicsScoreByType,
      result:"",
    }
  },
  async mounted() {
    this.result = this.result1;
    const ctx = document.getElementById('cardio_biomechanics_score_by_type');
    if (window.bar12 != undefined) {
      window.bar12.destroy();
    }
    new Chart(ctx, this.CardioBiomechanicsScoreByType);
    window.bar12 = new Chart(ctx, this.CardioBiomechanicsScoreByType(this.result?.data?.cardio_biomechanics?.type));
  }
}
</script>