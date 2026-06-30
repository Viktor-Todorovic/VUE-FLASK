<template>

    <div class="forma_izmena_proizvoda">
        <h1>Jedan proizvod</h1>
        <div class="p_tagovi">
            <div class="card" style="width: 18rem;">
                <img class="slika" :src="proizvod.proizvod_slika" alt="">
            <div class="card-body">
                <p class="card-text"><b>Naziv proizvoda:</b>{{ proizvod.naziv_proizvoda }}</p>
                <p class="card-text"><b>Opis:</b> {{ proizvod.opis }}</p>
                <p class="card-text"><b>Materijal:</b> {{ proizvod.materijal }}</p>
                <p class="card-text"><b>Mere:</b> {{ proizvod.mere }} cm</p>
                <p class="card-text"><b>Cena:</b> {{ proizvod.cena }} din.</p>
                <b>Trenutna kolicina:</b> {{ proizvod.kolicina }} 
                <input type="number" v-model="nova_kolicina">
                <button @click="dodaj_kolicinu" class="btn btn-primary mt-3"v-if="proizvod.korisnik_id == korisnik.id" >Dodaj kolicinu</button>
            </div>
</div>
        </div>

    </div>

    <div class="komentari">
        <div class="polje_za_komentare">
            <h2>Ostavi komentar</h2>
            <textarea name="komentar" id="" v-model="novi_komentar.tekst_komentara"></textarea>
            <button @click="dodaj_komentar" class="btn btn-primary mt-3">Ostavi komentar</button>
        </div>
    </div>
    
    <div class="ostavljeni_komentari" v-for="komentar in komentari" :key="komentar.komentar_id">
        <p>
            <b>Ostavio komentar:</b> {{ komentar.username }}  
        </p>
        <p>
            <b>Komentar:</b> {{ komentar.tekst_komentara }} 
        </p>
        <button @click="obrisi_komentar(komentar.komentar_id)" class="btn btn-danger"v-if="proizvod.korisnik_id == korisnik.id || korisnik.vrsta_korisnika == 'admin'">Obrisi komentar</button>
        
    </div>
</template>
<script>
import axios from 'axios'
export default {
    props:['id'],
    data() {
        return {
            proizvod: {},
            proizvod_slika: null,
            nova_kolicina: null,
            komentari: [],
            korisnik:{},
            novi_komentar: {
                tekst_komentara: ""
            }
        }
    },

    methods: {
        async dohvati_proizvod() {
            const data = await axios.get(`http://127.0.0.1:5000/products/${this.id}`)
            this.proizvod = data.data 
        },

        async dodaj_kolicinu() {
            await axios.patch(`http://127.0.0.1:5000/products/${this.proizvod.proizvod_id}/quantity`,{
                kolicina: this.nova_kolicina
            })
            this.$toast.success('Uspesno ste dodali kolicinu!')
            location.reload()
        },
        async dohvati_korisnike() {
            const data = await axios.get('http://127.0.0.1:5000/session')
            this.korisnik = data.data
        }, 

        async dodaj_komentar(){
            await axios.post(`http://127.0.0.1:5000/products/${this.proizvod.proizvod_id}/comments`, {
                korisnik_id: this.korisnik.id,
                tekst_komentara: this.novi_komentar.tekst_komentara
            })

            this.novi_komentar.tekst_komentara = ""
            this.dohvati_proizvod()
            this.$toast.success('Komentar uspesno dodat')
            location.reload()
        },

        async obrisi_komentar(id){
            
            await axios.delete(`http://127.0.0.1:5000/products/${this.proizvod.proizvod_id}/comments/${id}`)
            this.dohvati_komentare()
            this.$toast.success('Komentar uspesno obrisan')
            
        },

        async dohvati_komentare(){
            const komentari = await axios.get(`http://127.0.0.1:5000/products/${this.id}/comments`)
            this.komentari = komentari.data
        }
    },



    

    mounted() {
        this.dohvati_proizvod(),
        this.dohvati_komentare(),
        this.dohvati_korisnike()
    },
}
</script>
<style scoped>
.card{
    width: min(440px, calc(100vw - 2rem)) !important;

}


.ostavljeni_komentari{
    background-color: rgba(255, 255, 255, 0.86);
    width: min(800px, calc(100% - 2rem));
    margin: 1rem auto;
    padding: 1em;
    border: 1px solid rgba(255, 255, 255, 0.82);
    border-radius: 8px;
    box-shadow: 0 10px 28px rgba(64, 39, 103, 0.1);

}
.ostavljeni_komentari p{
    color: black;
}

.p_tagovi{
    display: flex;
    flex-direction: column;
    margin-top: 2em;
    align-items: center;
}

.polje_za_komentare{
    width: min(800px, calc(100% - 2rem));
    margin: 2rem auto;
    padding: 1.5rem;
    border: 1px solid rgba(255, 255, 255, 0.82);
    border-radius: 8px;
    background: rgba(255, 255, 255, 0.86);
    box-shadow: 0 10px 28px rgba(64, 39, 103, 0.1);
    display: flex;
    flex-direction: column;
}
.polje_za_komentare textarea{
    width: 100%;
    min-height: 130px;
}



.forma_izmena_proizvoda{
        display: flex;
        align-items: center;
        flex-direction: column;
        margin: 0 auto;
        margin-top: 4em;
        width: min(800px, calc(100% - 2rem));
        border-radius: 8px;
    }

    p{
        display: flex;
        flex-direction: row;
        color: black;
        font-size: 1rem;
        gap: 0.25rem;
        flex-wrap: wrap;
    }
    b{
        margin-right: 0.5em;
    }

    input{
        padding: 0.5em;
        min-height: 40px;
        background-color: white;
        color: black;
        margin-top: 0.5rem;
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
        margin-bottom: 0;
    }

    .opis{
        width: 239px;
        height: 200px;
        
    }


    textarea{
        height: 100%;
        border-radius: 8px;
        padding: 0.2em;
        background-color: white;
        color: black;
    }

</style>
