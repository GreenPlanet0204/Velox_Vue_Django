<template>
  <div>
    <canvas id="dna_cardio_biomechanics_score_by_type"></canvas>
  </div>
</template>

<script>
import Chart from 'chart.js'
import {DNACardioBiomechanicsScoreByType} from '../js/DNACardioBiomechanicsScoreByType.js'

export default {
  name: 'DNACardioBiomechanicsScoreByType',
  props: {
		result1:[],
	},
   data() {
    return {
      DNACardioBiomechanicsScoreByType: DNACardioBiomechanicsScoreByType,
      result:"",
    }
  },
  async mounted() {
    this.result = this.result1;
    const ctx = document.getElementById('dna_cardio_biomechanics_score_by_type');
    if (window.bar14 != undefined) {
      window.bar14.destroy();
    }
    new Chart(ctx, this.DNACardioBiomechanicsScoreByType);
    window.bar14 = new Chart(ctx, this.DNACardioBiomechanicsScoreByType(this.result?.data?.dna_cardio_biomechanics?.type));
  }
}
</script>