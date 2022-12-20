<template>
  <div>
    <Reportcomponent :locked="locked"/>
  </div>
</template>


<script>
import Reportcomponent from "../components/Reportcomponent.vue";

export default {
  props: ['locked'],
  components: {
   
    Reportcomponent
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
