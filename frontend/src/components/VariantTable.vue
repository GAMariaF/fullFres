<template>
  <b-container id="app" fluid v-if="variants">
  
  
  
    <h1>Variants for sample: {{ sampleID }}</h1>
    <br>
    <h5>Gene List: <b >{{ this.variants[0].Genelist }}</b> | Tumor %: <b>{{this.variants[0].Perc_Tumor}}</b></h5>
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
      @hide="resetInfoModal();sendVariants();allowClassification(false)"
    >
      <b-container fluid>
        <div v-if="locked === false">
        <b-row class="mb-1">
          <b-col cols="4">
            <label>Reply (Svares ut)</label>
            <b-form-select
              :options="replyOptions"
              class="py-sm-0 form-control"
              v-model="variants[selectedRowIndex].Reply"
              @change="updateVariants();setChanged()" 
            >
            </b-form-select>
          </b-col>            
          <b-col cols="4">
            <label>Classification date:</label>
            <td>{{ getDate() }}</td>
          </b-col> 
          <b-col cols="4">
            <b-button v-on:click="allowClassification(true)" class="btn mr-1 btn-info"> Edit Classification </b-button>
          </b-col>          
        </b-row>
        <br>
        <b-row class="mb-1">
          <b-col cols="6">
            <label>Population Data (GnomAD)<br><i>OP4: 2/152182 (+1)</i></label>
            <p v-if="!allowEdit">{{ variants[selectedRowIndex].Populasjonsdata }}</p>
             <b-form-textarea
                id="textarea"
                size="default"
                
                @click="changedatastate"
                v-if="allowEdit"
                v-model="variants[selectedRowIndex].Populasjonsdata"
                @change="updateVariants();setChanged()"
                

              ></b-form-textarea>
          </b-col>
          <b-col cols="6">
            <label>Computational Evidence (Revel)<br><i>SBP1: 0,448 Benign (-1)</i></label>
            <p v-if="!allowEdit">{{ variants[selectedRowIndex].Computational_evidens }}</p>
            <b-form-textarea
                id="textarea"
                size="default"
                
                @click="changedatastate"
                v-if="allowEdit"
                v-model="variants[selectedRowIndex].Computational_evidens"
                @change="updateVariants();setChanged()"

              ></b-form-textarea>
          </b-col>
        </b-row>

        <b-row class="mb-1">
          <b-col cols="6">
            <label>Functional Studies</label>
            <p v-if="!allowEdit">{{ variants[selectedRowIndex].Funksjonsstudier }}</p>
              <b-form-select
                :options="functionalOptions"
                class="py-sm-0 form-control"
                v-if="allowEdit"
                v-model="variants[selectedRowIndex].Funksjonsstudier"
                @change="updateVariants();setChanged()" 
              >
              </b-form-select>
          </b-col>
          <b-col cols="6">
            <label>Cancer Hotspots</label>
            <p v-if="!allowEdit">{{ variants[selectedRowIndex].Cancer_hotspots }}</p>
            <b-form-select
              :options="cancerhotspotsOptions"
              class="py-sm-0 form-control"
              v-if="allowEdit"
              v-model="variants[selectedRowIndex].Cancer_hotspots"
              @change="updateVariants();setChanged()" 
            >
            </b-form-select>
          </b-col>            		            

        </b-row>

        <b-row class="mb-1">
          <b-col cols="6">
            <label>Predictive Data </label>
            <p v-if="!allowEdit"><i>See evidence</i></p>
            <b-form-select
              :options="predictiveOptions"
              multiple :select-size="6"              
              class="py-sm-0 form-control"
              v-if="allowEdit"
              v-model="predictive_data"
              @change="updateVariants();setChanged()" 
            >
            </b-form-select>
          </b-col>       
          <b-col cols="6">
            <label>Conservation (PhyloP)</label>
            <p v-if="!allowEdit">{{ variants[selectedRowIndex].Konservering }}</p>
             <b-form-textarea
                id="textarea"
                size="default"
                
                @click="changedatastate"
                v-if="allowEdit"
                v-model="variants[selectedRowIndex].Konservering"
                @change="updateVariants();setChanged()"

              ></b-form-textarea>
              
          </b-col>

        </b-row>

        <b-row class="mb-1">
          <b-col cols="6">
            <label>ClinVar</label>
            <p v-if="!allowEdit">{{ variants[selectedRowIndex].ClinVar }}</p>
             <b-form-textarea
                id="textarea"
                size="default"
                
                @click="changedatastate"
                v-if="allowEdit"
                v-model="variants[selectedRowIndex].ClinVar"
                @change="updateVariants();setChanged()"

              ></b-form-textarea>
          </b-col>
          <b-col cols="6">
            <label>Other DB</label>
            <p v-if="!allowEdit">{{ variants[selectedRowIndex].Andre_DB }}</p>
             <b-form-textarea
                id="textarea"
                size="default"
                
                @click="changedatastate"
                v-if="allowEdit"
                v-model="variants[selectedRowIndex].Andre_DB"
                @change="updateVariants();setChanged()"

              ></b-form-textarea>
          </b-col>
        </b-row>    

        <b-row class="mb-1">
          <b-col cols="6">
              <label>Class</label>
              <p v-if="!allowEdit">{{ variants[selectedRowIndex].class }}</p>
              <b-form-select
                :options="classOptions"
                class="py-sm-0 form-control"
                v-if="allowEdit"
                v-model="variants[selectedRowIndex].class"
                @change="updateVariants();setChanged()" 
              >
              </b-form-select>
              
          </b-col>
          <b-col cols="6">
              <label>Tier</label>
              <p v-if="!allowEdit">{{ variants[selectedRowIndex].TierVPS }}</p>
              <b-form-select
                :options="tierOptions"
                class="py-sm-0 form-control"
                v-if="allowEdit"
                v-model="variants[selectedRowIndex].TierVPS"              
                @change="updateVariants();setChanged()" 
              ></b-form-select>
            </b-col>
        </b-row>

        <b-row class="mb-1">
          <b-col cols="12">
            <label>Classification Comment</label>
            <pre v-if="!allowEdit">{{ variants[selectedRowIndex].Comment }}</pre>
             <b-form-textarea
                id="textarea"
                size="default"
                
                @click="changedatastate"
                placeholder=""
                rows=4
                v-if="allowEdit"
                v-model="variants[selectedRowIndex].Comment"
                @change="updateVariants();setChanged()"

              ></b-form-textarea>
          </b-col>
        </b-row>
        <b-row>
          <b-col cols="12">
              <label>Alt Annotation:</label>
              <b-form-textarea
                id="textarea"
                
                @click="changedatastate"
                v-model="variants[selectedRowIndex].annotation_variant2"
                @change="updateVariants();setChanged()" 
              >
              </b-form-textarea>
              </b-col>
        </b-row>

        <hr />
        <b-row>
          <b-col cols="10">
            <label>Oncogenicity Info</label>
          </b-col>
        </b-row>
        <b-row>
          <b-col cols="12">
          <label>Available evidence types:</label>
          <br>
          <span v-for="item in oncogenicitycriteria" :key="item.tag">
            <b-button v-if="allowEdit" v-on:click="oncogenicitySelected(item);updateVariants();setChanged()" v-b-tooltip.hover type="button" :title="item.title" :class="item.class">{{item.tag}}</b-button><span>&nbsp;</span>
          </span>
          <br>
          <br>
            <label v-if="allowEdit" >Adjust Oncogenicity</label>
              <b-input v-if="allowEdit" v-model="oncoAdjust" placeholder="Adjust Oncogenicity"></b-input>
            <br>
        
            <div>
            <h5>Oncogenicity: {{ this.variants[this.selectedRowIndex].Oncogenicity }}</h5>
            <label>Chosen evidence types:</label>
            </div>
            {{this.variants[this.selectedRowIndex].evidence_types}}

        </b-col>
        </b-row>
        <br>
        <b-row class="mb-1">
          <b-col cols="12">
            <label>Sample Variant Comment</label>
             <b-form-textarea
                id="textarea"
                size="default"
                @click="changedatastate"
                placeholder=""
                rows=4
                v-model="variants[selectedRowIndex].CommentVPS"
                @change="updateVariants();setChanged()"

              ></b-form-textarea>
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
    <b-row class="mb-1">
          <b-col cols="12">
            <label>Sample Comment</label>
             <b-form-textarea
                id="textarea"
                size="default"
                
                @click="changedatastate"
                placeholder=""
                rows=4
                v-model="variants[0].CommentSamples"

              ></b-form-textarea>
          </b-col>
        </b-row>
        <b-col>
          <br>
          <b-button v-on:click="updateComment" class="btn mr-1 btn-info"> Update Comment </b-button>
          <br>
        </b-col>
        
     <br>       
    <b >{{ this.variants[0] }}</b>
      <br>
      <br>
      <div v-if="locked === false">
      <h5>When interpretation is done, please sign off here</h5>
      <br>

    <b-alert dismissible fade :show="showDismissibleAlert" @dismissed="showDismissibleAlert=false" variant="danger">All variants must have a reply!</b-alert>
      <b-row>
        <b-col>
          <b-button v-on:click="failedSample" class="btn mr-1 btn-danger btn-m"> Failed Sample </b-button>
          </b-col>
          <b-col>
          <b-button v-on:click="fillReply" class="btn mr-1 btn-warning btn-m"> Fill Reply </b-button>
          </b-col>
          <b-col>
          <b-button v-on:click="signOff" class="btn mr-1 btn-success btn-m"> Sign off </b-button>
        </b-col>
      </b-row>
      </div>
    <!--  -->
    <br>
  </b-container>
</template>
<script>

import { config } from '../config.js'
//import util_funcs from "@/appUtils";
export default {
  props: ['locked'],
  name: "varianttable",
  data() {
    return {
      predictive_data: [],
      datastate: true,
      showDismissibleAlert: false,
      loading: true,
      allowEdit: false,
      sortedIndex: ['runid',
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
                    'TierVPS'
                  ],
      oncoScore: 0,
      oncoAdjust: 0,
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
      replyOptions: config.replyOptions,
      functionalOptions: config.functionalOptions,
      predictiveOptions: config.predictiveOptions,
      cancerhotspotsOptions: config.cancerhotspotsOptions,
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
        {key: "Type", label: "Type", sortable: true},
        {key: "gene", sortable: true},
        {key: "exon"},
        {key: "Locus"},
        {key: "REF", label: "Ref"},
        {key: "ALTEND", label: "Alt / End"},
        {key: "annotation_variant", label: "Annotation Variant"},
        {key: "oncomineGeneClass"},
        {key: "oncomineVariantClass"},
        {key: "Specific", label: "Type Specific"},
        //{key: "AF", label: "Allele fraction", sortable: true},
        {key: "Oncogenicity"},
        {key: "class"},
        {key: "Reply", label: "Reply (Svares ut)"},
        {key: "Info"}
        ],
        
    };
  },
  methods: {
    changedatastate() {
      // What is the point of this?
      //(I changed it to false and false to avoid the previous behaviour)
      if (this.datastate == true) {
        this.datastate = false
      } else {
        this.datastate = false
        }
     
    },
    fillReply(){
      // Fills Not evaluated in the reply-col of the variants that are empty
      this.variants.forEach((item, index) => {
        if ((this.variants[index].Reply === null ) || (this.variants[index].Reply.length === 0 )) {
          this.variants[index].Reply = 'No';
          this.variants[index].changed = true;
          if ((this.variants[index].class === null) || (this.variants[index].class.length === 0)) {
            this.variants[index].class = 'Not evaluated';
          }
        }
      });
          
      this.updateVariants();
      this.sendVariants();
      
    },
    showAlert() {
        this.dismissCountDown = this.dismissSecs
      },
    updateVariants() {
      this.$store.commit("SET_STORE", this.variants);
      console.log("updateVariants");
    },

    oncoScoring(selectedoncogenicity_list) {
      if (selectedoncogenicity_list.length == 0) {
        this.variants[this.selectedRowIndex].Oncogenicity = "";
      } else {

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
          case 'adjust':
            this.oncoScore += parseInt(this.oncoAdjust)
            break;
          }
        })

        if (this.oncoScore == 0){
          this.oncoScore = "0";
        }
        this.variants[this.selectedRowIndex].Oncogenicity = this.oncoScore;
      }
    },

    setChanged() {
      this.variants[this.selectedRowIndex].visibility = true;
      this.variants[this.selectedRowIndex].changed = true;
      this.updateVariants();
      console.log("setChanged");
    },

    allowClassification (state) {
      this.allowEdit = state;
    },

    getDate() {
      var date =
      this.variants[this.selectedRowIndex].DATE_CHANGED_VARIANT_BROWSER.substring(4,6) + '.' + 
      this.variants[this.selectedRowIndex].DATE_CHANGED_VARIANT_BROWSER.substring(2,4) + '.' +
      this.variants[this.selectedRowIndex].DATE_CHANGED_VARIANT_BROWSER.substring(0,2)
      
      if (date === '..') {
        return("Not previously classified")
      } else {
        return(date)
      }
    },

    oncogenicitySelected(items) {
  
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

    typeSpecificValue(data) {
      if(data.item['Type'] === null) {
        return("")
      }
      switch(data.item['Type'].toUpperCase()) {
        case 'SNP':
            return("AF: "+data.item['AF']);
          case 'DEL':
            return("AF: "+data.item['AF']);
          case 'MNP':
            return("AF: "+data.item['AF']);
          case 'FUSION':
            return(data.item['Variant_ID']+"\nRPM: "+data.item['Read_Counts_Per_Million']);
          case 'CNV':
            return("CN: "+data.item['Copy_Number']);
          case 'INS':
            return("AF: "+data.item['AF']);
          case 'RNAEXONVARIANT':
            return(data.item['Variant_ID']+"\nRPM: "+data.item['Read_Counts_Per_Million']);
          case 'COMPLEX':
            return("AF: "+data.item['AF'])
          default:
            return("");
      }
    },

    rowSelected(items) {  
      if (items.length===1) {
        this.selectedVariant = items;
      } else if (items.length===0) {
        this.selectedVariant = "";
      }
    },

    openInfoModal(item, index, button) {
      console.log("openInfoModal");
      index = this.variants.indexOf(item);
      this.selectedRowIndex = index;
      // Convert Prediktive_data-feltet fra databasen til array for å sette inn i select-box
      if ((typeof(this.variants[this.selectedRowIndex].Prediktive_data) !== 'undefined') && (this.variants[this.selectedRowIndex].Prediktive_data !== null)) {
        this.predictive_data = this.variants[this.selectedRowIndex].Prediktive_data.split(",");
      }
      //this.infoModal.title = `Variant: ${index +1}`;
      this.infoModal.title = `${item['gene']}: ${item['annotation_variant']}`;
      this.$root.$emit("bv::show::modal", this.infoModal.id, button);
      this.datastate = true;
    },
    resetInfoModal() {
      this.infoModal.title = "";
      this.infoModal.content = "";
      this.selectedoncogenicity_list = [];
      this.oncoScore = 0;
      // Get Prediktive_data-field into variants for this specific variant
      this.variants[this.selectedRowIndex].Prediktive_data = this.predictive_data.join().toString();
      this.predictive_data = [];
      console.log("infomodal lukket");
    },
    updateComment() {
      var comment = this.variants[0].CommentSamples
      const baseURI = config.$backend_url + "/api/commentsample";
        this.$http.post(baseURI,
          {
            commentsamples: comment,
            sampleid: this.$route.params.id,
          },
          {
          withCredentials: true,
          headers: { "Content-Type": "application/json" },
          }
        ).then((response) => response.data);
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
          .then((response) => response.data);
      } 
    },

    failedSample() {

      var all_reply = true
      this.variants.forEach(item => {
        if (item.Reply != "Yes" & item.Reply != "No" & item.Reply != 'Yes, VN') {
          all_reply = false
        }
      })
      // Metode for  sende inn dato, og tolkede varianter til backend.
      const baseURI = config.$backend_url + "/api/failedsample";
      if(all_reply) {
      this.$http
        .post(
          baseURI,
          {
            sampleid: this.$route.params.id,
            user: this.$store.getters.username,
          },
          {
            withCredentials: true,
            headers: { "Content-Type": "application/json" },
          }
        )
        .then((response) => response.data);
        this.$router.push({
        name: "Samples"
        });
      } else { this.showDismissibleAlert=true }
    },

    signOff() {
      // This if only for signing off the user when interpretation is done. 
      console.log("Sign off method");
      
      // Først - sjekk om alle rader har yes/no på reply
      var all_reply = true
      this.variants.forEach(item => {
        if (item.Reply != "Yes" & item.Reply != "No" & item.Reply != 'Yes, VN') {
          all_reply = false
        }
      })
      // Metode for  sende inn dato, og tolkede varianter til backend.
      const baseURI = config.$backend_url + "/api/signoff";
      if(all_reply) {
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
        .then((response) => response.data);
        this.$router.push({
        name: "Samples"
        });
      } else { this.showDismissibleAlert=true }
    },
  },

  created: function() {
    this.$store.dispatch("initVariantStore", {"sample_id": this.$route.params.id, "selected": 'empty', "allVariants": false});
  },

  computed: {
    currentRouteName() {
        return this.$route.name;
    },
    variants: {
      get() {return this.$store.getters.variants;},
      set(value) {this.$store.commit("SET_STORE", value)},
      
    }
  },
  watch: {
      // Use of loading?
      variants(newVars, oldVars) {
      console.log(`Changed from ${oldVars} to ${newVars}`);
      this.loading = false;
      // When a new set of variants are selected they are checked for whether they are benigne or technical,
      // then automatically assiged 'No' as reply.
      this.variants.forEach(item => {
            if ((item.class === "Technical" || item.class === "1 - Benign") && (item.Reply === null || item.Reply === "")) {
                item.Reply = "No";
                item.visibility = true;
                item.changed = true;
            }
      })
      this.$store.commit('SET_STORE', this.variants);
      this.sendVariants();
    },
  },
};
</script>
<style>
label {
  color: rgb(7, 7, 129);
  font-size: large;
}
</style>
