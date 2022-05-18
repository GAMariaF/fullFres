<template>
  <div  id="app" class="container-fluid">
    <h1>Variants for sample: {{ sampleID }}</h1>
    <p>Click a row to start interpreting that Variant:</p>
    <b-table
      selectable
      select-mode="single"
      @row-selected="rowSelected"
      striped
      hover
      outlined
      :items="items"
      :fields="fields"
      :small="small"
    >

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
        updateVariants();
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
              ></b-form-textarea>
          </b-col>
          <b-col cols="2">
              <label>Class</label>
              <b-form-select :options="options"
                class="py-sm-0 form-control"
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
          <b-col cols="10">
          
              <h5>Available evidence types </h5>
              <b-table selectable select-mode="single" @row-selected="oncogenicitySelected" striped hover outlined :items="oncogenicitycriteria" :small="small" :fields="oncogenicityfields">
                <template #cell(evidence)="data">
                  <span v-html="data.value"></span>
                </template>
              </b-table>

            {{ oncoScore }}

            <br>
<div v-for="item in selectedoncogenicity_list" v-bind:key="item.id">
  <!-- content -->
  {{item.tag}}
</div>
            
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
  name: "varianttable",
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
      items: [
        {
          Kromosom: 4,
          Start: "123321",
          Stop: "123321",
          Variant: "c.432423A>T",
        },
        { Kromosom: 21, Start: "4213", Stop: "4213", Variant: "c.4323A>T" },
        {
          Kromosom: 9,
          Start: "32132",
          Stop: "32132",
          Variant: "c.41132423C>T",
        },
        { Kromosom: 8, Start: "3213", Stop: "3213", Variant: "c.43242A>G" },
      ],
      fields: ["Kromosom", "Start", "Stop", "Variant", "Info"],
    };
  },
  methods: {
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
    oncogenicitySelected(items) {
      console.log("selected row")
      console.log(typeof items[0])
      
      console.log(typeof items.length)

      
      // Utfør kun dersom en rad er valg - husk at på klikk to blir den deselektert
      // Ved klikk: hvis ikke allerede valgt, velg, ellers fjern.
      var index = this.selectedoncogenicity_list.indexOf(items[0]);
      if (index !== -1) {
        // Fjern hvis tilstede
        this.selectedoncogenicity_list.splice(index, 1);  
      } else {
        // Legge til hvis ikke tilstede
        this.selectedoncogenicity_list.push(items[0]);
        
      }
      // Legg til en tabell hvor default styrke er valgt
      // Tabellen vises kun hvis lengden av this.selectedACMG != 0
      // Regn ut oncoscore
      // Utfør kun om det faktisk er valgt en rad (length !== 0)
      if(items.length !== 0 | typeof items[0] !== 'undefined') {
        this.oncoScoring(this.selectedoncogenicity_list);
        }
      

      },    
    rowSelected(items) {
      this.selectedVariant = items[0].Variant;
      console.log("tester linje 100")
    },
    openInfoModal(item, index, button) {
        console.log("tester om openInfoModal funker")
      this.selectedRowIndex = index;
      this.infoModal.title = `Row index: ${index}`;
      this.infoModal.content = JSON.stringify({
        "name":"Amy",
        "age":37
      });
      this.$root.$emit("bv::show::modal", this.infoModal.id, button);  
    },

    resetInfoModal() {
      this.infoModal.title = "";
      this.infoModal.content = "";
    },
  },
};
</script>
