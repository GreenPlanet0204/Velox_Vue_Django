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

      <DNAMarkersForm
        v-if="selectedHorse.id"
        v-model="selectedHorse"
      ></DNAMarkersForm>

      <b-row>
        <b-col> </b-col>
      </b-row>
    </b-form>

    <template slot="modal-footer">
      <b-button
        variant="primary"
        class="mr-1"
        @click="onModalSave"
        :disabled="isSaveDisabled"
        >Save</b-button
      >
      <b-button variant="secondary" @click="onModalCancel">Cancel</b-button>
    </template>
  </b-modal>
</template>

<script>
import { VueAutosuggest } from "vue-autosuggest";

import vSelect from "vue-select";
import "vue-select/dist/vue-select.css";
import Datepicker from "vuejs-datepicker";

import dictionaryServices from "@/services/dictionary.service";
import horseServices from "@/services/horse.service";

import { validationMixin } from "vuelidate";
const { required, maxLength, minLength } = require("vuelidate/lib/validators");

import DNAMarkersForm from "./DNAMarkersForm";

export default {
  components: {
    VueAutosuggest,
    DNAMarkersForm
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
        date_of_birth: "",
        distance1: "",
        distance2: "",
        size1: "",
        class1: "",
        class2: "",
        class3: ""
      }
    };
  },
  async mounted() {},
  methods: {
    async onAutoSuggestInputChange(text, oldText) {
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

      if (this.selectedHorse.distance1) {
        this.$formHelpers.showInfo(
          "DNA Markers already exist and you can't add more."
        );
        this.isSaveDisabled = true;
      } else {
        this.isSaveDisabled = false;
      }
    },
    renderSuggestion(suggestion) {
      const character = suggestion.item;
      return character.name; /* renderSuggestion will override the default suggestion template slot. */
    },
    getSuggestionValue(suggestion) {
      return suggestion.item.name;
    },
    show() {
      this.selectedHorse = this.$formHelpers.resetObject(this.selectedHorse);

      this.$refs.modalRef.show();
    },
    hide() {
      this.$refs.modalRef.hide();
    },
    validate() {
      let result =
        this.selectedHorse.distance1 &&
        this.selectedHorse.distance2 &&
        this.selectedHorse.size1 &&
        this.selectedHorse.class1 &&
        this.selectedHorse.class2 &&
        this.selectedHorse.class3;

      return result;
    },
    async onModalSave() {
      if (!this.validate()) {
        this.$formHelpers.showError("All Markers must be complete to save");
        return;
      }

      const {
        id,
        distance1,
        distance2,
        size1,
        class1,
        class2,
        class3
      } = this.selectedHorse;

      try {
        let res = await horseServices.addDNAMarkers({
          id,
          distance1,
          distance2,
          size1,
          class1,
          class2,
          class3
        });

        this.$formHelpers.showInfo("Successfully Added");

        this.hide();
      } catch (e) {
        console.error(e);

        this.$formHelpers.showError(e);
      }
    },

    onModalCancel() {
      this.hide();
    }
  },
  watch: {}
};
</script>
