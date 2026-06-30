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
            const data = await axios.get('http://127.0.0.1:5000/users')
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
                await axios.post('http://127.0.0.1:5000/sessions',this.korisnik)
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
        width: min(440px, calc(100% - 2rem));
        margin: 5em auto 0;
        padding: 2rem;
        border: 1px solid rgba(255, 255, 255, 0.82);
        border-radius: 8px;
        background: rgba(255, 255, 255, 0.86);
        box-shadow: 0 18px 50px rgba(64, 39, 103, 0.14);
    }

    p{
        display: flex;
        flex-direction: column;
        color: black;
        width: 100%;
        font-size: 0.95rem;
        font-weight: 700;
        gap: 0.45rem;
    }

    input{
        border-radius: 10px;
        padding: 0.5em;
        min-height: 44px;
    }

    select{
        width: 240px;
        border-radius: 10px;
        height: 40px;
    }

    button{
        width: 230px;
        min-height: 48px;
    }

    h1{
        margin-bottom: 1.2rem;
    }
    
</style>
