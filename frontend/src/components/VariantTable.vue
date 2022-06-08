<template>
  <div  id="app" class="container-fluid">
    <h1>Variants for sample: {{ sampleID }}</h1>
    <br>
    <h5><i>Click a row to start interpreting that Variant</i></h5>
    <br>
    <h5>Gene List: <b>{{geneList}}</b> | Tumor %: <b>{{percTumor}}</b></h5>
    <br>
    <b-table
      selectable
      select-mode="single"
      @row-selected="rowSelected"
      striped
      hover
      outlined
      fixed
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
      @hide="
        resetInfoModal();
        
      "
    >
      <b-container fluid>
        <pre></pre>

        <b-row class="mb-1">
          <b-col cols="6">
              <b-form-checkbox
                id="checkbox-1"
                v-model="variants[selectedRowIndex].Svares_ut"
                name="checkbox-1"
                value="Yes"
                unchecked-value=""
                size="default"                
              >
              ' Check for reply (Svares ut)
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
          <b-col cols="4">
            <label>Tier</label>
             <b-form-textarea 
                id="textarea"
                size="sm"
                v-model="variants[selectedRowIndex].Tier"
                @change="updateVariants;setChanged()"
                
              ></b-form-textarea>
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
                v-model="variants[selectedRowIndex].Kommentar"
                @change="updateVariants;setChanged()"
                
              ></b-form-textarea>
          </b-col>
        </b-row>

        <b-row class="mb-1">
          <b-col cols="2">
              <label>Class</label>
              <b-form-select
                :options="classOptions"
                class="py-sm-0 form-control"
                v-model="variants[selectedRowIndex].class"
                @change="updateVariants;setChanged()" 
              ></b-form-select>
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
            <b-button v-on:click="oncogenicitySelected(item)" v-b-tooltip.hover type="button" :title="item.title" :class="item.class">{{item.tag}}</b-button><span>&nbsp;</span>
          </span>
            <br>
            <br>
            <div>
            <h5>Oncogenicity: {{ oncoScore }}</h5>
            </div>
            <h5></h5>

            <br>
            <div>
            <h5>Chosen evidence types</h5>
            </div>
        <div v-for="item in selectedoncogenicity_list" v-bind:key="item.id">
          <!-- content -->
          {{item.tag}}
        </div>
            
          </b-col>
        </b-row>
        <b-row>
          <b-col >
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
      <br>
      <br>
      <h5>When interpretation is done, please sign off here</h5>
      <br>
      <b-button v-on:click="signOff" class="btn mr-1 btn-info"> SIGN OFF </b-button>

    <!--  -->
    <br>
    <br>
    Class: {{variants[0].class}}
  </div>
</template>
<script>


import { config } from '../config.js'
//import { util_funcs } from '../appUtils.js'
export default {
  name: "varianttable",
  props: [ "loading" ],
  data() {
    return {
      geneList: "",
      percTumor: "",
      oncoScore: 0,
      selectedoncogenicity_list: [],
      oncogenicitycriteria: config.oncogenicitycriteria,
      oncogenicityfields: [
          {
            key: 'evidence',
            label: 'Available evidence types',
            sortable: true
      }],
      classOptions: config.classOptions,
      small: true,
      selectedRowIndex: 0,
      infoModal: {
        id: "info-modal",
        title: "",
        content: "",
      },
      sampleID: this.$route.params.id,
      selectedVariant: "",
      fields: [
        'Nr',
        {key: "Type", label: "Type"},
        {key: "gene"},
        {key: "Locus"},
        {key: "REF", label: "Ref"},
        {key: "ALTEND", label: "Alt / End"},
        {key: "oncomineGeneClass"},
        {key: "oncomineVariantClass"},
        {key: "FILTER", label: "Filter"},
        {key: "Oncogenicity"},        
        {key: "class"},        
        {key: "Svares_ut", label: "Reply"},        
        {key: "Info"}
        ],
    };
  },
  methods: {
    updateVariants(){
      this.$store.commit("SET_STORE", this.variants)
      console.log("updateVariants")
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
      case 'Suporting':
        this.oncoScore += 1
        break;
      }
    })
    },
    setChanged() {
      this.variants[this.selectedRowIndex].visibility = true;
      this.updateVariants();
      console.log("setChanged")
      },
    oncogenicitySelected(items) {
      console.log("selected row")
      console.log("--")
      console.log(items)
      console.log("--")

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
      if(items.length !== 0 | typeof items !== 'undefined') {
        this.oncoScoring(this.selectedoncogenicity_list);
      } 
    },
    rowSelected(items) {
      if (items.length===1) {
        this.selectedVariant = items[0].Variant;

      } else if (items.length===0) {
        this.selectedVariant = "";
        console.log("unselected")
      }
    },
    openInfoModal(item, index, button) {
      console.log("openInfoModal")
      this.selectedRowIndex = index;
      this.infoModal.title = `Row index: ${index}`;
      this.$root.$emit("bv::show::modal", this.infoModal.id, button);  
    },
    resetInfoModal() {
      this.infoModal.title = "";
      this.infoModal.content = "";
      console.log("infomodal lukket")
    },
    signOff() {
      console.log("Sign off method")
      // Metode for  sende inn dato, og tolkede varianter til backend.
      const baseURI = config.$backend_url + "/api/updatevariants";

      this.$http.post(
            baseURI,
            {
              sampleid: this.$route.params.id,
              variants: this.variants
            },
            {
              withCredentials: true,
              // headers: { "Content-Type": "application/x-www-form-urlencoded" },
              headers: { "Content-Type": "application/json" },
              

            }
          ).then((response) => response.data)
          .then((data) => {
            console.log(data);
          });

    },
    sendVariantsToPost() {
    },
  },
  created: function() {
    this.$store.dispatch("initVariantStore", {"sample_id": this.$route.params.id, "selected": 'empty', "allVariants": false});
    this.geneList = this.variants[0].Genliste;
    this.percTumor = this.variants[0].Perc_Tumor;
    return this.$store.getters.variants;
    
    
  },
  computed: {
    variants: {
      get() {return this.$store.getters.variants;},
      set(value) {this.$store.commit("SET_STORE", value)}
    }
    
    
  }

};
</script>


