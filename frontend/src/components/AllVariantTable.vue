<template>
  <div  id="app" class="container-fluid">
    <h1>All variants</h1>
    <br>
       
        <b-col lg="6" class="my-1">
           <b-input-group size="sm">
              <b-input v-model="filter" placeholder="Filter table.."></b-input> 
           </b-input-group>
        </b-col>
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

    <!--  test -->
<b-button v-on:click="sortTable(variants)" type="button">Testklikk sorter</b-button><span>&nbsp;</span>
    <!--  -->


  </div>
</template>
<script>


import { config } from '../config.js'
import util_funcs from "@/appUtils";
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
        {key: "annotation_variant", label: " Annotation Variant"},
        {key: "CHROM", sortable: true},        
        {key: "POS", label: "Pos", sortable: true},
        {key: "REF", label: "Ref", sortable: true},
        {key: "ALTEND", label: "Alt / End", sortable: true},
        {key: "Frequency", sortable: true, sortDirection: 'desc'},
        {key: "SamplesPerVariant", label: "Samples"},
        {key: "oncomineGeneClass", sortable: true},
        {key: "oncomineVariantClass", sortable: true},
        {key: "class", sortable: true},
        {key: "Info"}
        ],
      sortedIndex: [ 'SamplesPerVariant',
                    'gene',
                    'transcript',
                    'annotation_variant',
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
                    'Tier'
                  ],
      filter: '',
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
      case 'Supporting':
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
        this.selectedVariant = items;
        console.log("test")

      } else if (items.length===0) {
        this.selectedVariant = "";
        console.log("unselected")
      }
    },
    openInfoModal(item, index, button) {
      console.log("openInfoModal")
      this.selectedRowIndex = index;
      this.infoModal.title = `Variant: ${item.transcript}`;
      this.$root.$emit("bv::show::modal", this.infoModal.id, button);
      //this.variants = util_funcs.sort_table(this.variants);
      //this.$store.commit("SET_STORE",this.variants)
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
    sortTable() {
      this.variants = util_funcs.sort_table(this.variants);
      this.$store.commit("SET_STORE", this.variants)
      console.log("variants have been sorted")

    }
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
