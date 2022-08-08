<template>
  <div>
    <div class="container" id="login" v-if="items.length===0">
    <h3>No samples ready for interpretation.<br> Go have a coffee!</h3> 
    </div>
    <div class="container" id="login" v-if="items.length!==0">
      <div class="row row justify-content-center">
        <div class="col-md-10">
        <b-col cols="6">
        
          <h1>Select sample for interpretation</h1>
          <br>
          <b-table
            selectable
            select-mode="single"
            @row-selected="rowSelected"
            striped
            hover
            outlined
            :items="items"
            :fields="fields"
            :small="small"
          >
          <!-- Formatting Type column -->
          <template #cell(runid)="data">
            <b class="text-info">{{ data.value.toUpperCase() }}</b>
          </template>
          </b-table>
          
        </b-col>
        </div>
      </div>
    </div>
    <br>
          <br>
          <h5> Import latest data from import folder </h5>
          
            <template>
              <div>
                <label for="importFolderInput">Current import folder is:</label>
                <b-form-input id="importFolderInput" v-model="importFolder" :placeholder="importFolder"></b-form-input>
                  <div class="mt-2"></div>
                </div>
            </template>



          <br>
          <b-button v-on:click="loadData" class="btn mr-1 btn-info"> LOAD DATA </b-button>
  </div>
</template>
<script>
import { config } from "../config.js";
import axios from "axios";
//import util_funcs from "@/appUtils";

export default {
  name: "varianttable",
  data() {
    return {
      importFolder: 'test',
      loggedInStatus: false,
      small: true,
      sampleID: "",
      selectedSample: "",
      items: [],
      fields: [{key: "runid", label: "Run id"}, 
              {key: "sampleid", label: "Sample id"}],
    };
  },
  methods: {
    rowSelected(items) {
      if (items.length === 1) {
        this.selectedSample = items[0].sampleid;

      } else if (items.length === 0) {
        this.selectedSample = "";
      }
    },
    getsamples() {
      // Funksjon for å få samples fra backenc
      // util_funcs.query_backend(config.$backend_url,'samples').then(result => this.items = JSON.parse(result['data']))
      console.log("metode testaxios");
      const baseURI = config.$backend_url + "/api/samples";
      axios
        .get(baseURI)
        .then((response) => response.data)
        .then((data) => {
          (this.items = data.data)
          this.importFolder = data.message.replace("Success fetching samples. Import folder is: ", "");
          });
        
    },
    loadData() {
      // This is to import new data downloaded from Genexus GUI. 
      console.log("Load new data")
      const baseURI = config.$backend_url + "/api/import";
      axios
        .get(baseURI, { params: [this.importFolder] })
    },
  },
  created: function () {
    // initstore sjekk innlogging
    this.$store.dispatch("initStore");
    this.getsamples();
  },
  watch: {
    state(newState, oldState) {
      console.log(`State changed from ${oldState} to ${newState}`);
    },
    selectedSample: function () {
      this.$router.push({
        name: "Variants",
        params: { id: this.selectedSample },
      });
    },
  },
  computed: {
    state() {
      return this.$store.getters.loggedInStatus;
    },
  },
};
</script>
