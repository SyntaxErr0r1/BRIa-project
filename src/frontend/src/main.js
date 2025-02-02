import { createApp } from 'vue'
import App from './App.vue'
// import router from './router'
// import store from './store'
import PrimeVue from 'primevue/config'
import Menubar from 'primevue/menubar'
import 'primevue/resources/themes/lara-light-green/theme.css'
import router from "./router"
import ToastService from 'primevue/toastservice';

import Ripple from 'vuetify/lib/directives/ripple';
import store from './store'


let app = createApp(App)

app.use(router)
app.use(PrimeVue, {ripple: true})
app.use(ToastService)
app.use(store)
app.component('Menubar', Menubar)
app.directive('ripple', Ripple)


app.mount('#app')
