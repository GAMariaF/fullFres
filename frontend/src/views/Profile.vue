<template>
    <div>
     <b> Logged in as: {{username}} </b>
    </div>  
</template>

<script>

//import axios from 'axios';
import { config } from '../config.js'


export default {
  name: "profile",
  data: () => ({

    //username: "",
    tempdata: "",

    profile_URL: config.$backend_url + "/profile"    
  }),
  methods: {},
  created: function () {
    // initstore sjekk innlogging
    this.$store.dispatch("initStore");
  },
  watch: {
    state(newState, oldState) {
      console.log(`State changed from ${oldState} to ${newState}`);
    },
  },
  computed: {
    state() {
      return this.$store.getters.loggedInStatus;
    },
    username() {
      return this.$store.getters.username
    }
  },

}



</script>