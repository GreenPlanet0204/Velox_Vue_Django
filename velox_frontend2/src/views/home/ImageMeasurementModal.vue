<template>
  <b-modal id="modalId" ref="modalRef" size="xl">
    <div slot="modal-title" style="width: 40em">
      <b-row>
        <b-col cols="3">Search for Horse</b-col>
      </b-row>
    </div>

    <b-form class="av-tooltip tooltip-left-bottom">
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

      <AddImageMeasurementForm
        ref="imageForm"
        v-if="selectedHorse.id"
        v-model="imageData"
        :measurements="measurementsData"
        @date-changed="onMeasureDateChange"
      ></AddImageMeasurementForm>
      <!-- @completed="onImageUploadCompleted"-->

      <b-row>
        <b-col>
          <Pegasus
            v-if="isPegasusVisible"
            ref="pegasus"
            :morph-data="imageMeasureData.morph_data"
            @image-selected="onImageSelected"
            @morph="onRunMorph"
            @reset="onPegasusReset"
            @save="onPegasusSave"
          />
        </b-col>
      </b-row>
    </b-form>

    <template slot="modal-footer">
      <!--   <b-button
        variant="primary"
        class="mr-1"
        :disabled="isSaveDisabled"
        @click="onModalSave"
        >Save</b-button
      >-->
      <b-button variant="secondary" @click="onModalCancel">Cancel</b-button>
    </template>
  </b-modal>
</template>

<script>
import api from "@/services/axios";
import axios from "axios";
import moment from "moment";
import { VueAutosuggest } from "vue-autosuggest";
import horseServices from "@/services/horse.service";
import measureServices from "@/services/measure.service";
import commonServices from "@/services/common.service";
import AddImageMeasurementForm from "./AddImageMeasurementForm";
import Pegasus from "@/components/Pegasus/Pegasus";
import { setCurrentUser, getCurrentUser } from "@/utils";

export default {
  components: {
    VueAutosuggest,
    AddImageMeasurementForm,
    Pegasus
  },
  data() {
    return {
      isPegasusVisible: false,
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
      imageData: {
        file: { name: "", type: "", url: "" }
      },
      measureData: {},
      imageMeasureData: {
        morph_data: {}
      },
      // morphData: {},
      selectedImageFile: null
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

      this.imageData = this.$formHelpers.resetObject(this.imageData);

      this.fetchMeasurementsData();
    },
    async fetchMeasurementsData() {
      this.measurementsData = await measureServices.fetchHorseImageMeasures(
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
      this.imageData = this.$formHelpers.resetObject(this.imageData);

      this.isPegasusVisible = false;
      this.$refs.modalRef.show();
    },
    hide() {
      this.$refs.modalRef.hide();
    },
    validate() {
      let errors = [];

      if (!this.selectedHorse.id) errors.push("Please select a horse");

      if (!this.imageData.date_of_measure)
        errors.push("Please select date of measurement");

      //if (!this.imageData.file) errors.push("Please select image file");
      if (!this.imageData.file || !this.imageData.file.name)
        errors.push("Please select image file");

      if (errors.length) {
        this.$formHelpers.showError(errors[0]);
        return false;
      }

      return true;
    },
    async onPegasusSave(payload) {
      try {
        //this.measureData.id = measure ? measure.id : null;

        let response = await measureServices.updateImageMeasure({
          id: this.imageMeasureData.id,
          calculated_data: payload,
          date_of_measure: this.imageData.date_of_measure
        });

        this.$formHelpers.showInfo("Successfully Added");
      } catch (e) {
        console.error("error:", e);
        this.$formHelpers.showError(e.response.request.responseText);
      }
    },

    onImageSelected(e) {
      this.selectedImageFile = e;

      this.imageData.file = { name: "", type: "", url: "" };

      this.imageData.file.name = e.name;
      this.imageData.file.type = e.type;
    },

    onModalCancel() {
      this.hide();
    },
    resetForm() {
      if (this.$refs.imageForm) this.$refs.imageForm.removeAllFiles();

      this.isSaveDisabled = false;

      this.imageData = {
        file: { name: "", type: "", url: "" },
        date_of_measure: ""
      };
      this.measureData = {};
    },
    async addMeasureGetMorph() {
      try {
        if (!this.validate()) {
          return;
        }

        const image_data = {
          filename: this.selectedImageFile.name,
          content_type: this.selectedImageFile.type,
          file_type: "image_measurement",
          date_of_measure: moment
            .utc(this.imageData.date_of_measure)
            .format("YYYY-MM-DD")
        };
        console.log("image_data:", image_data);
        let response = await commonServices.getSignedUrl(image_data);

        let config = {
          headers: {
            "content-type": this.selectedImageFile.type
          }
        };
        let resp = await axios.put(
          response.data.url,
          this.selectedImageFile,
          config
        );

        this.measureData = {
          date_of_measure: moment
            .utc(this.imageData.date_of_measure)
            .format("YYYY-MM-DD"),
          horse: this.selectedHorse.id
        };
        this.measureData.image = {};
        this.measureData.image.path = response.data.gcs_path;
        this.measureData.image.bucket = response.data.gcs_bucket;
        this.measureData.image.filename = response.data.gcs_filename;
        this.measureData.image.url = response.data.url;

        this.imageData.file.url = response.data.url;

        let measure = this.measurementsData.find(
          m => m.date_of_measure === this.measureData.date_of_measure
        );

        let method = "createImageMeasure";

        //  if (measure) method = "updateImageMeasure";

        this.measureData.id = measure ? measure.id : null;

        response = await measureServices[method](this.measureData);

        this.imageMeasureData = response.data;

        //this.morphData = response.data.morph_data;

        //console.log("this.morphData:", this.morphData);

        // this.isSaveDisabled = true;

        this.fetchMeasurementsData();
      } catch (e) {
        console.error("error:", e);
        // this.$formHelpers.showError(e.response.request.responseText);
      }
    },
    onRunMorph() {
      this.addMeasureGetMorph();
    },
    onPegasusReset() {
      //this.morphData = {};
      this.imageMeasureData.morph_data = {};
    },
    onMeasureDateChange(payload) {
      this.isPegasusVisible = payload;
    },
    onPegasusDone(payload) {}
  },
  watch: {
    "imageData.date_of_measure"(newValue, oldValue) {
      if (newValue !== oldValue) {
        this.resetForm();

        // this.imageData.date_of_measure = moment(newValue).format("YYYY-MM-DD");
        this.imageData.date_of_measure = newValue;
      }
    }
  }
};
</script>
