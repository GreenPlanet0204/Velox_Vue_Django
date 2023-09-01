<template>
  <div>
    <canvas id="image_score_by_type"></canvas>
  </div>
</template>

<script>
import Chart from 'chart.js'
import ImageScoreByType from '../js/ImageScoreByType.js'

export default {
  name: 'ImageScoreByType',
   data() {
    return {
      ImageScoreByType: ImageScoreByType
    }
  },
  mounted() {
    const ctx = document.getElementById('image_score_by_type');
    new Chart(ctx, this.ImageScoreByType);
  }
}
</script>