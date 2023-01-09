<template>
  <div>
    <h1>All samples</h1>
    <br>
    <div class="container" id="login">
      <div class="row row justify-content-center">
        <div class="col-md-10">
          <b-col lg="6" class="my-1">
           <b-input-group size="sm">
              <b-input v-model="filter" placeholder="Filter table.."></b-input> 
           </b-input-group>
          </b-col>

          
          
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
            :filter="filter"
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
              {key: "Date_Signoff", label: "Date Sign off", sortable: true},
              {key: "User_Signoff", label: "User Sign off", sortable: false},
              {key: "Date_Approval", label: "Date Approval", sortable: true},
              {key: "User_Approval", label: "User Approval", sortable: false},],
      filter: '',
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
      const baseURI = config.$backend_url + "/api/allsamples";
      axios
        .get(baseURI)
        .then((response) => response.data)
        .then((data) => (this.items = data.data));
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
