<template>
  <div>
    <canvas id="image_score_by_cluster"></canvas>
  </div>
</template>

<script>
import Chart from 'chart.js'
import ImageScoreByCluster from '../js/ImageScoreByCluster.js'

export default {
  name: 'ImageScoreByCluster',
   data() {
    return {
      ImageScoreByCluster: ImageScoreByCluster
    }
  },
  mounted() {
    const ctx = document.getElementById('image_score_by_cluster');
    new Chart(ctx, this.ImageScoreByCluster);
  }
}
</script>