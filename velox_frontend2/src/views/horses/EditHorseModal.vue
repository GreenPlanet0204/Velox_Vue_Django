<template>
  <b-modal id="modalId" ref="modalRef" size="lg">
    <div slot="modal-title">
      <span class="icon success">
        <i class="iconsminds-add-file"></i>
      </span>
      <span>Horse details</span>
    </div>

    <b-form class="av-tooltip tooltip-left-bottom mb-5">
      <b-row>
        <b-col>
          <b-form-group label="Horse Name" class="tooltip-left-bottom">
            <b-form-input type="text" v-model.trim="$v.form.name.$model" />
          </b-form-group>
        </b-col>
        <b-col>
          <b-form-group label="Horse Type">
            <v-select
              v-model.trim="$v.form.type.$model"
              :options="typeOptions"
            />
          </b-form-group>
        </b-col>
        <b-col>
          <b-form-group label="Sex">
            <v-select v-model="form.sex" :options="sexOptions" />
          </b-form-group>
        </b-col>
        <b-col>
          <b-form-group label="Date of Birth">
            <datepicker
              :bootstrap-styling="true"
              placeholder="Date of Birth"
              v-model="form.date_of_birth"
              format="yyyy-MM-dd"
              :typeable="true"
              :use-utc="true"
            ></datepicker>
          </b-form-group>
        </b-col>
      </b-row>
      <b-row>
        <b-col>
          <b-form-group label="Sire" class="tooltip-left-bottom">
            <b-form-input type="text" v-model.trim="form.sire" />
          </b-form-group>
        </b-col>
        <b-col>
          <b-form-group label="Dam" class="tooltip-left-bottom">
            <b-form-input type="text" v-model.trim="form.dam" />
          </b-form-group>
        </b-col>
        <b-col>
          <b-form-group label="Broodmare Sire" class="tooltip-left-bottom">
            <b-form-input
              type="text"
              v-model.trim="form.broodmare_sire"
            />
          </b-form-group>
        </b-col>
        <b-col>
          <b-form-group label="Country Code" class="tooltip-left-bottom">
            <b-form-input
              type="text"
              v-model.trim="form.country_code"
            />
          </b-form-group>
        </b-col>
      </b-row>
      <b-row>
        <b-col>
          <b-form-group label="Starts">
            <b-input
              type="number"
              v-model="form.starts"
              :formatter="startsFormat"
            />
          </b-form-group>
        </b-col>
        <b-col>
          <b-form-group label="Starts Country" class="tooltip-left-bottom">
            <b-form-input
              type="text"
              v-model.trim="form.starts_country"
            />
          </b-form-group>
        </b-col>
        <b-col>
          <b-form-group label="Country">
            <v-select v-model="form.country" :options="countryOptions" />
          </b-form-group>
        </b-col>
        <b-col>
          <b-form-group label="Date Last Start">
            <datepicker
              :bootstrap-styling="true"
              placeholder="Date Last Start"
              v-model="form.date_last_start"
              format="yyyy-MM-dd"
              :typeable="true"
              :use-utc="true"
            ></datepicker>
          </b-form-group>
        </b-col>
      </b-row>
      <b-row>
        <b-col>
          <b-form-group label="Avg Distance Raced" class="tooltip-left-bottom">
            <b-form-input
              type="number"
              v-model.trim="form.avg_distance_raced"
            />
          </b-form-group>
        </b-col>
        <b-col>
          <b-form-group label="Optimal Distance">
            <v-select
              v-model="form.optimal_distance"
              :options="optimalDistanceOptions"
            />
          </b-form-group>
        </b-col>
        <b-col>
          <b-form-group label="Hurdle" class="tooltip-left-bottom">
            <b-form-input type="text" v-model.trim="form.hurdle" />
          </b-form-group>
        </b-col>
        <b-col>
          <b-form-group label="Status">
            <v-select v-model="form.status" :options="statusOptions" />
          </b-form-group>
        </b-col>
      </b-row>
      <b-row>
        <b-col>
          <b-form-group label="CPI Rating" class="tooltip-left-bottom">
            <b-form-input
              type="number"
              v-model.trim="form.cpi_rating"
            />
          </b-form-group>
        </b-col>
        <b-col>
          <b-form-group label="Race Rating">
            <b-input
              v-model="form.race_rating"
              type="number"
              :formatter="raceRatingFormat"
            />
          </b-form-group>
        </b-col>
        <b-col>
          <b-form-group label="TFReg">
            <b-input v-model="form.tf_reg" />
          </b-form-group>
        </b-col>
        <b-col> </b-col>
      </b-row>
    </b-form>

    <template slot="modal-footer">
      <b-button variant="primary" class="mr-1" @click="onModalSave"
        >Save</b-button
      >
      <b-button variant="secondary" @click="onModalCancel">Cancel</b-button>
    </template>
  </b-modal>
</template>

<script>
import moment from "moment";
import vSelect from "vue-select";
import "vue-select/dist/vue-select.css";
import Datepicker from "vuejs-datepicker";

import dictionaryServices from "@/services/dictionary.service";
import horseServices from "@/services/horse.service";

import { validationMixin } from "vuelidate";
const { required, maxLength, minLength } = require("vuelidate/lib/validators");

export default {
  components: {
    vSelect,
    Datepicker,
  },
  data() {
    return {
      form: {
        name: "",
        type: "",
        sex: "",
        date_of_birth: "",
        starts: "",
        date_last_start: "",
        tf_reg: "",
        race_rating: "",
        status: "",
        country: "",
        sire: "",
        dam: "",
        broodmare_sire: "",
        country_code: "",
        starts_country: "",
        avg_distance_raced: "",
        hurdle: "",
        cpi_rating: "",
      },
      typeOptions: [],
      sexOptions: [],
      statusOptions: [],
      countryOptions: [],
      optimalDistanceOptions: [],
    };
  },
  mixins: [validationMixin],
  validations: {
    form: {
      name: {
        required,
        minLength: minLength(2),
        maxLength: maxLength(35),
      },
      type: {
        required,
      },
      sex: {
        required,
      },
      date_of_birth: {
        required,
      },
      // sire: {
      //   required,
      // },
      // dam: {
      //   required,
      // },
      // broodmare_sire: {
      //   required,
      // },
      // country_code: {
      //   required,
      // },
      // starts_country: {
      //   required,
      // },
      // avg_distance_raced: {
      //   required,
      // },
      // hurdle: {
      //   required,
      // },
      // cpi_rating: {
      //   required,
      // },
    },
  },
  async mounted() {
    this.typeOptions = await dictionaryServices.fetchHorseTypeOptions();
    this.sexOptions = await dictionaryServices.fetchHorseSexOptions();
    this.countryOptions = await dictionaryServices.fetchCountries();
    this.statusOptions = await dictionaryServices.fetchHorseStatuses();
    this.optimalDistanceOptions =
      await dictionaryServices.fetchOptimalDistanceOptions();
  },
  methods: {
    startsFormat(e) {
      return parseInt(String(e).substring(0, 3)) || 0;
    },
    raceRatingFormat(e) {
      return parseInt(String(e).substring(0, 3)) || 0;
    },
    show(payload) {
      this.form = Object.assign({}, payload);

      this.form.starts = parseInt(this.form.starts) || 0;
      this.form.race_rating = parseInt(this.form.race_rating) || 0;

      this.$refs.modalRef.show();
    },
    hide() {
      this.$refs.modalRef.hide();
    },
    async onModalSave() {
      this.$v.form.$touch();

      if (this.$v.form.$anyError) {
        this.$formHelpers.showError(
          "Please complete Name, Type, Sex and Date of Birth to save a record"
        );
        return;
      }

      if (!this.$v.form.$anyError) {
        try {
          let res = await horseServices.updateHorse(this.form);

          //this.$formHelpers.showInfo(res.statusText);
          this.$formHelpers.showInfo("Successfully Updated");

          this.hide();

          this.$emit("updated", this.form);
        } catch (e) {
          console.error(e.response);
          this.$formHelpers.showError(e.response.request.responseText);
        }
      }
    },

    onModalCancel() {
      this.hide();
    },
    onDOBSelect(value) {},
  },
  watch: {
    "form.date_of_birth"(newValue) {
      //this.form.date_of_birth = moment(newValue).format("YYYY-MM-DD");
    },
  },
};
</script>
