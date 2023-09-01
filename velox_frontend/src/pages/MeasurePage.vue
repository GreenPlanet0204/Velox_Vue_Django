<template>
<div>
    <h1>Edit Measure</h1>
    <measure-form :measure-id="$route.params.id"></measure-form>
</div>
</template>

<script>
import MeasureForm from "../components/MeasureForm";

export default {
  name: "MeasurePage",
  components: {MeasureForm}
}
</script>

<style scoped>

</style>
