<template >
    <div class="sredina">

        <div class="table">
            <h1>Admin panel</h1>
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Slika</th>
                    <th>Username</th>
                    <th>Password</th>
                    <th>Email</th>
                    <th>Godina rodjenja</th>
                    <th>Trenutno stanje novca</th>
                    <th>Vrsta korisnika</th>
                    <th>Opcije</th>
                    <th>Opcije</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="(korisnik, index) in korisnici" :key="index">
                    <td>{{ korisnik.id }}</td>
                    <td><img class="slika" :src="korisnik.profilna_slika" alt=""></td>
                    <td>{{ korisnik.username }}</td>
                    <td>{{ korisnik.password }}</td>
                    <td>{{ korisnik.email }}</td>
                    <td>{{ korisnik.godina_rodjenja }}</td>
                    <td>{{ korisnik.trenutno_stanje_novca }}</td>
                    <td>{{ korisnik.vrsta_korisnika }}</td>
                    <td><button @click="obrisi_korisnika(korisnik.id)" class="btn btn-danger">Obrisi</button></td>
                    <td><button @click="izmeni_korisnika(korisnik.id)" class="btn btn-primary">Izmeni</button></td>    
                </tr>
            </tbody>
        </div>
    </div>
</template>
<script>
import axios from 'axios'
export default {
    data() {
        return {
            korisnik: {},
            korisnici: []
        }
    },

    methods: {
        async dohvati_korisnike() {
            const data = await axios.get('http://127.0.0.1:5000/korisnici')
            this.korisnici = data.data
        }, 

        async dohvati_korisnika_ulogovanog() {
            const data = await axios.get('http://127.0.0.1:5000/ulogovan_korisnik')
            this.korisnik = data.data
            this.izbaci_ako_nije_admin()
        }, 

        async obrisi_korisnika(id) {
            await axios.delete(`http://127.0.0.1:5000/korisnici/delete/${id}`)
			location.reload()
        },

        izmeni_korisnika(id) {
            this.$router.push(`admin-update-korisnika/${id}`)
        },

        izbaci_ako_nije_admin(){
            if(this.korisnik.vrsta_korisnika != 'admin'){
                this.$router.push('/')
                this.$toast.error('Morate biti admin da bi pristupili ovoj stranici!')
            }
        }

    },

    mounted() {
        this.dohvati_korisnike(),
        this.dohvati_korisnika_ulogovanog()
    },
}
</script>


<style scoped>
.sredina{ 
    margin-left: 30em;
} 
tr,th,td{
    border: 1px solid black;
    
}

.slika{
    width: 80px;
    height: 80px;
}


</style>