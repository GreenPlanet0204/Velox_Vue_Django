<template>
  <b-modal id="modalId" ref="modalRef" size="lg">
    <div slot="modal-title">
      <span class="icon success">
        <i class="iconsminds-add-file"></i>
      </span>
      <span>Country Weight details</span>
    </div>
      <b-form class="av-tooltip tooltip-left-bottom mb-5">
        <b-row>
          <b-col>
            <b-form-group label="Start Country" class="tooltip-left-bottom">
              <b-form-input type="text" v-model.trim="$v.form1.starts_country.$model" required readonly/>
            </b-form-group>
          </b-col>
          <b-col>
            <b-form-group label="Country">
              <v-select v-model.trim="form1.country" :options="controls.country.options"/>
            </b-form-group>
          </b-col>
          <b-col>
            <b-form-group label="Country Weight">
              <!-- <v-select v-model="selected" :options="['0.0','0.1','0.2','0.3','0.4','0.5','0.6','0.7','0.8','0.9','1.0']"/> -->
              <b-form-input type="number" v-model.trim="selected" min="0.0" max="1.0" step="0.1"/>
              
            </b-form-group>
          </b-col>
        </b-row>
      </b-form>

    <template slot="modal-footer">
      <b-button variant="primary" class="mr-1" @click="onModalUpdate()"
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
import userServices from "@/services/user.service";

import { validationMixin } from "vuelidate";
const { required, maxLength, minLength } = require("vuelidate/lib/validators");

export default {
  components: {
    vSelect,
    Datepicker
  },
  data() {
    return {
      form1 :{
        starts_country:"",
        country:"",
        country_weight:"",
      },
      selected:"1.0",
      controls: {
        country: {
          options: []
        }
      },
    };
  },
  mixins: [validationMixin],
  validations: {
    form1: {
      starts_country: {
        required
      }
    }
  },
  async mounted() {
     this.controls.country.options = await dictionaryServices.fetchCountries();
     this.controls.country.options.shift();
  },
  methods: {
    show(payload) {
      this.form1 = Object.assign({}, payload);

      this.$refs.modalRef.show();
    },
    hide() {
      this.$refs.modalRef.hide();
    },
    async onModalUpdate() {
   
        this.$v.form1.$touch();

        if (this.$v.form1.$anyError) {
        if (!this.$v.form1.starts_country.required)
            this.$formHelpers.showError("Start Country is required");

        return;
        }
        this.form1.country_weight = this.selected;
        try {
            let res, message;
            if (this.form1.starts_country) {
                res = await userServices.updateCountry(this.form1);
                message = "Country Successfully Updated";
            }

            this.$formHelpers.showInfo(message);

            //  this.hide();
            this.$emit("updated", this.form);
        } catch (e) {
            console.error(e);
            this.$formHelpers.showError(e.response.request.responseText);
        }
    },
    onModalCancel() {
      this.hide();
    },
    onDOBSelect(value) {},
  },
  watch: {}
};
</script>
