import axios from 'axios'
var util_funcs = {
    sort_table(objects) {
        const order = [ "chr1", "chr2", "chr4","chr10" ];       
        const orderIndex = {}
        order.forEach((value, index) => orderIndex[value] = index);
        // Sort
        objects.sort((a, b) => orderIndex[a.CHROM] - orderIndex[b.CHROM]);
        return objects
    },
    query_backend(url, query) {
        // Funksjon som sender query til backend
        const baseURI = url + '/api/' + query
        return axios.get(baseURI)
        .then(function (response) {return response.data});      
    },
    delete_cookie(name) {
        document.cookie = name + '=;expires=Thu, 01 Jan 1970 00:00:01 GMT;';
    }
};

export default util_funcs;

