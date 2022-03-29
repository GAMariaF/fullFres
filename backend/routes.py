from flask import Flask, request, jsonify, json
from backend import app
from flask_cors import cross_origin

'''
En route man kan sende alle varianter fra med POST request
'''

data = "['foo', {'bar': ('baz', None, 1.0, 2)}]"
samples = '[{"Sample": "4_21"}, {"Sample": "21_21"}, {"Sample": "9_21"}, {"Sample": "8_21"}]'
variants = '[{"CHROM": "chr1",	"POS": "11187893",	"ID": ".",	"REF": "T",	"ALT": "C",	"QUAL": "10540.1",	"FILTER": "PASS",	"AF": "0.995253",	"AO": "623",	"DP": "632",	"FAO": "629",	"FDP": "632"},{"CHROM": "chr1",	"POS": "27089638",	"ID": ".",	"REF": "A",	"ALT": "G",	"QUAL": "69.4455",	"FILTER": "PASS",	"AF": "0.0668449",	"AO": "25",	"DP": "374", "FAO": "25", "FDP": "374"},{"CHROM": "chr1",	"POS": "27100205",	"ID": ".",	"REF": "A",	"ALT": "AGCA",	"QUAL": "1451.4", 	"FILTER": "PASS",	"AF": "0.437299",	"AO": "146",	"DP": "453",	"FAO": "136",	"FDP": "311"}]'


@app.route('/api/<query>', methods=['GET', 'POST'])
@cross_origin()
def api(query):
    if request.method == 'GET':
        
        print(query)
        
        if query == "samples":
            return jsonify(isError= False, message= "Success", statusCode= 200, data=samples), 200
        if query == 'variants':
            return jsonify(isError= False, message= "Success", statusCode= 200, data=variants), 200
        else:
            return jsonify(isError= False, message= "Success", statusCode= 200, data=data), 200
    # Skriv feilmelding hvis det ikke er GET

