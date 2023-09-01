<template>
  <b-modal id="modalId" ref="modalRef" size="lg">
    <div slot="modal-title" style="width: 40em">
      <b-row>
        <b-col cols="3">Search for Horse</b-col>
      </b-row>
    </div>

    <b-form class="av-tooltip tooltip-left-bottom mb-5">
      <b-form-group label="Search" class="has-float-label">
        <vue-autosuggest
          class="autosuggest"
          :input-props="controls.search.props"
          :suggestions="filteredOptions"
          :render-suggestion="renderSuggestion"
          :get-suggestion-value="getSuggestionValue"
          :limit="6"
          @selected="onAutosuggestSelected"
          @input="onAutoSuggestInputChange"
        ></vue-autosuggest>
      </b-form-group>
      <b-row>
        <b-col>
          <b-form-group label="Name" class="has-float-label">
            <b-form-input type="text" v-model.trim="selectedHorse.name" />
          </b-form-group>
        </b-col>
        <b-col>
          <b-form-group label="Sex" class="has-float-label">
            <b-form-input type="text" v-model.trim="selectedHorse.sex" />
          </b-form-group>
        </b-col>
        <b-col>
          <b-form-group label="Date of Birth" class="has-float-label">
            <b-form-input
              type="text"
              v-model.trim="selectedHorse.date_of_birth"
            />
          </b-form-group>
        </b-col>
      </b-row>

      <BiomechanicsVideoForm
        ref="videoForm"
        v-if="selectedHorse.id"
        v-model="videoData"
        :measurements="measurementsData"
        @completed="onVideoUploadCompleted"
      ></BiomechanicsVideoForm>

      <b-row>
        <b-col> </b-col>
      </b-row>
    </b-form>

    <template slot="modal-footer">
      <b-button
        variant="primary"
        class="mr-1"
        :disabled="isSaveDisabled"
        @click="onModalSave"
        >Save</b-button
      >
      <b-button variant="secondary" @click="onModalCancel">Cancel</b-button>
    </template>
  </b-modal>
</template>

<script>
import api from "@/services/axios";
import moment from "moment";
import { VueAutosuggest } from "vue-autosuggest";
import horseServices from "@/services/horse.service";
import measureServices from "@/services/measure.service";
import commonServices from "@/services/common.service";
import BiomechanicsVideoForm from "./BiomechanicsVideoForm";

export default {
  components: {
    VueAutosuggest,
    BiomechanicsVideoForm
  },
  data() {
    return {
      isSaveDisabled: false,
      form: {
        search: ""
      },
      controls: {
        search: {
          props: {
            id: "autosuggest__input",
            class: "form-control",
            placeholder: "type horse name to search"
          }
        }
      },
      filteredOptions: [],
      selectedHorse: {
        id: "",
        name: "",
        sex: "",
        date_of_birth: ""
      },
      measurementsData: [],
      videoData: {
        file: ""
      },
      measureData: {},
      file: ""
    };
  },
  async mounted() {},
  methods: {
    async onAutoSuggestInputChange(text, oldText) {
      this.isSaveDisabled = false;

      if (!text) {
        this.selectedHorse = {};
        return;
      }

      if (typeof this.searchTimer !== "undefined") {
        clearTimeout(this.searchTimer);
      }

      this.searchTimer = setTimeout(async () => {
        let res = await horseServices.fetchHorses({ name: text });

        let data = res.data.results;

        const filteredData = data.filter(option => {
          return option.name.toLowerCase().indexOf(text.toLowerCase()) > -1;
        });

        this.filteredOptions = [
          {
            data: filteredData
          }
        ];
      }, 500);
    },
    async onAutosuggestSelected(item) {
      this.selectedHorse = item.item;

      this.videoData = this.$formHelpers.resetObject(this.videoData);

      this.fetchMeasurementsData();
    },
    async fetchMeasurementsData() {
      this.measurementsData = await measureServices.fetchHorseMeasures(
        this.selectedHorse
      );
    },
    renderSuggestion(suggestion) {
      // const character = suggestion.item;
      // return character.name;
       if(suggestion.item.name !='' && suggestion.item.sire !='' && suggestion.item.sire != null)
      {
        const character = suggestion.item;
        return character.name+ ' by '+character.sire;
      }
      else if(suggestion.item.name !='' && suggestion.item.sire == null || suggestion.item.sire == '')
      {
        const character = suggestion.item;
        return character.name;
      }
      else 
      {
        const character = suggestion.item;
        return character.name;
      }
    },
    getSuggestionValue(suggestion) {
      // return suggestion.item.name;
      if(suggestion.item.name !='' && suggestion.item.sire !='' && suggestion.item.sire != null)
      {
        return suggestion.item.name+ ' by '+ suggestion.item.sire;
      }
      else if(suggestion.item.name !='' && suggestion.item.sire == null || suggestion.item.sire == '')
      {
          return suggestion.item.name;
      }
      else 
      {
          return suggestion.item.name;
      }
    },
    show() {
      this.selectedHorse = this.$formHelpers.resetObject(this.selectedHorse);
      this.videoData = this.$formHelpers.resetObject(this.videoData);

      this.$refs.modalRef.show();
    },
    hide() {
      this.$refs.modalRef.hide();
    },
    validate() {
      let errors = [];

      if (!this.selectedHorse.id) errors.push("Please select a horse");

      if (!this.videoData.date_of_measure)
        errors.push("Please select date of measurement");

      if (!this.videoData.file) errors.push("Please select video file");

      // if (!this.videoData.video_qc) errors.push("Please select video quality");

      if (errors.length) {
        this.$formHelpers.showError(errors[0]);
        return false;
      }

      return true;
    },
    async onModalSave() {
      if (!this.validate()) {
        return;
      }

      this.measureData = {
        date_of_measure: moment
          .utc(this.videoData.date_of_measure)
          .format("YYYY-MM-DD"),
        horse: this.selectedHorse.id,
        // video_qc: this.videoData.video_qc
      };
      const video_data = {
        filename: this.videoData.file.upload.filename,
        content_type: this.videoData.file.type,
        video_type: "video",
        date_of_measure: moment
          .utc(this.videoData.date_of_measure)
          .format("YYYY-MM-DD")
      };

      try {
        let response = await commonServices.getSignedUrl(video_data);

        this.measureData = { ...this.measureData, ...response.data };

        this.videoData.file.url = this.measureData.url;

        this.$refs.videoForm.enqueueFile(this.videoData.file);
      } catch (e) {
        console.error("error:", e);
        this.$formHelpers.showError(e.response.request.responseText);
      }
    },
    async onVideoUploadCompleted(e) {
      if (e.status == "canceled") return;

      if (e.status !== "success") {
        this.$formHelpers.showError("Something went wrong. Please try again");
        //this.$refs.videoForm.removeAllFiles();
        return;
      }

      try {
        let measure = this.measurementsData.find(
          m => m.date_of_measure === this.measureData.date_of_measure
        );

        let method = "createMeasure";

        if (measure) method = "updateMeasure";

        this.measureData.id = measure ? measure.id : null;

        let response = await measureServices[method](this.measureData);

        //this.$formHelpers.showInfo(response.statusText);
        this.$formHelpers.showInfo("Successfully Added");

        this.isSaveDisabled = true;

        this.fetchMeasurementsData();
      } catch (e) {
        console.error("error:", e);
        this.$formHelpers.showError(e.response.request.responseText);
      }
    },

    onModalCancel() {
      this.hide();
    },
    resetForm() {
      if (this.$refs.videoForm) this.$refs.videoForm.removeAllFiles();

      this.isSaveDisabled = false;

      this.videoData = {
        file: "",
        date_of_measure: "",
        // video_qc: ""
      };
      this.measureData = {};
    }
  },
  watch: {
    "videoData.date_of_measure"(newValue, oldValue) {
      if (newValue !== oldValue) {
        this.resetForm();

        // this.videoData.date_of_measure = moment(newValue).format("YYYY-MM-DD");
        this.videoData.date_of_measure = newValue;
      }
    }
  }
};
</script>
