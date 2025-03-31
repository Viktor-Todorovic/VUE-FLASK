import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
      props:true
    },
    {
      path: '/registracija',
      name: 'registracija',
      component: () => import('../views/RegisterView.vue'),
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/LoginView.vue'),
    },
    {
      path: '/profil',
      name: 'profil',
      component: () => import('../views/ProfileView.vue'),
      props: true
    },
    {
      path: '/update-proizvoda/:id',
      name: 'update-proizvoda',
      component: () => import('../views/UpdateProizvod.vue'),
      props: true
    },
    {
      path: '/dodaj-proizvod',
      name: 'dodaj-proizvod',
      component: () => import('../views/AddProizvod.vue'),
      props: true
    },
    {
      path: '/ceo-admin-panel',
      name: 'ceo-admin-panel',
      component: () => import('../views/CeoAdminPanel.vue'),
      props: true
    },
    {
      path: '/admin-panel',
      name: 'admin-panel',
      component: () => import('../views/AdminPanel.vue'),
      props: true
    },
    {
      path: '/admin-panel-proizvodi-komentari',
      name: 'admin-panel-proizvodi-komentari',
      component: () => import('../views/AdminProizvodi.vue'),
      props: true
    },
    {
      path: '/admin-update-korisnika/:id',
      name: 'admin-update-korisnika',
      component: () => import('../views/AdminUpdateKorisnika.vue'),
      props: true
    },
    {
      path: '/jedan-proizvod/:id',
      name: 'jedan-proizvod',
      component: () => import('../views/JedanProizvod.vue'),
      props: true
    },
    {
      path: '/korpa',
      name: 'korpa',
      component: () => import('../views/Korpa.vue'),
      props:true
    },
    {
      path: '/svi-komentari-admin',
      name: 'svi-komentari-admin',
      component: () => import('../views/SviKomentariAdmin.vue'),
      props:true
    },
  ],
})

export default router
