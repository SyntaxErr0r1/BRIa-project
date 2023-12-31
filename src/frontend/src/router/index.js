import { createRouter, createWebHistory } from 'vue-router';

import HelloWorld from "@/components/HelloWorld.vue"

const routes = [
    {
        path: "/",
        name: "Home",
        component: HelloWorld,
    },
    {
      path: "/upload-data",
      name: "UploadData",
      component: () => import("../views/UploadData.vue")
    },
    {
      path: "/data-manager",
      name: "DataManager",
      component: () => import("../views/DataManager.vue")
    },
    {
      path: "/load-data",
      name: "LoadData",
      component: () => import("../views/LoadData.vue")
    },
    {
      path: "/high-pass",
      name: "HighPassFilter",
      component: () => import("../views/HighPassFilter.vue")
    },
    {
      path: "/ica",
      name: "ICA",
      component: () => import("../views/ICA.vue")
    },
    {
      path: "/connectivity",
      name: "Connectivity",
      component: () => import("../views/Connectivity.vue")
    }

]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router