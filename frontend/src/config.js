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
	]
};

export { config };
