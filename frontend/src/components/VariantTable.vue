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
          </b-col>
        </b-row>
        <hr />
        <b-row>
          <b-col cols="2">
            <p>Gene Info:</p>
          </b-col>
        </b-row>
      </b-container>
    </b-modal>

    <!--  -->
  </div>
</template>
<script>
export default {
  name: "varianttable",
  props: [ "loading" ],
  data() {
    return {
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
