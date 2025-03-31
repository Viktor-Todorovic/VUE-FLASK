
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap';
import ToastPlugin from 'vue-toast-notification';
import 'vue-toast-notification/dist/theme-bootstrap.css';
import axios from 'axios'


axios.defaults.withCredentials = true;
const app = createApp(App)
app.use(ToastPlugin);

app.use(router)

app.mount('#app')
