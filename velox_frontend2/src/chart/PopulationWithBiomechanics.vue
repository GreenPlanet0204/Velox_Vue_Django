<template>
  <div class="row">
    <div class="col-lg-1"></div>
    <div class="col-lg-10">
      <h5 class="text-center">Biomechanics Measurements by Population</h5>
      <canvas id="Population_with_biomechanics"></canvas>
      <div class="chart1">
        <div class="row text-center">
          <div class="col-lg-12">
            <label>Category:-</label><input type="radio" v-model="type" value="all" @change="chart_type($event)" checked="type=='all'"><label for="All">All</label>
            <input type="radio" v-model="type" value="elite" @change="chart_type($event)"><label for="Elite">Elite</label>
            <input type="radio" v-model="type" value="non_elite" @change="chart_type($event)"><label for="Non-Elite">Non-Elite</label>
          </div>
        </div>
      </div>
    </div>
    <div class="col-lg-1"></div>
  </div>
</template>

<script>
import Chart from 'chart.js'
import {PopulationWithBiomechanics} from '../js/PopulationWithBiomechanics.js'
import horseServices from "@/services/horse.service"; 

export default {
  name: 'PopulationWithBiomechanics',
  props: {
		result1:[],
	},
   data() {
    return {
      PopulationWithBiomechanics: PopulationWithBiomechanics,
      type:"",
      result:"",
    }
  },
  async mounted() {
      this.result = this.result1;
      const ctx = document.getElementById('Population_with_biomechanics');
      if (window.bar2 != undefined) {
        window.bar2.destroy();
      }
      window.bar2= new Chart(ctx, this.PopulationWithBiomechanics(this.result?.data?.population?.biomechanics?.all));
      this.type='all';
  },
  methods:{
    async chart_type(event)
    {
       var chart_type_val = event.target.value;
       let data;
        if(chart_type_val ==='elite')
        {
            data=this.result.data?.population.biomechanics.elite
        }
        else if(chart_type_val ==='non_elite')
        {
            data=this.result.data?.population.biomechanics.non_elite
        }
        else
        {
            data=this.result.data?.population.biomechanics.all
        }
        
        const ctx = document.getElementById('Population_with_biomechanics');
        if (window.bar2 != undefined) {
          window.bar2.destroy();
        }
        window.bar2 = new Chart(ctx, this.PopulationWithBiomechanics(data));
    },
  }
}
</script>
<style>
.chart label {
    margin-right: 10px;
}
.chart input[type="radio"] {
    margin-right: 5px;
}
.chart1 {
  margin-top: 10px;
}
</style>