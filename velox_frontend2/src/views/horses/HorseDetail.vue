<template>
  <b-modal id="modalId" ref="modalRef" size="xl">
    <div slot="modal-title">
      <span class="icon success">
        <i class="iconsminds-add-file"></i>
      </span>
      <span>Horse Detail</span>
    </div>
    <HorseDetailSingle :id="id" :getdata="getdata"></HorseDetailSingle>

    <template slot="modal-footer">
      <b-button variant="secondary" @click="onModalCancel">Cancel</b-button>
    </template>
  </b-modal>
</template>

<script>

import HorseDetailSingle from "@/views/horses/HorseDetailSingle";

export default {
  props: {
		getdata: Function,
	},
  components: {
    HorseDetailSingle
  },
  data() {
    return {
        form: {
      },
      id: [],
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
        this.id = payload
    },

    onModalCancel() {
      this.hide();
    },
  },

};
</script>
