<template>
  <div>
    <!-- Header -->
    <b-jumbotron
      header="Statistics"
      lead="Overview of samples, runs, and variants"
    >
    </b-jumbotron>

    <div class="container" id="login" v-if="items.length === 0">
      <b-row>
        <!--  -->
        <b-col>
          <b-card
            title="Number of runs"
            :sub-title="this.runText" >
            <b-card-text>
              <h4>{{stats.runs}}</h4>
            </b-card-text>
          </b-card>
        </b-col>
      </b-row>
      <br>
      <b-row> 
        <b-col>
          <b-card
            title="Samples"
            :sub-title="this.sampleText"
          >
            <b-card-text>
              <h4>{{stats.samples}}</h4>
            </b-card-text>
          </b-card>
        </b-col>
        <!--  -->
        <b-col>
          <b-card
            title="Interpretation"
            sub-title="Number of samples waiting for interpretation"
          >
            <b-card-text>
              <h4>{{stats.samples_waiting}}</h4>
            </b-card-text>
          </b-card>
        </b-col>
        <!--  -->
        <b-col>
          <b-card
            title="Control"
            sub-title="Number of samples waiting for control"
          >
            <b-card-text>
              <h4>{{stats.samples_signedoff}}</h4>
            </b-card-text>
          </b-card>
        </b-col>
      </b-row>
      <br>
      <b-row> 
        <b-col>
          <b-card
            title="Successful samples"
            sub-title="Number of successful samples"
          >
            <b-card-text>
              <h4>{{stats.samples_success}}</h4>
            </b-card-text>
          </b-card>
        </b-col>
        <!--  -->
        <b-col>
          <b-card
            title="Partial Successes"
            sub-title="Number of partial successes"
          >
            <b-card-text>
              <h4>{{stats.samples_partion}}</h4>
            </b-card-text>
          </b-card>
        </b-col>
        <b-col>
          <b-card
            title="Failed samples"
            sub-title="Number of failed samples"
          >
            <b-card-text>
              <h4>{{stats.samples_failed}}</h4>
            </b-card-text>
          </b-card>
        </b-col>
        <!--  -->

      </b-row>
      <br>
      <b-row>
        <b-col></b-col>
        <b-col>
          <b-input-group>
            <b-input v-model="startDate" placeholder="Start date: yyyymmdd"></b-input>
              <b-input v-model="endDate" placeholder="End date: yyyymmdd"></b-input>
           </b-input-group>
          <br>
          <b-button v-on:click="getstats();changeText()" type="button">Search date</b-button><span>&nbsp;</span>
        </b-col>
        <b-col></b-col>
      </b-row>

      <b-row>
      <!--Plotting variants per genelist -->    
        <b-col>
          <Plotly v-if="loaded" 
          :data="dataSamples"
          :layout="layoutSamples" 
          :display-mode-bar="false" />

        </b-col>
      </b-row>
      <br>
      <b-row>
        <!-- Number of variants -->
        <b-col>
          <b-card
            title="Number of variants"
            sub-title="Total number of Variants in database"
          >
            <b-card-text>
              <h4>{{stats.variants}}</h4>
            </b-card-text>
          </b-card>
        </b-col>
      </b-row>
      <b-row>
        <!-- Samples by users 
        
        
                      -->
        <b-col>

        </b-col>
      </b-row>
      <b-row>
      <!--Plotting variants per genelist -->    
        <b-col>
          <Plotly v-if="loaded" 
          :data="data"
          :layout="layout" 
          :display-mode-bar="false" />

        </b-col>
      </b-row>
      <b-row>
      <b-row>
      <!--Plotting variants per genelist and class-->    
        <b-col>
          <Plotly v-if="loaded" 
          :data="dataClass"
          :layout="layoutClass" 
          :display-mode-bar="false" />

        </b-col>
      </b-row>

        <!--  -->
        <b-col>
          <b-card
            title="Number of users"
            sub-title="Total number of users in database" >
            <b-card-text>
              <h4>{{stats.users}}</h4>
            </b-card-text>
          </b-card>
        </b-col>
      </b-row>
      <b-row>
      <!--Plotting samples per user -->    
        <b-col>
          <Plotly v-if="loaded" 
          :data="dataUser"
          :layout="layoutUser" 
          :display-mode-bar="false" />
        </b-col>
      </b-row>
    <!-- {{this.stats.variants_genelist.Genelist}} -->
  </div>

    <!-- Dette er hvis ikke logget inn -->
    <div class="container" id="login" v-if="items.length !== 0">
      <div class="row row justify-content-center">
        <div class="col-md-10">
          <p>Ikke logget inn</p>
        </div>
      </div>
    </div>
  </div>
</template>
<script>

import { config } from "../config.js";
import axios from "axios";
import { Plotly } from 'vue-plotly'
//import util_funcs from "@/appUtils";

export default {
  name: "statistics",
  components: { Plotly },
  data() {
    return {
      loggedInStatus: false,
      startDate: null,
      endDate: null,
      search: false,
      runText: "Total number of runs in database",
      sampleText: "Total number of samples in database",
      stats: {},
      items: [],
      loaded: true, 
      dataSamples:[{
                x: [],
                y: [],
                type: "bar"}, 
                ],
      layoutSamples: {
                title: "Samples by Genelist",
                autosize: true
            },
      data:[{
                x: [],
                y: [],
                type: "bar"}, 
                ],
      layout: {
                title: "Variants by Genelist",
                autosize: true
            },
      dataClass: [],
      layoutClass: {
                title: "Variants by Genelist and Class",
                autosize: true
            },
      dataUser:[{
                x: [],
                y: [],
                type: "bar"}, 
                ],
      layoutUser: {
                title: "Samples per User",
                autosize: true
            }
    };
  },
  methods: {
    getstats() {
      // Funksjon for å få data og tall fra backend
      const baseURI = config.$backend_url + "/api/statistics";
      axios
        .get(baseURI+this.generate_search())
        .then((response) => response.data)
        .then((data) => {
          this.stats = JSON.parse(data.data);
          this.dataSamples = [{
                x: this.stats.samples_genelist.Genelist,
                y: this.stats.samples_genelist.Freq,
                type: "bar"}, 
                ];
          this.data = [{
                x: this.stats.variants_genelist.Genelist,
                y: this.stats.variants_genelist.Freq,
                type: "bar"}, 
                ];
          this.dataUser = [{
                x: this.stats.users_samples.User_Signoff,
                y: this.stats.users_samples.Freq,
                type: "bar"}, 
                ];
          this.dataClass = [{
                x: this.stats.variants_class1.Genelist,
                y: this.stats.variants_class1.Freq,
                name: 'class1',
                type: "bar"}, 
                            {
                x: this.stats.variants_class2.Genelist,
                y: this.stats.variants_class2.Freq,
                name: 'class2',
                type: "bar"}, 
                            {
                x: this.stats.variants_class3.Genelist,
                y: this.stats.variants_class3.Freq,
                name: 'class3',
                type: "bar"}, 
                            {
                x: this.stats.variants_class4.Genelist,
                y: this.stats.variants_class4.Freq,
                name: 'class4',
                type: "bar"}, 
                            {
                x: this.stats.variants_class5.Genelist,
                y: this.stats.variants_class5.Freq,
                name: 'class5',
                type: "bar"}, 
                ];

        });
    },
    generate_search () {
      var search = "";
      if (this.startDate === null || this.startDate === ""){
        search = "00000000";
      } else {
        search = this.startDate;
      }
      if (this.endDate === null || this.endDate === ""){
        search += "00000000";
      } else {
        search += this.endDate;
      }
      return(search)
    },
    changeText() {
      this.runText = "Number of runs in search"
      this.sampleText = "Number of samples in search"
    }
  },
  created: function () {
    // initstore sjekk innlogging
    this.$store.dispatch("initStore");
    this.getstats();
  },
  watch: {
    state(newState, oldState) {
      console.log(`State changed from ${oldState} to ${newState}`);
    },
  },
  computed: {
    state() {
      return this.$store.getters.loggedInStatus;
    },
  },
};
</script>
