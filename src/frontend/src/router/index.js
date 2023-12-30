import { createRouter, createWebHistory } from 'vue-router';

import HelloWorld from "@/components/HelloWorld.vue"

const routes = [
    {
        path: "/",
        name: "Home",
        component: HelloWorld,
    },
    {
      path: "/upload",
      name: "UploadData",
      component: () => import("../views/UploadData.vue")
    },
    {
      path: "/load-data",
      name: "LoadData",
      component: () => import("../views/LoadData.vue")
    }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router