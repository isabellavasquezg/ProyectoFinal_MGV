import { createRouter, createWebHistory } from "vue-router";
const router=createRouter({
    history:createWebHistory(),
    routes:[
        {
            path:'/',
            name:'Login',
            component:()=>import('../views/GeneralEquipos.vue'),
            props: true
        },
        {
            path:'/Responsables',
            name:'Responsables',
            component:()=>import('../views/GeneralResponsables.vue'),
            props: true
        },
        {
            path:'/Servicios',
            name:'Servicios',
            component:()=>import('../views/GeneralServicios.vue'),
            props: true
        },

  ]
});
export default router;