<template>
  <div>
    <h1 v-if="!measureId">Create new Measurement</h1>
    <b-row>
      <b-col cols="4">
        <b-form @submit.stop.prevent="onSubmit">
          <b-form-group label="Horse" label-for="horse">
            <!--            <b-form-select id="horse" v-model="measure.horse" :options="horses" value-field="id"-->
            <!--                           text-field="name"-->
            <!--                           required></b-form-select>-->
            <v-select v-model="measure.horse" label="name" :reduce="(horse) => horse.id" :options="horses"></v-select>
          </b-form-group>

          <!--          <div class="error" v-if="measure.video_qc.required">Name is requiredx</div>-->
          <b-form-group label="Date of Measure" label-for="date-of-measure">
            <b-input-group class="mb-3">
              <b-form-input
                id="measure-date-input"
                v-model="measure.date_of_measure"
                placeholder="YYYY-MM-DD"
                type="text"
                autocomplete="off"
              ></b-form-input>
              <b-input-group-append>
                <b-form-datepicker id="date-of-measure" v-model="measure.date_of_measure" button-only right
                                   aria-controls="measure-date-input" @context="onContext"
                                   required>
                </b-form-datepicker>
              </b-input-group-append>


            </b-input-group>
          </b-form-group>
          <b-form-group label="File" label-for="file">
            <b-form-file
              id="file"
              v-model="file"
              :state="Boolean(file)"
              placeholder="Choose a video file or drop it here..."
              drop-placeholder="Drop video file here..."
              accept=".mp4, .mov"
            ></b-form-file>
            <b-link v-if="measure.video_url" :href="measure.video_url">{{ measure.video_url }}</b-link>
            <!--            <b-embed v-if="measure.video_url" type="video" :datasrc="measure.video_url" aspect="16by9"></b-embed>-->
          </b-form-group>

          <b-form-group label="Video QC" label-for="video-qc">
            <!-- <b-form-select id="video-qc" v-model="measure.video_qc" :options="videoQCOptions"
                           placeholder="Video Quality" required>
            </b-form-select> -->
            <!--            <div v-if="v$.video_qc.$error">VideoQC field has an error.</div>-->
          </b-form-group>

          <b-form-group label="Cardio Video" label-for="cardio-video">
            <b-form-file
              id="cardio-video"
              v-model="cardioFile"
              :state="Boolean(cardioFile)"
              placeholder="Choose a video file or drop it here..."
              drop-placeholder="Drop video file here..."
              accept=".mp4, .mov"
            ></b-form-file>
          </b-form-group>
          <b-link v-if="measure.cardio_video_url" :href="measure.cardio_video_url">{{ measure.cardio_video_url }}
          </b-link>
          <!--          <b-embed v-if="measure.cardio_video_url" type="iframe" :datasrc="measure.cardio_video_url" aspect="16by9"></b-embed>-->

          <b-form-group label="Cardio Video QC" label-for="cardio-video-qc">
            <!-- <b-form-select id="cardio-video-qc" v-model="measure.cardio_quality" :options="videoQCOptions"
                           placeholder="Video Quality" required>
            </b-form-select> -->
          </b-form-group>

          <b-form-group label="Cardio Type" label-for="cardio-type">
            <b-form-select id="cardio-type" v-model="measure.cardio_type" :options="cardioVideoTypes"
                           placeholder="Cardio Type" required>
            </b-form-select>
          </b-form-group>

          <!--          <p v-for="(error, index) of $v.$errors"-->
          <!--            :key="index">-->
          <!--            <strong>{{ error.$validator }}</strong>-->
          <!--            <small> on property</small>-->
          <!--            <strong>{{ error.$property }}</strong>-->
          <!--            <small> says:</small>-->
          <!--            <strong>{{ error.$message }}</strong>-->
          <!--          </p>-->
          <b-button @click="submit()"
                    :disabled="!((this.measure.video_url || this.measure.cardio_video_url) || (this.file || this.cardioFile))">
            Submit
          </b-button>
        </b-form>
      </b-col>
    </b-row>
  </div>
</template>

<script>
import axios from "axios";
import {getSignedAPIUrl} from "../utils/apis";
import {horsesAPIUrl} from "../utils/apis";
import {measuresAPIUrl} from "../utils/apis";
// import {reactive} from '@vue/composition-api';
import useVuelidate from '@vuelidate/core';
import {required} from '@vuelidate/validators';
import {ExecuteRequest} from "../utils/common";

export default {
  name: "MeasureForm",
  props: {
    measureId: {
      // type: Number
    }
  },
  data() {
    return {
      measure: {
        horse: '',
        // video_qc: '',
        // date_of_measure: '',
      },
      file: null,
      cardioFile: null,
      videoQCOptions: [
        {'value': 'OK', text: 'OK'},
        {'value': 'Good', text: 'Good'},
        {'value': 'Poor', text: 'Poor'}
      ],
      cardioVideoTypes: [
        {value: 'Bullseye', text: 'Bullseye'},
        {value: 'Turf/Off-speed Dirt', text: 'Turf/Off-speed Dirt'},
        {value: 'Irregular/Immature', text: 'Irregular/Immature'},
        {value: 'Small/Sprint', text: 'Small/Sprint'},
      ],
      horses: []
    }
  },

  setup: () => ({v$: useVuelidate()}),

  validations() {
    return {
      measure: {
        horse: {required},
        // video_qc: {required},
        date_of_measure: {required},
      },
      file: {required}
    }
  },
  methods: {
    onContext(ctx) {
      // The date formatted in the locale, or the `label-no-date-selected` string
      this.formatted = ctx.selectedFormatted
      // The following will be an empty string until a valid date is entered
      this.selected = ctx.selectedYMD
    },
    getHorses() {
      ExecuteRequest(horsesAPIUrl).then(data => {
        this.horses = data;
      })
    },
    submit() {
      // console.log(this.v$);
      // const result = this.v$.$validate();
      // console.log(result);
      // if (!result) {
      //   // notify user form is invalid
      //   return
      // }


      this.$bvToast.toast('Uploading files and data', {
        title: 'Measure'
      })

      let v = this;

      function uploadVideo() {
        if (v.file == null) {
          return Promise.resolve();
        }
        const data = {
          filename: v.file.name,
          content_type: v.file.type,
          video_type: 'video',
          date_of_measure: v.measure.date_of_measure
        }
        console.log(data);
        return axios.post(getSignedAPIUrl, data).then(response => {
            const data = response.data;
            v.measure['gcs_path'] = data.gcs_path;
            v.measure['gcs_bucket'] = data.gcs_bucket
            v.measure['gcs_filename'] = data.gcs_filename
            return data;
          }
        ).then(data => {
          let config = {
            headers: {
              'content-type': v.file.type,
            }
          }
          return axios.put(data.url, v.file, config)
        }).catch(error => {
          console.log(error);
          //${error.response.data.detail}
          v.$bvToast.toast(`${error.response.data}`, {
            title: 'Error',
            variant: 'danger'
          })
          return Promise.reject(error);
        })
      }

      function uploadCardioVideoFile() {
        if (v.file == null) {
          return Promise.resolve();
        }
        if (v.cardioFile != null) {
          const cardioFileData = {
            filename: v.cardioFile.name,
            content_type: v.cardioFile.type,
            video_type: 'cardio',
            date_of_measure: v.measure.date_of_measure
          }
          let cardioVideo = {}
          return axios.post(getSignedAPIUrl, cardioFileData).then(response => {
              const data = response.data;
              cardioVideo['path'] = data.gcs_path;
              cardioVideo['bucket'] = data.gcs_bucket
              cardioVideo['filename'] = data.gcs_filename
              v.measure['cardio_video'] = cardioVideo
              return data;
            }
          ).then(data => {
            let config = {
              headers: {
                'content-type': v.cardioFile.type,
              }
            }
            return axios.put(data.url, v.cardioFile, config)
          })
            .catch(error => {
              console.log('catching error for upload')
              console.log(error);
              let errorMsg = "";
              if (error.response != null) {
                errorMsg = error.response.data;
              } else {
                errorMsg = error;
              }
              v.$bvToast.toast(errorMsg, {
                title: 'Error',
                variant: 'danger'
              })
            })
        }
      }

      uploadVideo().then(response => {
          return uploadCardioVideoFile()
        }
      ).then(response => {
        console.log('making request to the Measure API')
        console.log(v.measure);
        let method = 'post';
        let measureUrl = measuresAPIUrl;
        const measureId = v.measure['id']
        let measure = v.measure
        if (measureId !== undefined) {
          method = 'patch';
          measureUrl = `${measuresAPIUrl}${measureId}/`;
          // TODO remove fields for Measure
        }
        axios.request({
          method: method,
          url: measureUrl,
          data: measure
        }).then(response => {
          if (method==="post") {
            this.measure = {};
            this.file = null;
            this.cardioFile = null;
          }
          axios.get(measureUrl).then(resp => {
            v.measure = resp.data;
          })
          this.$bvToast.toast(`Data saved successfully`, {
            title: 'Measure'
          })
        }).catch(error => {
          //${error.response.data.detail}
          let errorMsg = "";
          if (error.response != null) {
            errorMsg = error.response.data;
          } else {
            errorMsg = error;
          }
          this.$bvToast.toast(errorMsg, {
            title: 'Error',
            variant: 'danger'
          })
        })
      })
    }

  },
  mounted() {
    this.getHorses()
    if (this.measureId) {
      const measureUrl = `${measuresAPIUrl}${this.measureId}`
      axios.get(measureUrl).then(resp => {
        console.log(resp.data)
        this.measure = resp.data;
      })
    }
  }
}
</script>

<style scoped>

</style>
