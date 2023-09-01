<template>
  <div class="icon-cards-row">
    <glide-component :settings="glideIconsOption">
      <icon-card
        title="Horse Count"
        icon="iconsminds-bar-chart-4"
        :value="14"
      />
      <icon-card
        title="Active Horses"
        icon="iconsminds-monitor-analytics"
        :value="32"
      />
      <icon-card title="Elite Horses" icon="iconsminds-trophy" :value="74" />
    </glide-component>
  </div>
</template>
<script>
import GlideComponent from "../../components/Carousel/GlideComponent";
import IconCard from "../../components/Cards/IconCard";

export default {
  components: {
    "glide-component": GlideComponent,
    "icon-card": IconCard
  },
  data() {
    return {
      glideIconsOption: {
        gap: 5,
        perView: 3,
        type: "carousel",
        breakpoints: {
          320: {
            perView: 1
          },
          576: {
            perView: 2
          },
          1600: {
            perView: 3
          },
          1800: {
            perView: 3
          }
        },
        hideNav: true
      }
    };
  }
};
</script>
