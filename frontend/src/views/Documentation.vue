<template>
    <div>

     <b-row>
      <b-col cols="2">
        <br />
        <h4 style="text-align:left;">&nbsp;&nbsp;&nbsp;Overview:</h4>

        <b-table
            selectable
            select-mode="single"
            @row-selected="pageRowSelected"
            hover
            thead-class="text-white"
            :items="pages"
            :fields="field"
            :small="small"
            >
            <template #cell(page)="data">
              <b>{{ data.value }}</b>
            </template>
          </b-table>

      </b-col>
      <b-col cols="1"></b-col>
      <b-col>
        <br />
        <h1 style="text-align:left;">&nbsp;&nbsp;{{ this.page }}</h1>

        <div>
          <p class="docPage">{{ this.text }}</p>
        </div>

      </b-col>
     </b-row>


    </div>   
</template>


<script>

import { docTexts } from '../docTexts.js'

export default {
  data() {
    return {
      pages: [{"Page": "Samples", "Key": "samplesText"}, 
              {"Page": "Control", "Key": "controlText"}, 
              {"Page": "All Samples", "Key": "allSamplesText"}, 
              {"Page": "Var Stats", "Key": "varStatsText"}, 
              {"Page": "Statistics", "Key": "statisticsText"}, 
              {"Page": "Report", "Key": "reportText"}
            ],
      page: "Documentation",
      field: ["Page"],
      small: true,
      //texts: docTexts.docTexts,
      text: ``,
    }
  },
  methods: {
    pageRowSelected(item){
      this.page = item[0].Page;
      this.text = docTexts[item[0].Key];
    },
  }
}

</script>

<style>
p.docPage {
  white-space: pre-wrap;
  text-align: left;
  text-size-adjust: 200%;
}
</style> 