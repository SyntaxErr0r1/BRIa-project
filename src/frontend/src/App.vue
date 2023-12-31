<template>
  <!-- <h1>DWADWDW</h1> -->
  <Menubar :model="items">
    <template #start>
        <h3>EEG Analysis Tool</h3>
    </template>
    <template #item="{ item }">
      <router-link v-if="item.route" :to="item.route">
        <span class="side-menu-item">
            <span :class="['ml-2', { 'font-semibold': item.items }]"><strong>{{ item.label }}</strong></span>
        </span>
      </router-link>
    </template>
    <template #end>
      <router-link to="/upload-data">
        <Button label="New Data" icon="pi pi-plus" class="p-mr-2" />
      </router-link>
    </template>
  </Menubar>

  <Splitter class="splitter">
    <SplitterPanel class="flex align-items-center justify-content-center" :size="25" :minSize="10"> 
      <PanelMenu :model="sideItems">
        <template #item="{ item }">
          <router-link v-if="item.route" :to="item.route">
            <span class="side-menu-item">
                <span :class="['ml-2', { 'font-semibold': item.items }]"><strong>{{ item.label }}</strong></span>
                <Checkbox class="ml-auto" v-model="item.enabled" :binary="true" />
            </span>
          </router-link>
        </template>
      </PanelMenu>
    </SplitterPanel>
    <SplitterPanel class="flex align-items-center justify-content-center" :size="75"> 
      <router-view></router-view>
    </SplitterPanel>
  </Splitter>

  <Toast></Toast>
</template>

<script>
import HelloWorld from './components/HelloWorld.vue'
import Menubar from 'primevue/menubar';
import PanelMenu from 'primevue/panelmenu';
import Splitter from 'primevue/splitter';
import SplitterPanel from 'primevue/splitterpanel';
import Button from 'primevue/button';
import Badge from 'primevue/badge';
import Ripple from 'primevue/ripple';
import Checkbox from 'primevue/checkbox';
import RouterLink from 'vue-router';
import RouterView from 'vue-router';
import Toast from 'primevue/toast';
import 'primeicons/primeicons.css'

export default {
  name: 'App',
  components: {
    HelloWorld,
    Menubar,
    PanelMenu,
    Splitter,
    SplitterPanel,
    Button,
    Badge,
    Ripple,
    Checkbox,
    RouterLink,
    RouterView,
    Toast
  },
  methods: {
    loadDatasets: function() {
      this.$store.dispatch('loadDatasets');
    }
  },
  data: () => {
    return {

      datasets: [],

      sideItems: [
        {
          label: 'Load Data',
          enabled: true,
          route: '/load-data'
        },
        {
          label: 'High Pass Filter',
          enabled: true,
          route: '/high-pass'
        },
        {
          label: "ICA",
          enabled: true,
          route: '/ica'
        },
        {
          label: "Connectivity",
          enabled: true,
          route: '/connectivity'
        }
      ],

      items: [
        {
          label: 'Manage Recordings',
          icon: 'pi pi-fw pi-file',
          route: '/data-manager'
        },
      ]
    }
  }
}
</script>

<style>

body{
  margin: 0;
}

body > *{
  flex: 1;
  justify-self: stretch;
}

.splitter{
  flex: 1;
  background-color: #f4f4f4;
}

#app {
  display: flex;
  flex-direction: column;
  height: 100vh;
}

.side-menu-item{
  display: flex;
  align-items: center;
  padding: 0.5rem 1rem;
  color: #000;
  text-decoration: none;
  transition: all 0.2s ease-in-out;
  justify-content: space-between;
  text-decoration: none;
}

</style>
