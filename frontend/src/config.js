let config;

config = {
	$backend_url: 'http://172.16.0.3:5000',
	$signout_url: function() {
		return this.$backend_url + '/newlogout';
	},
	classOptions: [
		// Obs - dont use 0 (it is reserved)
		{ value: null, text: 'Please select an option' },
		{ value: 1, text: '1' },
		{ value: 2, text: '2' },
		{ value: 3, text: '3' },
		{ value: 4, text: '4' },
		{ value: 5, text: '5' },
		{ value: '6', text: '6' }
	],
	oncogenicitycriteria: [
		{tag: "OVS1", button: '<button type="button" class="btn mr-1 btn-danger btn-sm">OVS1</button>', evidence: '<div><button type="button" class="btn mr-1 btn-danger btn-sm">OVS1</button> Null variant (nonsense, frameshift, canonical ±1 or 2 splice sites, initiation codon, single-exon or multiexon deletion) in a bona fide tumor suppressor gene.</div>', default: "Very Strong", categories: ["Very Strong", "Strong", "Moderate", "Supporting"] },
		{tag: "OS1",  button: '<div><button type="button" class="btn mr-1 btn-danger btn-sm">OS1</button></div>', evidence: '<div><button type="button" class="btn mr-1 btn-danger btn-sm">OS1</button> Same amino acid change as a previously established oncogenic variant (using this standard) regardless of nucleotide change. Example: Val→Leu caused by either G>C or G>T in the same codon. </div>', default: "Strong", categories: ["Very Strong", "Strong", "Moderate", "Supporting"] },
		{tag: "OS2",  button: '<div><button type="button" class="btn mr-1 btn-danger btn-sm">OS2</button></div>', evidence: '<div><button type="button" class="btn mr-1 btn-danger btn-sm">OS2</button> Well-established in vitro or in vivo functional studies, supportive of an oncogenic effect of the variant. </div>', default: "Strong", categories: ["Very Strong", "Strong", "Moderate", "Supporting"] },
		{tag: "OS3",  button: '<div><button type="button" class="btn mr-1 btn-danger btn-sm">OS3</button></div>', evidence: '<div><button type="button" class="btn mr-1 btn-danger btn-sm">OS3</button> Located in one of the hotspots in cancerhotspots. org with at least 50 samples with a somatic variant at the same amino acid position, and the same amino acid change count in cancerhotspots.org in at least 10 samples.</div>', default: "Strong", categories: ["Very Strong", "Strong", "Moderate", "Supporting"] },
		{tag: "OM1",  button: '<div><button type="button" class="btn mr-1 btn-danger btn-sm">OM1</button></div>', evidence: '<div><button type="button" class="btn mr-1 btn-danger btn-sm">OM1</button> Located in a critical and well-established part of a functional domain (eg, active site of an enzyme). </div>', default: "Strong", categories: ["Very Strong", "Strong", "Moderate", "Supporting"] },
		{tag: "OM2",  button: '<div><button type="button" class="btn mr-1 btn-warning btn-sm">OM2</button></div>', evidence: '<div><button type="button" class="btn mr-1 btn-warning btn-sm">OM2</button> Protein length changes as a result of in-frame deletions/insertions in a known oncogene or tumor suppressor gene or stop-loss variants in a known tumor suppressor gene. </div>', default: "Moderate", categories: ["Very Strong", "Strong", "Moderate", "Supporting"] },
		{tag: "OM3",  button: '<div><button type="button" class="btn mr-1 btn-warning btn-sm">OM3</button></div>', evidence: '<div><button type="button" class="btn mr-1 btn-warning btn-sm">OM3</button> Missense variant at an amino acid residue where a different missense variant determined to be oncogenic (using this standard) has been documented. Amino acid difference from reference amino acid should be greater or at least approximately the same as for missense change determined to be oncogenic </div>', default: "Moderate", categories: ["Very Strong", "Strong", "Moderate", "Supporting"] },
		{tag: "OM4",  button: '<div><button type="button" class="btn mr-1 btn-warning btn-sm">OM4</button></div>', evidence: '<div><button type="button" class="btn mr-1 btn-warning btn-sm">OM4</button> Located in one of the hotspots in cancerhotspots. org with <50 samples with a somatic variant at the same amino acid position, and the same amino acid change count in cancerhotspots.org is at least 10.</div>', default: "Moderate", categories: ["Very Strong", "Strong", "Moderate", "Supporting"] },
		{tag: "OP1",  button: '<div><button type="button" class="btn mr-1 btn-warning btn-sm">OP1</button></div>', evidence: '<div><button type="button" class="btn mr-1 btn-warning btn-sm">OP1</button> All used lines of computational evidence support an oncogenic effect of a variant (conservation/ evolutionary, splicing effect, etc.). </div>', default: "Supporting", categories: ["Very Strong", "Strong", "Moderate", "Supporting"] },
		{tag: "OP2",  button: '<div><button type="button" class="btn mr-1 btn-warning btn-sm">OP2</button></div>', evidence: '<div><button type="button" class="btn mr-1 btn-warning btn-sm">OP2</button> Somatic variant in a gene in a malignancy with a single genetic etiology. Example: retinoblastoma is caused by bi-allelic RB1 inactivation. </div>', default: "Supporting", categories: ["Very Strong", "Strong", "Moderate", "Supporting"] },
		{tag: "OP3",  button: '<div><button type="button" class="btn mr-1 btn-warning btn-sm">OP3</button></div>', evidence: '<div><button type="button" class="btn mr-1 btn-warning btn-sm">OP3</button> Located in one of the hotspots in cancerhotspots.org and the particular amino acid change count in cancerhotspots.org is below 10. </div>', default: "Supporting", categories: ["Very Strong", "Strong", "Moderate", "Supporting"] },
		{tag: "OP4",  button: '<div><button type="button" class="btn mr-1 btn-success btn-sm">OP4</button></div>', evidence: '<div><button type="button" class="btn mr-1 btn-success btn-sm">OP4</button> Absent from controls (or at an extremely lowf requency) in gnomAD.</div>', default: "Supporting", categories: ["Very Strong", "Strong", "Moderate", "Supporting"] },
	],

};

export { config };
























