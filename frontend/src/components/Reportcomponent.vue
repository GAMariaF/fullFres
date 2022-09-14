<template>
  <b-container id="app" fluid v-show="state">
    
    
    <b-row>
      <b-col cols="3">
        <br />

        <h2>Approved samples</h2>
        <br />

        <div>
    


          <b-form-select v-model="selected" @change="updateFilter" size="sm" class="mt-3">
            <option v-for="run in runs" v-bind:value="{ id: run.value, text: run.text }" :key="run.value">{{ run.text }}
            </option>
          </b-form-select>
          <div class="mt-3">Selected: <strong>{{ selected }} -- {{filter}}  </strong></div>
        </div>
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
          :filter="filter"
          :filter-included-fields="filterOn"
        >
          <template #cell(runid)="data">
            <b class="text-info">{{ data.value.toUpperCase() }}</b>
          </template>
        </b-table>
      </b-col>
      <b-col>
        <br />
        <h2 v-if="selectedSample === ''">Please select a sample</h2>
        <div v-if="selectedSample !== ''">
          <h2>Variants for sample {{ selectedSample }}</h2>
          <br /><br />
          <h5>
            Gene List: <b>{{ this.variants[0].Genelist }}</b> | Tumor %:
            <b>{{ this.variants[0].Perc_Tumor }}</b>
          </h5>
          <br />
          <h2><p style="text-align: left">Classified variants</p></h2>
          <br />
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
            :filter="filter2"
            :filter-included-fields="filterOn2"
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
                @click="openReportModal(row.item, row.index, $event.target)"
                class="mr-1"
              >
                Report
              </b-button>
            </template>
          </b-table>
          <br />
     
          <br />
          

          <br /><br />
        </div>
      </b-col>
    </b-row>


<!-- -->
<b-modal
    v-if="selectedSample !== ''"
    :id="reportModal.id"
    :title="reportModal.title"
    ok-only
    size="lg"
    @hide="resetReportModal()"
    >
      <b-container fluid>
        <b-row class="mb-1">
          <b-col cols="4">
      
          </b-col>            
        </b-row>
        <br>
        <b-row class="mb-1">
          <b-col cols="6">

          </b-col>
          <b-col cols="6">
   
          </b-col>
        </b-row>

        <b-row class="mb-1">
          <b-col cols="6">

          </b-col>
          <b-col cols="6">

          </b-col>            		            

        </b-row>

        <b-row class="mb-1">
          <b-col cols="6">

          </b-col>       
          <b-col cols="6">
   
          </b-col>

        </b-row>

        <b-row class="mb-1">
          <b-col cols="6">
 
          </b-col>
          <b-col cols="6">

          </b-col>
        </b-row>    

        <b-row class="mb-1">
          <b-col cols="6">

          </b-col>
          <b-col cols="6">

            </b-col>
        </b-row>

        <b-row class="mb-1">
          <b-col cols="12">

          </b-col>
        </b-row>

        <hr />
        <b-row>
          <b-col cols="10">
            <p>Gene Info:</p>
          </b-col>
        </b-row>

        <hr />        



          <b-row>
            <b-col>
                <div class="table-responsive">
                  <table class="table-hover">
                    <thead>
                      <tr>
                        <th>Name</th>
                        <th>Value</th>
                      </tr>
                    </thead>
                    <tbody >
                      <tr v-for="name in sortedIndex" :key="name">
                        <td>{{ name }}</td>
                        <td>{{ variants[selectedRowIndex][name] }}</td>
                      </tr>
                    </tbody>
                  </table>   
                </div>                          
            </b-col>
          </b-row>    
      </b-container>
  </b-modal>

<!-- -->



  </b-container>
</template>
<script>
import { config } from '../config.js'
import util_funcs from "@/appUtils";


export default {
  props: ["locked"],
  name: "reportcomponent",
  data() {
    return {
      selectedRowIndex: 0,
      sortedIndex: config.sortedIndex,
      reportModal: {
        id: "report-modal",
        title: "",
        content: "",
      },
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
        {key: "Reply", label: "Reply"},           
        {key: "Info"}
        ],
      filter: "",
      filterOn: ["runid"],
      filter2: "Ja",
      filterOn2: ["Reply"],
      selected: null,
      runs: [{ value: null, text: 'Please select an option' },],
      loggedInStatus: false,
      selectedSample: "",
      small: true,
      items: [],
      fields: [
        { key: "runid", label: "Run id" },
        { key: "sampleid", label: "Sample id" },
        { key: "Date_Approval", label: "Date Approval" },
      ],
    };
  },
  methods: {
    updateFilter() {      
      this.filter = this.selected.text
    },
    getRuns() {
      console.log("getRuns!!! Running!! ")
      console.log("---")
      console.log(this.items)
      console.log("---")
      // console.log(this.items)
      var runs = []
      var result = []
      this.items.forEach((item, index) => {
        if(!runs.includes(item.runid)){
          
          runs.push(item.runid)
          result.push({value: index, text: item.runid})          
        }
        
        this.runs = result
      });
      // var runsset = new Set({ value: null, text: 'Please select an option' })
      // var check = []
      
      // this.items.forEach((item, index) => {
      //   if(!check.includes(item.runid)){
      //   runsset.add({ "value": index+1, "text": item.runid })
        
      //   check.push(item.runid)
      //   }  

      // })
    // this.runs = Array.from(runsset);

    },
    rowSelected(items) {
      if (items.length===1) {
        this.selectedVariant = items[0].Variant;
        
      } else if (items.length===0) {
        this.selectedVariant = "";
        console.log("unselected")
      }
    },
    sampleRowSelected(items) {
      if (items.length === 1) {
        this.selectedSample = items[0].sampleid;
        console.log(this.selectedSample);
        // Get variants for that sample:
        this.$store.dispatch("initVariantStore", {
          sample_id: this.selectedSample,
          selected: "empty",
          allVariants: false,
        });
        this.variants = this.$store.getters.variants;
      } else if (items.length === 0) {
        this.selectedSample = "";
      }
    },
    openReportModal(item, index, button) {
      console.log("openReportModal")
      index = this.variants.indexOf(item);
      this.selectedRowIndex = index;
      this.reportModal.title = `Variant: ${index + 1}`;
      this.$root.$emit("bv::show::modal", this.reportModal.id, button);  
    },
    resetReportModal() {
      this.reportModal.title = "";
      this.reportModal.content = "";
      console.log("infomodal lukket")
    },
  },
  created: function () {
    util_funcs.query_backend(config.$backend_url, "report").then(data => {
      this.items = data.data
      this.getRuns()});
    
  },
  computed: {
    state() {
      return this.$store.getters.loggedInStatus;
    },
  },
  watch: {},
};
</script>
