<template>
    <nav class="navbar navbar-expand-lg bg-body-tertiary">
  <div class="container-fluid">
    
    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="navbarNav">
      <ul class="navbar-nav">
        <li class="nav-item" v-for="(item, index) in meni" :key="index">
          <RouterLink class="nav-link" :to="item.url">{{ item.title }}</RouterLink>
        </li>

        <li class="nav-item">
          <RouterLink v-if="!korisnik" class="nav-link" to="/login">Login</RouterLink>
        </li>

        <li class="nav-item">
          <RouterLink v-if="korisnik.vrsta_korisnika == 'krojac' || korisnik.vrsta_korisnika == 'admin' " class="nav-link" to="/dodaj-proizvod">Dodaj proizvod</RouterLink>
        </li>
        <li class="nav-item">
          <RouterLink v-if="korisnik.vrsta_korisnika == 'admin'" class="nav-link" to="/ceo-admin-panel">Admin panel</RouterLink>
        </li>
        
      </ul>
      <button class="btn btn-danger" v-if="korisnik" @click="logout">Logout</button>
      <RouterLink class="btn btn-primary moj_profil" v-if="korisnik" to="/profil">Moj profil</RouterLink>
      <RouterLink class="btn btn-success ms-4" v-if="korisnik" to="/korpa">Korpa</RouterLink>
    </div>
  </div>
</nav>
</template>
<script>
import axios from 'axios'
export default {
    data() {
        return {
            meni: [
                {
                    url: '/',
                    title: 'Home'
                },
                {
                    url: '/registracija',
                    title: 'Registracija'
                }
                
                
            ],
            korisnik: {}
        }
    },
    methods: {
      async logout(){
        await axios.get('http://127.0.0.1:5000/logout')
        this.$router.push('/login').then(() => {
                    window.location.reload();
                });
      },
      async dohvati_korisnike() {
            const data = await axios.get('http://127.0.0.1:5000/ulogovan_korisnik')
            this.korisnik = data.data
        },
    },
    mounted() {
      this.dohvati_korisnike()
    },
}
</script>
<style scoped>
.moj_profil{
  margin-left: 63%;
}
</style>