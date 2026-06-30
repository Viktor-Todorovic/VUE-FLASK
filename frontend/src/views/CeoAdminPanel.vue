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
            const data = await axios.get('http://127.0.0.1:5000/session')
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
    color: #211a2f;
    font-size: 1.35rem;
    font-weight: 800;
    border: 1px solid rgba(255, 255, 255, 0.82);
    width: 100%;
    justify-content: center;
    align-items: center;
    padding: 1em;
    border-radius: 8px;
    background-color: rgba(255, 255, 255, 0.86);
    box-shadow: 0 18px 50px rgba(64, 39, 103, 0.14);

}

p button{
    width: 300px;
    height: 50px;
}

.glavna{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
    gap: 1.25rem;
    width: min(920px, calc(100% - 2rem));
    margin: 3em auto 0;
}
    
</style>
