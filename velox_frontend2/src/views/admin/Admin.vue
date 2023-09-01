<template>
  <div>
    <b-row>
      <b-colxx xxs="12">
        <div class="separator mb-5"></div>
      </b-colxx>
    </b-row>
    <b-row>
      <b-colxx xxs="12">
        <b-card class="mb-4" title="Admin">
          <b-row>
              <b-col>
                  <span class="pt-5">
                    <b-form-group label="Starts Country" class="has-float-label">
                      <v-select v-model="filters.start_country" :options="controls.start_country.options"/>
                    </b-form-group>
                  </span>
              </b-col>
          </b-row>
          <b-row>
            <b-col>
              <UsersTable ref="usersTable" @updated="onUsersTableUpdate">
              </UsersTable>
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
import UsersTable from "./UsersTable";
import userServices from "@/services/user.service";
//import adminServices from "@/services/admin.service";

export default {
  props: {},
  components: {
    vSelect,
    UsersTable
  },

  data() {
    return {
      controls: {},
      controls: {
        start_country: {
          options: []
        }
      },
      filters: {
        start_country: "",
      },
    };
  },
  async mounted() {
    let fresult;
    // await this.fetchData();
    fresult = await userServices.fetchstartcountry();
    this.controls.start_country.options.push("All");
    fresult.data.results.forEach((value, index) => {
      this.controls.start_country.options.push(value['starts_country']);
    });
    
  },
  methods: {
    async fetchData() {
      let payload = {};
      if (this.filters.start_country && this.filters.start_country !== "All")
        payload.starts_country = this.filters.start_country;
        this.$refs.usersTable.fetchData(payload);
    },
    onUsersTableUpdate() {
      this.fetchData();
    }
  },
  watch: {
    "filters.start_country"(newVal, oldVal) {
      this.fetchData();
    },
  }
};
</script>

<style scoped>
.icon {
  font-size: 28px;
}
</style>
