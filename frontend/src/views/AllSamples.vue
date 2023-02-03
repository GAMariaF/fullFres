<template>
  <div>
    <br/>
    <h1>All samples</h1>
    <br/>
    <b-row>
      <b-col></b-col>
        <b-col>
          <b-input-group>
            <b-input v-model="runid" placeholder="Run ID"></b-input>
            <b-input v-model="sampleid" placeholder="Sample ID"></b-input>
           </b-input-group>
          </b-col>
          <b-col></b-col>
        </b-row>
        <br/>
        <b-button v-on:click="getsamples()" type="button">Search</b-button><span>&nbsp;</span>
        <br/>
        <br/>
    <div class="container" id="login">
      <div class="row row justify-content-center">
        <div class="col-md-10">
          
          <b-table
            selectable
            select-mode="single"
            @row-selected="rowSelected"
            striped
            hover
            outlined
            label-sort-asc=""
            label-sort-desc=""
            label-sort-clear=""
            :items="items"
            :fields="fields"
            :small="small"
            
          >
          <!-- Formatting Type column -->
          <template #cell(runid)="data">
            <b class="text-info">{{ data.value.toUpperCase() }}</b>
          </template>
          </b-table>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { config } from "../config.js";
import axios from "axios";
//import util_funcs from "@/appUtils";

export default {
  name: "allsampletable",
  data() {
    return {
      loggedInStatus: false,
      small: true,
      sampleID: "",
      selectedSample: "",
      items: [],
      fields: [{key: "runid", label: "Run id", sortable: true}, 
              {key: "sampleid", label: "Sample id", sortable: true},
              {key: "Seq_Date", label: "Sequencing Date", sortable: false},
              {key: "Status", label: "Status", sortable: false},
              {key: "Date_Signoff", label: "Date Sign off", sortable: true},
              {key: "User_Signoff", label: "User Sign off", sortable: false},
              {key: "Date_Approval", label: "Date Approval", sortable: true},
              {key: "User_Approval", label: "User Approval", sortable: false}],

      filter: '',
      runid: "",
      sampleid: "",
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
      var search = "|date"
      if (this.runid !== ""){
        search = "|runid|"+this.runid;
      } else if(this.sampleid !== "") {
        search = "|sampleid|"+this.sampleid;
      }
      console.log("metode testaxios");
      const baseURI = config.$backend_url + "/api/allsamples";
      axios
        .get(baseURI+search)
        .then((response) => response.data)
        .then((data) => (this.items = data.data));
      this.runid = "";
      this.sampleid = "";
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
        params: { id: this.selectedSample, locked: true },
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
