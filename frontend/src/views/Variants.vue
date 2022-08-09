<template>
  <div>
  
    <variant-table :locked="locked"/>
    
  </div>
</template>



<script>
import VariantTable from "../components/VariantTable";

export default {
  props: ['locked'],
  components: {
    VariantTable,
  },
  data() {
    return {
      sampleid: this.$route.params.id,
    
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
