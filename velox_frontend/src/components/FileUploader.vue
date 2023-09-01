<!--<template>-->
<!--  <div>-->
<!--    <div class="col-xs-3">-->
<!--      &lt;!&ndash; Styled &ndash;&gt;-->
<!--      <div v-if="!displaySearch">-->
<!--        <b-form-file-->
<!--          v-model="file"-->
<!--          :state="Boolean(file)"-->
<!--          placeholder="Choose a file or drop it here..."-->
<!--          drop-placeholder="Drop file here..."-->
<!--        ></b-form-file>-->

<!--        <b-button v-if="displayUploadButton" @click="uploadFile" :disabled="!this.file">Upload</b-button>-->
<!--        <b-button v-if="displayUploadButton" @click="clearFile">Clear</b-button>-->
<!--      </div>-->


<!--    </div>-->
<!--  </div>-->
<!--</template>-->

<!--<script>-->
<!--import axios from "axios";-->

<!--let searchAPIUrl = "/cmmc/api/document/search/";-->
<!--let documentAPIUrl = "/cmmc/api/document/"-->

<!--export default {-->
<!--  name: "FileUploader",-->
<!--  props: {-->
<!--    "displayUpload":-->
<!--      {-->
<!--        type: Boolean,-->
<!--        default: true-->
<!--      },-->
<!--    "displaySearchArea": {-->
<!--      type: Boolean,-->
<!--      default: true-->
<!--    }-->
<!--  },-->
<!--  data() {-->
<!--    return {-->
<!--      file: null,-->
<!--      searchQuery: "",-->
<!--      displaySearch: false,-->
<!--      displayUploadButton: this.displayUpload,-->
<!--      searchResults: [],-->
<!--      documentFields: [-->
<!--        {key: "nameurl", "label": "Name"},-->
<!--        {key: "date_created", label: 'Upload Date'},-->
<!--        {key: "select"}-->
<!--      ],-->
<!--      selectedFile: null-->
<!--    }-->
<!--  },-->
<!--  watch: {-->
<!--    "file": function () {-->
<!--      this.$emit('file-set');-->
<!--    }-->
<!--  },-->
<!--  computed: {-->
<!--    buttonSwitchTech() {-->
<!--      if (this.displaySearch) {-->
<!--        return "Upload new file"-->
<!--      } else {-->
<!--        return "Search uploaded files"-->
<!--      }-->
<!--    }-->
<!--  },-->
<!--  methods: {-->
<!--    fileSet(fileId) {-->
<!--      //fires event after file has been uploaded with fileId-->
<!--      this.$emit('file-set', fileId);-->
<!--    },-->
<!--    clearFile() {-->
<!--      this.file = null-->
<!--      this.selectedFile = null;-->
<!--    },-->
<!--    searchFiles() {-->
<!--      if (this.searchQuery === "") {-->
<!--        this.searchResults = [];-->
<!--      } else if (this.searchQuery.length > 3) {-->
<!--        axios.get(searchAPIUrl, {params: {q: this.searchQuery}}).then(resp => {-->
<!--            this.searchResults = resp.data-->
<!--          }-->
<!--        ).catch(error => {-->
<!--          if (error.response) {-->
<!--            this.$bvToast.toast(`${error.response.data.detail}`, {-->
<!--              title: 'Error',-->
<!--              variant: 'danger'-->
<!--            })-->
<!--          }-->
<!--        })-->
<!--      }-->
<!--    },-->
<!--    selectExisting() {-->
<!--      this.displaySearch = !this.displaySearch-->
<!--    },-->
<!--    selectExistingFile(file) {-->
<!--      this.selectedFile = file-->
<!--      this.$emit('file-set', file.id);-->
<!--    },-->
<!--    uploadFile() {-->
<!--      if (this.file) {-->
<!--        let formData = new FormData();-->
<!--        formData.append('document', this.file);-->
<!--        formData.append('name', this.file.name);-->

<!--        return new Promise((resolve, reject) => {-->
<!--          axios.post(documentAPIUrl, formData, {-->
<!--            headers: {-->
<!--              'Content-Type': 'multipart/form-data'-->
<!--            }-->
<!--          }).then(resp => {-->
<!--            this.file = null;-->
<!--            let fileId = resp.data.id-->
<!--            this.fileSet(fileId);-->
<!--            resolve(resp);-->
<!--          })-->
<!--            .catch(error => {-->
<!--              reject(error)-->
<!--            })-->
<!--        })-->
<!--      }-->
<!--    }-->
<!--  }-->
<!--}-->
<!--</script>-->
