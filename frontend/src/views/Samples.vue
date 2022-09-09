<template>
  <div>
    <br>
    <br>
    <div class="container" id="login" v-if="items.length===0">
      <b-col cols="6">
        <h3>No samples ready for interpretation.<br> Go have a coffee!</h3> 
        <template>
          <br>
          <h3>Or</h3> 
          <br>
          <br>
          <div>
            <label for="importFolderInput"><h3> Import latest samples from folder:</h3></label>
            <br>
            <br>
            <b-form-input id="importFolderInput" v-model="importFolder" :placeholder="importFolder"></b-form-input>
            <div class="mt-2"></div>
            </div>
        </template>
        <br>
        <b-button v-on:click="loadData" class="btn mr-1 btn-info"> IMPORT SAMPLES </b-button>
      </b-col>
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
          <template>
            <br>
            <br>
            <br>
            <div>
              <label for="importFolderInput"><h5> Import latest samples from folder:</h5></label>
              <br>
              <br>
              <b-form-input id="importFolderInput" v-model="importFolder" :placeholder="importFolder"></b-form-input>
              <div class="mt-2"></div>
              </div>
          </template>
          <br>
          <b-button v-on:click="loadData" class="btn mr-1 btn-info"> LOAD DATA </b-button>
          
        </b-col>
        </div>
      </div>
    </div>
    <br>
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
        .then(window.location.reload(true) );
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
        params: { id: this.selectedSample, locked: false },
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
