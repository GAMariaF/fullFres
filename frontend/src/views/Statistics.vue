<template>
  <div>
    <!-- Header -->
    <b-jumbotron
      header="Statistics"
      lead="Overview of samples, runs and variants"
    >
    </b-jumbotron>

    <div class="container" id="login" v-if="items.length === 0">
    {{stats}}
      <b-row>
        <b-col>
          <b-card
            title="Number of runs"
            sub-title="Total number of runs in database"
          >
            <b-card-text>
              <h4>{{stats.runs}}</h4>
            </b-card-text>
          </b-card>
        </b-col>
        <!--  -->
        <b-col>
          <b-card
            title="Number of samples"
            sub-title="Total number of samples in database"
          >
            <b-card-text>
              <h4>{{stats.samples}}</h4>
            </b-card-text>
          </b-card>
        </b-col>
        <!--  -->
        <b-col>
          <b-card
            title="Number of variants"
            sub-title="Total number of Variants in database"
          >
            <b-card-text>
              <h4>1546</h4>
            </b-card-text>
          </b-card>
        </b-col>
      </b-row>
      <!-- Samples in the workflow -->
      <br>
      <b-row>
        
        <!--  -->
        <b-col>
          <b-card
            title="Number of samples wating for interpretation"
            sub-title="Total number of samples Waiting for interpretation"
          >
            <b-card-text>
              <h4>5</h4>
            </b-card-text>
          </b-card>
        </b-col>
        <!--  -->
        <b-col>
          <b-card
            title="Number of Samples waiting for control"
            sub-title="Total number of Samples waiting for control"
          >
            <b-card-text>
              <h4>5</h4>
            </b-card-text>
          </b-card>
        </b-col>
      </b-row>
      <!--  -->

      
      <b-row>
        <!-- Variants by class -->
        <b-col>

        </b-col>
        <!-- Variants by cancer types -->
        <b-col>

        </b-col>
        <!-- Samples by users -->
        <b-col>

        </b-col>
      </b-row>
    <!--Plotting  -->
    <b-row>
      <b-col>
        <Plotly v-if="loaded" :data="data" :layout="layout" :display-mode-bar="false" />
      
        
      </b-col>
    </b-row>
    {{stats}}
    {{stats.runs}}
    <b-button v-on:click="getstats" class="btn mr-1 btn-info"> Approve </b-button>
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
      data:[{
                x: ["1","2","3","4","5"],
                y: [10,15,13,17,11],
                type: "bar"},
                
                ],
      layout: {
                title: "Variants by class",
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
