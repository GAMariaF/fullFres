import { config } from '../../config.js';
import util_funcs from "@/appUtils";


const state = {
	variants: []
};

const getters = {
	variants: (state) => {
		return state.variants;
	}
};

const actions = {
	initVariantStore: ({ commit }, payload) => {
        util_funcs.query_backend(config.$backend_url,'variants_' + payload.sample_id).then(result => {
			var variants = result['data'];
            commit('SET_STORE', Object.values(variants));
        })
	}
};

const mutations = {
	SET_STORE(state, variants) {
		console.log("updated variants")
		state.variants = variants;
	}
};

export default {
	name: 'variants',
	state,
	getters,
	actions,
	mutations
};
