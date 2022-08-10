import util_funcs from '../appUtils'
<template>
  <div id="app" class="container-fluid" v-if="!loading">
    <h1>Variants for sample: {{ sampleID }}</h1>
    <br>
    <h5>Gene List: <b>{{this.variants[0].Genelist}}</b> | Tumor %: <b>{{this.variants[0].Perc_Tumor}}</b></h5>
    <br>
    <b-table
      selectable
      select-mode="single"
      @row-selected="rowSelected"
      striped
      hover
      outlined
      fixed
      label-sort-asc=""
      label-sort-desc=""
      label-sort-clear=""
      :items="variants"
      :fields="fields"
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
    {{ selectedVariant }}

    <!--  -->

    <b-modal

      :id="infoModal.id"
      :title="infoModal.title"
      ok-only
      size="lg"
      @hide="resetInfoModal();sendVariants()"
    >
      <b-container fluid>
        <div v-if="locked === false">
        <b-row class="mb-1">
          <b-col cols="6">
              <b-form-checkbox
                id="checkbox-1"
                v-model="variants[selectedRowIndex].Reply"
                name="checkbox-1"
                value="Yes"
                unchecked-value=""
                size="default"
                @change="updateVariants;setChanged()"
              >
              <h6>&nbsp; Check for reply (Svares ut)</h6>
              </b-form-checkbox>

            </b-col>
        </b-row>
        <br>
        <b-row class="mb-1">
          <b-col cols="4">
            <label>Population Data</label>
             <b-form-textarea
                id="textarea"
                size="sm"
                v-model="variants[selectedRowIndex].Populasjonsdata"
                @change="updateVariants;setChanged()"

              ></b-form-textarea>
          </b-col>
          <b-col cols="4">
            <label>Functional Studies</label>
             <b-form-textarea
                id="textarea"
                size="sm"
                v-model="variants[selectedRowIndex].Funksjonsstudier"
                @change="updateVariants;setChanged()"

              ></b-form-textarea>
          </b-col>
          <b-col cols="4">
            <label>Predictive Data</label>
             <b-form-textarea
                id="textarea"
                size="sm"
                v-model="variants[selectedRowIndex].Prediktive_data"
                @change="updateVariants;setChanged()"

              ></b-form-textarea>
          </b-col>
        </b-row>

        <b-row class="mb-1">
          <b-col cols="4">
            <label>Cancer Hotspots</label>
              <b-form-textarea
                id="textarea"
                size="sm"
                v-model="variants[selectedRowIndex].Cancer_hotspots"
                @change="updateVariants;setChanged()"

              ></b-form-textarea>
          </b-col>
          <b-col cols="4">
            <label>Computational evidence</label>
             <b-form-textarea
                id="textarea"
                size="sm"
                v-model="variants[selectedRowIndex].Computational_evidens"
                @change="updateVariants;setChanged()"

              ></b-form-textarea>
          </b-col>
          <b-col cols="4">
            <label>Conservation</label>
             <b-form-textarea
                id="textarea"
                size="sm"
                v-model="variants[selectedRowIndex].Konservering"
                @change="updateVariants;setChanged()"

              ></b-form-textarea>
          </b-col>
        </b-row>

        <b-row class="mb-1">
          <b-col cols="4">
            <label>ClinVar</label>
             <b-form-textarea
                id="textarea"
                size="sm"
                v-model="variants[selectedRowIndex].ClinVar"
                @change="updateVariants;setChanged()"

              ></b-form-textarea>
          </b-col>
          <b-col cols="4">
            <label>Other DB</label>
             <b-form-textarea
                id="textarea"
                size="sm"
                v-model="variants[selectedRowIndex].Andre_DB"
                @change="updateVariants;setChanged()"

              ></b-form-textarea>
          </b-col>
        </b-row>    

        <b-row class="mb-1">
          <b-col cols="4">
              <label>Class</label>
              <b-form-select
                :options="classOptions"
                class="py-sm-0 form-control"
                v-model="variants[selectedRowIndex].class"
                @change="updateVariants;setChanged()" 
              >
              </b-form-select>
          </b-col>
          <b-col cols="4">
              <label>Tier</label>
              <b-form-select
                :options="tierOptions"
                class="py-sm-0 form-control"
                v-model="variants[selectedRowIndex].Tier"              
                @change="updateVariants;setChanged()" 
              ></b-form-select>
            </b-col>
        </b-row>

        <b-row class="mb-1">
          <b-col cols="12">
            <label>Comment</label>
             <b-form-textarea
                id="textarea"
                size="default"
                placeholder=""
                rows=4
                v-model="variants[selectedRowIndex].Comment"
                @change="updateVariants;setChanged()"

              ></b-form-textarea>
          </b-col>
        </b-row>

        <hr />
        <b-row>
          <b-col cols="10">
            <p>Gene Info:</p>
          </b-col>
        </b-row>
        <b-row>
          <b-col cols="12">
          <h5>Available evidence types </h5>
          <span v-for="item in oncogenicitycriteria" :key="item.tag">
            <b-button v-on:click="oncogenicitySelected(item);updateVariants;setChanged()" v-b-tooltip.hover type="button" :title="item.title" :class="item.class">{{item.tag}}</b-button><span>&nbsp;</span>
          </span>
            <br>
            <br>
            <div>
            <h5>Oncogenicity: {{ this.variants[this.selectedRowIndex].Oncogenicity }}</h5>
            
            
            </div>
            <h5></h5>

            <br>
            <div>
            <h5>Chosen evidence types</h5>
            </div>
            {{this.variants[this.selectedRowIndex].evidence_types}}
     





        </b-col>
        </b-row>
        <hr />     
        </div>   
        <b-row>
          <b-col >
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
      <br>
      <br>
      <div v-if="locked === false">
      <h5>When interpretation is done, please sign off here</h5>
      <br>
      <b-button v-on:click="signOff" class="btn mr-1 btn-info"> SIGN OFF </b-button>
      </div>
    <!--  -->
    <br>
    <br>
    Class: {{variants[0].class}}



  </div>
  
</template>
<script>

import { config } from '../config.js'
export default {
  props: ['locked'],
  name: "varianttable",
  data() {
    return {
  
      loading: true,
      sortedIndex: [ 'runid',
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
                    'Tier'
                  ],
      oncoScore: 0,
      selectedoncogenicity_list: [],
      oncogenicitycriteria: config.oncogenicitycriteria,
      oncogenicityfields: [
          {
            key: 'evidence',
            label: 'Available evidence types',
            sortable: true
      }],
      small: true,
      selectedRowIndex: 0,
      classOptions: config.classOptions,
      tierOptions: config.tierOptions,
      infoModal: {
        id: "info-modal",
        title: "",
        content: "",
      },
      sampleID: this.$route.params.id,
      selectedVariant: "",
      fields: [
        'Nr',
        {key: "Type", label: "Type", sortable: true},
        {key: "gene", sortable: true},
        {key: "exon"},
        {key: "Locus", sortable: true},
        {key: "REF", label: "Ref"},
        {key: "ALTEND", label: "Alt / End"},
        {key: "oncomineGeneClass"},
        {key: "oncomineVariantClass"},
        {key: "FILTER", label: "Filter"},
        {key: "Oncogenicity"},
        {key: "class"},
        {key: "Reply", label: "Reply (Svares ut)"},
        {key: "Info"}
        ],
    };
  },
  methods: {
    updateVariants() {
      this.$store.commit("SET_STORE", this.variants);
      console.log("updateVariants");
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
        case 'bVery Strong':
        this.oncoScore += -8
        break;
      case 'bStrong':
        this.oncoScore += -4
        break;
      case 'bModerate':
        this.oncoScore += -2
        break;
      case 'bSupporting':
        this.oncoScore += -1
        break;
      }
    })
    this.variants[this.selectedRowIndex].Oncogenicity = "" + this.oncoScore;
    },
    setChanged() {
      this.variants[this.selectedRowIndex].visibility = true;
      this.variants[this.selectedRowIndex].changed = true;
      this.updateVariants();
      console.log("setChanged");
    },
    oncogenicitySelected(items) {
      console.log("selected row");
      console.log("--");
      console.log(items);
      console.log("--");
  
      // Utfør kun dersom en rad er valg - husk at på klikk to blir den deselektert
      // Ved klikk: hvis ikke allerede valgt, velg, ellers fjern.
      var index = this.selectedoncogenicity_list.indexOf(items);
      if (index !== -1) {
        // Fjern hvis tilstede
        this.selectedoncogenicity_list.splice(index, 1);
      } else {
        // Legge til hvis ikke tilstede
        this.selectedoncogenicity_list.push(items);
      }
      // Legg til en tabell hvor default styrke er valgt
      // Tabellen vises kun hvis lengden av this.selectedACMG != 0
      // Regn ut oncoscore
      // Utfør kun om det faktisk er valgt en rad (length !== 0)
      if ((items.length !== 0) | (typeof items !== "undefined")) {
        this.oncoScoring(this.selectedoncogenicity_list);
        // Apply evidence to table:
        var tmplist = []
        this.selectedoncogenicity_list.forEach(function (arrayItem) {
          tmplist.push(arrayItem.tag)
        });
        this.variants[this.selectedRowIndex].evidence_types = tmplist.toString();
      }
    },


    rowSelected(items) {  
      if (items.length===1) {
        this.selectedVariant = items;
        console.log(items)
      } else if (items.length===0) {
        this.selectedVariant = "";
        console.log("unselected");
      }
    },


    openInfoModal(item, index, button) {
      console.log("openInfoModal");
      this.selectedRowIndex = index;
      this.infoModal.title = `Variant: ${index +1}`;
      this.$root.$emit("bv::show::modal", this.infoModal.id, button);
    },
    resetInfoModal() {
      this.infoModal.title = "";
      this.infoModal.content = "";
      this.selectedoncogenicity_list = [];
      this.oncoScore = 0;
      console.log("infomodal lukket");
    },
    sendVariants() {
      // This is for updating variants in the db whenever there has been a change. Should be triggered by leaving the interp-modal but only send if anything has changed
      // If any changed:
      
      
      if (this.variants.filter(e => e.changed === true).length > 0) {
        console.log("Something has changed - sending updated data to db")


      // Metode for  sende inn dato, og tolkede varianter til backend.
      const baseURI = config.$backend_url + "/api/updatevariants";
      this.$http
        .post(
          baseURI,
          {
            sampleid: this.$route.params.id,
            variants: this.variants,
            user: this.$store.getters.username,
          },
          {
            withCredentials: true,
            headers: { "Content-Type": "application/json" },
          }
        )
        .then((response) => response.data)
        .then((data) => {
          console.log(data);
        });

      } 
      console.log("tester om sendvariants blir aktivert when leaving modal")
    },
    signOff() {
      // This if only for signing off the user when interpretation is done. 
      console.log("Sign off method");
      
      // Metode for  sende inn dato, og tolkede varianter til backend.
      const baseURI = config.$backend_url + "/api/signoff";
      this.$http
        .post(
          baseURI,
          {
            sampleid: this.$route.params.id,
            variants: this.variants,
            user: this.$store.getters.username,
          },
          {
            withCredentials: true,
            // headers: { "Content-Type": "application/x-www-form-urlencoded" },
            headers: { "Content-Type": "application/json" },
          }
        )
        .then((response) => response.data)
        .then((data) => {
          console.log(data);
        });
        this.$router.push({
        name: "Samples"
        });
    },
    
  },
  created: function() {
    this.$store.dispatch("initVariantStore", {"sample_id": this.$route.params.id, "selected": 'empty', "allVariants": false});
    
    return this.$store.getters.variants;
    
  },
  computed: {
    currentRouteName() {
        return this.$route.name;
    },
    variants: {
      get() {return this.$store.getters.variants;},
      set(value) {this.$store.commit("SET_STORE", value)}
    }
  },
  watch: {
      variants(newVars, oldVars) {
      console.log(`Changed from ${oldVars} to ${newVars}`);
      this.loading = false;
    },
  },
};
</script>
