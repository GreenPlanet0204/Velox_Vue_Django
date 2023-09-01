<template>
  <div>
    <datatable-heading
      title="Title"
      :changePageSize="changePageSize"
      :searchChange="searchChange"
      :from="from"
      :to="to"
      :total="total"
      :perPage="perPage"
      :searchBox="true"
    ></datatable-heading>

    <b-row>
      <b-colxx xxs="12">
        <!--
          :query-params="makeQueryParams"
          :per-page="perPage"
          :data="filteredData"


-->
        <vuetable
          ref="vuetable"
          class="table-divided order-with-arrow"
          :http-fetch="httpFetch"
          :fields="fields"
          :sort-order="sortOrder"
          pagination-path=""
          data-path="results"
          :per-page="perPage"
          @vuetable:pagination-data="onPaginationData"
          @vuetable:loading="onLoading"
          @vuetable:loaded="onLoaded"
        >
          <!--
        <vuetable
          ref="vuetable"
          class="table-divided order-with-arrow"
          api-url=""
          :api-mode="true"
          :fields="fields"
          :http-fetch="fetchData"
          :load-on-start="true"
          :per-page="perPage"
          pagination-path=""
          data-path="data"
          @vuetable:pagination-data="onPaginationData"
          @vuetable:loading="onLoading"
          @vuetable:loaded="onLoaded"
        >
        -->
          <template slot="name" slot-scope="props">
            <div style="width: 150px">
              <span> {{ props.rowData.name }}</span>
              <div class="mt-1">
                <span class="icon success action-icon" @click="onEditHorseClick(props.rowData)">
                  <i class="iconsminds-file-edit"></i>
                </span>
                <span class="icon success ml-2 action-icon" @click="onDeleteHorseClick(props.rowData)">
                  <i class="iconsminds-remove-file"></i>
                </span>
              </div>
            </div>
          </template>

          <template slot="measurements" slot-scope="props">
            <i
              v-if="props.rowData.measurements.hasDNA"
              class="iconsminds-dna-2"
            ></i>
            <i
              v-if="props.rowData.measurements.hasImage"
              class="iconsminds-photo"
            ></i>
            <i
              v-if="props.rowData.measurements.hasBioVideo"
              class="iconsminds-gears"
            ></i>
            <i
              v-if="props.rowData.measurements.hasCardioVideo"
              class="iconsminds-pulse"
            ></i>
            <i
              v-if="props.rowData.measurements.image_measurements"
              class="iconsminds-camera-3"
            ></i>
          </template>

          <template slot="actions" slot-scope="props">
            <b-button-group>
              <!-- <i
                class="iconsminds-remove-file action-icon"
                @click="onDeleteHorseClick(props.rowData)"
              ></i> -->

              <i
                class="iconsminds-files action-icon"
                @click="onEditMeasuresClick(props.rowData)"
              ></i>
            </b-button-group>
          </template>
        </vuetable>

        <vuetable-pagination-bootstrap
          class="mt-4"
          ref="pagination"
          @vuetable-pagination:change-page="onChangePage"
        />
      </b-colxx>
    </b-row>
    <EditHorseModal
      ref="editHorseModal"
      @updated="onHorseUpdate"
    ></EditHorseModal>
    <EditMeasuresModal
      ref="editMeasuresModal"
      @updated="onMeasureUpdate"
    ></EditMeasuresModal>
  </div>
</template>
<script>
import _ from "lodash";
import Vuetable from "vuetable-2/src/components/Vuetable";
import VuetablePaginationBootstrap from "@/components/Common/VuetablePaginationBootstrap";
import { apiUrl } from "@/constants/config";
import DatatableHeading from "@/containers/datatable/DatatableHeading";
import horseServices from "@/services/horse.service";
import EditHorseModal from "@/views/horses/EditHorseModal";
import EditMeasuresModal from "@/views/horses/EditMeasuresModal";

export default {
  props: {
    data: {
      type: Array,
      default: () => []
    }
  },

  components: {
    vuetable: Vuetable,
    VuetablePaginationBootstrap,
    DatatableHeading,
    EditHorseModal,
    EditMeasuresModal
  },
  data() {
    return {
      isLoad: false,
      filteredData: [],
      sort: "",
      page: 1,
      perPage: 30,
      search: "",
      from: 0,
      to: 0,
      total: 0,
      lastPage: 0,
      items: [],
      selectedItems: [],
      searchTimer: undefined,

      sortOrder: [
        {
          field: "date_of_birth",
          direction: "asc"
        }
      ],
      fields: [
        {
          name: "__slot:name",
          sortField: "name",
          title: "Name",
          //dataClass: "list-item-heading"
          dataClass: "text-muted"
          //width: "10%"
        },
        {
          name: "type",
          sortField: "type",
          title: "Type",
          dataClass: "text-muted"
        },
        {
          name: "sex",
          sortField: "sex",
          title: "Sex",
          dataClass: "text-muted"
        },
        // {
        //   name: "date_of_birth",
        //   sortField: "date_of_birth",
        //   title: "Date of Birth",
        //   dataClass: "text-muted"
        // },

        // {
        //   name: "starts",
        //   sortField: "starts",
        //   title: "Starts",
        //   dataClass: "text-muted"
        // },
        // {
        //   name: "date_last_start",
        //   sortField: "date_last_start",
        //   title: "Date Last Start",
        //   dataClass: "text-muted"
        // },
        /*
        {
          name: "date_last_start",
          sortField: "date_last_start",
          title: "Update Days",
          dataClass: "text-muted"
        },*/
        // {
        //   name: "race_rating",
        //   sortField: "race_rating",
        //   title: "Race Rating",
        //   dataClass: "text-muted"
        // },
        {
          name: "active",
          sortField: "active",
          title: "Active",
          dataClass: "text-muted"
        },
        {
          name: "status",
          sortField: "status",
          title: "Status",
          dataClass: "text-muted"
        },
        {
          name: "elite",
          sortField: "elite",
          title: "Elite",
          dataClass: "text-muted"
        },
        {
          name: "__slot:measurements",
          title: "Measurements"
        },
        {
          name: "__slot:actions",
          title: ""
        }
      ],
      filters: {}
    };
  },
  async mounted() {
    // await this.fetchData();
  },
  methods: {
    fetchData(payload) {
      this.filters.country = payload.country || "";
      this.filters.status = payload.status || "";

      this.$refs.vuetable.refresh();
    },
    async httpFetch(apiUrl, httpOptions) {
      console.log("httpFetch", JSON.stringify(httpOptions.params));

      let payload = {
        page: httpOptions.params.page,
        page_size: this.perPage
      };

      if (httpOptions.params.sort) {
        let sort = httpOptions.params.sort.replace("|asc", "");

        if (sort.indexOf("|desc") > 0) {
          sort = "-" + sort.replace("|desc", "");
        }
        payload.ordering = sort;
      }

      //add filters by country and status
      if (this.filters) payload = { ...payload, ...this.filters };

      let response = await horseServices.fetchHorses(payload);

      response = response.data;
      //console.log("res", response);

      let data = {
        total: response.count,
        per_page: this.perPage,
        current_page: httpOptions.params.page,
        last_page: Math.round(response.count / httpOptions.params.per_page),
        next_page_url: response.next,
        prev_page_url: response.previous,
        from: 1 + (httpOptions.params.page - 1) * this.perPage,
        to: this.perPage + (httpOptions.params.page - 1) * this.perPage,
        results: response.results
      };

      data = this.prepareMeasuresData(data);

      console.log("result", data);
      return { data: data };
    },
    prepareMeasuresData(data) {
      for (let horse of data.results) {
        horse.measurements = {};

        if (
          horse.distance1 &&
          horse.distance2 &&
          horse.size1 &&
          horse.class1 &&
          horse.class2 &&
          horse.class3
        )
          horse.measurements.hasDNA = true;
          if (horse.image_measurements && horse.image_measurements.length > 0) {
            if (horse.image_measurements.find(i => i.image))
            {
              horse.measurements.image_measurements = true;
            }
              
          }

        if (horse.measures && horse.measures.length > 0) {
          /*
          if (horse.measures.find(i => i.dlc_gaf_image_url))
            horse.measurements.hasImage = true;
*/
          if (horse.measures.find(i => i.video_url))
            horse.measurements.hasBioVideo = true;

          if (horse.measures.find(i => i.cardio_video_url))
            horse.measurements.hasCardioVideo = true;
        }
      }

      return data;
    },

    onRowClass(dataItem, index) {
      if (this.selectedItems.includes(dataItem.id)) {
        return "selected";
      }
      return "";
    },

    onPaginationData(paginationData) {
      this.from = paginationData.from;
      this.to = paginationData.to;
      this.total = paginationData.total;
      this.lastPage = paginationData.last_page;
      this.items = paginationData.data;
      this.$refs.pagination.setPaginationData(paginationData);
    },

    onChangePage(page) {
      this.$refs.vuetable.changePage(page);
    },

    changePageSize(perPage) {
      console.log("changePageSize", perPage);
      this.perPage = perPage;
      this.$refs.vuetable.refresh();
    },

    searchChange(val) {
      console.log("searchChange", val);
      if (typeof this.searchTimer !== "undefined") {
        clearTimeout(this.searchTimer);
      }
      this.searchTimer = setTimeout(() => {
        this.filters.name = val.toLowerCase();

        this.$refs.vuetable.refresh();

        /*
        this.filteredData = this.data.filter(i =>
          i.name.toLowerCase().includes(this.searchValue)
        );

        this.updateDataSet(this.filteredData);*/
      }, 500);
    },

    onEditHorseClick(e) {
      this.$refs.editHorseModal.show(e);
    },
    onHorseUpdate(e) {
      /*
      console.log("onHorseUpdate", e);
      let index = this.filteredData.findIndex(i => i.id == e.id);
      this.filteredData[index] = e;
*/
      //this.updateDataSet(this.filteredData);

      this.$refs.vuetable.refresh();

      this.$emit("updated");
    },
    onMeasureUpdate(e) {
      console.log("HorsesTable.onMeasureUpdate", e);

      this.$refs.vuetable.refresh();

      this.$emit("updated");
    },
    onEditMeasuresClick(e) {
      this.$refs.editMeasuresModal.show(e);
    },
    async onDeleteHorseClick(e) {
      let result = await this.$formHelpers.showConfirmation(
        "Are you sure you want to delete this record and its associated measurements?"
      );
      console.log("result", result);
      if (!result) return;

      try {
        console.log("onDeleteHorseClick.e", e);
        await horseServices.deleteHorse(e);

        this.$formHelpers.showError("Horse deleted");

        this.$emit("updated");
      } catch (e) {
        console.error(e);

        this.$formHelpers.showError(e);
      }
    },
    onLoading() {},
    onLoaded() {}
  },

  watch: {
    data(newVal) {
      //this.updateDataSet(newVal);
    }
  }
};
</script>

<style scoped>
.action-icon {
  cursor: pointer;
  font-size: 16px;
}
</style>
