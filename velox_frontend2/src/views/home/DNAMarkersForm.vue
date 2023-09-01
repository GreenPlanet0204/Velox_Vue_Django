<template>
  <b-form class="av-tooltip tooltip-left-bottom mb-5">
    <div>
      <h5 class="mb-4 card-title">
        <span class="icon success">
          <i class="iconsminds-dna-2"></i>
        </span>
        <span>DNA Markers</span>
      </h5>
    </div>
    <b-row>
      <b-col
        ><b-form-group label="Distance 1" class="has-float-label">
          <v-select
            v-model="value.distance1"
            :options="controls.distance1.options"
          />
        </b-form-group>
      </b-col>
      <b-col>
        <b-form-group label="Distance 2" class="has-float-label">
          <v-select
            v-model="value.distance2"
            :options="controls.distance2.options"
          />
        </b-form-group>
      </b-col>
      <b-col>
        <b-form-group label="Size" class="has-float-label">
          <v-select v-model="value.size1" :options="controls.size1.options" />
        </b-form-group>
      </b-col>
    </b-row>
    <b-row>
      <b-col>
        <b-form-group label="Class 1" class="has-float-label">
          <v-select v-model="value.class1" :options="controls.class1.options" />
        </b-form-group>
      </b-col>
      <b-col>
        <b-form-group label="Class 2" class="has-float-label">
          <v-select v-model="value.class2" :options="controls.class2.options" />
        </b-form-group>
      </b-col>
      <b-col>
        <b-form-group label="Class 3" class="has-float-label">
          <v-select v-model="value.class3" :options="controls.class3.options" />
        </b-form-group>
      </b-col>
    </b-row>
  </b-form>
</template>

<script>
import vSelect from "vue-select";
import "vue-select/dist/vue-select.css";
import dictionaryServices from "@/services/dictionary.service.js";

export default {
  props: {
    value: {
      type: Object,
      default: () => {}
    }
  },
  components: {
    vSelect
  },

  data() {
    return {
      controls: {
        distance1: {
          options: []
        },
        distance2: {
          options: []
        },
        size1: {
          options: []
        },
        class1: {
          options: []
        },
        class2: {
          options: []
        },
        class3: {
          options: []
        }
      }
    };
  },
  async mounted() {
    let res = await dictionaryServices.fetchDNAMarkersOptions();

    this.controls.distance1.options = res.distance1;
    this.controls.distance2.options = res.distance2;
    this.controls.size1.options = res.size;
    this.controls.class1.options = res.class1;
    this.controls.class2.options = res.class2;
    this.controls.class3.options = res.class3;
  },
  methods: {}
};
</script>

<style></style>
