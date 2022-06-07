<template>
  <b-container fluid v-show="state">
    <b-row>
      <b-col cols="4">
        <h2>Signed off samples:</h2>
        <b-table
          selectable
          select-mode="single"
          @row-selected="sampleRowSelected"
          striped
          hover
          outlined
          :items="items"
          :fields="fields"
          :small="small"
        ></b-table>
      </b-col>
      <b-col>
        <h3 v-if="selectedSample === ''">No sample selected!</h3>
        <div v-if="selectedSample !== ''">
          Her skal variantene komme som en tabell
          <br />
              <b-table
      selectable
      select-mode="single"
      @row-selected="rowSelected"
      striped
      hover
      outlined
      :filter="filter"
      :filter-included-fields="filterOn"
      :items="variants"
      :fields="variantFields"
      :small="small"
    >

     <template #cell(Info)="row">
          <b-button
            size="sm"
            @click="openInfoModal(row.item, row.index, $event.target)"
            class="mr-1"
          >
            Info
          </b-button>
        </template>
    </b-table>
          <br />
          {{ selectedSample }}
        </div>
        {{ state }}
        {{ user }}
      </b-col>
    </b-row>
  </b-container>
</template>
<script>
import axios from "axios";
import { config } from "../config.js";

export default {
  components: {},
  data() {
    return {
      loggedInStatus: false,
      small: true,
      sampleID: "",
      selectedSample: "",
      items: [],
      fields: ["sampleid"],
      variantFields: [
        {key: "CHROM",
        label: "Kromosom"},
        {key: "POS"},
        {key: "REF"},
        {key: "ALT"},
        {key: "FILTER"},
        {key: "Info"}
        ],
        filter: "true",
        filterOn: ["visibility"],

    };
  },
  created: function () {
    this.$store.dispatch("initStore"); // hent state for logged in?
    this.getsamples();
    
  },
  methods: {
    rowSelected(items) {
      if (items.length===1) {
        this.selectedVariant = items[0].Variant;
        console.log("tester linje 100")
      } else if (items.length===0) {
        this.selectedVariant = "";
        console.log("unselected")
      }
    },
    sampleRowSelected(items) {
      if (items.length === 1) {
        this.selectedSample = items[0].sampleid;
        // Get variants for that sample:
        this.$store.dispatch("initVariantStore", {"sample_id": this.selectedSample, "selected": 'empty'});
        this.variants =  this.$store.getters.variants;
        // this.signOff();
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
        .then((data) => (this.items = data.data));
    }
  },
  watch: {
    state(newState, oldState) {
      console.log(`State changed from ${oldState} to ${newState}`);
    },
    user(newUser, oldUser) {
      console.log(`State changed from ${oldUser} to ${newUser}`);
    },
  },
  computed: {
    state() {
      return this.$store.getters.loggedInStatus;
    },
    user() {
      return this.$store.getters.username;
    },
  },
};
</script>
