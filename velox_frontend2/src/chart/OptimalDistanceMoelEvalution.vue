<template>
  <div class="row">
    <div class="col-lg-6">
        <h5 class="text-center">Optimal Distance</h5>
        <canvas id="optimal_distance_model_evalution"></canvas>
    </div>
    <div class="col-lg-6 matrix">
        <h5 class="text-center">Confusion Matrix</h5>
        <table class="table table-bordered">
          <thead>
            <tr>
              <th scope="col">True label/Predicted Label</th>
              <th>{{annotations[2]}}</th>
              <th>{{annotations[1]}}</th>
              <th>{{annotations[0]}}</th>
              <th>{{annotations[3]}}</th>
            </tr>
          </thead>
          <tbody v-if="confusion_matrix && confusion_matrix.length > 0">
            <tr>
              <th scope="row">{{annotations[2]}}</th>
              <td>{{confusion_matrix[2][2] ? confusion_matrix[2][2]+'%' : '-' }}</td>
              <td>{{confusion_matrix[2][1] ? confusion_matrix[2][1]+'%' : '-' }}</td>
              <td>{{confusion_matrix[2][0] ? confusion_matrix[2][0]+'%' : '-' }}</td>
              <td>{{confusion_matrix[2][3] ? confusion_matrix[2][3]+'%' : '-' }}</td>
            </tr>
             <tr>
              <th scope="row">{{annotations[1]}}</th>
              <td>{{confusion_matrix[1][2] ? confusion_matrix[1][2] +'%': '-' }}</td>
              <td>{{confusion_matrix[1][1] ? confusion_matrix[1][1] +'%': '-' }}</td>
              <td>{{confusion_matrix[1][0] ? confusion_matrix[1][0] +'%': '-' }}</td>
              <td>{{confusion_matrix[1][3] ? confusion_matrix[1][3] +'%': '-' }}</td>
            </tr>
             <tr>
              <th scope="row">{{annotations[0]}}</th>
              <td>{{confusion_matrix[0][2] ? confusion_matrix[0][2] +'%': '-' }}</td>
              <td>{{confusion_matrix[0][1] ? confusion_matrix[0][1] +'%': '-' }}</td>
              <td>{{confusion_matrix[0][0] ? confusion_matrix[0][0] +'%': '-' }}</td>
              <td>{{confusion_matrix[0][3] ? confusion_matrix[0][3] +'%': '-' }}</td>
            </tr>
             <tr >
              <th scope="row">{{annotations[3]}}</th>
              <td>{{confusion_matrix[3][2] ? confusion_matrix[3][2] +'%': '-' }}</td>
              <td>{{confusion_matrix[3][1] ? confusion_matrix[3][1] +'%': '-' }}</td>
              <td>{{confusion_matrix[3][0] ? confusion_matrix[3][0] +'%': '-' }}</td>
              <td>{{confusion_matrix[3][3] ? confusion_matrix[3][3] +'%': '-' }}</td>
            </tr>
          </tbody>
        </table>
    </div>
  </div>
</template>

<script>
import Chart from 'chart.js'
import {OptimalDistanceMoelEvalution} from '../js/OptimalDistanceMoelEvalution.js'

export default {
  name: 'OptimalDistanceMoelEvalution',
  props: {
		result1:[],
    },
   data() {
    return {
      OptimalDistanceMoelEvalution: OptimalDistanceMoelEvalution,
      result:"",
      annotations:[],
      confusion_matrix:[],
    }
  },
  async mounted() {
    this.result = this.result1;
    this.annotations=this.result?.data?.ml_models_metadata?.optimal_distance?.annotations;
    this.confusion_matrix=this.result?.data?.ml_models_metadata?.optimal_distance?.confusion_matrix;
    const ctx = document.getElementById('optimal_distance_model_evalution');
    if (window.bar16 != undefined) {
      window.bar16.destroy();
    }
    window.bar16 = new Chart(ctx, this.OptimalDistanceMoelEvalution(this.result?.data?.ml_models_metadata?.optimal_distance?.feature_attributions));
  }
}
</script>
