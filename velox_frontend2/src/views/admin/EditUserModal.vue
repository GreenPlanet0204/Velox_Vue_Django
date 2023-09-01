<template>
  <b-modal id="modalId" ref="modalRef" size="lg">
    <div slot="modal-title">
      <span class="icon success">
        <i class="iconsminds-add-file"></i>
      </span>
      <span>User details</span>
    </div>
  <b-tabs content-class="mt-3">
    <b-tab title="Admin" id="admin" @click="tab_type('admin')" active>
      <b-form class="av-tooltip tooltip-left-bottom mb-5">
        <b-row>
          <b-col>
            <b-form-group label="Email" class="tooltip-left-bottom">
              <b-form-input type="text" v-model.trim="$v.form.email.$model" />
            </b-form-group>
          </b-col>
          <b-col>
            <b-form-group label="Password">
              <b-form-input type="password" v-model.trim="form.password" />
            </b-form-group>
          </b-col>
          <b-col>
            <b-form-group label="First Name">
              <b-form-input type="text" v-model.trim="form.first_name" />
            </b-form-group>
          </b-col>
          <b-col>
            <b-form-group label="Last Name">
              <b-form-input type="text" v-model.trim="form.last_name" />
            </b-form-group>
          </b-col>
        </b-row>
      </b-form>
    </b-tab>
    <b-tab title="Country Weights" id="country" @click="tab_type('country')" v-if="!this.form.id">
      <b-form class="av-tooltip tooltip-left-bottom mb-5">
        <b-row>
          <b-col>
            <b-form-group label="Start Country" class="tooltip-left-bottom">
              <b-form-input type="text" v-model.trim="$v.form1.starts_country.$model" required/>
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
          <!-- <b-col>
            <b-form-group label="Country Full Name" class="tooltip-left-bottom">
              <b-form-input type="text" v-model.trim="form.country_fullname"/>
            </b-form-group>
          </b-col> -->
        </b-row>
      </b-form>
    </b-tab>
  </b-tabs>

    <template slot="modal-footer">
      <b-button variant="primary" class="mr-1" @click="onModalSave()"
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
      form: {
        email: "",
        password: "",
        first_name: "",
        last_name: "",
      },
      form1 :{
        starts_country:"",
        country:"",
        country_weight:"",
        // country_fullname:"",
      },
      selected:"1.0",
      controls: {
        country: {
          options: []
        }
      },
      tabtype:''
    };
  },
  mixins: [validationMixin],
  validations: {
    form: {
      email: {
        required
      }
    },
    form1: {
      starts_country: {
        required
      }
    }
  },
  async mounted() {
     this.controls.country.options = await dictionaryServices.fetchCountries();
     this.controls.country.options.shift();
     this.tabtype='admin'
  },
  methods: {
    show(payload) {
      this.form = Object.assign({}, payload);

      this.$refs.modalRef.show();
    },
    hide() {
      this.$refs.modalRef.hide();
    },
    async onModalSave() {
      if(this.tabtype=='admin')
      {
          this.$v.form.$touch();
          console.log("this.$v.form", this.form, this.$v.form);

          if (this.$v.form.$anyError) {
            if (!this.$v.form.email.required)
              this.$formHelpers.showError("Email is required");

            return;
          }
        
          try {
            let res, message;
            if (this.form.id) {
              res = await userServices.updateUser(this.form);
              console.log("onModalSave.updateUser", res);
              message = "Successfully Updated";
            } else {
              res = await userServices.addUser(this.form);
              console.log("onModalSave.addUser", res);
              message = "Successfully Created";
            }

            this.$formHelpers.showInfo(message);

            //  this.hide();
            this.$emit("updated", this.form);
          } catch (e) {
            console.error(e);
            this.$formHelpers.showError(e.response.request.responseText);
          }
      }
      else
      {
          this.$v.form1.$touch();

          if (this.$v.form1.$anyError) {
            if (!this.$v.form1.starts_country.required)
              this.$formHelpers.showError("Start Country is required");

            return;
          }
          this.form1.country_weight = this.selected;
            try {
              let res, message;
              res = await userServices.addCountry(this.form1);
              message = "Country Successfully Created";

              this.$formHelpers.showInfo(message);

              //  this.hide();
              this.$emit("updated", this.form);
            } catch (e) {
              console.error(e);
              this.$formHelpers.showError(e.response.request.responseText);
            }
      }
    },
    onModalCancel() {
      this.hide();
    },
    onDOBSelect(value) {},
    tab_type(type)
    {
        this.tabtype=type
    }
  },
  watch: {}
};
</script>
