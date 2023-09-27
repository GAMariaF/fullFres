<template>
  <div  id="app" class="container-fluid">
    <h1>Welcome to the most amazing variant lookup tab!</h1>
    <h3>We promise to fulfill all your variant statistics wishes</h3>
    <h6 style="color: lightgray">(Accurate results not guaranteed)</h6>
    <br>

        <b-col  class="my-1">
           <b-input-group size="sm">
              <b-input v-model="run_input" placeholder="Enter Run(s)"></b-input> 
              <b-input v-model="sample_input" placeholder="Enter Sample(s)"></b-input> 

                <b-form-select
                :options="geneListOptions"
                class="py-sm-0 form-control"
                v-model="selectedGeneList"
                @change="addGeneList" 
                >
                <template #first>
                  <b-form-select-option :value="null" disabled>Gene Lists</b-form-select-option>
                </template> 
              </b-form-select>

              <b-input v-model="var_input" placeholder="Enter Variant(s)"></b-input>
              <b-input v-model="gene_input" placeholder="Enter Gene (One only)"></b-input>

              <b-form-select
                :options="replySearchOptions"
                class="py-sm-0 form-control"
                v-model="selectedReplyOption"
                >
    
              </b-form-select>

           </b-input-group>
        </b-col>
        <div class="mt-3"><strong>Current gene lists search: {{ this.geneListSearch }}</strong></div>
        <br>
        <b-button v-on:click="query(run_input, sample_input, var_input, gene_input)" type="button">Search</b-button><span>&nbsp;</span>
        <b-button v-on:click="resetSearch()" type="button">Reset</b-button><span>&nbsp;</span>
        <br>
        <br>
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
      :items="variants"
      :fields="fields"
      :small="small"
      :filter="filter"
    >
    <!-- Formatting Type column -->
    <template #cell(Type)="data">
      <b class="text-info">{{ data.value.toUpperCase() }}</b>
    </template>

    <template #cell(Stats)="row">
        <b-button size="sm" @click="row.toggleDetails();getClassifications(row.item)" class="mr-2">
           Details
        </b-button>
        <div v-if="row.detailsShowing">{{ plotPie(row.item) }}</div>



      <!-- As `row.showDetails` is one-way, we call the toggleDetails function on @change -->
      <!-- <b-form-checkbox v-model="row.detailsShowing" @change="row.toggleDetails">
        Details via check
      </b-form-checkbox> -->
    </template>


    <template #row-details="row">
        <b-card>
          <b-row class="mb-2">   
            <b-col>
              <Plotly 
                :data="pieData"
                :layout="pieLayout" 
                :display-mode-bar="false" />
            </b-col>
              <br/>
              <b-col>
                <VuePerfectScrollbar class="scroll-area" :settings="settingsScrollBar">
                <b-table
                  selectable
                  select-mode="single"
                  @row-selected="rowSelected_class"
                  striped
                  hover
                  outlined
                  label-sort-asc=""
                  label-sort-desc=""
                  label-sort-clear=""
                  :items="classifications"
                  :fields="fieldsVariant"
                  :small="small"
                  :filter="filter"
                >
                <!-- Formatting Type column -->
                <template #cell(Type)="data">
                  <b class="text-info">{{ data.value.toUpperCase() }}</b>
                </template>

                  <template #cell(Classification)="row">
                        <b-button
                          size="sm"
                          @click="openClassificationModal(row.item, row.index, $event.target)"
                          class="mr-1"
                        >
                          Classification
                        </b-button>
                      </template>
                  </b-table>
                </VuePerfectScrollbar>
                <br>
              <div><p style="text-align:left;">Classification(s): {{ row.item.ClassesPerVariant }}</p></div>
            </b-col>           
          </b-row>
          <b-button size="sm" @click="row.toggleDetails">Hide Details</b-button>
        </b-card>
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
    {{ selectedVariant }}

    <!--  -->

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
              <tbody>
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
    <!--  -->
    <b-modal
      :id="classificationModal.id"
      :title="classificationModal.title"
      ok-only
      size="lg"
      @hide="
        resetClassificationModal();

      "
    >
      <b-container fluid>
        <b-row class="mb-1">
          <b-col cols="4">
            <label>Classification date:</label>
            <p>{{ classifications[selectedRowIndexClassification].date + " by: " + classifications[selectedRowIndexClassification].User_Class }}</p>
            </b-col> 
        </b-row>
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
              <tbody>
                      <tr v-for="name in sortedIndexClassification" :key="name">
                        <td>{{ name }}</td>
                        <td>{{ classifications[selectedRowIndexClassification][name] }}</td>
                      </tr>
              </tbody>
            </table>
          </div>
          </b-col>
        </b-row>

      </b-container>
    </b-modal>

    <!--  test -->
<!-- <b-button v-on:click="sortTable(variants)" type="button">Testklikk sorter</b-button><span>&nbsp;</span> -->
    <!--  -->


  </div>
</template>
<script>


import { config } from '../config.js';
import util_funcs from "@/appUtils";
import { Plotly } from 'vue-plotly';
import VuePerfectScrollbar from "vue-perfect-scrollbar";
// must also add to components below
export default {
  name: "allvarianttable",
  props: [ "loading" ],
  components: { Plotly, VuePerfectScrollbar },
  data() {
    return {

      geneListSearch: "",
      run_input: "",
      sample_input: "",
      var_input: "",
      gene_input: "",


      variantSampleList: "",
      variants: ['SamplesPerVariant'],
      classifications: ["sampleid", "date"],
      oncoScore: 0,
      selectedoncogenicity_list: [],
      oncogenicitycriteria: config.oncogenicitycriteria,
      oncogenicityfields: [
          {
            key: 'evidence',
            label: 'Available evidence types',
            sortable: true
      }],
      options: config.classOptions,
      geneListOptions: config.geneListOptions,
      replySearchOptions: config.replySearchOptions,
      selectedGeneList: null,
      selectedReplyOption: "",
      small: true,
      selectedRowIndex: 0,
      selectedRowIndexClassification: 0,
      infoModal: {
        id: "info-modal",
        title: "",
        content: "",
      },
      classificationModal : {
        id: "classification-modal",
        title: "",
        content: "",
      },
      sampleID: this.$route.params.id,
      selectedVariant: "",
      selectedClassification: "",

      settingsScrollBar: {
        maxScrollbarLength: 60},
      fields: [
        {key: "Type", label: "Type", sortable: true},
        {key: "gene", sortable: true},
        {key: "annotation_variant2", label: " Annotation Variant (alt)"},
        {key: "CHROM", sortable: true},        
        {key: "POS", label: "Pos", sortable: true},
        {key: "REF", label: "Ref", sortable: true},
        {key: "ALTEND", label: "Alt / End", sortable: true},
        {key: "FreqSamples", label: "N Samples", sortable: true},
        {key: "FreqGenLis", label: "N Gene Lists", sortable: true},
        {key: "oncomineGeneClass", sortable: true},
        {key: "oncomineVariantClass", sortable: true},
        {key: "Stats"},
        {key: "Info"}
        ],
      sortedIndex: [ 'SamplesPerVariant',
                    'gene',
                    'transcript',
                    'annotation_variant2',
                    'COSMIC',
                    'class',
                    'oncomineGeneClass',
                    'oncomineVariantClass',
                    'Locus',
                    'protein',
                    'REF',
                    'ALTEND',
                    'coding',
                    'Populasjonsdata',
                    'Funksjonsstudier',
                    'Prediktive_data',
                    'Cancer_hotspots',
                    'Computational_evidens',
                    'Konservering',
                    'ClinVar',
                    'Andre_DB',
                    'Comment',
                    'evidence_types',
                    'Oncogenicity',
                    'Tier',
                    'FreqSamples',
                    'FreqGenLis'
                  ],
    sortedIndexClassification: ['runid',
                    'sampleid',
                    'Genelist',
                    'Perc_Tumor',
                    'gene',
                    'exon',
                    'transcript',
                    'annotation_variant',
                    'Reads',
                    'FILTER',
                    'AF',
                    'COSMIC',
                    'Reply',
                    'User_Classification',
                    'class',
                    'Variant_ID',
                    'Variant_Name',
                    'Key_Variant',
                    'Oncomine_Reporter_Evidence',
                    'Type',
                    'oncomineGeneClass',
                    'oncomineVariantClass',
                    'Locus',
                    'protein',
                    'REF',
                    'ALTEND',
                    'Call',
                    'DP',
                    'FDP',
                    'FAO',
                    'coding',
                    'P_Value',
                    'Read_Counts_Per_Million',
                    'Oncomine_Driver_Gene',
                    'Copy_Number',
                    'CNV_Confidence',
                    'Valid_CNV_Amplicons',
                    'Populasjonsdata',
                    'Funksjonsstudier',
                    'Prediktive_data',
                    'Cancer_hotspots',
                    'Computational_evidens',
                    'Konservering',
                    'ClinVar',
                    'CLSF',
                    'Andre_DB',
                    'Comment',
                    'evidence_types',
                    'Oncogenicity',
                    'TierVPS',
                    'User_Class'
                  ],
      filter: '',
      fieldsVariant: [
        {key: 'sampleid', label: 'Sample'}, 
        {key: 'Reply', label: 'Reply', sortable: true}, 
        {key: 'Genelist', label: 'Gene List', sortable: true},
        {key: 'date', label: 'Date Classified', sortable: true},
        {key: 'Classification'},
      ]
    };
  },
  methods: {
    query(run_input, sample_input, var_input, gene_input) {

        const run_input_array = run_input.split(' AND ')
        const sample_input_array = sample_input.split(' AND ')
        const diag_input_array = this.geneListSearch.split(' AND ')
        const var_input_array = var_input.split(' AND ')
        const gene_input_array = [gene_input]
        const reply_input_array = [this.selectedReplyOption]
        console.log(gene_input)
        console.log(this.run_input_array)


        const array_1 = JSON.stringify([run_input_array, sample_input_array, diag_input_array, var_input_array, gene_input_array, reply_input_array]);
        console.log(array_1)
        if (array_1 === '[[""],[""],[""],[""],[""],[""]]'){
          console.log('Empty Search')
          this.displayWarning("No search parameters provided!")
        } else {
          util_funcs.query_backend(config.$backend_url, "stat_search" + array_1).then(result => {
            var variants = Object.values(result['data']);
            if (variants.length) {
              this.variants = variants;
            } else {
              this.variants = ['SamplesPerVariant'];
            }
            
            console.log(this.variants);
          })
        }
          //Prostate Cancer AND Colorectal Cancer
    },
    updateVariants(){
      
    },
    resetSearch() {
      this.geneListSearch = "";
      this.run_input =  "";
      this.sample_input = "";
      this.var_input = "";
      this.gene_input = "";
      this.selectedGeneList = null;
      this.selectedReplyOption = "";
    },

    getClassifications(item){
      var query = 'get_class|'+item.CHROM+'|'+item.POS+'|'+item.REF+'|'+item.ALTEND

      util_funcs.query_backend(config.$backend_url, query)
        .then(result => {this.classifications = Object.values(result['data']);

      for (let i = 0; i < this.classifications.length; i++) {
        this.classifications[i].date = this.classifications[i].DATE_CHANGED_VARIANT_BROWSER.substring(4,6) + '.' + 
                                      this.classifications[i].DATE_CHANGED_VARIANT_BROWSER.substring(2,4) + '.' +
                                      this.classifications[i].DATE_CHANGED_VARIANT_BROWSER.substring(0,2);
      }})
    },

    addGeneList(item){
      if (this.geneListSearch === "") {
        this.geneListSearch += item;
      } else {
      this.geneListSearch += " AND " + item;
      }
      console.log(this.geneListSearch)
    },
    oncoScoring(selectedoncogenicity_list) {
    this.oncoScore = 0;
    selectedoncogenicity_list.forEach(item => {
    switch(item.default) {
      case 'Very Strong':
        this.oncoScore += 8
        break;
      case 'Strong':
        this.oncoScore += 4
        break;
      case 'Moderate':
        this.oncoScore += 2
        break;
      case 'Supporting':
        this.oncoScore += 1
        break;
      }
    })
    },

    calcGeneListInfo(item) {
      console.log(item)
      const geneList = item.GenelistsPerVariant.split(', ')
      var uniqueGeneList = geneList.filter((v, i, a) => a.indexOf(v) === i);
      let geneListDict = new Object();
      for (var index = 0; index < uniqueGeneList.length; index++) {
        var count = 0;
        for(var i = 0; i < geneList.length; ++i){
            if(geneList[i] === uniqueGeneList[index])
                count++;
        }
        geneListDict[uniqueGeneList[index]] = count;
      }
      return(geneListDict)
    },

    makeSampleList(item) {
      var samples = item.SamplesPerVariant.split(', ');
      var geneList = item.GenelistsPerVariant.split(', ');
      var replyList = item.ReplyListPerVariant.split('|');

      var res_string = "Sample:          Reply          Gene List\n";

      for (var i=0; i<samples.length; i++){
        res_string += samples[i] +': ' + replyList[i] + '  ' + geneList[i] + '\n';
      }
      return(res_string);
    },

    plotPie(item) {
      var data = this.calcGeneListInfo(item);

      var values = [];
      var labels = [];

      for (const  [key, value] of Object.entries(data)) {
          values.push(value);
          labels.push(key);

        }
      this.pieLayout = {
        height: 460,
        width: 680
      };
      this.pieData = [{
        values,
        labels,
        type: 'pie'
      }];
      

    },

    rowSelected(items) {
      if (items.length===1) {
        this.selectedVariant = items;
        console.log("test")
        //console.log(items)

      } else if (items.length===0) {
        this.selectedVariant = "";
        console.log("unselected")
      }
    },

    rowSelected_class(items) {
      if (items.length===1) {
        this.selectedClassification = items;
        console.log("test")
        console.log(items)

      } else if (items.length===0) {
        this.selectedClassification = "";
        console.log("unselected")
      }
    },

    openInfoModal(item, index, button) {
      console.log("openInfoModal")
      this.selectedRowIndex = index;
      //this.infoModal.title = `Variant: ${item.transcript}`;
      this.infoModal.title = `${item['gene']}: ${item['annotation_variant2']}`;
      this.$root.$emit("bv::show::modal", this.infoModal.id, button);
      //this.variants = util_funcs.sort_table(this.variants);
      //this.$store.commit("SET_STORE",this.variants)
    },

    openClassificationModal(item, index, button) {
      console.log("openClassificationModal")
      this.selectedRowIndexClassification = index;
      //this.infoModal.title = `Variant: ${item.transcript}`;
      this.classificationModal.title = `${item['sampleid']}: ${item['annotation_variant2']} Classification`;
      this.$root.$emit("bv::show::modal", this.classificationModal.id, button);
      //this.variants = util_funcs.sort_table(this.variants);
      //this.$store.commit("SET_STORE",this.variants)
    },

    resetInfoModal() {
      this.infoModal.title = "";
      this.infoModal.content = "";
      console.log("infomodal lukket")
    },

    resetClassificationModal() {
      this.classificationModal.title = "";
      this.classificationModal.content = "";
      console.log("classificationModal lukket")
    },

    sortTable() {
      this.variants = util_funcs.sort_table(this.variants);
    },

    displayWarning(message) {
      alert(message);
      
    }
  },
  created: function() {
    const array_1 = JSON.stringify([[""], ["22SKH02673"], [""], [""], [""], [""]]);
    util_funcs.query_backend(config.$backend_url, "stat_search" + array_1).then(result => {
      this.variants = Object.values(result['data']);     
    }) 
  },

  computed: {

  }

};
</script>

<style>

div.sampleList {
  white-space: pre-wrap;
  text-align: left;
}
.scroll-area {
  position: relative;
  margin: auto;
  width: 620px;
  height: 420px;
  text-align: center;
}
.center {
  text-align: center;
}
</style> 
