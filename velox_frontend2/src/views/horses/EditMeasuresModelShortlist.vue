<template>
  <b-modal id="modalId" ref="modalRef" size="xl">
    <div slot="modal-title">
      <span class="icon success">
        <i class="iconsminds-add-file"></i>
      </span>
      <span
        >Measurement View
        <b>{{ horse_name }} - {{ yob }} - by {{ sire }}</b></span
      >
    </div>

    <b-tabs content-class="mt-3">
      <b-tab title="DNA" @click="tab_type('DNA')" v-model="tabtype" active>
        <DNAMarkersForm v-model="form"></DNAMarkersForm>
      </b-tab>
      <b-tab title="Conformation" @click="tab_type('image')">
        <measures-table
          :data="imageMeasures"
          mode="image"
          @updated="onMeasuresTableUpdate"
        ></measures-table>
      </b-tab>
      <b-tab title="Cardio" @click="tab_type('cardio')">
        <measures-table
          :data="cardioMeasures"
          mode="cardio"
          @updated="onMeasuresTableUpdate"
        ></measures-table>
      </b-tab>
      <b-tab title="Biomechanics" @click="tab_type('bio')">
        <measures-table
          :data="bioMeasures"
          mode="bio"
          @updated="onMeasuresTableUpdate"
        ></measures-table>
      </b-tab>
    </b-tabs>

    <template slot="modal-footer">
      <b-button
        variant="primary"
        class="mr-1"
        @click="onModalSave"
        v-if="tabtype == 'DNA'"
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
import DNAMarkersForm from "@/views/home/DNAMarkersForm";
import MeasuresTable from "@/views/horses/MeasuresTable";

import dictionaryServices from "@/services/dictionary.service";
import horseServices from "@/services/horse.service";

import { validationMixin } from "vuelidate";

const { required, maxLength, minLength } = require("vuelidate/lib/validators");

export default {
  components: {
    vSelect,
    Datepicker,
    DNAMarkersForm,
    MeasuresTable
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

        distance1: "",
        distance2: "",
        size1: "",
        class1: "",
        class2: "",
        class3: ""
      },
      typeOptions: [],
      sexOptions: [],
      statusOptions: [],
      countryOptions: [],
      imageMeasures: [],
      cardioMeasures: [],
      bioMeasures: [],
      tabtype: "",
      horse_name: "",
      sire: "",
      yob: ""
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
      }
    }
  },
  async mounted() {
    /*
      this.typeOptions = await dictionaryServices.fetchHorseTypeOptions();
      this.sexOptions = await dictionaryServices.fetchHorseSexOptions();
      this.countryOptions = await dictionaryServices.fetchCountries();
      this.statusOptions = await dictionaryServices.fetchHorseStatuses();
      */
    this.tabtype = "DNA";
  },
  methods: {
    show(payload) {
      this.horse_name = payload.name;
      this.sire = payload.sire;
      let yob = new Date(payload.date_of_birth);
      this.yob = yob.getFullYear();
      this.updateData(payload);

      this.$refs.modalRef.show();
      this.tab_type("DNA");
    },
    hide() {
      this.$refs.modalRef.hide();
    },
    async updateData(payload) {
      let response = await horseServices.fetchHorse(payload.horse_id);
      this.form = response.data;

      //vuejs-datepicker client timezone fix
      /*
        for (let measure of this.form.measures) {
          measure.date_of_measure = moment
            .utc(measure.date_of_measure, "YYYY-MM-DD")
            .format("DD MMM YYYY");
        }*/
      if (this.form.measures) {
        this.cardioMeasures = this.form.measures.filter(
          m => m.cardio_video_url
        );
        this.bioMeasures = this.form.measures.filter(m => m.video_url);
      }

      if (this.form.image_measurements) {
        this.imageMeasures = this.form.image_measurements.filter(m => m.image);
      }
    },
    async onMeasuresTableUpdate() {
      try {
        let response = await horseServices.fetchHorse(this.form.id);

        this.form = response.data;

        this.updateData(this.form);

        console.log("EditMeasuresModal.onMeasuresTableUpdate.form", this.form);

        this.$emit("updated", this.form);
      } catch (e) {
        console.error(e.response);
        this.$formHelpers.showError(e.response.request.responseText);
      }
    },
    validate() {
      let result =
        this.form.distance1 &&
        this.form.distance2 &&
        this.form.size1 &&
        this.form.class1 &&
        this.form.class2 &&
        this.form.class3;

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
      } = this.form;

      try {
        let res = await horseServices.updateHorse({
          id,
          distance1,
          distance2,
          size1,
          class1,
          class2,
          class3
        });

        this.$formHelpers.showInfo("Successfully Updated");

        // this.hide();

        this.$emit("updated", this.form);
      } catch (e) {
        console.error(e.response);
        this.$formHelpers.showError(e.response.request.responseText);
      }
    },

    onModalCancel() {
      this.hide();
    },
    onDOBSelect(value) {},
    tab_type(type) {
      this.tabtype = type;
    }
  },
  watch: {
    "form.date_of_birth"(newValue) {
      // this.form.date_of_birth = moment(newValue).format("YYYY-MM-DD");
    }
  }
};
</script>
