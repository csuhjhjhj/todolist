import { createApp } from 'vue';
import App from './App.vue';
import Vant from 'vant';
import 'vant/lib/index.css';
createApp(App).mount('#app');

const app = createApp(App);
app.use(Vant);
app.mount('#app');

