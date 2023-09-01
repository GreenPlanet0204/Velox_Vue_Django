<template>
  <div v-show="isActive">
    <slot></slot>
  </div>
</template>

<script>
export default {
  name: "tab",
  props: {
    name: {
      default: ""
    },
    desc: {},
    type: {
      default: "tab"
    },
    selected: {
      default: false
    },
    done: {
      default: false
    },
    validate: {
      type: Function,
      default: () => {
        return true;
      }
    },
    submit: {
      type: Function,
      default: () => {
        return true;
      }
    }
  },
  data() {
    return {
      isActive: false,
      isDone: false
    };
  },
  created() {
    this.isActive = this.selected;
    this.isDone = this.done;
  }
};
</script>

<style></style>
