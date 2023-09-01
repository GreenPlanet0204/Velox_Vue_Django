//import api from '@/services/axios';

const DictionaryService = {
  async fetchHorseTypeOptions() {
    return ["Flat", "National Hunt"];
  },
  async fetchHorseSexOptions() {
    return ["Male", "Female"];
  },
  async fetchHorseStatuses() {
    return ["Unnamed", "Unraced", "Live", "Retired"];
  },
  async fetchOptimalDistanceOptions() {
    return ["5-7f", "6-8f", "8-10f", "10f+"];
  },
  async fetchCountries() {
    return ["All", "Australia", "Europe", "Overseas", "North America"];
  },
  async fetchDNAMarkersOptions() {
    return {
      distance1: ["CC", "CT", "TT"],
      distance2: ["CC", "CT", "TT"],
      size: ["CC", "CT", "TT"],
      class1: ["AA", "AC", "CC"],
      class2: ["GG", "GA", "AA"],
      class3: ["AA", "AC", "CC"]
    };
  },
  async fetchVideoQualityOptions() {
    return ["Poor", "OK", "Good"];
  },
  async fetchCardioTypeOptions() {
    return [
      "Bullseye",
      "Turf/Off-speed Dirt",
      "Irregular/Immature",
      "Small/Sprint"
    ];
  }
};

export default DictionaryService;
