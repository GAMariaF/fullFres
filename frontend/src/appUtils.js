import axios from 'axios'
var util_funcs = {

    query_backend(url, query) {
        // Funksjon som sender query til backend
        const baseURI = url + '/api/' + query
        return axios.get(baseURI)
        .then(function (response) {return response.data});      
    },
    sort_table(objects){
        console.log("sort_table")
        // const order = ["Locus","Ref","ALTEND","gene"];
        // const orderIndex = {}
        // order.forEach((value,index) => orderIndex[value]=index);
        // console.log(orderIndex)
        // // //const sortable = Object.entries(objects)
        //console.log(objects[sortable])
        // Sort
        //objects.sort((a,b) => orderIndex[a.CHROM] - orderIndex[b.CHROM]);
        return objects
    }
};

export default util_funcs;

