<template>
  <div>
    <AllStatsComponent :locked="locked"/>
  </div>
</template>


<script>
import AllStatsComponent from "../components/AllStatsComponent.vue";

export default {
  props: ['locked'],
  components: {
   
    AllStatsComponent
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
