<template>
  <b-row>
    <b-colxx xxs="12">
      <vue-dropzone
        ref="vue-dropzone"
        id="vue-dropzone"
        :options="dropzoneOptions"
        @vdropzone-sending="onDropzoneSending"
        @vdropzone-processing="onDropzoneProcessing"
        @vdropzone-complete="onDropzoneComplete"
        @vdropzone-file-added="onDropzoneFileAdded"
      ></vue-dropzone>
    </b-colxx>
  </b-row>
</template>
<script>
import VueDropzone from "vue2-dropzone";
export default {
  components: {
    "vue-dropzone": VueDropzone
  },
  data() {
    return {
      dropzoneOptions: {
        url: "https://httpbin.org/post",
        uploadMultiple: false,
        autoQueue: false,
        thumbnailHeight: 160,
        maxFilesize: 100,
        previewTemplate: this.dropzoneTemplate(),
        method: "PUT",
        headers: {
          "Cache-Control": ""
          // "Content-Type": "video/mp4"
          // "Content-Type": "image/jpeg"
        },
        sending: function(file, xhr) {
          var _send = xhr.send;
          xhr.send = function() {
            _send.call(xhr, file);
          };
        }
      }
    };
  },
  methods: {
    dropzoneTemplate() {
      return `<div class="dz-preview dz-file-preview mb-3">
                  <div class="d-flex flex-row "> <div class="p-0 w-30 position-relative">
                      <div class="dz-error-mark"><span><i></i>  </span></div>
                      <div class="dz-success-mark"><span><i></i></span></div>
                      <div class="preview-container">
                        <img data-dz-thumbnail class="img-thumbnail border-0" />
                        <i class="simple-icon-doc preview-icon"></i>
                      </div>
                  </div>
                  <div class="pl-3 pt-2 pr-2 pb-1 w-70 dz-details position-relative">
                    <div> <span data-dz-name /> </div>
                    <div class="text-primary text-extra-small" data-dz-size /> </div>
                    <div class="dz-progress"><span class="dz-upload" data-dz-uploadprogress></span></div>
                    <div class="dz-error-message"><span data-dz-errormessage></span></div>
                  </div>
                  <a href="#" class="remove" data-dz-remove> <i class="glyph-icon simple-icon-trash"></i> </a>
                </div>
        `;
    },
    onDropzoneProcessing(file) {},
    async enqueueFile(file) {
      this.$refs["vue-dropzone"].setOption("url", file.url);

      let headers = {
        "Cache-Control": "",
        "Content-Type": file.type
      };
      this.$refs["vue-dropzone"].setOption("headers", headers);

      await this.$refs["vue-dropzone"].dropzone.enqueueFile(file);
    },
    async onDropzoneFileAdded(file) {
      this.$emit("file-added", file);

      //let s = await this.$refs["vue-dropzone"].dropzone.getAcceptedFiles();

      let s = await this.$refs["vue-dropzone"].dropzone.files[0];
      console.log("onDropzoneFileAdded:", JSON.stringify(s));
    },
    onDropzoneSending(file, xhr, formData) {},
    onDropzoneComplete(response) {
      this.$emit("completed", response);
    },
    removeAllFiles() {
      this.$refs["vue-dropzone"].removeAllFiles();
    }
  }
};
</script>
