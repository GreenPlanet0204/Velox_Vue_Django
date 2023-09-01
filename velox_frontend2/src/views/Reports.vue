<template>
  <div>
    <b-row>
      <b-colxx xxs="12">
        <div class="separator mb-5"></div>
      </b-colxx>
    </b-row>
    <b-row>
      <b-colxx xxs="12">
        <b-card class="mb-4" title="Reports"> 
          <b-row>
            <b-col>
              <HorsesList ref="horseList" @updated="onHorsesTableUpdate"></HorsesList>
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
import HorsesList from "@/views/horses/HorsesList";

export default {
  props: {},
  components: {
    vSelect,
    HorsesList
  },

  data() {
    return {
      localData: [],
      filteredData: [],
    };
  },
  async mounted() {
  },
  methods: {
    async fetchData() {
      let payload = {};
      this.$refs.horseList.fetchData(payload);
    },
    onHorsesTableUpdate() {
      this.fetchData();
    }
  },
  watch: {
  }
};
</script>

<style scoped>
.icon {
  font-size: 28px;
}
</style>

