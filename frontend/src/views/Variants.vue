<template>
  <div>
  
    <variant-table  :loading="loading"   />
  </div>
</template>



<script>
import VariantTable from "../components/VariantTable";

export default {
  components: {
    VariantTable,
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
