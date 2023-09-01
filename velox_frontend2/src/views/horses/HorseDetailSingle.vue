<template>
  <div class="matrix">
    <div v-if="loading" class="loader">
      <svg
        width="200px"
        height="200px"
        xmlns="http://www.w3.org/2000/svg"
        xmlns:xlink="http://www.w3.org/1999/xlink"
        viewBox="0 0 100 100"
        preserveAspectRatio="xMidYMid"
        style="background: none"
      >
        <circle cx="75" cy="50" fill="#363a3c" r="6.39718">
          <animate
            attributeName="r"
            values="4.8;4.8;8;4.8;4.8"
            times="0;0.1;0.2;0.3;1"
            dur="1s"
            repeatCount="indefinite"
            begin="-0.875s"
          ></animate>
        </circle>
        <circle cx="67.678" cy="67.678" fill="#363a3c" r="4.8">
          <animate
            attributeName="r"
            values="4.8;4.8;8;4.8;4.8"
            times="0;0.1;0.2;0.3;1"
            dur="1s"
            repeatCount="indefinite"
            begin="-0.75s"
          ></animate>
        </circle>
        <circle cx="50" cy="75" fill="#363a3c" r="4.8">
          <animate
            attributeName="r"
            values="4.8;4.8;8;4.8;4.8"
            times="0;0.1;0.2;0.3;1"
            dur="1s"
            repeatCount="indefinite"
            begin="-0.625s"
          ></animate>
        </circle>
        <circle cx="32.322" cy="67.678" fill="#363a3c" r="4.8">
          <animate
            attributeName="r"
            values="4.8;4.8;8;4.8;4.8"
            times="0;0.1;0.2;0.3;1"
            dur="1s"
            repeatCount="indefinite"
            begin="-0.5s"
          ></animate>
        </circle>
        <circle cx="25" cy="50" fill="#363a3c" r="4.8">
          <animate
            attributeName="r"
            values="4.8;4.8;8;4.8;4.8"
            times="0;0.1;0.2;0.3;1"
            dur="1s"
            repeatCount="indefinite"
            begin="-0.375s"
          ></animate>
        </circle>
        <circle cx="32.322" cy="32.322" fill="#363a3c" r="4.80282">
          <animate
            attributeName="r"
            values="4.8;4.8;8;4.8;4.8"
            times="0;0.1;0.2;0.3;1"
            dur="1s"
            repeatCount="indefinite"
            begin="-0.25s"
          ></animate>
        </circle>
        <circle cx="50" cy="25" fill="#363a3c" r="6.40282">
          <animate
            attributeName="r"
            values="4.8;4.8;8;4.8;4.8"
            times="0;0.1;0.2;0.3;1"
            dur="1s"
            repeatCount="indefinite"
            begin="-0.125s"
          ></animate>
        </circle>
        <circle cx="67.678" cy="32.322" fill="#363a3c" r="7.99718">
          <animate
            attributeName="r"
            values="4.8;4.8;8;4.8;4.8"
            times="0;0.1;0.2;0.3;1"
            dur="1s"
            repeatCount="indefinite"
            begin="0s"
          ></animate>
        </circle>
      </svg>
    </div>
    <div v-else>
      <div class="table-responsive">
        <div @click="refresh('refresh')" class="refresh text-right mb-2 mr-2" style="font-size: 17px;"><i class="simple-icon-refresh"></i></div>
        <table class="table table-bordered">
          <thead>
            <tr>
              <th scope="col">Name</th>
              <th scope="col">Date of Measure</th>
              <th scope="col">Measures</th>
              <th scope="col">Last Score</th>
              <th scope="col">Cardio + Bio</th>
              <th scope="col">DNA + Cardio + Bio</th>
              <th scope="col">Optimal Distance</th>
              <th scope="col">Score</th>
            </tr>
          </thead>
          <tbody v-if="measures.length > 0">
            <tr v-for="(item,index) in measures" :key="index">
              <td>{{ data.name ? data.name : "-" }}</td>
              <td>{{ item.date_of_measure ? item.date_of_measure : "-" }}</td>
              <td>
                <span v-if="item.prob_bio_model"
                  ><i class="iconsminds-gears"></i
                ></span>
                <span v-if="item.cardio_video_probability"
                  ><i class="iconsminds-pulse"></i
                ></span>
                <span v-if="data.distance1"
                  ><i class="iconsminds-dna-2"></i
                ></span>
              </td>
              <td>{{ item.updated_at ? new Date(item.updated_at).getFullYear()+'-'+(new Date(item.updated_at).getMonth()+1)+'-'+new Date(item.updated_at).getDate()+' ' +new Date(item.updated_at).toLocaleTimeString('en',{ timeStyle: 'short', hour12: false, timeZone: 'UTC' }) : "-" }}</td>
              <td>
                <router-link
                  :to="{ name: 'CardioBioReport', params: { measure_id:item.id,id: data.id } }"
                  target="_blank"
                >
                  <span v-if="item.prob_cardio_bio_model" class="cardio_bio_report"
                    ><i class="simple-icon-doc"></i
                  ></span>
                </router-link>
                <span v-if="!item.prob_cardio_bio_model">-</span>
              </td>
              <td>
                <router-link
                  :to="{ name: 'DnaCardioBioReport', params: { measure_id:item.id,id: data.id } }"
                  target="_blank"
                >
                  <span v-if="item.prob_dna_cardio_bio_model" class="dna_cardio_bio_report"
                    ><i class="simple-icon-doc"></i
                  ></span>
                </router-link>
                <span v-if="!item.prob_dna_cardio_bio_model">-</span>
              </td>
              <td>{{ data.pred_opt_dist ? data.pred_opt_dist : "-" }}</td>
              <td>
                <span
                  v-if="item.prob_bio_model && item.cardio_video_probability && (item.prob_cardio_bio_model_score==null || item.prob_dna_cardio_bio_model_score==null)"
                  @click="score(item.id)"
                  class="score"
                  ><i class="simple-icon-target"></i
                ></span>
                <span v-else>-</span>
              </td>
            </tr>
          </tbody>
          <tbody v-else>
            <tr>
                <td colspan="8">
                    <h4 class="text-center">No Data Available</h4>
                </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import api from "@/services/axios";
import measureServices from "@/services/measure.service";

export default {
  props: {
    id: Number,
    getdata: Function,
  },
  data() {
    return {
      data: {},
      loading: false,
      measures:{},
    };
  },
  mounted() {
    this.loading = true;
    this.refresh();
  },
  methods: {
    refresh(text) {
      $(".refresh i").addClass("rotate");

      api.get(`/horses/${this.id}/`)   
        .then((response) => {
          this.data = response.data;
          this.measures= this.data.measures.filter(item => item.prob_bio_model != null && item.cardio_video_probability != null)
          
          if(text)
          {
            this.$formHelpers.showInfo('Success');
            this.getdata();
          }

          $(".refresh i").removeClass("rotate");
        })
        .catch((error) => {
          this.$formHelpers.showError('Error');
        })
        .finally(() => (this.loading = false));
    },
    async score(id) 
    {
      try 
      {
          await measureServices.measureScore(id);
          this.$formHelpers.showInfo('Success');

      } catch (e) {
          this.$formHelpers.showError('Error');
      }
    },
  },
};
</script>

<style>
.matrix .table-bordered {
  border: 5px solid #dee2e6;
}
.matrix .table-bordered th,
.table-bordered td {
  border: 5px solid #dee2e6 !important;
}
.cardio_bio_report,
.dna_cardio_bio_report,
.refresh,
.score {
  cursor: pointer;
}
.loader {
  text-align: center;
}
.refresh i {
  display: inline-block;
}
.rotate {
  -webkit-animation: spin 4s linear;
  -moz-animation: spin 4s linear;
  animation: spin 4s linear;
}
@-moz-keyframes spin {
  100% {
    -moz-transform: rotate(360deg);
  }
}
@-webkit-keyframes spin {
  100% {
    -webkit-transform: rotate(360deg);
  }
}
@keyframes spin {
  100% {
    -webkit-transform: rotate(360deg);
    transform: rotate(360deg);
  }
}
</style>

