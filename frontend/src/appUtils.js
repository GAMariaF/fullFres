import axios from 'axios'
var util_funcs = {

    query_backend(url, query) {
        // Funksjon som sender query til backend
        const baseURI = url + '/api/' + query
        return axios.get(baseURI)
        .then(function (response) {return response.data});      
    },
    sort_by_list(variant) {
        print('hei')
        return variant;
    }

};

export default util_funcs;

