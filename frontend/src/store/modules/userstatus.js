import axios from 'axios';
import { config } from '../../config.js'
const state = {
    loggedInStatus: false,
    username: '',
    token: 'fdsksalkfdsø'
};

const getters = {
    loggedInStatus: (state) => state.loggedInStatus,
    username: (state) => state.username,
    token: (state) => state.token
}

const actions = {
    initStore: ({ commit }) => {
        const baseURI = config.$backend_url + "/chklogin";
        axios.get(baseURI)
        .then((response) => response.data)
        .then((data) => {
            commit('SET_STORE_STATUS', Boolean(data.logstatus));
            commit('SET_STORE_USERNAME', data.username);
        }
        );
    },
    UPDATE_TOKEN({commit}, token) {
        commit('SET_STORE_TOKEN', token);
    },
    UPDATE_STATUS({commit}, loggedInStatus) {
        commit('SET_STORE_STATUS', loggedInStatus);
    },
    UPDATE_USERNAME({commit}, username) {
        commit('SET_STORE_USERNAME', username);
    }

}

const mutations = {
    SET_STORE_TOKEN(state, token) {
        state.token = token;
    },
    SET_STORE_STATUS(state, loggedInStatus) {
        state.loggedInStatus = loggedInStatus;
    },
    SET_STORE_USERNAME(state, username) {
        state.username = username;
    },
}



export default {
    name: 'userstatus',
    state,
    getters,
    mutations,
    actions
}