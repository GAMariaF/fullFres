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
          selected-variant="warning"
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
        <h2 v-if="selectedSample === ''">Please select a sample to begin control</h2>
        <div v-if="selectedSample !== ''">
          <h2>Variants for sample {{ selectedSample }}</h2>
          <h5>Signed off by {{ this.sampleUserSignoff }}</h5>
          <br>
          <h5>Gene List: <b>{{ this.variants[0].Genelist }}</b> 
            | Tumor %: <b>{{ this.variants[0].Perc_Tumor }}</b> 
            | Status: 
                <b style="color:rgb(100, 207, 100);" v-show="this.variants[0].Status=='Success'">Success</b>
                <b style="color:red;" v-show="this.variants[0].Status=='Failed'">Failed</b>
          </h5>
          <br>
          <h2><p style="text-align:left;">Reply (Svares ut)</p></h2>
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
          <br>
          <h2><p style="text-align:left;">No reply </p></h2>
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
            :filter-function="filterTable"
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
          <br>
          <h2><p style="text-align:left;">Not evaluated and Technical </p></h2>
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
            :filter="filter3"
            :filter-function="filterTable"
          >
            <!-- Adding index column -->
            <template #cell(Nr)="data">
              {{ data.index + 1 }}
            </template>
            <!-- Formatting Type column -->
            <template #cell(Type)="data">
              <b class="text-info">{{ data.value.toUpperCase() }}</b>
            </template>
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
          <br>
          <b-row class="mb-1">
          <b-col cols="12">
            <label>Sample Comment</label>
             <b-form-textarea
                id="textarea"
                size="default"
                
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
                    
          <br><br>
          <h3 v-if="warning !== ''">{{ this.warning }}</h3>
          <b-row>
            <b-col>
              <b-button v-on:click="unApprove();location.reload()" class="btn mr-1 btn-danger btn-lg"> Send Back </b-button>
            </b-col>
            <b-col>
              <b-button v-on:click="approve" class="btn mr-1 btn-success btn-lg"> Approve </b-button>
            </b-col>
          </b-row>
          
          <br><br>
        </div>
   
      </b-col>
    </b-row>
    <b-modal
    v-if="selectedSample !== ''"
    :id="infoModal.id"
    :title="infoModal.title"
    ok-only
    size="lg"
    @hide="resetInfoModal();sendVariants();allowClassification(false)"
    >
      <b-container fluid>
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
            <label>Predictive Data</label>
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
          <label v-if="allowEdit">Available evidence types:</label>
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
                placeholder=""
                rows=4
                v-model="variants[selectedRowIndex].CommentVPS"
                @change="updateVariants();setChanged()"

              ></b-form-textarea>
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
      allowEdit: false,
      sortedIndex: ['runid',
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
                    'TierVPS'
                  ],
      predictive_data: [],
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
      loggedInStatus: false,
      somethingChanged: false,
      warning: "",
      small: true,
      selectedSample: "",
      selectedRowIndex: 0,
      sampleUserSignoff: "",
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
      items: [],
      fields: [
        {key: "runid", label: "Run id"}, 
        {key: "sampleid", label: "Sample id"},
        {key: "Date_Signoff", label: "Date Sign off"},
        {key: "User_Signoff", label: "User"}    
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
        {key: "Specific", label: "Type Specific"},
        {key: "FILTER", label: "Filter"},
        {key: "Oncogenicity"},        
        {key: "class"},        
        {key: "Reply", label: "Reply"},           
        {key: "Info"}
        ],

      filter1: /Yes/,
      filterOn: ["Reply"],

      filter2: "row['Reply'] === 'No' && !['Not evaluated', 'Technical'].includes(row['class'])",
      filter3: "row['Reply'] === 'No' && ['Not evaluated', 'Technical'].includes(row['class'])", 
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
        // Get variants for that sample:
        this.$store.dispatch("initVariantStore", {"sample_id": this.selectedSample, "selected": 'empty', "allVariants": false});
        this.variants =  this.$store.getters.variants;
        this.sampleUserSignoff = items[0].User_Signoff
      } else if (items.length === 0) {
        
        this.selectedSample = "";
      }
    },
    updateVariants() {
      this.$store.commit("SET_STORE", this.variants);
      console.log("updateVariants");
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

    filterTable(row, filter) {
      //console.log(row)
      return(eval(filter));
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

    openInfoModal(item, index, button) {
      console.log("openInfoModal")
      index = this.variants.indexOf(item);
      this.selectedRowIndex = index;
      // Convert Prediktive_data-feltet fra databasen til array for å sette inn i select-box
      if ((typeof(this.variants[this.selectedRowIndex].Prediktive_data) !== 'undefined') && (this.variants[this.selectedRowIndex].Prediktive_data !== null)) {
        this.predictive_data = this.variants[this.selectedRowIndex].Prediktive_data.split(",");
      }
      //this.infoModal.title = `Variant: ${index + 1}`;
      this.infoModal.title = `${item['gene']}: ${item['annotation_variant']}`;
      this.$root.$emit("bv::show::modal", this.infoModal.id, button);  
    },
    resetInfoModal() {
      this.infoModal.title = "";
      this.infoModal.content = "";
      console.log("infomodal lukket")
      this.variants[this.selectedRowIndex].Prediktive_data = this.predictive_data.join().toString();
      this.predictive_data = [];
      console.log("infomodal lukket");
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
        // Viss noko har blitt endra, er det ikkje lenger mulig å godkjenne.
        this.unApprove();
        this.somethingChanged = true
        console.log("Something has changed - sending updated data to db")
      // Metode for  sende inn dato, og tolkede varianter til backend.
      // OBS: fjerner også signoff, altså prøven blir sendt tilbake til samples.
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

    updateComment() {
      var comment = this.variants[0].CommentSamples
      const baseURI = config.$backend_url + "/api/commentsample";
        this.$http.post(baseURI,
          {
            commentsamples: comment,
            sampleid: this.selectedSample,
          },
          {
          withCredentials: true,
          headers: { "Content-Type": "application/json" },
          }
        ).then((response) => response.data);
    },


    approve() {
      // Sending approval date to database
      // This if only for signing off the user when interpretation is done. 
      console.log("Sign off method");
      
      // Metode for  sende inn dato, og tolkede varianter til backend.
      
      // Må sjekke om noko har blitt endra.
      if(this.somethingChanged) {
        this.warning = "You are not allowed to approve after making changes."
      } else if(this.sampleUserSignoff === this.$store.getters.username) {
        this.warning = "You are not allowed to both sign off on and approve a sample."
      } else {

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
          //.then((response) => response.data);
          //this.$router.push({
          //name: "Control"
        //});
        location.reload();
      }
    },

    unApprove() {
      // If the sample is not ready and needs to be sent back to the interpretation-list this button is used.
      // The button does the opposite of the sign-off 
      console.log("Sign off method");
      
      // Metode for sende inn dato, og tolkede varianter til backend.
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
        .then((response) => response.data);
        //this.$router.push({
        //name: "Control"
        //});
        //location.reload();
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
<style>
label {
  color: rgb(7, 7, 129);
  font-size: large;
}
</style>