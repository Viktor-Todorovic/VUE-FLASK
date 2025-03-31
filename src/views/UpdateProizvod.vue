<template>

    <div class="forma_izmena_proizvoda">
        <h1>Izmena proizvoda</h1>
        <img class="slika" :src="proizvod.proizvod_slika" alt="">
        <p>
            Naziv proizvoda
            <input type="text" v-model="proizvod.naziv_proizvoda">
        </p>
        <p class="opis">
            Opis
            <textarea name="" id="" v-model="proizvod.opis"></textarea>
        </p>
        <p>
            Materijal
            <input type="text"v-model="proizvod.materijal">
        </p>
        <p>
            Mere
            <input type="number"v-model="proizvod.mere"> 
        </p>
        <p>
            Cena
            <input type="number" v-model="proizvod.cena">
        </p>
        <p>
            Kolicina
            <input type="number" v-model="proizvod.kolicina">
        </p>
        <p>
            Slika proizvoda
            <input type="file" @change="handleFileUpload">
        </p>

        <button @click="izmeni" class="btn btn-primary">Izmeni</button>
    </div>
</template>


<script>
import axios from 'axios'
export default {
    props:['id'],
    data() {
        return {
            proizvod: {
                naziv_proizvoda: "",
                opis: "",
                materijal: "",
                mere: "",
                cena: "",
                kolicina: ""
            },
            korisnik: {},
            proizvod_slika: null
            
        }
    },

    methods: {

        handleFileUpload(event){
            this.proizvod_slika = event.target.files[0]
        },

        async dohvati_proizvod() {
            const data = await axios.get(`http://127.0.0.1:5000/dohvati_proizvod_po_idu/${this.id}`)
            this.proizvod = data.data 
            this.nije_dozvoljeno()
        },

        async dohvati_korisnike() {
            const data = await axios.get('http://127.0.0.1:5000/ulogovan_korisnik')
            this.korisnik = data.data
        },

        async izmeni(){

            if(this.proizvod.naziv_proizvoda == "" || this.proizvod.opis == "" || this.proizvod.materijal == "" || this.proizvod.mere == "" || this.proizvod.cena == ""){
                this.$toast.error("Sva polja moraju biti popunjena!")
                return
            }

            if(this.proizvod.naziv_proizvoda.length <2){
                this.$toast.error("Naziv mora imati vise od dva karaktera!")
                return
            }
            if(this.proizvod.materijal.length <2){
                this.$toast.error("Materijal mora imati vise od dva karaktera!")
                return
            }
            if(this.proizvod.mere < 0){
                this.$toast.error("Mere ne mogu biti negativne")
                return
            }
            if(this.proizvod.cena < 0){
                this.$toast.error("Cena ne moze biti negativna")
                return
            }

            const formData = new FormData();
            formData.append('proizvod_id', this.proizvod.proizvod_id);
            formData.append('naziv_proizvoda', this.proizvod.naziv_proizvoda);
            formData.append('opis', this.proizvod.opis);
            formData.append('materijal', this.proizvod.materijal);
            formData.append('mere', this.proizvod.mere);
            formData.append('cena', this.proizvod.cena);
            formData.append('kolicina', this.proizvod.cena);
            if (this.proizvod_slika) {
                formData.append('proizvod_slika', this.proizvod_slika);
            }

            try {
                const response = await axios.put('http://127.0.0.1:5000/proizvodi/update', formData, {
                    headers: {
                        'Content-Type': 'multipart/form-data'
                    }
                });

                if (response.data.user) {
                    this.proizvod = response.data.user;
                }

                this.$toast.success('Proizvod uspesno izmenjen!');
                setTimeout(() => {
                    this.$router.push('/').then(() => {
                        window.location.reload();
                    });
                }, 500);
            } catch (error) {
                this.$toast.error('Greska prilikom izmene profila.');
            }
        },

        nije_dozvoljeno(){
            if(this.korisnik.id != this.proizvod.korisnik_id && this.korisnik.vrsta_korisnika != 'admin'){
                this.greska = "Ne mozete pristupiti ovoj stranici jer niste admin!"
                this.$toast.error(this.greska)
                this.$router.push('/')
                console.log(this.proizvod)
            }
        }
    },

    mounted() {
        this.dohvati_proizvod(),
        this.dohvati_korisnike()
    },
}

</script>

<style scoped>
.slika{
    width: 430px;
    height: 300px;
    border-radius: 15px;
    margin-bottom: 1em;
    border: 1px solid black;
}

.forma_izmena_proizvoda{
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
        color: black;
        font-size: 4em;
    }

    .opis{
        width: 239px;
        height: 200px;
    }

    textarea{
        height: 100%;
        border-radius: 10px;
        padding: 0.2em;
    }

    
</style>