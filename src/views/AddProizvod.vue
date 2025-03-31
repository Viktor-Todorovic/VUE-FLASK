<template>
    <div class="forma_dodaj_proizvod">
        <h1>Dodaj proizvod</h1>
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
            <input type="text" v-model="proizvod.materijal">
        </p>
        <p>
            Mere
            <input type="number" v-model="proizvod.mere">
        </p>
        <p>
            Cena
            <input type="number" v-model="proizvod.cena">
        </p>
        <p>
            Kolicina
            <input type="number" v-model="proizvod.kolicina">
        </p>
        <p id="file_p">
            Slika proizvoda
            <input id="file" type="file" @change="handleFileUpload">
        </p>

        <button @click="dodaj_proizvod" class="btn btn-primary mb-5">Dodaj</button>
    </div>
</template>


<script>
import axios from 'axios'
export default {
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
            proizvodi: [],
            proizvod_slika: null
        }
    },

    methods: {
        async dohvati_proizvode() {
            const data = await axios.get('http://127.0.0.1:5000/proizvodi')
            this.proizvodi = data.data
        },
        handleFileUpload(event){
            this.proizvod_slika = event.target.files[0]
        },

        async dodaj_proizvod(){

            if(this.proizvod.naziv_proizvoda == "" || this.proizvod.opis == "" || this.proizvod.materijal == "" || this.proizvod.mere == "" || this.proizvod.cena == "") {
                this.$toast.error("Sva polja moraju biti popunjena!")
                return
            }

            if(this.proizvod.naziv_proizvoda.length <3){
                this.$toast.error("Naziv mora imati vise od tri karaktera!")
                return
            }

            if(this.proizvod.materijal.length <3){
                this.$toast.error("Naziv mora imati vise od tri karaktera!")
                return
            }

            if(this.proizvod.mere < 0){
                this.$toast.error("Mere ne mogu biti negativne!")
                return
            }
            if(this.proizvod.cena < 0){
                this.$toast.error("Cena ne moze biti negativna!")
                return
            }

            // await axios.post('http://127.0.0.1:5000/dodaj_proizvod',this.proizvod)
            // this.$toast.success("Uspesno ste dodali proizvod!")
            // this.$router.push('/')
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
                const response = await axios.post('http://127.0.0.1:5000/dodaj_proizvod', formData, {
                    headers: {
                        'Content-Type': 'multipart/form-data'
                    }
                });

                if (response.data.user) {
                    this.proizvod = response.data.user;
                }

                this.$toast.success('Proizvod uspesno dodat!')
                this.$router.push('/')

            } catch (error) {
                this.$toast.error('Greska prilikom izmene profila.');
            }
        }
    },

    mounted() {
        this.dohvati_proizvode()
    },
}

</script>


<style scoped>
.forma_dodaj_proizvod{
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

    .opis{
        width: 239px;
        height: 200px;
    }

    textarea{
        height: 100%;
        border-radius: 10px;
        padding: 0.2em;
    }

    #file{
        border: 0;
        /* margin-left: 5em; */
    }

    #file_p{
        margin-left: 7em;
    }
</style>