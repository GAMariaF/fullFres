let config;

config = {
    $backend_url: 'http://172.16.0.3:5001',
    //$backend_url: 'http://'+process.env.IP+':'+process.env.PORTBACKEND,
    $signout_url: function() {
        return this.$backend_url + '/newlogout';
    },
    replyOptions: [
        // Obs - dont use 0 (it is reserved)
        { value: null, text: 'Please select an option' },
        { value: 'Yes', text: 'Yes' },
        { value: 'Yes, VN', text: 'Yes, vertification needed' },
        { value: 'No', text: 'No' }
        //{ value: 'Failed sample', text: 'Failed sample' }	
    ],
    functionalOptions: [
        // Obs - dont use 0 (it is reserved)
        { value: null, text: '' },
        { value: 'OS2: Ja (ref) (+4)', text: 'OS2: Ja (ref) (+4)' },
        { value: 'OS2: OncoKB: Likely oncogenic (+4)', text: 'OS2: OncoKB: Likely oncogenic (+4)' },		
        { value: 'OS2: OncoKB: Oncogenic (+4)', text: 'OS2: OncoKB: Oncogenic (+4)' },
        { value: 'SBS2: Ja (ref) (-4)', text: 'SBS2: Ja (ref) (-4)'},
    ],
    predictiveOptions: [
        // Obs - dont use 0 (it is reserved)
        { value: null, text: '' },
        { value: 'OS1: Same AA prev established (+4)', text: 'OS1: Same AA prev established (+4)' },
        { value: 'OM1: Functional domain (+2)', text: 'OM1: Functional domain (+2)' },
        { value: 'OM2: Protein length changes (+2)', text: 'OM2: Protein length changes (+2)' },
        { value: 'OM3: Different AA in known oncogenic site (+2)', text: 'OM3: Different AA in known oncogenic site (+2)' },
        { value: 'OVS1: Nullvariant (+8)', text: 'OVS1: Nullvariant (+8)' },
        { value: 'SBVS1: (-8)', text: 'SBVS1: (-8)'},
        { value: 'SBP2: (-1)', text: 'SBP2: (-1)'},
        { value: 'SBP1: (-1)', text: 'SBP1: (-1)'},
        { value: 'SBS1: (-4)', text: 'SBS1: (-4)'},
        
    ],
    cancerhotspotsOptions: [
        // Obs - dont use 0 (it is reserved)
        { value: null, text: '' },
        { value: 'OS3: Ja (ref) (+4)', text: 'OS3: Ja (ref) (+4)' },
        { value: 'OM4: Hotspot medium freq (+2)', text: 'OM4: Hotspot medium freq (+2)' },
        { value: 'OP3: Hotspot low freq (+1)', text: 'OP3: Hotspot low freq (+1)' },
        { value: 'OS3: Hotspot high freq (+4)', text: 'OS3: Hotspot high freq (+4)' }
    ],
    classOptions: [
        // Obs - dont use 0 (it is reserved)
        { value: null, text: 'Please select an option' },
        { value: 'Not evaluated', text: 'Not Evaluated' },
        { value: 'Not Relevant', text: 'Not Relevant' },
        { value: 'Technical', text: 'Technical' },
        { value: 'Homopolymer', text: 'Homopolymer' },
        { value: '1 - Benign', text: '1 - Benign ( - -7 )' },
        { value: '2 - Likely Benign', text: '2 - Likely Benign ( -6 - -1 )' },
        { value: '3 - VUS', text: '3 - VUS ( 0 - 5 )' },
        { value: '4 - Likely Oncogenic', text: '4 - Likely Oncogenic (6 - 9 )' },
        { value: '5 - Oncogenic', text: '5 - Oncogenic ( 10 - )' }
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
        {tag: "OM1",  class: 'btn mr-1 btn-warning btn-sm', title: 'Located in a critical and well-established part of a functional domain (eg, active site of an enzyme).', default: "Moderate", categories: ["Very Strong", "Strong", "Moderate", "Supporting"] },
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
        {tag: "SBS2",  class: 'btn mr-1 btn-success btn-sm',	title: 'Well-established in vitro or in vivo functional studies show no oncogenic effects.', default: "bStrong", categories: ["bVery Strong", "bStrong", "bModerate", "bSupporting"] },
        {tag: "ADJUST",  class: 'btn mr-1 btn-info btn-sm',	title: 'Adjust the score', default: "adjust"}
    ],
    sortedIndex: [ 'runid',
                    'sampleid',
                    'Genelist',
                    'Perc_Tumor',
                    'gene',
                    'transcript',
                    'annotation_variant',
                    'annotation_variant2',
                    'Reads',
                    'FILTER',
                    'AF',
                    'COSMIC',
                    'Reply',
                    'User_Classification',
                    'class',
                    'Variant_ID',
                    'Variant_Name',
                    'Key_Variant',
                    'Oncomine_Reporter_Evidence',
                    'Type',
                    'oncomineGeneClass',
                    'oncomineVariantClass',
                    'Locus',
                    'protein',
                    'REF',
                    'ALTEND',
                    'Call',
                    'DP',
                    'FDP',
                    'FAO',
                    'coding',
                    'P_Value',
                    'Read_Counts_Per_Million',
                    'Oncomine_Driver_Gene',
                    'Copy_Number',
                    'CNV_Confidence',
                    'Valid_CNV_Amplicons',
                    'Populasjonsdata',
                    'Funksjonsstudier',
                    'Prediktive_data',
                    'Cancer_hotspots',
                    'Computational_evidens',
                    'Konservering',
                    'ClinVar',
                    'CLSF',
                    'Andre_DB',
                    'Comment',
                    'evidence_types',
                    'Oncogenicity',
                    'TierVPS',
                    'CommentVPS',
                    'User_Class'
    ],

    reportcodes: [
    // {value: "NGS-N", class: "btn mr-1 btn-warning btn-sm", text: "Det er ikke påvist mutasjoner relevante for behandling, prognose eller diagnose (referanse)."},
    {value: "NGS-P1", class: "btn mr-1 btn-warning btn-sm", text: "Den påviste sekvensvarianten ${name} (${annoVar}) med allelfraksjon ${Math.round(variant['AF'])}% er relevant for behandling (referanse)."},
    {value: "NGS-P2", class: "btn mr-1 btn-warning btn-sm", text: "Den påviste sekvensvarianten ${name} (${annoVar}) med allelfraksjon ${Math.round(variant['AF'])}% er relevant for behandling av annen krefttype (referanse), og kan være relevant for inkludering i kliniske studier (ClinicalTrials.gov)"},
    {value: "NGS-P3", class: "btn mr-1 btn-warning btn-sm", text: "Den påviste sekvensvarianten ${name} (${annoVar}) med allelfraksjon ${Math.round(variant['AF'])}% kan være relevant for inkludering i kliniske studier (ClinicalTrials.gov)."},
    {value: "NGS-F", class: "btn mr-1 btn-warning btn-sm", text: "Den påviste fusjonen ${name} med ${Math.round(variant['Read_Counts_Per_Million'])} reads/million er relevant for behandling (referanse)."},
    {value: "NGS-CNV", class: "btn mr-1 btn-warning btn-sm", text: "Den påviste kopitallsvarianten i ${variant['gene']}-genet (${Math.round(variant['Copy_Number'])-2}+2 kopier) er relevant for behandling (referanse). «Varianten bør verifiseres før den benyttes klinisk.»"},
    {value: "NGS-VUS", class: "btn mr-1 btn-warning btn-sm", text: "Det ble påviste en ${type}av usikker betydning i ${variant['gene']}-genet. Det betyr at varianten ikke kan klassifiseres som sannsynlig benign eller sannsynlig onkogen med dagens kunnskap. Det er pr. i dag ikke indikasjon for behandling."}
    // {value: "NGS-MIS", class: "btn mr-1 btn-warning btn-sm", text: "Analysen kunne ikke fullføres pga. for lite/uegnet prøvemateriale eller tekniske problemer.\nDersom annet egnet prøvemateriale er tilgjengelig kan om ønskelig ny analyse rekvireres. (tumorandel > 20 % foretrekkes)."},
    ],

    geneListOptions: [
    {value: "Non-Small Cell Lung Cancer", text: "Non-Small Cell Lung Cancer"},
    {value: "Colorectal Cancer", text: "Colorectal Cancer"},
    {value: "Melanoma", text: "Melanoma"},
    {value: "Prostate Cancer", text: "Prostate Cancer"},
    {value: "Breast Cancer", text: "Breast Cancer"},
    {value: "Cholangiocarcinoma", text: "Cholanigiocarcinoma"},
    {value: "Kidney Cancer", text: "Kidney Cancer"},
    {value: "Bladder Urothelial Carcinoma", text: "Bladder Urothelial Carcinoma"},
    {value: "Pancreatic Cancer", text: "Pancreatic Cancer"},
    {value: "Other Solid Tumor", text: "Other Solid Tumors"},
    ],

    replySearchOptions: [
        {value: "", text: "Any Reply"},
        {value: "Yes_A", text: "Yes"},
        {value: "Yes, VN", text: "Yes, VN"},
        {value: "Yes_O", text: "Yes Only"},
        {value: "Yes_No", text: "Yes-No Mix"},
        {value: "No", text: "No"},
        {value: "No_O", text: "No Only"},
    ],

    
};

export { config };






















