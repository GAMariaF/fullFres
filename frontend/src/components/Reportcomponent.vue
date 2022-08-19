<template>
  <b-container id="app" fluid v-show="state">
    <p>Tester at det kommer noe</p>

    <b-row>
      <b-col cols="3">
        <br />

        <h2>Approved samples</h2>
        <br />
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
        <br />
        <h2 v-if="selectedSample === ''">Please select a sample</h2>
        <div v-if="selectedSample !== ''">
          <h2>Variants for sample {{ selectedSample }}</h2>
          <br /><br />
          <h5>
            Gene List: <b>{{ this.variants[0].Genelist }}</b> | Tumor %:
            <b>{{ this.variants[0].Perc_Tumor }}</b>
          </h5>
          <br />
          <h2><p style="text-align: left">Classified variants</p></h2>
          <br />
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
          <br />
          <h2>
            <p style="text-align: left">
              Not Relevant, Technical or not interpreted variants
            </p>
          </h2>
          <br />
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

          <br /><br />
        </div>
      </b-col>
    </b-row>
  </b-container>
</template>
<script>
import { config } from '../config.js'
import util_funcs from "@/appUtils";


export default {
  props: ["locked"],
  name: "reportcomponent",
  data() {
    return {
      loggedInStatus: false,
      selectedSample: "",
      small: true,
      items: [],
      fields: [
        { key: "runid", label: "Run id" },
        { key: "sampleid", label: "Sample id" },
        { key: "Date_Approval", label: "Date Approval" },
      ],
    };
  },
  methods: {
    sampleRowSelected(items) {
      if (items.length === 1) {
        this.selectedSample = items[0].sampleid;
        console.log(this.selectedSample);
        // Get variants for that sample:
        this.$store.dispatch("initVariantStore", {
          sample_id: this.selectedSample,
          selected: "empty",
          allVariants: false,
        });
        this.variants = this.$store.getters.variants;
      } else if (items.length === 0) {
        this.selectedSample = "";
      }
    },
  },
  created: function () {
    util_funcs.query_backend(config.$backend_url, "report").then(data => this.items = data.data);

  },
  computed: {
    state() {
      return this.$store.getters.loggedInStatus;
    },
  },
  watch: {},
};
</script>
