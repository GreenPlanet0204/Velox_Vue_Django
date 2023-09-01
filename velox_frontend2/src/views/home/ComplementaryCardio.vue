<template>
  <b-modal id="modalId" ref="modalRef" size="md">
    <h1>Is this Cardio Video the complimentary video to the Biomechanics video for this horse on {{measure_date}}?</h1>
    <template slot="modal-footer">
      <b-button variant="primary" class="mr-1" @click="onModalYes">Yes</b-button>
      <b-button variant="primary" @click="onModalCancel">No</b-button>
    </template>
  </b-modal>
</template>

<script>
export default {
  data() {
    return {
        measure_date:'',
    };
  },
  async mounted() {
  },
  methods: {
    show(payload) {
      this.updateData(payload);
      this.$refs.modalRef.show();
    },

    hide() {
      this.$refs.modalRef.hide();
    },

    updateData(payload) {
      this.measure_date = payload
    },

    onModalCancel() {
      this.hide();
      this.$formHelpers.showError(
            "Video already exists on this date please select another date of measure"
      );
    },

     onModalYes() {
      this.hide();
    },
  },

};
</script>
