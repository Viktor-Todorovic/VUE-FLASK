
<template>
    <div class="forma">
        <h1>Registracija</h1>
        <p>
            Username
            <input type="text" v-model="korisnik.username">
        </p>
        <p>
            Password
            <input type="password"v-model="korisnik.password">
        </p>
        <p>
            Email
            <input type="text"v-model="korisnik.email">
        </p>
        <p>
            Godina rodjenja
            <input type="number"v-model="korisnik.godina_rodjenja"> 
        </p>
        <p>
            Vrsta korisnika
            <select name="vrsta_korisnika" v-model="korisnik.vrsta_korisnika">
                <option value="krojac">Krojac</option>
                <option value="kupac">Kupac</option>
                <option value="admin" v-if="ulogovan.vrsta_korisnika == 'admin'">Admin</option>
            </select>
        </p>

        <button @click="dodaj" class="btn btn-primary">Registruj se</button>
    </div>
</template>


<script>
import axios from 'axios'

export default {
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

            korisnici: [],
            ulogovan: {}
        }
    },

    methods: {
        async dohvati_korisnike() {
            const data = await axios.get('http://127.0.0.1:5000/korisnici')
            this.korisnici = data.data
        },
        async dohvati_korisnika() {
            const data = await axios.get('http://127.0.0.1:5000/ulogovan_korisnik')
            this.ulogovan = data.data
        }, 

        async dodaj() {
            

            if(this.korisnik.username == "" || this.korisnik.password == "" || this.korisnik.email == "" || this.korisnik.godina_rodjenja == "" || this.korisnik.vrsta_korisnika == "") {
                this.$toast.error("Sva polja moraju biti popunjena!")
                return
            }

            if(this.korisnik.username.length < 3){
                this.$toast.error("Duzina usernamea mora biti iznad 3 karaktera!")
                return
            }

            if(this.korisnik.password.length < 6){
                this.$toast.error("Password mora imati vise od 6 karaktera!")
                return
            }

            if(!this.korisnik.email.includes('@')){
                this.$toast.error("Email mora imati @ u sebi!")
                return
            }

            if(this.korisnik.godina_rodjenja < 1900 || this.korisnik.godina_rodjenja > 2025){
                this.$toast.error("Godina rodjenja nije dobra!")
                return
            }

            for(const user of this.korisnici){
                if(user.username == this.korisnik.username){
                    this.$toast.error("Username vec postoji")
                    return
                }

                if(user.email == this.korisnik.email){
                    this.$toast.error("Email vec postoji")
                    return
                }
            }

            await axios.post('http://127.0.0.1:5000/register',this.korisnik)

            this.$router.push('/')
        },


    },

    mounted() {
        this.dohvati_korisnike(),
        this.dohvati_korisnika()
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
        color: black;
        font-size: 1.2em;
    }

    input{
        border-radius: 10px;
        border: 1px solid black;
        padding: 0.5em;
        height: 40px;
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
        color: black;
        font-size: 4em;
    }
</style>