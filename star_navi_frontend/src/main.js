import Vue from 'vue';
import qs from 'querystring';
import axios from 'axios';
import VueCookies from 'vue-cookies';
import App from './App.vue';
import router from './router';

Vue.config.productionTip = false;
Vue.use(VueCookies);
Vue.use(require('vue-moment'));

Vue.prototype.$http = axios;
Vue.prototype.$qs = qs;

new Vue({
  router,
  render: (h) => h(App),
}).$mount('#app');
