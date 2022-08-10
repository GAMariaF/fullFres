let config;

config = {
	$backend_url: 'http://172.16.0.3:5000',
	$signout_url: function() {
		return this.$backend_url + '/newlogout';
	},
	classOptions: [
		// Obs - dont use 0 (it is reserved)
		{ value: null, text: 'Please select an option' },
		{ value: 'Not Relevant', text: 'Not Relevant' },
		{ value: 'Technical', text: 'Technical' },
		{ value: '1 - Benign', text: '1 - Benign' },
		{ value: '2 - Likely Benign', text: '2 - Likely Benign' },
		{ value: '3 - VUS', text: '3 - VUS' },
		{ value: '4 - Likely Ongogenic', text: '4 - Likely Ongogenic' },
		{ value: '5 - Oncogenic', text: '5 - Oncogenic' },
		{ value: '6', text: '6' }
	],
	tierOptions: [
		// Obs - dont use 0 (it is reserved)
		{ value: null, text: 'Please select an option' },
		{ value: 'I A', text: 'I A' },
		{ value: 'I B', text: 'I B' },		
		{ value: 'II C', text: 'II C' },
		{ value: 'II D', text: 'II D' },		
		{ value: 'III', text: 'III' },
		{ value: 'VI', text: 'IV' }
	],

	oncogenicitycriteria: [
		{tag: "OVS1", class: 'btn mr-1 btn-danger btn-sm', 	title: 'Null variant (nonsense, frameshift, canonical ±1 or 2 splice sites, initiation codon, single-exon or multiexon deletion) in a bona fide tumor suppressor gene.', default: "Very Strong", categories: ["Very Strong", "Strong", "Moderate", "Supporting"] },
		{tag: "OS1",  class: 'btn mr-1 btn-danger btn-sm', 	title: 'Same amino acid change as a previously established oncogenic variant (using this standard) regardless of nucleotide change. Example: Val→Leu caused by either G>C or G>T in the same codon.', default: "Strong", categories: ["Very Strong", "Strong", "Moderate", "Supporting"] },
		{tag: "OS2",  class: 'btn mr-1 btn-danger btn-sm', 	title: 'Well-established in vitro or in vivo functional studies, supportive of an oncogenic effect of the variant.', default: "Strong", categories: ["Very Strong", "Strong", "Moderate", "Supporting"] },
		{tag: "OS3",  class: 'btn mr-1 btn-danger btn-sm', 	title: 'Located in one of the hotspots in cancerhotspots. org with at least 50 samples with a somatic variant at the same amino acid position, and the same amino acid change count in cancerhotspots.org in at least 10 samples.', default: "Strong", categories: ["Very Strong", "Strong", "Moderate", "Supporting"] },
		{tag: "OM1",  class: 'btn mr-1 btn-warning btn-sm', 	title: 'Located in a critical and well-established part of a functional domain (eg, active site of an enzyme).', default: "Moderate", categories: ["Very Strong", "Strong", "Moderate", "Supporting"] },
		{tag: "OM2",  class: 'btn mr-1 btn-warning btn-sm',	title: 'Protein length changes as a result of in-frame deletions/insertions in a known oncogene or tumor suppressor gene or stop-loss variants in a known tumor suppressor gene.', default: "Moderate", categories: ["Very Strong", "Strong", "Moderate", "Supporting"] },
		{tag: "OM3",  class: 'btn mr-1 btn-warning btn-sm',	title: 'Missense variant at an amino acid residue where a different missense variant determined to be oncogenic (using this standard) has been documented. Amino acid difference from reference amino acid should be greater or at least approximately the same as for missense change determined to be oncogenic.', default: "Moderate", categories: ["Very Strong", "Strong", "Moderate", "Supporting"] },
		{tag: "OM4",  class: 'btn mr-1 btn-warning btn-sm',	title: 'Located in one of the hotspots in cancerhotspots. org with <50 samples with a somatic variant at the same amino acid position, and the same amino acid change count in cancerhotspots.org is at least 10.', default: "Moderate", categories: ["Very Strong", "Strong", "Moderate", "Supporting"] },
		{tag: "OP1",  class: 'btn mr-1 btn-warning btn-sm',	title: 'All used lines of computational evidence support an oncogenic effect of a variant (conservation/ evolutionary, splicing effect, etc.).', default: "Supporting", categories: ["Very Strong", "Strong", "Moderate", "Supporting"] },
		{tag: "OP2",  class: 'btn mr-1 btn-warning btn-sm',	title: 'Somatic variant in a gene in a malignancy with a single genetic etiology. Example: retinoblastoma is caused by bi-allelic RB1 inactivation.', default: "Supporting", categories: ["Very Strong", "Strong", "Moderate", "Supporting"] },
		{tag: "OP3",  class: 'btn mr-1 btn-warning btn-sm',	title: 'Located in one of the hotspots in cancerhotspots.org and the particular amino acid change count in cancerhotspots.org is below 10.', default: "Supporting", categories: ["Very Strong", "Strong", "Moderate", "Supporting"] },
		{tag: "OP4",  class: 'btn mr-1 btn-warning btn-sm',	title: 'Absent from controls (or at an extremely low frequency) in gnomAD.', default: "Supporting", categories: ["Very Strong", "Strong", "Moderate", "Supporting"] },
		{tag: "SBVS1",  class: 'btn mr-1 btn-success btn-sm',	title: 'Minor allele frequency is >5% in Genome Aggregation Database (gnomAD) in any of 5 general continental populations: African, East Asian, European (Non-Finnish), Latino, and South Asian. If the somatic variant is in a gene known to cause predisposition to hereditary cancer, ACMG/AMP ClinGen germline expert panel gene specific guidelines (if they exist) must be consulted to establish a cutoff that takes disease prevalence into account.', default: "bVery Strong", categories: ["bVery Strong", "bStrong", "bModerate", "bSupporting"] },
		{tag: "SBP2",  class: 'btn mr-1 btn-success btn-sm',	title: 'A synonymous (silent) variant for which splicing prediction algorithms predict no impact to the splice consensus sequence nor the creation of a new splice site AND the nucleotide is not highly conserved.', default: "bSupporting", categories: ["bVery Strong", "bStrong", "bModerate", "bSupporting"] },
		{tag: "SBP1",  class: 'btn mr-1 btn-success btn-sm',	title: 'All utilized lines of computational evidence suggest no impact of a variant (conservation/ evolutionary, splicing impact, etc.). Caveat: Because many in silico algorithms use the same or very similar input for their predictions, each algorithm cannot be counted as an independent criterion. Can be used only once in any evaluation of a variant.', default: "bSupporting", categories: ["bVery Strong", "bStrong", "bModerate", "bSupporting"] },
		{tag: "SBS1",  class: 'btn mr-1 btn-success btn-sm',	title: 'Minor allele frequency is >1% in Genome Aggregation Database (gnomAD) in any of 5 general continental populations: African, East Asian, European (Non-Finnish), Latino, and South Asian. If the somatic variant is in a gene known to cause predisposition to hereditary cancer, ACMG/AMP ClinGen germline expert panel gene specific guidelines (if they exist) must be consulted to establish a cutoff that takes disease prevalence into account.', default: "bStrong", categories: ["bVery Strong", "bStrong", "bModerate", "bSupporting"] },
		{tag: "SBS2",  class: 'btn mr-1 btn-success btn-sm',	title: 'Well-established in vitro or in vivo functional studies show no oncogenic effects.', default: "bStrong", categories: ["bVery Strong", "bStrong", "bModerate", "bSupporting"] }
	],

};

export { config };
























