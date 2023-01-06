<template>
  <div id="app">
    <b-container fluid>
    <navbar />
    <router-view />
    </b-container>
  </div>
</template>

<script>

import Navbar from './components/Navbar.vue';

export default {
  name: 'App',
  components: {
    Navbar
  },
  data() {
    return {
    }
  },
  computed: {
    state() {
      return  this.$store.getters.loggedInStatus
      }
  },
  watch: {
    state (newState, oldState) {
      console.log(`State changed from ${oldState} to ${newState}`)
    }
  },
  created: function() {
    this.$store.dispatch("initStore");
    console.log(this.$store.getters.loggedInStatus);
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
