<template>
  <div>
      <h1>hei</h1>
    <all-variant-table  :loading="loading"   />
  </div>
</template>
<script>
import AllVariantTable from "../components/AllVariantTable";

export default {
  components: {
    AllVariantTable,
  },
  data() {
    return {
      sampleid: this.$route.params.id,
      loading:  false
    };
  },
  created: function () {
    this.$store.dispatch("initStore");
  },
  methods: {},
  watch: {},
  computed: {
    state() {
      return this.$store.getters.loggedInStatus;
    }
  }
};
</script>
