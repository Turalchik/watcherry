import { createApp, provide } from 'vue';
import { authState } from './auth';
import App from './App.vue';
import router from './router';

const app = createApp(App);
app.provide('authState', authState);
app.use(router);
app.mount('#app');
