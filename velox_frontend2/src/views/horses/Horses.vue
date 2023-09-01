<template>
  <div>
    <b-row>
      <b-colxx xxs="12">
        <div class="separator mb-5"></div>
      </b-colxx>
    </b-row>
    <b-row>
      <b-colxx xxs="12">
        <b-card class="mb-4" title="Horse Data">
          <b-row>
            <b-col>
              <span class="icon success " style="float:left">
                <i class="iconsminds-globe-2"></i>
              </span>
              <span class="pt-5">
                <b-form-group label="Country" class="has-float-label">
                  <v-select
                    v-model="filters.country"
                    :options="controls.country.options"
                  />
                </b-form-group>
              </span>
            </b-col>
            <b-col>
              <span class="icon success" style="float:left">
                <i class="iconsminds-finger-print"></i>
              </span>
              <span class="pt-5">
                <b-form-group label="Status" class="has-float-label">
                  <v-select
                    v-model="filters.status"
                    :options="controls.status.options"
                  />
                </b-form-group>
              </span>
            </b-col>
          </b-row>

          <b-row>
            <b-col>
              <HorsesTable ref="horsesTable" @updated="onHorsesTableUpdate">
              </HorsesTable>
            </b-col>
          </b-row>
        </b-card>
      </b-colxx>
    </b-row>
  </div>
</template>

<script>
import vSelect from "vue-select";
import "vue-select/dist/vue-select.css";
import dictionaryServices from "@/services/dictionary.service.js";
import HorsesTable from "@/views/horses/HorsesTable";
import horseServices from "@/services/horse.service";

export default {
  props: {},
  components: {
    vSelect,
    HorsesTable
  },

  data() {
    return {
      localData: [],
      filteredData: [],
      filters: {
        country: "",
        status: ""
      },

      controls: {
        country: {
          options: []
        },
        status: {
          options: []
        }
      }
    };
  },
  async mounted() {
    this.controls.country.options = await dictionaryServices.fetchCountries();

    this.controls.status.options = await dictionaryServices.fetchHorseStatuses();

    //  this.fetchData();
  },
  methods: {
    async fetchData() {
      let payload = {};
      if (this.filters.country && this.filters.country !== "All")
        payload.country = this.filters.country;
      if (this.filters.status) payload.status = this.filters.status;

      this.$refs.horsesTable.fetchData(payload);
    },
    onHorsesTableUpdate() {
      this.fetchData();
    }
  },
  watch: {
    "filters.country"(newVal, oldVal) {
      this.fetchData();
    },
    "filters.status"(newVal, oldVal) {
      this.fetchData();
    }
  }
};
</script>

<style scoped>
.icon {
  font-size: 28px;
}
</style>
