<template>
  <div>
    <datatable-heading
      title="Title"
      :keymap="keymap"
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
          :api-mode="false"
          :fields="fields"
          :per-page="perPage"
          pagination-path="pagination"
          :row-class="onRowClass"
          :sort-order="sortOrder"
          :data-manager="dataManager"
          @vuetable:pagination-data="onPaginationData"
        >
          <template slot="name" slot-scope="props">
            <div style="width: 150px">
              <span> {{ props.rowData.name }}</span>
              <span
                class="icon success ml-2 action-icon"
                @click="onEditHorseClick(props.rowData)"
              >
                <i class="iconsminds-file-edit"></i>
              </span>
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
          </template>

          <template slot="actions" slot-scope="props">
            <b-button-group>
              <i
                class="iconsminds-remove-file action-icon"
                @click="onDeleteHorseClick(props.rowData)"
              ></i>

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
        {
          name: "date_of_birth",
          sortField: "date_of_birth",
          title: "Date of Birth",
          dataClass: "text-muted"
        },

        {
          name: "starts",
          sortField: "starts",
          title: "Starts",
          dataClass: "text-muted"
        },
        {
          name: "date_last_start",
          sortField: "date_last_start",
          title: "Date Last Start",
          dataClass: "text-muted"
        },
        /*
        {
          name: "date_last_start",
          sortField: "date_last_start",
          title: "Update Days",
          dataClass: "text-muted"
        },*/
        {
          name: "race_rating",
          sortField: "race_rating",
          title: "Race Rating",
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
          name: "__slot:measurements",
          title: "Measurements"
        },
        {
          name: "__slot:actions",
          title: ""
        }
      ]
    };
  },
  async mounted() {
    // await this.fetchData();
  },
  methods: {
    async fetchData() {
      let res = await horseServices.fetchHorses();

      this.localData = res.data.results;
    },
    makeQueryParams(sortOrder, currentPage, perPage) {
      this.selectedItems = [];
      return sortOrder[0]
        ? {
            sort: sortOrder[0]
              ? sortOrder[0].field + "|" + sortOrder[0].direction
              : "",
            page: currentPage,
            per_page: this.perPage,
            search: this.searchValue
          }
        : {
            page: currentPage,
            per_page: this.perPage,
            search: this.searchValue
          };
    },
    onRowClass(dataItem, index) {
      if (this.selectedItems.includes(dataItem.id)) {
        return "selected";
      }
      return "";
    },

    rowClicked(dataItem, event) {
      const itemId = dataItem.id;
      if (event.shiftKey && this.selectedItems.length > 0) {
        let itemsForToggle = this.items;
        var start = this.getIndex(itemId, itemsForToggle, "id");
        var end = this.getIndex(
          this.selectedItems[this.selectedItems.length - 1],
          itemsForToggle,
          "id"
        );
        itemsForToggle = itemsForToggle.slice(
          Math.min(start, end),
          Math.max(start, end) + 1
        );
        this.selectedItems.push(
          ...itemsForToggle.map(item => {
            return item.id;
          })
        );
        this.selectedItems = [...new Set(this.selectedItems)];
      } else {
        if (this.selectedItems.includes(itemId)) {
          this.selectedItems = this.selectedItems.filter(x => x !== itemId);
        } else this.selectedItems.push(itemId);
      }
    },
    rightClicked(dataItem, field, event) {
      event.preventDefault();
      if (!this.selectedItems.includes(dataItem.id)) {
        this.selectedItems = [dataItem.id];
      }
      this.$refs.contextmenu.show({ top: event.pageY, left: event.pageX });
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
      this.perPage = perPage;
      this.$refs.vuetable.refresh();
    },

    searchChange(val) {
      if (typeof this.searchTimer !== "undefined") {
        clearTimeout(this.searchTimer);
      }
      this.searchTimer = setTimeout(() => {
        this.searchValue = val.toLowerCase();

        console.log("searchChange", val);
        this.filteredData = this.data.filter(i =>
          i.name.toLowerCase().includes(this.searchValue)
        );

        this.updateDataSet(this.filteredData);
      }, 500);
    },

    selectAll(isToggle) {
      if (this.selectedItems.length >= this.items.length) {
        if (isToggle) this.selectedItems = [];
      } else {
        this.selectedItems = this.items.map(x => x.id);
      }
    },
    keymap(event) {
      switch (event.srcKey) {
        case "select":
          this.selectAll(false);
          break;
        case "undo":
          this.selectedItems = [];
          break;
      }
    },
    getIndex(value, arr, prop) {
      for (var i = 0; i < arr.length; i++) {
        if (arr[i][prop] === value) {
          return i;
        }
      }
      return -1;
    },

    onContextMenuAction(action) {},
    dataManager(sortOrder, pagination) {
      //if (this.filteredData.length < 1) return;

      let local = this.filteredData;

      // sortOrder can be empty, so we have to check for that as well
      if (sortOrder.length > 0) {
        local = _.orderBy(
          local,
          sortOrder[0].sortField,
          sortOrder[0].direction
        );
      }

      pagination = this.$refs.vuetable.makePagination(
        local ? local.length : 0,
        this.perPage
      );

      let from = pagination.from - 1;
      let to = from + this.perPage;

      return {
        pagination: pagination,
        data: _.slice(local, from, to)
      };
    },
    updateDataSet(payload) {
      this.filteredData = payload;

      let val = this.dataManager([], {});

      this.$refs.vuetable.setData(val);
    },
    onEditHorseClick(e) {
      this.$refs.editHorseModal.show(e);
    },
    onHorseUpdate(e) {
      let index = this.filteredData.findIndex(i => i.id == e.id);

      this.filteredData[index] = e;

      this.updateDataSet(this.filteredData);

      this.$emit("updated");
    },
    onMeasureUpdate(e) {
      console.log("HorsesTable.onMeasureUpdate", e);

      /*
      let index = this.filteredData.findIndex(i => i.id == e.id);

      this.filteredData[index] = e;

      this.updateDataSet(this.filteredData);
*/
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
    }
  },

  watch: {
    data(newVal) {
      this.updateDataSet(newVal);
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
