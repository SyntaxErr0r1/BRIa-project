import { createApp } from 'vue'
import App from './App.vue'
// import router from './router'
// import store from './store'
import PrimeVue from 'primevue/config'
import Menubar from 'primevue/menubar'
import 'primevue/resources/themes/lara-light-green/theme.css'
import VueRouter from 'vue-router'
import router from "./router"

import Ripple from 'vuetify/lib/directives/ripple';


let app = createApp(App)

app.use(router)
app.use(PrimeVue, {ripple: true})
app.component('Menubar', Menubar)
app.directive('ripple', Ripple)


app.mount('#app')
