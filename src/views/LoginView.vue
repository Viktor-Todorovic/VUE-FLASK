<template>
    <div class="forma_login">
        <h1>Login</h1>
        <p>
            Username
            <input type="text" v-model="korisnik.username">
        </p>
        <p>
            Password
            <input type="password" v-model="korisnik.password">
        </p>
        <button @click="gotov_login" class="btn btn-primary">Login</button>
    </div>
</template>
<script>
import axios from 'axios'
export default {
    data() {
        return {
            korisnici: [],
            korisnik: {
                username: "",
                password: ""
            }
        }
    },

    methods: {
        async dohvati_korisnike() {
            const data = await axios.get('http://127.0.0.1:5000/korisnici')
            this.korisnici = data.data
        },

        login() {

            if(this.korisnik.username == "" || this.korisnik.password == ""){
                this.$toast.error("Sva polja moraju biti popunjena!")
                return
            }

            for(let user of this.korisnici){
                if(user.username == this.korisnik.username && user.password == this.korisnik.password){
                    this.korisnik = user
                    return true
                    
                }

            }
            this.$toast.error("Los username ili sifra!")
            return false

            
        },

        async gotov_login() {

            if(this.login()){
                this.$toast.success("Uspesno ste se ulogovali!")
                await axios.post('http://127.0.0.1:5000/login',this.korisnik)
                this.$router.push('/').then(() => {
                    window.location.reload();
                });
            }

        }
    },

    mounted() {
        this.dohvati_korisnike()
    },
}
</script>
<style scoped>
.forma_login{
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