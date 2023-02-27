
<template>
  <b-container id="app" fluid v-show="state">
    <b-row>
      <b-col cols="3">
        <br />

        <h2>Approved samples</h2>
        <br />

        <b-row>
          <b-col>
            <b-input-group>
              <b-input v-model="runid" placeholder="Run ID"></b-input>
              <b-input v-model="sampleid" placeholder="Sample ID"></b-input>
            </b-input-group>
            <br>
              <b-button v-on:click="getSamples()" type="button">Search</b-button><span>&nbsp;</span>
            <br>
          </b-col>
        </b-row>

        
        <br>
        
        <!-- Scrollbar for the run and samples table -->
        <!-- :filter-included-fields="filterRunOn" -->
        
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
          <h2><p style="text-align: left">Classified variants:</p></h2>
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
            :filter="filterVar"
            :filter-included-fields="filterVarOn"
          >
            <!-- Adding index column -->
            <template #cell(Nr)="data">
              {{ data.index + 1 }}
            </template>
            <!-- Formatting Type column -->
            <template #cell(Type)="data">
              <b class="text-info">{{ data.value.toUpperCase() }}</b>
            </template>
            <!-- Get specific values for specific variant types -->
            <template #cell(Specific)="data">
              <b class="text-info">{{ typeSpecificValue(data) }}</b>
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
            <h3 v-if="this.warning !== ''">No variant selected!</h3>
          <br />
          <!-- 
          <b-form-select v-model="selectedCategory" @change="generateVarRep" size="sm" class="mt-3">
            <option v-for="cat in categories" v-bind:value="cat.text" :key="cat.value">{{ cat.value }}
            </option>
          </b-form-select>
          -->
          <!-- Use buttons instead of dropdown menu -->
          <span v-for="cat in categories" :key="cat.value">
            <b-button v-on:click="generateVarRep(cat.text)" type="button" :class="cat.class">{{cat.value}}</b-button><span>&nbsp;</span>
          </span>
          <br />
          <br />
          <h5 class="report">
            {{ report }} 
          </h5>
          <body>
            <span>
            <b-button size="sm" @click="revertLast()" class="mr-1" type="button">Revert</b-button>&nbsp;
            <b-button size="sm" @click="generateGenRep()" class="mr-1" type="button">Reset Report</b-button>&nbsp;
          </span>
          </body>
          <br />
          <br>
          {{selectedVariant}} 
        </div>
      </b-col>
    </b-row>
<!-- -->

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
        {key: "Specific", label: "Type Specific"},
        {key: "FILTER", label: "Filter"},
        {key: "Oncogenicity"},        
        {key: "class"},        
        {key: "Reply", label: "Reply"},           
        {key: "Info"}
        ],
      filterRun: "",
      //filterRunOn: ["runid"],
      // OBS: "Yes" på nyere data, "Ja" på eldre. 
      filterVar: "Yes",
      filterVarOn: ["Reply"],
      selected: null,
      //selectedCategory: null,
      runs: [{ value: null, text: 'Please select an option' },],
      categories: config.reportcodes,
      loggedInStatus: false,
      selectedSample: "",
      selectedVariant: "",
      small: true,
      items: [],
      // 'Variants' is a placeholder to prevent errors until the data is fetched from backend.
      // Also ensures the component is rerendered when the data arrives. 
      variants: ["Genelist"],
      generalReport: "",
      reportArray: [],
      report: "",
      warning: "",
      runid: "",
      sampleid: "",
      fields: [
        { key: "runid", label: "Run id" },
        { key: "sampleid", label: "Sample id" },
        { key: "Date_Approval", label: "Date Approval" },
      ],
      // Settings for Vue perfect scrollbar.
      settings: {
        maxScrollbarLength: 60},
    };
  },

  methods: {
    updateFilter() { 
      this.filterRun = this.selected.text
    },
    filterTable(row, filter) {
      return(row['runid']===filter);
    },
    getRuns() {
      console.log("getRuns!!! Running!! ")
      console.log(this.items)

      var runs = []
      var result = []

      this.items.forEach((item, index) => {
        if(!runs.includes(item.runid)){
          runs.push(item.runid) 
          result.push({value: index, text: item.runid})          
        }});

      this.runs = result
      // Used to only show last run on render.
      this.filterRun = runs[runs.length-1];

    },

    rowSelected(items) {
      console.log("rowSelect items: ")
      console.log(items)
      if (items.length===1) {
        // this.selectedVariant = items[0].Variant;
        this.selectedVariant = items;
        this.warning = "";
        console.log("Selected")
      } else if (items.length===0) {
        this.selectedVariant = "";
        console.log("unselected")
      }
      // Resette categori/report når ny varaint velges, eller ved deselect.
      //this.report = "";
      //this.selectedCategory = null;
    },

    async sampleRowSelected(items) {
      if (items.length === 1) {

        this.selectedSample = items[0].sampleid;
        console.log(this.selectedSample);
         //Get variants for that sample:

        //this.$store.dispatch("initVariantStore", {
        //  sample_id: this.selectedSample,
        //  selected: "empty",
        //  allVariants: false,
        //});
        
        // Query and commit to store here instead of having the store do it.
        await util_funcs.query_backend(config.$backend_url,'variants_' + this.selectedSample).then(result => {
          console.log(typeof result);
          var variants = Object.values(result['data']);
          this.variants = variants}) 
        
        this.$store.commit('SET_STORE', this.variants);
        this.generateGenRep();

      } else if (items.length === 0) {
        this.selectedSample = "";
        this.generalReport = "";
      }
    },

    getSamples() {
      var search = "|date"
      if (this.runid !== ""){
        search = "|runid|"+this.runid;
      } else if(this.sampleid !== "") {
        search = "|sampleid|"+this.sampleid;
      }

      util_funcs.query_backend(config.$backend_url, "report"+search).then(data => {
        this.items = data.data
        this.getRuns()
      });

      this.runid = "";
      this.sampleid = "";

    },

    openReportModal(item, index, button) {
      console.log("openReportModal")
      index = this.variants.indexOf(item);
      this.selectedRowIndex = index;
      //this.reportModal.title = `Variant: ${index + 1}`;
      this.reportModal.title = `${item['gene']}: ${item['annotation_variant']}`;
      this.$root.$emit("bv::show::modal", this.reportModal.id, button);  
    },

    resetReportModal() {
      this.reportModal.title = "";
      this.reportModal.content = "";
      console.log("infomodal lukket")
    },

    typeSpecificValue(data) {
      switch(data.item['Type'].toUpperCase()) {
        case 'SNP':
            return("AF: "+data.item['AF']);
          case 'DEL':
            return("AF: "+data.item['AF']);
          case 'MNP':
            return("AF: "+data.item['AF']);
          case 'FUSION':
            return(data.item['Variant_Name'].split(' ')[0]+"\nRPM: "+data.item['Read_Counts_Per_Million']);
          case 'CNV':
            return("CN: "+data.item['Copy_Number']);
          case 'INS':
            return("AF: "+data.item['AF']);
          case 'RNAEXONVARIANT':
            return("AF: "+data.item['AF']);
          case 'COMPLEX':
            return("AF: "+data.item['AF'])
          default:
            return("");
      }
    },

    generateGenRep() {
      if (this.selectedSample === "") {
        console.log("No row selected")
        this.report = "No row selected";
      } else {
        this.reportArray = [`${this.variants[0]['Genelist']} | XXbiopsi | Tumor %: ${this.variants[0]['Perc_Tumor']}\n\n`];
        this.generateReport();
      }
    },

    generateVarRep(category) {

      if (this.selectedVariant.length === 0) {
        console.log("No variant selected")
        this.warning = "No variant selected"
      } else {

        var variant = this.selectedVariant[0]
        var name = variant['Variant_Name']

        var type = 'varianten'
        switch (variant['Type'].toUpperCase()) {
          case 'SNP':
            type = 'sekvensvarianten';
            break;
          case 'DEL':
            type = 'delesjonen';
            break;
          case 'MNP':
            type = 'multinukelotidvarianten';
            break;
          case 'FUSION':
            type = 'fusjonen';
            name = variant['Variant_Name'].split(' ')[0];
            break;
          case 'CNV':
            type = 'kopitallsvarianten';
            break;
          case 'INS':
            type = 'insettingsvarianten';
            break;
          case 'RNAEXONVARIANT':
            type = "exonvarianten";
            break;
          case 'COMPLEX':
            type = "kompleksvarianten"
            break;
        }
        type = type + " ";

        var annoVar = "";
        if (variant['annotation_variant2'] !== ": ()"){
          annoVar = variant['annotation_variant2'] + " ";
        }
        

        // Trengs for å "lese" variabelene, kan nok gjøres på ein anna måte.
        console.log(variant)
        console.log(type)
        console.log(annoVar)
        console.log(name)

        this.reportArray.push(eval('`'+category+' \n\n`'));
        //this.report = this.report.concat(eval('`'+category+' \n\n`'));
        this.generateReport();
      }
    },

    revertLast() {
      this.reportArray.splice(-1, 1);
      this.generateReport();
    },

    generateReport() {
      this.report = this.reportArray.join('')
    },

    async copyToClipboard(text) { 
      // Needs https to work, not currently active.
      try {
        await navigator.clipboard.writeText(text);
        console.log('Text copied to clipboard');
      } catch (err) {
        console.error('Error in copying text: ', err);
      }
    },
  },

  created: function () {
    this.getSamples();
  },

  computed: {
    state() {
      return this.$store.getters.loggedInStatus;
    },
  },
  watch: {},
};
</script>


<style>
h5.report {
  white-space: pre-wrap;
  color: rgb(9, 9, 180);
  text-align: left;
}
</style> 