<template>
  <b-modal id="modalId" ref="modalRef" size="lg">
    <div slot="modal-title">
      <span class="icon success">
        <i class="iconsminds-add-file"></i>
      </span>
      <span>Horse details</span>
    </div>

    <b-form class="av-tooltip tooltip-left-bottom mb-5">
      <b-form-group label="Horse Name" class="tooltip-left-bottom">
        <b-form-input type="text" v-model.trim="$v.form.name.$model" />
      </b-form-group>
      <b-form-group label="Country Code" class="tooltip-left-bottom">
        <b-form-input type="text" v-model.trim="$v.form.country_code.$model" />
      </b-form-group>
      <b-form-group label="Horse Type">
        <v-select
          v-model.trim="$v.form.type.$model"
          :options="horseTypeOptions"
        />
      </b-form-group>
      <b-form-group label="Sex">
        <v-select v-model="form.sex" :options="horseSexOptions" />
      </b-form-group>
      <b-form-group label="Date of Birth">
        <datepicker
          :bootstrap-styling="true"
          placeholder="Date of Birth"
          v-model="form.date_of_birth"
          format="yyyy-MM-dd"
          @selected="onDOBSelect"
          :typeable="true"
          :use-utc="true"
        ></datepicker>
      </b-form-group>
      <b-form-group label="Sire" class="tooltip-left-bottom">
        <b-form-input type="text" v-model.trim="$v.form.sire.$model" />
      </b-form-group>
      <b-form-group label="Dam" class="tooltip-left-bottom">
        <b-form-input type="text" v-model.trim="$v.form.dam.$model" />
      </b-form-group>
      <b-form-group label="Broodmare Sire" class="tooltip-left-bottom">
        <b-form-input
          type="text"
          v-model.trim="$v.form.broodmare_sire.$model"
        />
      </b-form-group>
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
    Datepicker
  },
  data() {
    return {
      form: {
        name: "",
        type: "",
        sex: "",
        date_of_birth: "",
        country_code: "",
        sire: "",
        dam: "",
        broodmare_sire: ""
      },
      horseTypeOptions: [],
      horseSexOptions: []
    };
  },
  mixins: [validationMixin],
  validations: {
    form: {
      name: {
        required,
        minLength: minLength(2),
        maxLength: maxLength(25)
      },
      type: {
        required
      },
      sex: {
        required
      },
      date_of_birth: {
        required
      },
      country_code: {
        required,
        minLength: minLength(1),
        maxLength: maxLength(4)
      },
      sire: {
        required,
        minLength: minLength(1),
        maxLength: maxLength(18)
      },
      dam: {
        required,
        minLength: minLength(1),
        maxLength: maxLength(18)
      },
      broodmare_sire: {
        required,
        minLength: minLength(1),
        maxLength: maxLength(18)
      }
    }
  },
  async mounted() {
    this.horseTypeOptions = await dictionaryServices.fetchHorseTypeOptions();
    this.horseSexOptions = await dictionaryServices.fetchHorseSexOptions();
  },
  methods: {
    show() {
      this.form = this.$formHelpers.resetObject(this.form);

      this.$refs.modalRef.show();
    },
    hide() {
      this.$refs.modalRef.hide();
    },
    async onModalSave() {
      this.$v.form.$touch();

      if (this.$v.form.$anyError) {
        this.$formHelpers.showError(
          "All fields must be complete to add a record"
        );
        return;
      }

      if (!this.$v.form.$anyError) {
        try {
          let res = await horseServices.addHorse(this.form);

          //this.$formHelpers.showInfo(res.statusText);
          this.$formHelpers.showInfo("Successfully Added");

          this.hide();
        } catch (e) {
          console.error(e.response);
          this.$formHelpers.showError(e.response.request.responseText);
        }
      }
    },

    onModalCancel() {
      this.hide();
    },
    onDOBSelect(value) {}
  },
  watch: {
    "form.date_of_birth"(newValue) {
      //this.form.date_of_birth = moment(newValue).format("YYYY-MM-DD");
    }
  }
};
</script>
