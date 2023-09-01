<template>
  <div>
    <canvas id="image_score_by_age"></canvas>
  </div>
</template>

<script>
import Chart from 'chart.js'
import ImageScoreByAge from '../js/ImageScoreByAge.js'

export default {
  name: 'ImageScoreByAge',
   data() {
    return {
      ImageScoreByAge: ImageScoreByAge
    }
  },
  mounted() {
    const ctx = document.getElementById('image_score_by_age');
    new Chart(ctx, this.ImageScoreByAge);
  }
}
</script>