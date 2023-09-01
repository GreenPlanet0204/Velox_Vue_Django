<template>
  <div class="row">
    <div class="col-lg-12">
      <div class="chart1">
        <div class="row text-center">
          <div class="col-lg-3">
            <b-form-group label="Year" class="has-float-label">
              <v-select
                v-model="filters.year"
                :options="controls.year.options"
                @input="changeyear"
              />
            </b-form-group>
          </div>
          <div class="col-lg-6">
            <input
              type="radio"
              v-model="type"
              value="all_horses"
              @change="horse_type($event)"
              checked="type=='all_horses'"
            /><label for="All Horses">All Horses</label>
            <input
              type="radio"
              v-model="type"
              value="active_horses"
              @change="horse_type($event)"
            /><label for="Active horses">Active Horses</label>
            <h5>
              <b>{{ text }}</b>
            </h5>
          </div>
          <div class="col-lg-12">
            <datatable-heading
              title="Title"
              class="horse_data"
            ></datatable-heading>
            <b-row>
              <b-colxx xxs="12">
                <vuetable
                  ref="vuetable"
                  class="table-divided order-with-arrow"
                  :http-fetch="httpFetch"
                  :fields="fields"
                  :sort-order="sortOrder"
                  pagination-path=""
                  data-path="results"
                  @vuetable:loading="onLoading"
                  @vuetable:loaded="onLoaded"
                >
                  <template slot="name" slot-scope="props">
                    <div style="width: 150px">
                      <span> {{ props.rowData.name }}</span>
                      <div class="mt-1">
                        <span
                          class="icon success action-icon"
                          @click="onEditMeasuresClick(props.rowData)"
                        >
                          <i class="iconsminds-files action-icon"></i>
                        </span>
                      </div>
                    </div>
                  </template>
                </vuetable>
              </b-colxx>
            </b-row>
            <EditMeasuresModelShortlist
              ref="editMeasuresModal"
              @updated="onMeasureUpdate"
            ></EditMeasuresModelShortlist>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Vuetable from "vuetable-2/src/components/Vuetable";
import VuetablePaginationBootstrap from "@/components/Common/VuetablePaginationBootstrap";
import DatatableHeading from "@/containers/datatable/DatatableHeading";
import api from "@/services/axios";
import vSelect from "vue-select";
import "vue-select/dist/vue-select.css";
import EditMeasuresModelShortlist from "@/views/horses/EditMeasuresModelShortlist";
export default {
  name: "TheShortlist",
  props: {
    data: {
      type: Array,
      default: () => [],
    },
  },
  components: {
    vuetable: Vuetable,
    VuetablePaginationBootstrap,
    DatatableHeading,
    vSelect,
    EditMeasuresModelShortlist,
  },
  data() {
    return {
      controls: {},
      controls: {
        year: {
          options: [],
        },
      },
      filters: {
        year: "",
      },
      type: "",
      result2: "",
      fields: [
        {
          name: "__slot:name",
          title: "Name",
          sortField: "name",
        },
        {
          name: "sire",
          title: "Sire",
        },
        {
          name: "date_of_birth",
          title: "YOB",
        },
        {
          name: "active",
          title: "Active",
        },
        {
          name: "elite",
          title: "Elite",
        },
        {
          name: "prob_bio_model",
          sortField: "prob_bio_model",
          title: "Prob Bio",
        },
        {
          name: "prob_conform_model",
          sortField: "prob_conform_model",
          title: "Prob Conf",
        },
        {
          name: "cum_prob",
          sortField: "cum_prob",
          title: "Cum Prob",
        },
      ],
      sortOrder: [
        {
          field: "cum_prob",
          direction: "desc",
        },
      ],
      text: "",
      all_data: "",
      total_horses: "",
    };
  },
  async mounted() {
    this.type = "all_horses";
    await api
      .get(`/horses/shortlisttab/`)
      .then((response) => {
        this.all_data = response.data.items;
        this.total_horses = response.data.items.length;
      })
      .catch((error) => {});
    this.controls.year.options.push("All");
    this.all_data.forEach((element) => {
      this.controls.year.options.push(element.date_of_birth.split("-")[0]);
    });
    this.controls.year.options = [...new Set(this.controls.year.options)]
      .sort()
      .reverse();
  },
  methods: {
    onMeasureUpdate(e) {
      console.log("HorsesTable.onMeasureUpdate", e);

      this.$refs.vuetable.refresh();

      this.$emit("updated");
    },
    onEditMeasuresClick(e) {
      this.$refs.editMeasuresModal.show(e);
    },
    horse_type(event) {
      let horse_type = event?.target?.value || "all_horses";
      this.fetchData(horse_type);
    },
    changeyear() {
      let payload = {};
      if (this.filters.year && this.filters.year !== "All")
        payload.year = this.filters.year;
      this.fetchData(payload);
    },
    fetchData(payload) {
      payload.horse_type == "active_horses" || "";
      this.filters.year = payload.year || "";
      this.$refs.vuetable.refresh();
    },
    async httpFetch(apiUrl, httpOptions) {
      let data = [];
      const sortField = httpOptions.params.sort.split("|")[0];
      const sortOrder = httpOptions.params.sort.split("|")[1];
      await api
        .get(`/horses/shortlisttab/`)
        .then((response) => {
          this.result2 = this.test(response);
        })
        .catch((error) => {});

      data = {
        results: this.result2,
      };

      const newData = data.results.sort((a, b) => {
        if (a[sortField] < b[sortField]) {
          return sortOrder === "asc" ? -1 : 1;
        }
        if (a[sortField] > b[sortField]) {
          return sortOrder === "asc" ? 1 : -1;
        }
        return 0;
      });

      return { data: { results: newData } };
    },
    test(res) {
      let data = [];
      let horse_data = [];
      let horse_data1 = [];
      let horse_data2 = [];
      let updated_horse_data = [];
      if (this.type === "active_horses") {
        horse_data = res.data.items.filter((x) => x.active == "Yes");
        horse_data1 = res.data.items.filter((x) => x.elite == "Yes");
        // horse_data.forEach((element) => {
        //   element.date_of_birth = element.date_of_birth.split("-")[0];
        //   updated_horse_data.push(element);
        // });
        // horse_data = updated_horse_data;
        this.text = "Horse Count - " + horse_data.length + " - ";
        this.text +=
          ((horse_data.length / res.data.total_number_active) * 100).toFixed(
            2
          ) + "% Elite to all Active - ";
        if (horse_data1.length > 0 && horse_data.length > 0) {
          this.text +=
            ((horse_data1.length / horse_data.length) * 100).toFixed(2) +
            "% Elite to Shortlist";
        } else {
          this.text += "0.00% Elite to Shortlist";
        }
        if (this.filters.year) {
          horse_data = horse_data.filter(
            (x) => x.date_of_birth.split("-")[0] == this.filters.year
          );
          horse_data1 = horse_data.filter((x) => x.active == "Yes");
          horse_data2 = horse_data.filter((x) => x.elite == "Yes");
          this.text = "Horse Count - " + horse_data.length + " - ";
          this.text +=
            ((horse_data.length / res.data.total_number_active) * 100).toFixed(
              2
            ) + "% Elite to all Active - ";

          if (horse_data1.length > 0 && horse_data2.length > 0) {
            this.text +=
              ((horse_data2.length / horse_data1.length) * 100).toFixed(2) +
              "% Elite to Shortlist";
          } else {
            this.text += "0.00% Elite to Shortlist";
          }
        }
      } else if (
        this.type === "" ||
        this.type == null ||
        this.type == "all_horses"
      ) {
        horse_data = res.data.items.filter(
          (x) => x.prob_bio_model >= 0.5 && x.prob_conform_model >= 0.5
        );
        horse_data.forEach((element) => {
          element.date_of_birth = element.date_of_birth.split("-")[0];
          updated_horse_data.push(element);
        });
        horse_data = updated_horse_data;
        this.text = "Horse Count - " + horse_data.length + " - ";
        this.text +=
          ((horse_data.length / res.data.total_number) * 100).toFixed(2) +
          "% of Total Population";
        if (this.filters.year) {
          horse_data = horse_data.filter(
            (x) => x.date_of_birth == this.filters.year
          );
          this.text = "Horse Count - " + horse_data.length + " - ";
          this.text +=
            ((horse_data.length / res.data.total_number) * 100).toFixed(2) +
            "% of Total Population";
        }
      }
      return horse_data;
    },

    onLoading() {},
    onLoaded() {},
  },
  watch: {
    data(newVal) {},
  },
};
</script>
<style>
.chart label {
  margin-right: 10px;
}
.chart input[type="radio"] {
  margin-right: 5px;
}
.chart1 {
  margin-top: 10px;
}
.horse_data .float-md-right.pt-1 {
  display: none;
}
</style>
