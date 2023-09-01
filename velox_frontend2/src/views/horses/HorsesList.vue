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
    <div v-show="loading" class="loader">
        <svg width="200px" height="200px"  xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 100 100" preserveAspectRatio="xMidYMid" style="background: none;">
            <circle cx="75" cy="50" fill="#363a3c" r="6.39718">
                <animate attributeName="r" values="4.8;4.8;8;4.8;4.8" times="0;0.1;0.2;0.3;1" dur="1s" repeatCount="indefinite" begin="-0.875s"></animate>
            </circle>
            <circle cx="67.678" cy="67.678" fill="#363a3c" r="4.8">
                <animate attributeName="r" values="4.8;4.8;8;4.8;4.8" times="0;0.1;0.2;0.3;1" dur="1s" repeatCount="indefinite" begin="-0.75s"></animate>
            </circle>
            <circle cx="50" cy="75" fill="#363a3c" r="4.8">
                <animate attributeName="r" values="4.8;4.8;8;4.8;4.8" times="0;0.1;0.2;0.3;1" dur="1s" repeatCount="indefinite" begin="-0.625s"></animate>
            </circle>
            <circle cx="32.322" cy="67.678" fill="#363a3c" r="4.8">
                <animate attributeName="r" values="4.8;4.8;8;4.8;4.8" times="0;0.1;0.2;0.3;1" dur="1s" repeatCount="indefinite" begin="-0.5s"></animate>
            </circle>
            <circle cx="25" cy="50" fill="#363a3c" r="4.8">
                <animate attributeName="r" values="4.8;4.8;8;4.8;4.8" times="0;0.1;0.2;0.3;1" dur="1s" repeatCount="indefinite" begin="-0.375s"></animate>
            </circle>
            <circle cx="32.322" cy="32.322" fill="#363a3c" r="4.80282">
                <animate attributeName="r" values="4.8;4.8;8;4.8;4.8" times="0;0.1;0.2;0.3;1" dur="1s" repeatCount="indefinite" begin="-0.25s"></animate>
            </circle>
            <circle cx="50" cy="25" fill="#363a3c" r="6.40282">
                <animate attributeName="r" values="4.8;4.8;8;4.8;4.8" times="0;0.1;0.2;0.3;1" dur="1s" repeatCount="indefinite" begin="-0.125s"></animate>
            </circle>
            <circle cx="67.678" cy="32.322" fill="#363a3c" r="7.99718">
                <animate attributeName="r" values="4.8;4.8;8;4.8;4.8" times="0;0.1;0.2;0.3;1" dur="1s" repeatCount="indefinite" begin="0s"></animate>
            </circle>
        </svg>
    </div>  
    <b-row v-show="!loading">
      <b-colxx xxs="12">
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
          <template slot="name" slot-scope="props">
            <div style="width: 150px">
              <span> {{ props.rowData.name }}</span>
            </div>
          </template>
          <template slot="actions" slot-scope="props">
            <b-button-group>
              <i
                class="iconsminds-files action-icon"
                @click="onEditMeasuresClick(props.rowData.id)"
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
        
    <HorseDetail
      ref="horsedetail"
      @updated="onMeasureUpdate"
      :getdata="getdata"
    ></HorseDetail>
  </div>
</template>
<script>
import _ from "lodash";
import Vuetable from "vuetable-2/src/components/Vuetable";
import VuetablePaginationBootstrap from "@/components/Common/VuetablePaginationBootstrap";
import { apiUrl } from "@/constants/config";
import DatatableHeading from "@/containers/datatable/DatatableHeading";
import horseServices from "@/services/horse.service";
import HorseDetail from "@/views/horses/HorseDetail";

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
    HorseDetail
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
      loading: false,

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
          dataClass: "text-muted"
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
          name: "__slot:actions",
          title: ""
        }
      ],
      filters: {}
    };
  },
  async mounted() {
  },
  methods: {
    fetchData(payload) {
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

      }, 500);
    },
    onHorseUpdate(e) {

      this.$refs.vuetable.refresh();

      this.$emit("updated");
    },
    onMeasureUpdate(e) {
      console.log("HorsesTable.onMeasureUpdate", e);

      this.$refs.vuetable.refresh();

      this.$emit("updated");
    },
    onEditMeasuresClick(e) {
      this.$refs.horsedetail.show(e);
    },
    getdata() {
				this.$refs.vuetable.refresh();
		},
    onLoading() {
      this.loading = true
    },
    onLoaded() {
      this.loading = false
    }
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
