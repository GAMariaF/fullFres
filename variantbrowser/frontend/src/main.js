import Vue from 'vue'
import App from './App.vue'
import axios from 'axios'
// Bootstrap imports
import { BootstrapVue, IconsPlugin } from 'bootstrap-vue'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import router from './router'
import { store } from './store'

Vue.config.productionTip = false

// Install BootstrapVue
Vue.use(BootstrapVue)
Vue.use(IconsPlugin)
Vue.prototype.$http = axios
axios.defaults.withCredentials = true

new Vue({
  router,
  store,
  render: h => h(App),
}).$mount('#app')
