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
          <h5>Gene List: <b>{{this.variants[0].Genelist}}</b> | Tumor %: <b>{{this.variants[0].Perc_Tumor}}</b></h5>
          <br>
          <h2><p style="text-align:left;">Classified variants</p></h2>
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
            :filter="filter1"
            :filter-included-fields="filterOn"
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
          <br>
          <h2><p style="text-align:left;">Not Relevant, Technical or not interpreted variants </p></h2>
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
            :filter="filter2"
            :filter-included-fields="filterOn"
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
            
          <div>
            <b-button v-on:click="approve" class="btn mr-1 btn-info"> Approve </b-button>
            <p></p>
            <b-button v-on:click="unApprove" class="btn mr-1 btn-info"> Send Back </b-button>
          </div>
          
          <br><br>
        </div>
   
      </b-col>
    </b-row>
    <b-modal
    :id="infoModal.id"
    :title="infoModal.title"
    ok-only
    size="lg"
    @hide="resetInfoModal();sendVariants();"
    >
      <b-container fluid>
        <b-row class="mb-1">
          <b-col cols="4">
            <label>Reply (Svares ut)</label>
            <b-form-select
              :options="replyOptions"
              class="py-sm-0 form-control"
              v-model="variants[selectedRowIndex].Reply"
              @change="updateVariants;setChanged()" 
            >
            </b-form-select>
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
            <b-button v-on:click="oncogenicitySelected(item)" v-b-tooltip.hover type="button" :title="item.title" :class="item.class">{{item.tag}}</b-button><span>&nbsp;</span>
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
  </b-container>
</template>
<script>
// import axios from "axios";
import { config } from "../config.js"

export default {
  components: {},
  data() {
    return {
      //classVariants: [],
      //notClassVariants: [],
      sortedIndex: [ 'runid',
                    'sampleid',
                    'Genelist',
                    'Perc_Tumor',
                    'gene',
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
      loggedInStatus: false,
      small: true,
      sampleID: "",
      selectedSample: "",
      selectedRowIndex: 0,
      replyOptions: config.replyOptions,
      classOptions: config.classOptions,
      tierOptions: config.tierOptions,
      infoModal: {
        id: "info-modal",
        title: "",
        content: "",
      },
      items: [],
      fields: [
        {key: "runid", label: "Run id"}, 
        {key: "sampleid", label: "Sample id"},
        {key: "Date_Signoff", label: "Date Sign off"}        
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
        {key: "Reply", label: "Reply"},           
        {key: "Info"}
        ],
      filter1: /^\d/,
      filter2: /Not Relevant|Technical|^\s*$/i,
      filterOn: ["class"],
      Technical: ["Technical"],
      NotRelevant: ["Not Relevant"],
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
      } else if (items.length === 0) {
        
        this.selectedSample = "";
      }
    },
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
    this.variants[this.selectedRowIndex].Oncogenicity = this.oncoScore;
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
    openInfoModal(item, index, button) {
      console.log("openInfoModal")
      index = this.variants.indexOf(item);
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
      console.log("method to get signed off samples");
      const baseURI = config.$backend_url + "/api/signoff_samples";
      this.$http
        .get(baseURI)
        .then((response) => response.data)
        .then((data) => (this.items = data.data));
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


    approve() {
      // Sending approval date to database
      // This if only for signing off the user when interpretation is done. 
      console.log("Sign off method");
      
      // Metode for  sende inn dato, og tolkede varianter til backend.
      const baseURI = config.$backend_url + "/api/approve";
      this.$http
        .post(
          baseURI,
          {
            sampleid: this.selectedSample,
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
        this.$router.push({
        name: "Samples"
        });


    },

    unApprove() {
      // If the sample is not ready and needs to be sent back to the interpretation-list this button is used.
      // The button does the opposite of the sign-off
       // This if only for signing off the user when interpretation is done. 
      console.log("Sign off method");
      
      // Metode for  sende inn dato, og tolkede varianter til backend.
      const baseURI = config.$backend_url + "/api/unsignoff";
      this.$http
        .post(
          baseURI,
          {
            sampleid: this.selectedSample,
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