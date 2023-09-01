<template>
  <b-modal id="modalId" ref="modalRef" size="lg">
    <div slot="modal-title">
    </div>
    <img :src="image" class="imagemodel"/>
    <template slot="modal-footer">
      <b-button variant="secondary" @click="onModalCancel">Cancel</b-button>
    </template>
  </b-modal>
</template>

<script>

export default {
  data() {
    return {
      image:'',
    };
  },
  methods: {
    show(payload) {
      this.image = payload.image.url;
      this.$refs.modalRef.show();
    },
    hide() {
      this.$refs.modalRef.hide();
    },
    onModalCancel() {
      this.hide();
    },
  },
};
</script>

<style>
img.imagemodel {
    width: 100%;
}
</style>
