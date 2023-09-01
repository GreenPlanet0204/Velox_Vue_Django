<template>
  <div>
    <b-row>
      <b-colxx xxs="12">
        <div class="separator mb-5"></div>
      </b-colxx>
    </b-row>
    <b-row>
      <b-colxx xxs="12">
        <b-card class="mb-4" title="Home">
          <b-row>
            <b-colxx xl="8" lg="12">
              <HorseStatsCarousel></HorseStatsCarousel>
            </b-colxx>
            <b-colxx xl="4" lg="12" class="mb-4">
              <!--  <recent-orders></recent-orders> -->
              <b-card class="mb-4 text-center">
                <b-button
                  class="mb-2"
                  block
                  size="xs"
                  variant="primary"
                  @click="onAddHorseClick"
                  >Add a Horse</b-button
                >
                <b-button
                  class="mb-2"
                  block
                  size="xs"
                  variant="primary"
                  @click="onAddDNAClick"
                  >Add DNA to Horse</b-button
                >
                <b-button
                  class="mb-2"
                  block
                  size="xs"
                  variant="primary"
                  @click="onAddImageMeasurementClick"
                  >Add Conformation Measurement</b-button
                >
                <b-button
                  class="mb-2"
                  block
                  size="xs"
                  variant="primary"
                  @click="onAddBiomechanicsVideoClick"
                  >Add Biomechanics Video</b-button
                >
                <b-button
                  class="mb-2"
                  block
                  size="xs"
                  variant="primary"
                  @click="onAddCardioVideoClick"
                  >Add Cardio Video</b-button
                >
              </b-card>
            </b-colxx>
          </b-row>
        </b-card>
      </b-colxx>
    </b-row>
    <AddHorseModal ref="AddHorseModal"></AddHorseModal>
    <DNADetailsModal ref="DNADetailsModal"></DNADetailsModal>
    <ImageMeasurementModal ref="imageMeasurementModal"></ImageMeasurementModal>
    <BiomechanicsVideoModal
      ref="biomechanicsVideoModal"
    ></BiomechanicsVideoModal>
    <CardioVideoModal ref="cardioVideoModal"></CardioVideoModal>
  </div>
</template>

<script>
import HorseStatsCarousel from "@/views/home/HorseStatsCarousel";
import RecentOrders from "@/containers/dashboards/RecentOrders";
import SalesChartCard from "@/containers/dashboards/SalesChartCard";
import AddHorseModal from "./AddHorseModal";
import DNADetailsModal from "./DNADetailsModal";
import ImageMeasurementModal from "./ImageMeasurementModal";
import BiomechanicsVideoModal from "./BiomechanicsVideoModal.vue";
import CardioVideoModal from "./CardioVideoModal.vue";

export default {
  components: {
    HorseStatsCarousel,
    RecentOrders,
    SalesChartCard,
    AddHorseModal,
    DNADetailsModal,
    ImageMeasurementModal,
    BiomechanicsVideoModal,
    CardioVideoModal
  },
  data() {
    return {};
  },
  async mounted() {},
  methods: {
    onAddHorseClick() {
      this.$refs["AddHorseModal"].show();
    },
    onAddDNAClick() {
      this.$refs["DNADetailsModal"].show();
    },
    onAddImageMeasurementClick() {
      this.$refs["imageMeasurementModal"].show();
    },
    onAddBiomechanicsVideoClick() {
      this.$refs["biomechanicsVideoModal"].show();
    },
    onAddCardioVideoClick() {
      this.$refs["cardioVideoModal"].show();
    }
  }
};
</script>
