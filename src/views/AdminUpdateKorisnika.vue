<template>
    <div class="forma">
        <h1>Admin update profila</h1>
        <p>
            Username
            <input type="text" v-model="korisnik.username" >
        </p>
        <p>
            Password
            <input type="text"v-model="korisnik.password" >
        </p>
        <p>
            Email
            <input type="text"v-model="korisnik.email" >
        </p>
        <p>
            Godina rodjenja
            <input type="number"v-model="korisnik.godina_rodjenja" > 
        </p>
        <p>
            Vrsta korisnika
            <select name="vrsta_korisnika" v-model="korisnik.vrsta_korisnika" >
                <option value="krojac">Krojac</option>
                <option value="kupac">Kupac</option>
            </select>
        </p>

        <button class="btn btn-primary" @click="izmeni">Izmeni</button>

    </div>
</template>
<script>
import axios from 'axios'
export default {
    props:['id'],
    data() {
        return {
            korisnik:{
                username: "",
                password: "",
                email: "",
                godina_rodjenja: "",
                trenutno_stanje_novca: 0,
                vrsta_korisnika: ""
            },
            proizvodi: [],
            korisnici: []
        }
    },

    methods: {
        async dohvati_korisnika() {
            const data = await axios.get(`http://127.0.0.1:5000/dohvati_korisnika_po_idu/${this.id}`)
            this.korisnik = data.data
        },
        async dohvati_korisnika_ulogovanog() {
            const data = await axios.get('http://127.0.0.1:5000/ulogovan_korisnik')
            this.korisnik = data.data
            this.izbaci_ako_nije_admin()
        }, 
        async izmeni() {

            if(this.korisnik.username == "" || this.korisnik.password == "" || this.korisnik.email == "" || this.korisnik.godina_rodjenja == "" || this.korisnik.vrsta_korisnika == "") {
                this.$toast.error("Sva polja moraju biti popunjena!")
                return
            }

            if(!this.korisnik.email.includes('@')){
                this.$toast.error("Email mora imati @ u sebi!")
                return
            }

            if(this.korisnik.password.length < 6){
                this.$toast.error("Password mora imati vise od 6 karaktera!")
                return
            }

            if(this.korisnik.username.length < 3){
                this.$toast.error("Duzina usernamea mora biti iznad 3 karaktera!")
                return
            }

            const data = await axios.put('http://127.0.0.1:5000/update_korisnika',this.korisnik)
            this.korisnik = data.data
            // location.reload()
            this.$toast.success("Uspesno ste izmenili svoj profil!")
            this.$router.push('/ceo-admin-panel')
        },
        izbaci_ako_nije_admin(){
            if(this.korisnik.vrsta_korisnika != 'admin'){
                this.$router.push('/')
                this.$toast.error('Morate biti admin da bi pristupili ovoj stranici!')
            }
        }
    },

    mounted() {
        this.dohvati_korisnika(),
        this.dohvati_korisnika_ulogovanog()
    },
}
</script>
<style scoped>
    .forma{
        display: flex;
        align-items: center;
        flex-direction: column;
        margin-top: 5em;
    }

    p{
        display: flex;
        flex-direction: column;
        color: white;
        font-size: 1.2em;
    }

    input{
        border-radius: 10px;
        border: 0;
        padding: 0.5em;
        height: 40px;
        background-color: white;
    }

    select{
        width: 240px;
        border-radius: 10px;
        height: 40px;
    }

    button{
        width: 230px;
        height: 50px;
    }

    h1{
        color: white;
        font-size: 4em;
    }
</style>