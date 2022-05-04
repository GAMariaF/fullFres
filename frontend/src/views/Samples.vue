<template>

  <div>
    {{loggedInStatus}}
    <h1>Select the sample to interpret</h1>
    <b-table selectable select-mode="single" @row-selected="rowSelected" striped hover outlined :items="items" :fields="fields" :small="small"></b-table>
  </div>

</template>
<script>

//import { config } from '../config.js'
//import util_funcs from "@/appUtils";


export default {
  name: "varianttable", 
  data() {
      return {
          loggedInStatus: false,
          small:true,
          sampleID: "",
          selectedSample: "",
          items: [],
          fields: [
        'Sample'
      ]
      }
  },
  methods: {
      rowSelected(items) {
          this.selectedSample = items[0].Sample
      },
      getsamples(){
        // Funksjon for å få samples fra backenc
        // util_funcs.query_backend(config.$backend_url,'samples').then(result => this.items = JSON.parse(result['data']))
        console.log("metode testaxios")
      }
  },
  created: function () {
    // initstore sjekk innlogging
    this.$store.dispatch("initStore")
    this.token = this.$store.getters.token;
    this.loggedInStatus = this.$store.getters.loggedInStatus;
    this.getsamples()
  },
  watch: {
      selectedSample: function () {
          this.$router.push({name: 'Variants', params: {id: this.selectedSample}})
      }
  }
};
</script>
