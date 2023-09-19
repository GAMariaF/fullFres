<template>
  <div id="login">
    <div class="h-100 bg-plum-plate-login bg-animation">
      <div class="d-flex h-100 justify-content-center align-items-center">
        <b-col md="8" class="mx-auto app-login-box">
          
        <span v-show="state">You are already logged in. Go to <router-link to="/samples">samples ready for interpretation</router-link></span>
          <div v-show="!state" class="modal-dialog w-100 mx-auto">
            <div class="modal-content">
              <div class="modal-body">
                <div class="h5 modal-title text-center">
                  <h4 class="mt-2">
                    <div>Welcome to the Variant Browser!</div>
                    <span></span>
                  </h4>
                </div>
                
                <div class="divider" />

                <div class="row row justify-content-center">
                  <div class="col-xs-12">
                    <form
                      name="login"
                      method="POST"
                      class="box"
                    >
                      <h1 class="h3">Please sign in:</h1>
                      <label for="defaultFormLoginEmailEx" class="grey-text"
                        >Your username</label
                      >
                      <input
                        name="username"
                        type="username"
                        v-model="username"
                        id="defaultFormLoginEmailEx"
                        class="form-control input is-rounded"
                        dir="auto"
                        
                      />
                      <br />
                      <label for="defaultFormLoginPasswordEx" class="grey-text"
                        >Your password</label
                      >
                      <input
                        name="password"
                        type="password"
                        v-model="password"
                        class="form-control input is-rounded"
                        dir="auto"
                        
                      />
                      <div class="text-center mt-4">
                    <b-button variant="primary" @click="doLogin" size="lg">Login</b-button>
                      </div>
                    </form>
                  </div>
                </div>

                <div class="divider" />
              </div>

              <div class="modal-footer clearfix">
                <div class="float-right">
                  
                  <br />
                  <br />
                  <br />
                  {{ tempdata }}
                  <br />
                  <br />
                  
                  <br />
                  
                  <br />
                  
                  <br />
                  <br />
                  
                  
                </div>
              </div>
            </div>
          </div>
          <div class="text-center text-white opacity-8 mt-3">
            <strong> Copyright &copy; camellabs.com </strong>
          </div>
        </b-col>
      </div>
    </div>
  </div>
</template>


<script>
import axios from 'axios';
import { config } from '../config.js'


export default {
  name: "Login",
  data: () => ({
    username: "",
    password: "",
    tempdata: "",
    login_URL: config.$backend_url + "/login"    
  }),
  methods: {
    doLogin: function () {
      // Sjekker brukernavn og passord mot database og sender tilbake en JWT
      if (this.username != "" && this.password != "") { 
        const baseURI = config.$backend_url + "/login";
        const article = {
            username: this.username,
            password: this.password
         };
        const headers = { 
            //"Authorization": "Bearer my-token",
        };
        axios.post(baseURI, article, {headers})
          .then((response) => response.data)
          .catch((error) => {
            console.log(error.response.data.message);
            alert("Wrong Credentials.");
          })
          .then((data) => {
            console.log(data);
            console.log(data['token']);
            // Send token to Store
            this.$store.commit('SET_STORE_TOKEN', data['token']);
            this.token = this.$store.getters.token;
            // Send status to store
            this.$store.commit('SET_STORE_STATUS', true);
            this.loggedInStatus = this.$store.getters.loggedInStatus;
            // Send username to store
            this.$store.commit('SET_STORE_USERNAME', this.username);
          });
      } else {
        alert("Please fill both fields!");
      }
    },
   
  },
  created: function() {
      this.$store.dispatch("initStore");
  },
  computed: {
    state() {
      return  this.$store.getters.loggedInStatus
      }
  },
  watch: {
    state (newState, oldState) {
      console.log(`State changed from ${oldState} to ${newState}`)
      if(newState) {
        this.$router.push({        name: "Profile"        });
      }
    }
  },
};
</script>