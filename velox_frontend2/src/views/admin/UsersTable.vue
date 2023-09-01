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
      :searchBox="false"
      :addRecordButton="true"
      @add-record="onAddRecord"
      v-if="tabtype=='admin'"
    ></datatable-heading>
     <b-tabs content-class="mt-3">
        <b-tab title="Admin" id="admin" @click="tab_type('admin')" active>
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
                  :per-page="perPage"
                  @vuetable:pagination-data="onPaginationData"
                  @vuetable:loading="onLoading"
                  @vuetable:loaded="onLoaded"
                  v-if="tabtype=='admin'"
                >
                  <template slot="actions" slot-scope="props">
                    <b-button-group>
                      <i
                        class="iconsminds-remove-file action-icon"
                        @click="onDeleteUserClick(props.rowData)"
                      ></i>

                      <i
                        class="iconsminds-files action-icon"
                        @click="onEditUserClick(props.rowData)"
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
        </b-tab>
         <b-tab title="Country Weights" id="country" @click="tab_type('country')" >
             <b-row>
              <b-colxx xxs="12">
                <vuetable
                  ref="vuetable"
                  class="table-divided order-with-arrow"
                  :http-fetch="httpFetch"
                  :fields="fields1"
                  :sort-order="sortOrder"
                  pagination-path=""
                  data-path="results"
                  @vuetable:loading="onLoading"
                  @vuetable:loaded="onLoaded"
                  v-if="tabtype=='country'"
                >
                  <template slot="actions" slot-scope="props">
                    <b-button-group>
                      <!-- <i
                        class="iconsminds-remove-file action-icon"
                        @click="onDeleteUserClick(props.rowData)"
                      ></i> -->

                      <i
                        class="iconsminds-files action-icon"
                        @click="onEditCountyWeightClick(props.rowData)"
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
         </b-tab>
     </b-tabs>

   
    <EditUserModal ref="editUserModal" @updated="onUserUpdate"></EditUserModal>
    <EditCountryWeightModal ref="editCountryWeightModal" @updated="onCountryWeightUpdate"></EditCountryWeightModal>
  </div>
</template>
<script>
import _ from "lodash";
import Vuetable from "vuetable-2/src/components/Vuetable";
import VuetablePaginationBootstrap from "@/components/Common/VuetablePaginationBootstrap";
import { apiUrl } from "@/constants/config";
import DatatableHeading from "@/containers/datatable/DatatableHeading";
import userServices from "@/services/user.service";
import EditUserModal from "@/views/admin/EditUserModal";
import EditCountryWeightModal from "@/views/admin/EditCountryWeightModal";
import vSelect from "vue-select";

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
    EditUserModal,
    EditCountryWeightModal,
    vSelect
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
      tabtype:'',
      searchTimer: undefined,

      sortOrder: [
        {
          field: "id",
          direction: "asc"
        }
      ],
      fields: [
        {
          name: "email",
          sortField: "email",
          title: "Email",
          dataClass: "text-muted"
        },
        {
          name: "first_name",
          sortField: "first_name",
          title: "First Name",
          dataClass: "text-muted"
        },
        {
          name: "last_name",
          sortField: "last_name",
          title: "Last Name",
          dataClass: "text-muted"
        },
        {
          name: "__slot:actions",
          title: ""
        }
      ],
      fields1: [
        {
          name: "starts_country",
          sortField: "starts_country",
          title: "Start Country",
          dataClass: "text-muted"
        },
        {
          name: "country",
          sortField: "country",
          title: "Country",
          dataClass: "text-muted"
        },
        {
          name: "country_weight",
          sortField: "country_weight",
          title: "Country Weight",
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
    // await this.fetchData();
    this.tabtype='admin'
  },
  methods: {
    fetchData(payload) {
      this.filters.start_country = payload.starts_country || "";
      this.$refs.vuetable.refresh();
    },
    async httpFetch(apiUrl, httpOptions) {
      let data = [];
      if(this.tabtype=='admin')
      {
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

          let response = await userServices.fetchUsers(payload);

          response = response.data;

          data = {
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

          console.log("httpFetch.result", data);
      }

      else if(this.tabtype=='country')
      {
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
        
          if(!payload.start_country)
          {
            let response = await userServices.fetchcountyweights(payload);

            response = response.data;

            data = {
              per_page: this.perPage,
              current_page: httpOptions.params.page,
              last_page: Math.round(response.count / httpOptions.params.per_page),
              next_page_url: response.next,
              prev_page_url: response.previous,
              from: 1 + (httpOptions.params.page - 1) * this.perPage,
              to: this.perPage + (httpOptions.params.page - 1) * this.perPage,
              results: response.results
            };
          }
          else
          {
            let response = await userServices.fetchcountyweights(payload);

            response = response.data;
            let result = 
              {
                result: response
              }

            data = {
              per_page: this.perPage,
              current_page: httpOptions.params.page,
              last_page: Math.round(response.count / httpOptions.params.per_page),
              next_page_url: response.next,
              prev_page_url: response.previous,
              from: 1 + (httpOptions.params.page - 1) * this.perPage,
              to: this.perPage + (httpOptions.params.page - 1) * this.perPage,
              results: result
            };
          }
          
          console.log("httpFetch.result", data);
      }
      else 
      {
          
      }
      return { data: data };
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

    onEditUserClick(e) {
      this.$refs.editUserModal.show(e);
    },

    onEditCountyWeightClick(e) {
      this.$refs.editCountryWeightModal.show(e);
    },
    onUserUpdate(e) {
      this.$refs.vuetable.refresh();

      this.$emit("updated");
    },
    onUserUpdate(e) {
      console.log("UsersTable.onUserUpdate", e);

      this.$refs.vuetable.refresh();

      this.$emit("updated");
    },

    onCountryWeightUpdate(e) {
      this.$refs.vuetable.refresh();

      this.$emit("updated");
    },
    onCountryWeightUpdate(e) {
      console.log("countyweight update", e);

      this.$refs.vuetable.refresh();

      this.$emit("updated");
    },

    async onDeleteUserClick(e) {
      let result = await this.$formHelpers.showConfirmation(
        "Are you sure you want to delete this record?"
      );
      console.log("result", result);
      if (!result) return;

      try {
        console.log("onDeleteUserClick.e", e);
        await userServices.deleteUser(e);

        this.$formHelpers.showError("User deleted");

        this.$emit("updated");
      } catch (e) {
        console.error(e);

        this.$formHelpers.showError(e);
      }
    },
    onAddRecord() {
      this.$refs.editUserModal.show();
    },
    onLoading() {},
    onLoaded() {},
    tab_type(type)
    {
        this.tabtype=type
    },
  },

  watch: {
    data(newVal) {}
  }
};
</script>

<style scoped>
.action-icon {
  cursor: pointer;
  font-size: 16px;
}
</style>
