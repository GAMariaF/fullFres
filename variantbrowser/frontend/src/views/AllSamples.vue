<template>
  <div>
    <br/>
    <h1>All samples</h1>
    <br/>
    <b-row>
      
        <b-col>
          <b-input-group>
            <b-input v-model="runid" placeholder="Run ID"></b-input>
            <b-input v-model="sampleid" placeholder="Sample ID"></b-input>
            <b-form-select
                :options="geneListOptions"
                class="py-sm-0 form-control"
                v-model="selectedGeneList"
                >
                <template #first>
                  <b-form-select-option :value="null" disabled>Gene Lists</b-form-select-option>
              </template> 
              </b-form-select>
            <b-input v-model="startDate" placeholder="Start date: yyyymmdd"></b-input>
            <b-input v-model="endDate" placeholder="End date: yyyymmdd"></b-input>
           </b-input-group>
          </b-col>
          
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
            sort-by="Seq_Date"
            :sort-desc="true" 
          >
          <!-- Formatting Type column -->
          <template #cell(Nr)="data">
            {{ data.index + 1 }}
          </template>
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

export default {
  name: "allsampletable",
  data() {
    return {
      loggedInStatus: false,
      small: true,
      sampleID: "",
      selectedSample: "",
      items: [],
      fields: [{key: "Nr", label: "Nr", sortable: false},
              {key: "runid", label: "Run id", sortable: true}, 
              {key: "sampleid", label: "Sample id", sortable: false},
              {key: "Genelist", label: "Gene List", sortable: true},
              {key: "Seq_Date", label: "Sequencing Date", sortable: true},
              {key: "Status", label: "Status", sortable: true},
              {key: "Date_Signoff", label: "Date Sign off", sortable: true},
              {key: "User_Signoff", label: "User Sign off", sortable: false},
              {key: "Date_Approval", label: "Date Approval", sortable: true},
              {key: "User_Approval", label: "User Approval", sortable: false}],

      filter: '',
      runid: "",
      sampleid: "",
      selectedGeneList: null,
      startDate: "",
      endDate: "",
      geneListOptions: config.geneListOptions,
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
      var geneList = ""
      if (this.selectedGeneList === null) {
        geneList = "";
      } else {
        geneList = this.selectedGeneList;
      }
      var search = "|" + this.runid + "|" + this.sampleid + "|" + geneList + "|" + this.startDate + "|" + this.endDate
      console.log(search)
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
