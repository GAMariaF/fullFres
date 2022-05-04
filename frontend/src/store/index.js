import Vue from 'vue';
import Vuex from 'vuex';
import userstatus from './modules/userstatus';

//general


Vue.use(Vuex);
export const store = new Vuex.Store({
    modules: {
        userstatus
    }
});