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
      :pageSizes="[3, 5, 10]"
      :searchBox="false"
    ></datatable-heading>

    <b-row>
      <b-colxx xxs="12">
        <div class="table-responsive">
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
            <template slot="date_of_measure" slot-scope="props">
              <datepicker
                :bootstrap-styling="true"
                placeholder="Date of Measurement"
                :value="props.rowData.date_of_measure"
                :disabled-dates="disabledDates"
                @selected="onDateOfMeasureSelect($event, props.rowData)"
                format="yyyy-MM-dd"
                :typeable="false"
                :use-utc="true"
                :disabled="disableDatePicker"
              ></datepicker>
            </template>
            <template slot="dlc_gaf_image_url" slot-scope="props">
              <img
                width="220"
                height="140"
                :src="props.rowData.image.url"
                @click="imagepopup(props.rowData)"
                class="imagepopup"
              />
            </template>
            <template slot="prob_conform_model_score" slot-scope="props">
              <!-- <input type="number" :value="props.rowData.cardio_cluster" @input="onCardioCluster($event, props.rowData)" readonly> -->
              <label>{{ props.rowData.prob_conform_model_score }}</label>
            </template>

            <!-- <template slot="video_qc" slot-scope="props">
            <v-select
              :value="props.rowData.video_qc"
              :options="controls.video_qc.options"
              @input="onVideoQCSelect($event, props.rowData)"
            />
          </template> -->
            <!-- <template slot="cardio_quality" slot-scope="props">
            <v-select
              :value="props.rowData.cardio_quality"
              :options="controls.cardio_quality.options"
              @input="onCardioQSelect($event, props.rowData)"
            />
          </template> -->

            <template slot="video_url" slot-scope="props">
              <video
                width="220"
                height="140"
                :src="props.rowData.video_url"
                type="video/mp4"
                controls
              ></video>
            </template>

            <!-- <template slot="cardio_type" slot-scope="props">
            <v-select
              :value="props.rowData.cardio_type"
              :options="controls.cardio_type.options"
              @input="onCardioTypeSelect($event, props.rowData)"
            />
          </template> -->
            <template slot="cardio_cluster" slot-scope="props">
              <!-- <input type="number" :value="props.rowData.cardio_cluster" @input="onCardioCluster($event, props.rowData)" readonly> -->
              <label>{{ props.rowData.cardio_cluster }}</label>
            </template>

            <template slot="cardio_type" slot-scope="props">
              <!-- <v-select
              :value="props.rowData.cardio_type"
              :options="controls.cardio_type.options"
              @input="onCardioTypeSelect($event, props.rowData)"
            /> -->
              <!-- <input :value="props.rowData.cardio_type" @input="onCardioType($event, props.rowData)" readonly> -->
              <label>{{ props.rowData.cardio_type }}</label>
            </template>

            <template slot="cardio_video_score" slot-scope="props">
              <!-- <input :value="props.rowData.cardio_video_score" readonly> -->
              <label>{{ props.rowData.cardio_video_score }}</label>
            </template>
            <template slot="biomechanics_cluster" slot-scope="props">
              <!-- <input type="number" :value="props.rowData.biomechanics_cluster" @input="onBiomechanicsCluster($event, props.rowData)" readonly> -->
              <label>{{ props.rowData.biomechanics_cluster }}</label>
            </template>
            <template slot="prob_bio_model_score" slot-scope="props">
              <!-- <input :value="props.rowData.dlc_jrg_score" @input="onBiomechanicsJRPScrore($event, props.rowData)" readonly> -->
              <label>{{ props.rowData.prob_bio_model_score }}</label>
            </template>

            <template slot="cardio_video_url" slot-scope="props">
              <video
                width="220"
                height="140"
                :src="props.rowData.cardio_video_url"
                type="video/mp4"
                controls
              ></video>
              <!-- <source :src="props.rowData.cardio_video_url" type="video/mp4" /> -->
            </template>
            <template slot="actions" slot-scope="props">
              <b-button-group v-if="mode == 'cardio' || mode == 'bio'">
                <i
                  class="iconsminds-remove-file action-icon"
                  @click="onDeleteMeasureClick(props.rowData)"
                ></i>
              </b-button-group>
              <b-button-group v-else>
                <i
                  class="iconsminds-remove-file action-icon"
                  @click="onDeleteImageMeasureClick(props.rowData)"
                ></i>
              </b-button-group>
            </template>
          </vuetable>

          <vuetable-pagination-bootstrap
            class="mt-4"
            ref="pagination"
            @vuetable-pagination:change-page="onChangePage"
          />
        </div>
      </b-colxx>
    </b-row>
    <ImageModal ref="imageModal"></ImageModal>
  </div>
</template>
<script>
import _ from "lodash";
import moment from "moment";

import Vuetable from "vuetable-2/src/components/Vuetable";
import VuetablePaginationBootstrap from "@/components/Common/VuetablePaginationBootstrap";
import { apiUrl } from "@/constants/config";
import DatatableHeading from "@/containers/datatable/DatatableHeading";
import measureServices from "@/services/measure.service";
import EditHorseModal from "@/views/horses/EditHorseModal";
import EditMeasuresModal from "@/views/horses/EditMeasuresModal";
import Datepicker from "vuejs-datepicker";
import dictionaryServices from "@/services/dictionary.service.js";
import vSelect from "vue-select";
import ImageModal from "@/views/horses/ImageModal";
import "vue-select/dist/vue-select.css";

export default {
  props: {
    data: {
      type: Array,
      default: () => []
    },
    mode: {
      type: String
    }
  },

  components: {
    vuetable: Vuetable,
    VuetablePaginationBootstrap,
    DatatableHeading,
    EditHorseModal,
    EditMeasuresModal,
    Datepicker,
    vSelect,
    ImageModal
  },
  data() {
    return {
      disableDatePicker: false,
      isLoad: false,
      filteredData: [],
      sort: "",
      page: 1,
      perPage: 5,
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
          field: "date_of_measure",
          direction: "asc"
        }
      ],
      fields: [
        {
          name: "__slot:date_of_measure",
          sortField: "date_of_measure",
          title: "Date of Measure",
          dataClass: "text-muted"
        },
        // {
        //   name: "__slot:video_qc",
        //   sortField: "video_qc",
        //   title: "Quality Control1",
        //   dataClass: "text-muted",
        //   visible: false
        // },
        {
          name: "__slot:cardio_video_url",
          sortField: "cardio_video_url",
          title: "Cardio Video",
          dataClass: "text-muted",
          visible: false
        },
        {
          name: "__slot:cardio_cluster",
          sortField: "cardio_cluster",
          title: "Cardio Cluster",
          dataClass: "text-muted",
          visible: false
        },
        {
          name: "__slot:cardio_type",
          sortField: "cardio_type",
          title: "Cardio Type",
          dataClass: "text-muted",
          visible: false
        },
        {
          name: "__slot:cardio_video_score",
          sortField: "cardio_video_score",
          title: "Cardio Video Score",
          dataClass: "text-muted",
          visible: false
        },
        {
          name: "__slot:dlc_gaf_image_url",
          title: "Image",
          dataClass: "text-muted",
          visible: false
        },
        {
          name: "__slot:prob_conform_model_score",
          sortField: "prob_conform_model_score",
          title: "Conformation Score",
          dataClass: "text-muted",
          visible: false
        },
        {
          name: "__slot:video_url",
          sortField: "video_url",
          title: "Biomechanics Video",
          dataClass: "text-muted",
          visible: false
        },
        {
          name: "__slot:biomechanics_cluster",
          sortField: "biomechanics_cluster",
          title: "Biomechanics Cluster",
          dataClass: "text-muted",
          visible: false
        },
        {
          name: "__slot:prob_bio_model_score",
          sortField: "prob_bio_model_score",
          title: "Biomechanics Model Score",
          dataClass: "text-muted",
          visible: false
        },
        // {
        //   name: "__slot:cardio_quality",
        //   sortField: "cardio_quality",
        //   title: "Quality Control",
        //   dataClass: "text-muted",
        //   visible: false
        // },

        {
          name: "__slot:actions",
          title: ""
        }
      ],
      disabledDates: {
        dates: []
      },
      controls: {
        // video_qc: {
        //   options: []
        // },
        // cardio_quality: {
        //   options: []
        // },
        cardio_type: {
          options: []
        }
      }
    };
  },
  async mounted() {
    // this.controls.video_qc.options = await dictionaryServices.fetchVideoQualityOptions();
    // this.controls.cardio_quality.options = await dictionaryServices.fetchVideoQualityOptions();

    this.controls.cardio_type.options = await dictionaryServices.fetchCardioTypeOptions();

    this.updateColumns();
    // this.onCardioCluster();
  },
  methods: {
    updateColumns() {
      let columnTitle = "";
      if (this.mode == "image") {
        //this.disableDatePicker = true;
        this.$refs.vuetable.showField(
          this.fields.findIndex(f => f.title == "Image")
        );

        this.$refs.vuetable.showField(
          this.fields.findIndex(f => f.title == "Conformation Score")
        );
      }
      if (this.mode == "bio") {
        this.disableDatePicker = false;
        // this.$refs.vuetable.showField(
        //   this.fields.findIndex(f => f.name == "__slot:video_qc")
        // );

        this.$refs.vuetable.showField(
          this.fields.findIndex(f => f.title == "Biomechanics Video")
        );
        this.$refs.vuetable.showField(
          this.fields.findIndex(f => f.title == "Biomechanics Cluster")
        );
        this.$refs.vuetable.showField(
          this.fields.findIndex(f => f.title == "Biomechanics Model Score")
        );
      }

      if (this.mode == "cardio") {
        this.disableDatePicker = false;
        // this.$refs.vuetable.showField(
        //   this.fields.findIndex(f => f.name == "__slot:cardio_quality")
        // );

        this.$refs.vuetable.showField(
          this.fields.findIndex(f => f.title == "Cardio Video")
        );
        this.$refs.vuetable.showField(
          this.fields.findIndex(f => f.title == "Cardio Type")
        );
        this.$refs.vuetable.showField(
          this.fields.findIndex(f => f.title == "Cardio Cluster")
        );
        this.$refs.vuetable.showField(
          this.fields.findIndex(f => f.title == "Cardio Video Score")
        );
      }
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
      this.perPage = perPage;
      this.$refs.vuetable.refresh();
    },

    searchChange(val) {
      if (typeof this.searchTimer !== "undefined") {
        clearTimeout(this.searchTimer);
      }
      this.searchTimer = setTimeout(() => {
        this.searchValue = val;

        this.filteredData = this.data.filter(i =>
          i.date_of_measure.toLowerCase().includes(this.searchValue)
        );

        this.updateDataSet(this.filteredData);
      }, 500);
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

    dataManager(sortOrder, pagination) {
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
      console.log("measuresTable.updateDataSet", payload);
      this.filteredData = payload;

      let val = this.dataManager([], {});

      this.$refs.vuetable.setData(val);
    },

    async onDeleteMeasureClick(e) {
      let result = await this.$formHelpers.showConfirmation(
        "Are you sure you wish to delete this measurement?"
      );

      if (!result) return;

      try {
        await measureServices.deleteMeasure(e);

        this.$formHelpers.showInfo("Measure deleted");

        this.filteredData = this.filteredData.filter(i => i.id !== e.id);

        this.updateDataSet(this.filteredData);

        this.$emit("updated");
      } catch (e) {
        console.error(e);

        this.$formHelpers.showError(e);
      }
    },
    async onDeleteImageMeasureClick(e) {
      let result = await this.$formHelpers.showConfirmation(
        "Are you sure you wish to delete this measurement?"
      );

      if (!result) return;

      try {
        await measureServices.deleteImageMeasure(e);

        this.$formHelpers.showInfo("Image Measure deleted");

        this.filteredData = this.filteredData.filter(i => i.id !== e.id);

        this.updateDataSet(this.filteredData);

        this.$emit("updated");
      } catch (e) {
        console.error(e);

        this.$formHelpers.showError(e);
      }
    },
    async onDateOfMeasureSelect(e, row) {
      console.log();
      console.log("onDateOfMeasureSelect", e, row);

      try {
        let date_of_measure = moment.utc(e).format("YYYY-MM-DD");

        if (row.prob_conform_model_score !== undefined) {
          await measureServices.updateImageMeasure({
            id: row.id,
            date_of_measure: date_of_measure
          });
          this.$formHelpers.showInfo("Date of Image Measure updated");
        } else {
          await measureServices.updateMeasure({
            id: row.id,
            date_of_measure: date_of_measure
          });
          this.$formHelpers.showInfo("Date of Measure updated");
        }

        this.$emit("updated");
      } catch (e) {
        this.$formHelpers.showError(e);
      }
    },
    async onVideoQCSelect(e, row) {
      try {
        await measureServices.updateMeasure({
          id: row.id
          // video_qc: e
        });
        this.$formHelpers.showInfo("Quality Control updated");

        this.$emit("updated");
      } catch (e) {
        this.$formHelpers.showError(e);
      }
    },
    async onCardioQSelect(e, row) {
      try {
        await measureServices.updateMeasure({
          id: row.id
          // cardio_quality: e
        });
        this.$formHelpers.showInfo("Quality Control updated");

        this.$emit("updated");
      } catch (e) {
        this.$formHelpers.showError(e);
      }
    },
    async onCardioTypeSelect(e, row) {
      try {
        await measureServices.updateMeasure({
          id: row.id,
          cardio_type: e
        });
        this.$formHelpers.showInfo("Cardio Type updated");

        this.$emit("updated");
      } catch (e) {
        this.$formHelpers.showError(e);
      }
    },
    async onCardioCluster(e, row) {
      try {
        await measureServices.updateMeasure({
          id: row.id,
          cardio_cluster: e.target.value
        });
        this.$formHelpers.showInfo("Cardio Cluster updated");

        this.$emit("updated");
      } catch (e) {
        this.$formHelpers.showError(e);
      }
    },
    async onCardioType(e, row) {
      try {
        await measureServices.updateMeasure({
          id: row.id,
          cardio_type: e.target.value
        });
        this.$formHelpers.showInfo("Cardio Type updated");

        this.$emit("updated");
      } catch (e) {
        this.$formHelpers.showError(e);
      }
    },
    async onCardioVideoProbability(e, row) {
      try {
        await measureServices.updateMeasure({
          id: row.id,
          cardio_video_probability: e.target.value
        });
        this.$formHelpers.showInfo("Cardio Video Probability updated");

        this.$emit("updated");
      } catch (e) {
        this.$formHelpers.showError(e);
      }
    },
    async onBiomechanicsCluster(e, row) {
      try {
        await measureServices.updateMeasure({
          id: row.id,
          biomechanics_cluster: e.target.value
        });
        this.$formHelpers.showInfo("Biomechanics Cluster updated");

        this.$emit("updated");
      } catch (e) {
        this.$formHelpers.showError(e);
      }
    },
    async onBiomechanicsVideoScore(e, row) {
      try {
        await measureServices.updateMeasure({
          id: row.id,
          biomechanics_video_score: e.target.value
        });
        this.$formHelpers.showInfo("Biomechanics Video Score updated");

        this.$emit("updated");
      } catch (e) {
        this.$formHelpers.showError(e);
      }
    },
    async onBiomechanicsDLCScrore(e, row) {
      try {
        await measureServices.updateMeasure({
          id: row.id,
          biomechanics_keypoint_score: e.target.value
        });
        this.$formHelpers.showInfo("Biomechanics Keypoint Score updated");

        this.$emit("updated");
      } catch (e) {
        this.$formHelpers.showError(e);
      }
    },
    async onBiomechanicsGAFScrore(e, row) {
      try {
        await measureServices.updateMeasure({
          id: row.id,
          biomechanics_gaf_score: e.target.value
        });
        this.$formHelpers.showInfo("Biomechanics GAF Score updated");

        this.$emit("updated");
      } catch (e) {
        this.$formHelpers.showError(e);
      }
    },
    async onBiomechanicsJRPScrore(e, row) {
      try {
        await measureServices.updateMeasure({
          id: row.id,
          dlc_jrg_score: e.target.value
        });
        this.$formHelpers.showInfo("Biomechanics JRP Score updated");

        this.$emit("updated");
      } catch (e) {
        this.$formHelpers.showError(e);
      }
    },
    imagepopup(e) {
      this.$refs.imageModal.show(e);
    }
  },

  watch: {
    data: {
      immediate: true,
      handler(newVal, oldVal) {
        this.disabledDates.dates = newVal.map(i => new Date(i.date_of_measure));

        this.$nextTick(() => {
          this.updateDataSet(newVal);
        });
      }
    }
  }
};
</script>

<style>
.action-icon {
  cursor: pointer;
  font-size: 16px;
}
th.vuetable-th-slot-date_of_measure.sortable {
  min-width: 150px;
  display: block;
}
img.imagepopup {
  cursor: pointer;
}
</style>
