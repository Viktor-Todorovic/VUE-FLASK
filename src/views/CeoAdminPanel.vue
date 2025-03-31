<template>
    <div class="glavna">
        <!-- <h1>Sve funkcije admina</h1> -->
        <p>
            Tabela sa korisnicima
            <router-link to="/admin-panel"><button class="btn btn-primary">Tabela sa korisnicima</button></router-link>
        </p>
        <p>
            Svi proizvodi 
            <router-link to="/admin-panel-proizvodi-komentari"><button class="btn btn-primary">Svi proizvodi</button></router-link>
        </p>
        <p>
            Svi komentari 
            <router-link to="/svi-komentari-admin"><button class="btn btn-primary">Svi komentari</button></router-link>
        </p>

        <p>
            Dodaj admina 
            <router-link to="/registracija"><button class="btn btn-primary">Dodaj admina</button></router-link>
        </p>

    </div>
</template>
<script>
import axios from 'axios'

export default {
    data() {
        return {
            korisnik:{}
        }
    },

    methods: {

        async dohvati_korisnike() {
            const data = await axios.get('http://127.0.0.1:5000/ulogovan_korisnik')
            this.korisnik = data.data
            this.nije_dozvoljeno()
        },

        nije_dozvoljeno(){

            if(this.korisnik.vrsta_korisnika != 'admin'){
                this.greska = "Ne mozete pristupiti ovoj stranici jer niste admin!"
                this.$toast.error(this.greska)
                this.$router.push('/')
                console.log(this.proizvod)
            }
        }
    },

    mounted() {
        this.dohvati_korisnike()
    },


}
</script>
<style scoped>
p{
    display: flex;
    flex-direction: column;
    color: black;
    font-size: 2em;
    border: 1px solid black;
    width: 40%;
    justify-content: center;
    align-items: center;
    padding: 1em;
    background-color: #a0d2eb;
    box-shadow: rgba(240, 46, 170, 0.4) 5px 5px, rgba(240, 46, 170, 0.3) 10px 10px, rgba(240, 46, 170, 0.2) 15px 15px, rgba(240, 46, 170, 0.1) 20px 20px, rgba(240, 46, 170, 0.05) 25px 25px;

}

p button{
    width: 300px;
    height: 50px;
}

.glavna{
    display: flex;
    gap: 2em;
    flex-direction: column;
    margin-left: 40em;
    margin-top: 3em;
}
    
</style>