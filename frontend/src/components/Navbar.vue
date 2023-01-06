<template>

<b-navbar toggleable="lg" type="dark" variant="info">
    <b-navbar-brand to="/"> &nbsp; Variant browser</b-navbar-brand>
    <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>
     <b-navbar-nav>
        <b-nav-item to="/samples" v-show="state">Samples</b-nav-item>
        <b-nav-item to="/control" v-show="state">Control</b-nav-item>        
        <b-nav-item to="/allvariants" v-show="state">All Variants</b-nav-item>
        <b-nav-item to="/allsamples" v-show="state">All Samples</b-nav-item>  
        <b-nav-item to="/statistics" v-show="state">Statistics</b-nav-item>
        <b-nav-item to="/report" v-show="state">Report</b-nav-item>
        <b-nav-item to="/login" v-show="!state">Login</b-nav-item>
        
          <b-nav-item-dropdown right v-show="state">
          <!-- Using 'button-content' slot -->
          <template #button-content>
            <em v-show="state">{{username}}</em>
            <em v-show="!state">User</em>
          </template>
          <b-dropdown-item to="/profile">Profile</b-dropdown-item>
          <b-dropdown-item to="/" @click="signout">Sign Out</b-dropdown-item>
        </b-nav-item-dropdown>
      </b-navbar-nav>
</b-navbar>
</template> 

<script>
import { config } from '../config.js';
import util_funcs from "@/appUtils";
export default {
    name: "navbar",
    data() {
      return {
        signOut_URL: config.$signout_url(),
        //username: this.$store.getters.username
      }
    },
    methods: {
      signout() {
        console.log("signout")
        // Delete cookie (logs you out)
        util_funcs.delete_cookie('sid')
        // Reload the page
        this.$router.push({        name: "login"        });

      }
    },
    computed: {
    state() {
      return this.$store.getters.loggedInStatus
      },
    username() {
      return this.$store.getters.username
    }
    },
    watch: {
    state (newState, oldState) {
      console.log(`State changed from ${oldState} to ${newState}`)
      this.$forceUpdate();
    },
  },
}
</script>
