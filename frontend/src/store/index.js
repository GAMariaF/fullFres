import Vue from 'vue';
import Vuex from 'vuex';
import userstatus from './modules/userstatus';
import variants from './modules/variants';

//general


Vue.use(Vuex);
export const store = new Vuex.Store({
    modules: {
        userstatus,
        variants
    }
});