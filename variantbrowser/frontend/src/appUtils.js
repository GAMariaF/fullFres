import axios from 'axios'
import { config } from './config.js'
var util_funcs = {
    sort_table(objects) {
        const order = [ "chr1", "chr2", "chr4","chr10" ];       
        const orderIndex = {}
        order.forEach((value, index) => orderIndex[value] = index);
        // Sort
        objects.sort((a, b) => orderIndex[a.CHROM] - orderIndex[b.CHROM]);
        return objects
    },
    query_backend(url, query, terms = {}) {
        // Funksjon som sender query til backend
        const baseURI = url + '/api/' + query
        return axios.get(baseURI, terms)
        .then((response) => {return response.data});      
    },
    delete_cookie(name) {
        document.cookie = name + '=;expires=Thu, 01 Jan 1970 00:00:01 GMT;';
    },
    generate_report() {
        // Hent en categori fra cat
        config.reportcodes
        return ("generate_report")
        
    } 
};

export default util_funcs;

