<template>
  <div>
    <variant-table  :loading="loading"   />
    
  </div>
</template>
<script>
import VariantTable from "../components/VariantTable";
import { config } from '../config.js'
import util_funcs from "@/appUtils";


export default {
  
  components: {
    VariantTable,
  },
  data() {
    return {
      variants: {},
      sampleid: this.$route.params.id,
      loading: false
    };
  },
  created: function () {
    this.getvariants()
  },
  methods: {
    getvariants(){
      util_funcs.query_backend(config.$backend_url,'variants').then(result => this.variants = JSON.parse(result['data']))
    }
  },
  watch: {},
};
</script>
