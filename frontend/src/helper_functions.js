//import axios from 'axios';


import * as fs from 'fs'

var helper_funcs = {

}

export default helper_funcs;


export function get_ip() {

    //const { readIniFile } = require('read-ini-file')
    const path = '/illumina/analysis/dev/2023/mfahls/db/config_ip.ini'
    //const { fs } = require('fs')

    var text = fs.readFileSync(path,'utf8')
    console.log (text)
   
    
  }


