<template>

    <div class="forma_izmena_proizvoda">
        <h1>Jedan proizvod</h1>
        <!-- <img class="slika" :src="proizvod.proizvod_slika" alt=""> -->
        <div class="p_tagovi">

            <!-- <p>
                Naziv proizvoda: {{ proizvod.naziv_proizvoda }}
                <input type="text" v-model="proizvod.naziv_proizvoda" disabled>
            </p>
            <p class="opis">
                Opis
                <textarea name="" id="" v-model="proizvod.opis" disabled></textarea>
            </p>
            <p>
                Materijal
                <input type="text"v-model="proizvod.materijal" disabled>
            </p>
            <p>
                Mere
                <input type="number"v-model="proizvod.mere" disabled> 
            </p>
            <p>
                Cena 
                <input type="number" v-model="proizvod.cena" disabled>
            </p>
            <p>
                Trenutna kolicina: {{ proizvod.kolicina }} 
                <input type="number" v-model="nova_kolicina">
                <button @click="dodaj_kolicinu" class="btn btn-primary"v-if="proizvod.korisnik_id == korisnik.id" >Dodaj kolicinu</button>
            </p> -->

            
            <!-- <p>
                <b>Naziv proizvoda:</b>{{ proizvod.naziv_proizvoda }}
            </p>
            <p>
                <b>Opis:</b> {{ proizvod.opis }}
            </p>
            <p>
                <b>Materijal:</b> {{ proizvod.materijal }}
            </p>
            <p>
                <b>Mere:</b> {{ proizvod.mere }}
            </p>
            <p>
                <b>Cena:</b> {{ proizvod.cena }}
            </p>
            <p>
                <b>Trenutna kolicina:</b> {{ proizvod.kolicina }} 
                <input type="number" v-model="nova_kolicina">
                <button @click="dodaj_kolicinu" class="btn btn-primary"v-if="proizvod.korisnik_id == korisnik.id" >Dodaj kolicinu</button>
            </p> -->

            <div class="card" style="width: 18rem;">
                <!-- <p><b>Objavio:</b>{{ proizvod.korisnik_id }}</p> -->
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
            const data = await axios.get(`http://127.0.0.1:5000/dohvati_proizvod_po_idu/${this.id}`)
            this.proizvod = data.data 
        },

        async dodaj_kolicinu() {
            await axios.post('http://127.0.0.1:5000/dodaj_kolicinu',{
                proizvod_id: this.proizvod.proizvod_id,
                kolicina: this.nova_kolicina
            })
            this.$toast.success('Uspesno ste dodali kolicinu!')
            location.reload()
        },
        async dohvati_korisnike() {
            const data = await axios.get('http://127.0.0.1:5000/ulogovan_korisnik')
            this.korisnik = data.data
        }, 

        async dodaj_komentar(){
            await axios.post(`http://127.0.0.1:5000/proizvodi/komentari`, {
                proizvod_id: this.proizvod.proizvod_id,
                korisnik_id: this.korisnik.id,
                tekst_komentara: this.novi_komentar.tekst_komentara
            })

            this.novi_komentar.tekst_komentara = ""
            this.dohvati_proizvod()
            this.$toast.success('Komentar uspesno dodat')
            location.reload()
        },

        async obrisi_komentar(id){
            
            await axios.delete(`http://127.0.0.1:5000/proizvod/${this.proizvod.proizvod_id}/komentar/obrisi/${id}`)
            this.dohvati_komentare()
            this.$toast.success('Komentar uspesno obrisan')
            
        },

        async dohvati_komentare(){
            const komentari = await axios.get(`http://127.0.0.1:5000/dohvatiKomentare/${this.id}`)
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
    /* width: 500px; */
    box-shadow: rgba(240, 46, 170, 0.4) 5px 5px, rgba(240, 46, 170, 0.3) 10px 10px, rgba(240, 46, 170, 0.2) 15px 15px, rgba(240, 46, 170, 0.1) 20px 20px, rgba(240, 46, 170, 0.05) 25px 25px;

}


.ostavljeni_komentari{
    background-color: aliceblue;
    width: 57%;
    margin-left: 23em;
    margin-top: 3em;
    padding: 1em;
    border-radius: 15px;
    box-shadow: rgba(240, 46, 170, 0.4) 5px 5px, rgba(240, 46, 170, 0.3) 10px 10px, rgba(240, 46, 170, 0.2) 15px 15px, rgba(240, 46, 170, 0.1) 20px 20px, rgba(240, 46, 170, 0.05) 25px 25px;

}
.ostavljeni_komentari p{
    color: black;
}

.p_tagovi{
    display: flex;
    flex-direction: column;
    margin-top: 2em;
}

.polje_za_komentare{
    margin-left: 23em;
    display: flex;
    flex-direction: column;
}
.polje_za_komentare textarea{
    width: 70%;
    border-radius: 0;
}



.forma_izmena_proizvoda{
        display: flex;
        align-items: center;
        flex-direction: column;
        margin: 0 auto;
        margin-top: 5em;
        width: 80%;
        border-radius: 10px;
    }

    p{
        display: flex;
        flex-direction: row;
        color: black;
        font-size: 1.2em;
    }
    b{
        margin-right: 0.5em;
    }

    input{
        border-radius: 10px;
        border: 0;
        padding: 0.5em;
        height: 30px;
        background-color: white;
        border: 1px solid black;
        color: black;
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
        box-shadow: rgba(0, 0, 0, 0.05) 0px 1px 2px 0px;
    }

    .opis{
        width: 239px;
        height: 200px;
        
    }


    textarea{
        height: 100%;
        border-radius: 10px;
        padding: 0.2em;
        border: 1px solid black;
        background-color: white;
        color: black;
    }

</style>