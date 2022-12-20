<template>
  <div>
    <!-- Header -->
    <b-jumbotron
      header="Statistics"
      lead="Overview of samples, runs and variants"
    >
    </b-jumbotron>

    <div class="container" id="login" v-if="items.length === 0">
      <b-row>
        <!--  -->
        <b-col>
          <b-card
            title="Number of runs"
            sub-title="Total number of runs in database" >
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
            title="Number of samples"
            sub-title="Total number of samples in database"
          >
            <b-card-text>
              <h4><br>{{stats.samples}}</h4>
            </b-card-text>
          </b-card>
        </b-col>
        <!--  -->
        <b-col>
          <b-card
            title="Number of samples wating for interpretation"
            sub-title="Total number of samples Waiting for interpretation"
          >
            <b-card-text>
              <h4>{{stats.samples_waiting}}</h4>
            </b-card-text>
          </b-card>
        </b-col>
        <!--  -->
        <b-col>
          <b-card
            title="Number of samples waiting for control"
            sub-title="Total number of Samples waiting for control"
          >
            <b-card-text>
              <h4>{{stats.samples_signedoff}}</h4>
            </b-card-text>
          </b-card>
        </b-col>
      </b-row>
      <br>
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
        .get(baseURI)
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
