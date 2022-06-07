<template>
  <div  id="app" class="container-fluid">
    <h1>All variants</h1>
    <p>Click a row to start interpreting that Variant:</p>
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
        <pre>Set comment and class for variant:</pre>
        <b-row class="mb-1">
          <b-col cols="10">
            <label>Comment</label>
             <b-form-textarea 
                id="textarea"
                size="sm"
                placeholder="Comment here: "
                v-model="variants[selectedRowIndex].comment"
                @change="updateVariants;setChanged()"
                
              ></b-form-textarea>
          </b-col>
          <b-col cols="2">
              <label>Class</label>
              <b-form-select
                :options="options"
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
          <pre>Select which criterions apply to this variant:</pre>
          <b-col cols="12">
          <h5>Available evidence types </h5>
          <span v-for="item in oncogenicitycriteria" :key="item.tag">
            <b-button v-on:click="oncogenicitySelected(item)" v-b-tooltip.hover type="button" :title="item.title" :class="item.class">{{item.tag}}</b-button><span>&nbsp;</span>
          </span>
            <br>
            <div>
            Oncoscore:
            </div>
            {{ oncoScore }}

            <br>
        <div v-for="item in selectedoncogenicity_list" v-bind:key="item.id">
          <!-- content -->
          {{item.tag}}
        </div>
            
          </b-col>
        </b-row>

        <b-row>
          <b-col>
          <pre>  
          <b-button v-b-toggle.variant_info_full_collapse variant="info">Show full variant info</b-button>
            <b-collapse id="variant_info_full_collapse" class="mt-2">
          <div class="table-responsive">
            <table class="table-hover">
              <thead>
                <tr>
                    <th>Key</th>
                    <th>Value</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(value, name) in variants[selectedRowIndex]" :key="name">
                    <td>{{ name }}</td>
                    <td>{{ value }}</td>
                </tr>
              </tbody>
            </table>   
          </div>
</b-collapse>

          </pre>

          </b-col>
        </b-row>

      </b-container>
    </b-modal>
    
    

    <!--  -->
    
    
  </div>
</template>
<script>


import { config } from '../config.js'
export default {
  name: "allvarianttable",
  props: [ "loading" ],
  data() {
    return {
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
        {key: "Type", label: "Type", sortable: true},
        {key: "gene", sortable: true},
        {key: "CHROM", label: "Chrom", sortable: true},
        {key: "POS", label: "Pos", sortable: true},
        {key: "REF", label: "Ref", sortable: true},        
        {key: "ALTEND", label: "Alt / End", sortable: true},
        {key: "Frequency", sortable: true, sortDirection: 'desc'},
        {key: "oncomineGeneClass", sortable: true},
        {key: "oncomineVariantClass", sortable: true},
        {key: "class", sortable: true},
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
    },
    sendVariantsToPost() {
        console.log()

    },
  },
  created: function() {
    this.$store.dispatch("initVariantStore", {"sample_id": this.$route.params.id, "selected": 'empty', "allVariants": true});
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


