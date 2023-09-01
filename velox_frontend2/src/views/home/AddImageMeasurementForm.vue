<template>
  <b-form class="av-tooltip tooltip-left-bottom">
    <div>
      <h5 class="mb-4 card-title">
        <span class="icon success">
          <i class="iconsminds-gears"></i>
        </span>
        <span>Add Image Measurement</span>
      </h5>
    </div>

    <b-row>
      <b-col cols="4">
        <b-form-group label="Date of Measurement" class="has-float-label">
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
    </b-row>
    <!--
    <b-row v-if="isDateofMeasureSelected">
      <b-col>
        <dropzone
          ref="dropzone"
          @file-added="onFileAdded"
          @completed="onCompleted"
        ></dropzone>
      </b-col>
    </b-row>
    -->
  </b-form>
</template>

<script>
import moment from "moment";
import vSelect from "vue-select";
import "vue-select/dist/vue-select.css";
import dictionaryServices from "@/services/dictionary.service.js";
import Datepicker from "vuejs-datepicker";
import Dropzone from "@/components/Dropzone";

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
    Dropzone
  },

  data() {
    return {
      isDateofMeasureSelected: false,
      controls: {}
    };
  },
  async mounted() {},
  methods: {
    onDateOfMeasurementSelect(e) {
      let selectedDate = moment.utc(e).format("YYYY-MM-DD");

      let measure = this.measurements.find(
        m => m.date_of_measure === selectedDate
      );

      if (measure) {
        if (measure.image) {
          this.isDateofMeasureSelected = false;

          this.$formHelpers.showError(
            "An image measurement is already on this date, please delete previous file to attach a new one"
          );
        } else {
          this.isDateofMeasureSelected = true;
        }
      } else {
        this.isDateofMeasureSelected = true;
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
  },
  watch: {
    isDateofMeasureSelected(newValue, oldValue) {
      if (newValue !== oldValue) this.$emit("date-changed", newValue);
    }
  }
};
</script>

<style></style>
