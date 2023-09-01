<template>
  <b-form class="av-tooltip tooltip-left-bottom mb-5">
    <div>
      <h5 class="mb-4 card-title">
        <span class="icon success">
          <i class="iconsminds-pulse"></i>
        </span>
        <span>Load Cardio Video</span>
      </h5>
    </div>
    <b-row>
      <b-col cols="4"
        ><b-form-group label="Date of Measurement" class="has-float-label">
          <datepicker
            :bootstrap-styling="true"
            placeholder="Date of Measurement"
            v-model="value.date_of_measure"
            @selected="onDateOfMeasurementSelect"
            format="yyyy-MM-dd"
            :typeable="true"
            :use-utc="true"
          ></datepicker>
        </b-form-group>
      </b-col>

      <!-- <b-col v-if="value.file.upload" cols="4"
        ><b-form-group label="Quality Control" class="has-float-label">
          <v-select
            v-model="value.video_qc"
            :options="controls.video_qc.options"
          />
        </b-form-group>
      </b-col>
      <b-col v-if="value.file.upload" cols="4"
        ><b-form-group label="Cardio Type" class="has-float-label">
          <v-select
            v-model="value.cardio_type"
            :options="controls.cardio_type.options"
          />
        </b-form-group>
      </b-col> -->
    </b-row>
    <b-row v-if="isVideoAreaVisible">
      <b-col>
        <dropzone
          ref="dropzone"
          @file-added="onFileAdded"
          @completed="onCompleted"
        ></dropzone>
      </b-col>
    </b-row>

    <ComplementaryCardio
      ref="complementarycardio"
    ></ComplementaryCardio>
  </b-form>
</template>

<script>
import moment from "moment";
import vSelect from "vue-select";
import "vue-select/dist/vue-select.css";
import dictionaryServices from "@/services/dictionary.service.js";
import Datepicker from "vuejs-datepicker";
import Dropzone from "@/components/Dropzone";
import ComplementaryCardio from "./ComplementaryCardio";

export default {
  props: {
    value: {
      type: Object,
      default: () => {}
    },
    measurements: {
      type: Array,
      default: () => []
    }
  },
  components: {
    vSelect,
    Datepicker,
    Dropzone,
    ComplementaryCardio
  },

  data() {
    return {
      isVideoAreaVisible: false,
      // controls: {
      //   video_qc: {
      //     options: []
      //   },
      //   cardio_type: {
      //     options: []
      //   }
      // }
    };
  },
  async mounted() {
    // this.controls.video_qc.options = await dictionaryServices.fetchVideoQualityOptions();

    // this.controls.cardio_type.options = await dictionaryServices.fetchCardioTypeOptions();
  },
  methods: {
    onDateOfMeasurementSelect(e) {
      let selectedDate = moment.utc(e).format("YYYY-MM-DD");

      console.log("onDateOfMeasurementSelect", selectedDate, this.measurements);
      let measure = this.measurements.find(
        m => m.date_of_measure === selectedDate
      );
      console.log("onDateOfMeasurementSelect.measure", measure);
      if (measure) {
        if (measure.cardio_video) {
          this.isVideoAreaVisible = false;

          this.$formHelpers.showError(
            "Cardio Video already on this date, please delete previous file to attach a new one"
          );
          
        } else {
          this.isVideoAreaVisible = true;
          this.$refs.complementarycardio.show(selectedDate);
        }
        
      } else {
        this.isVideoAreaVisible = true;
      }
    },
    onFileAdded(file) {
      this.value.file = file;
    },
    enqueueFile(file) {
      this.$refs.dropzone.enqueueFile(file);
    },
    removeAllFiles() {
      if (this.$refs.dropzone) this.$refs.dropzone.removeAllFiles();
    },

    onCompleted(e) {
      this.$emit("completed", e);
    }
  }
};
</script>

<style></style>
