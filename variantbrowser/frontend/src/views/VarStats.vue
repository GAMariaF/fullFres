<template>
  <div>
    <VarStatsComponent :locked="locked"/>
  </div>
</template>

<script>
import VarStatsComponent from "../components/VarStatsComponent.vue";

export default {
  props: ['locked'],
  components: {
   
    VarStatsComponent
},
  data() {
    return {
      
    };
  },
  created: function () {
    this.$store.dispatch("initStore");
  },
  methods: {},
  watch: {},
  computed: {
    state() {
      return this.$store.getters.loggedInStatus;
    }
  }
};
</script>
