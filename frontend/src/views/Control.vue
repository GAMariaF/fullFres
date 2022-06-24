<template>
  <b-container fluid v-show="state">
    <b-row>
      <b-col cols="3">
        <br>
        <h2>Signed off samples</h2>
        <br>
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
        >
        <template #cell(runid)="data">
          <b class="text-info">{{ data.value.toUpperCase() }}</b>
        </template>        
        </b-table>
      </b-col>
      <b-col>
        <br>
        <h2 v-if="selectedSample === ''">Please select a sample</h2>
        <div v-if="selectedSample !== ''">
          <h2>Variants for sample {{ selectedSample }}</h2>
          <br><br>
          <h5>Gene List: <b>{{this.variants[0].Genliste}}</b> | Tumor %: <b>{{this.variants[0].Perc_Tumor}}</b></h5>
          <br>          
          <b-table
            selectable
            select-mode="single"
            @row-selected="rowSelected"
            striped
            hover
            outlined
            :items="variants"
            :fields="variantFields"
            :small="small"
          >
            <!-- Adding index column -->
            <template #cell(Nr)="data">
              {{ data.index + 1 }}
            </template>
            <!-- Formatting Type column -->
            <template #cell(Type)="data">
              <b class="text-info">{{ data.value.toUpperCase() }}</b>
            </template>
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
          <br><br>
            <b-button v-on:click="approve" class="btn mr-1 btn-info"> Approve </b-button>
          <br><br>
        </div>
        {{ state }}
        {{ user }}
      </b-col>
    </b-row>
    <b-modal
    :id="infoModal.id"
    :title="infoModal.title"
    ok-only
    size="lg"
    @hide="
    resetInfoModal();
    "
    >
      <b-container fluid>
          <b-row class="mb-1">
            <b-col cols="6">
              <pre>  
                <div class="table-responsive">
                  <table class="table-hover">
                    <thead>
                      <tr>
                        <th>Key</th>
                        <th>Value</th>
                      </tr>
                    </thead>
                    <tbody >
                      <tr v-for="(value, name) in variants[selectedRowIndex]" :key="name">
                        <td>{{ name }}</td>
                        <td>{{ value }}</td>
                      </tr>
                    </tbody>
                  </table>   
                </div>
              </pre>                            
            </b-col>
          </b-row>    
      </b-container>
  </b-modal>
  </b-container>
</template>
<script>
import axios from "axios";
import { config } from "../config.js"

export default {
  components: {},
  data() {
    return {
      geneList: "",
      percTumor: "",
      loggedInStatus: false,
      small: true,
      sampleID: "",
      selectedSample: "",
      selectedRowIndex: 0,
      infoModal: {
        id: "info-modal",
        title: "",
        content: "",
      },
      items: [],
      fields: [
        {key: "runid", label: "Run id"}, 
        {key: "sampleid", label: "Sample id"}
        ],
      variantFields: [
        {key: "Nr"},        
        {key: "Type", label: "Type"},
        {key: "gene"},
        {key: "Locus"},
        {key: "REF", label: "Ref"},
        {key: "ALTEND", label: "Alt / End"},
        {key: "annotation_variant", label: "Annotation Variant"},
        {key: "oncomineGeneClass"},
        {key: "oncomineVariantClass"},
        {key: "FILTER", label: "Filter"},
        {key: "Oncogenicity"},        
        {key: "class"},        
        {key: "Svares_ut", label: "Reply"},           
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
        console.log(this.selectedSample)
        // Get variants for that sample:
        this.$store.dispatch("initVariantStore", {"sample_id": this.selectedSample, "selected": 'empty', "allVariants": false});
        this.variants =  this.$store.getters.variants;
        //this.geneList = this.variants[0].Genliste;
        //this.percTumor = this.variants[0].Perc_Tumor;
      } else if (items.length === 0) {
        console.log("linje 175")
        this.selectedSample = "";
      }
    },
    openInfoModal(item, index, button) {
      console.log("openInfoModal")
      console.log(index)
      this.selectedRowIndex = index;
      this.infoModal.title = `Variant: ${index + 1}`;
      this.$root.$emit("bv::show::modal", this.infoModal.id, button);  
    },
    resetInfoModal() {
      this.infoModal.title = "";
      this.infoModal.content = "";
      console.log("infomodal lukket")
    },
    getsamples() {
      // Funksjon for å få samples fra backenc
      // util_funcs.query_backend(config.$backend_url,'samples').then(result => this.items = JSON.parse(result['data']))
      console.log("metode testaxios");
      const baseURI = config.$backend_url + "/api/signoff_samples";
      axios
        .get(baseURI)
        .then((response) => response.data)
        .then((data) => (this.items = data.data));
    },
    approve() {
      // Sending approval date to database
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
    variants: {
     get() {return this.$store.getters.variants;},
     set(value) {this.$store.commit("SET_STORE", value)}
   },
    state() {
      return this.$store.getters.loggedInStatus;
    },
    user() {
      return this.$store.getters.username;
    },
  },
};
</script>
