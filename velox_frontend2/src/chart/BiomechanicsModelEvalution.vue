<template>
  <div class="row">
    <div class="col-lg-6">
        <h5 class="text-center">Biomechanics</h5>
        <canvas id="biomechanics_model_evalution"></canvas>
    </div>
    <div class="col-lg-6 matrix">
        <h5 class="text-center">Confusion Matrix</h5>
        <table class="table table-bordered">
          <thead>
            <tr>
              <th scope="col">True label/Predicted Label</th>
              <th scope="col" v-for="annotation in  annotations" :key="annotation">{{annotation}}</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="annotation ,index in  annotations" :key="index">
              <th>{{annotation}}</th>
              <td v-for="annotation ,index_1 in  annotations" :key="index_1" v-bind:style="index==index_1 ? (index == 0) ? 'background-color: #a0cad8;color: black;' : 'background-color: #bbdeea;color: black;' : ''">
                {{confusion_matrix[index][index_1] ? confusion_matrix[index][index_1]+'%' : '-'}}
              </td>
            </tr>
          </tbody>
        </table>
    </div>
  </div>
</template>

<script>
import Chart from 'chart.js'
import {BiomechanicsModelEvalution} from '../js/BiomechanicsModelEvalution.js'

export default {
  name: 'BiomechanicsModelEvalution',
  props: {
		result1:[],
    },
   data() {
    return {
      BiomechanicsModelEvalution: BiomechanicsModelEvalution,
      result:"",
      annotations:[],
      confusion_matrix:[],
    }
  },
  async mounted() {
    this.result = this.result1;
    this.annotations=this.result?.data?.ml_models_metadata?.biomechanics?.annotations;
    this.confusion_matrix=this.result?.data?.ml_models_metadata?.biomechanics?.confusion_matrix;
    const ctx = document.getElementById('biomechanics_model_evalution');
    if (window.bar15 != undefined) {
      window.bar15.destroy();
    }
    window.bar15 = new Chart(ctx, this.BiomechanicsModelEvalution(this.result?.data?.ml_models_metadata?.biomechanics?.feature_attributions));
  }
}
</script>
<style>
.matrix .table-bordered {
    border: 5px solid #dee2e6;
}
.matrix .table-bordered th, .table-bordered td {
    border: 5px solid #dee2e6 !important;
}
</style>