import Vue from 'vue';
import VueRouter from 'vue-router';
Vue.use(VueRouter);
import Profile from '../views/Profile.vue';
import Samples from '../views/Samples.vue';
import AllSamples from '../views/AllSamples.vue';
import Variants from '../views/Variants.vue';
import AllVariants from '../views/AllVariants.vue';
import Control from '../views/Control.vue';
import Statistics from '../views/Statistics.vue';
import Report from '../views/Report.vue';
import VarStats from '../views/VarStats.vue';

// temp?
import login from '../views/LoginWorld.vue';


const routes = [
	{
		path: '/variants/:id',
		name: 'Variants',
		component: Variants,
		props: true
	},
	{
		path: '/allvariants',
		name: 'AllVariants',
		component: AllVariants,
		props: true
	},
	{
		path: '/samples',
		name: 'Samples',
		component: Samples
	},
	{
		path: '/allsamples',
		name: 'AllSamples',
		component: AllSamples
	},
	{
		path: '/control',
		name: 'Control',
		component: Control
	},
	{
		path: '/varstats',
		name: 'VarStats',
		component: VarStats,
	},
	{
		path: '/statistics',
		name: 'Statistics',
		component: Statistics
	},
	{
		path: '/profile',
		name: 'Profile',
		component: Profile
	},
	{
		path: '/login',
		name: 'login',
		component: login
	},
	{
		path: '/report',
		name: 'Report',
		component: Report
	},
	
];
const router = new VueRouter({
	mode: 'history',
	base: process.env.BASE_URL,
	routes
});
export default router;
