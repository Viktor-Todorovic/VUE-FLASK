<template>
    <div class="table">
        <h1>Korpa</h1>
        <h4><b>Vase stanje novca: {{ korisnik.trenutno_stanje_novca }} din.</b></h4>
        <thead>
            <tr>
                <!-- <th>ID</th> -->
                <th>Naziv proizvoda</th>
                <th>Kolicina</th>
                <th>Cena</th>
                <th>Opcije</th>
            </tr>
        </thead>
        <tbody>
            <tr v-for="proizvod in korpa" :key="proizvod.proizvod_id">
                <!-- <img :src="proizvod.proizvod_slika" class="card-img-top" alt="..."> -->
                <td>{{ proizvod.naziv_proizvoda }}</td>
                <td><button @click="smanjiKolicinu(proizvod.proizvod_id)">-</button><input type="number" v-model="proizvod.kolicina" min="1" @change="azurirajKolicinu(proizvod)"><button @click="povecajKolicinu(proizvod.proizvod_id)">+</button></td>
                <td>{{ proizvod.cena }} din.</td>
                
                <td><button @click="obrisi_iz_korpe(proizvod.proizvod_id)" class="btn btn-danger">Obrisi</button></td>
            </tr>
        </tbody>
        <div class="total-price mt-3">
            <h4>Ukupna cena: <span>{{ ukupnaCena }} din</span></h4>
        </div>
        <button id="kupi_korpa" class="btn btn-success" @click="zavrsiKupovinu">Kupi</button>
    </div>
</template>
<script>
import axios from 'axios'
export default {
    data() {
        return {
            proizvod: {},
            korisnik: {},
            korpa: []
        }
    },

    methods: {
        async dohvati_korisnike() {
            const data = await axios.get('http://127.0.0.1:5000/ulogovan_korisnik')
            this.korisnik = data.data
        }, 

        async dohvati_proizvod_za_korpu() {
            const data = await axios.get('http://127.0.0.1:5000/korpa')
            this.korpa = data.data
        }, 

        async obrisi_iz_korpe(proizvod_id){
            await axios.delete(`http://127.0.0.1:5000/korpa/obrisi/${proizvod_id}`)
            this.$toast.success("Uspesno ste obrisali proizvod iz korpe!")
			location.reload()
            console.log(proizvod_id)
        },

        async azurirajKolicinu(item) {
            try {
                await axios.post(`http://127.0.0.1:5000/cart/update/${item.proizvod_id}`, {
                    kolicina: item.kolicina
                });
                // this.ukupnaCena += razlikaUKolicini * proizvod.cena;
            } catch (error) {
                console.error("Greska: ", error);
            }
        },
        async smanjiKolicinu(id) {
            let item = this.korpa.find(p => p.proizvod_id === id);
            if (item.kolicina > 1) {
                item.kolicina--;
                await this.azurirajKolicinu(item);
            }
        },
        async povecajKolicinu(id) {
            let item = this.korpa.find(p => p.proizvod_id === id);
            item.kolicina++;
            await this.azurirajKolicinu(item);
        },
        // async zavrsiKupovinu() {
        //     await axios.post('http://127.0.0.1:5000/cart/checkout')

            
            
        //     location.reload()
        //     this.$toast.success("Uspesno ste kupili")
        // },

        async zavrsiKupovinu() {
    try {
        await axios.post('http://127.0.0.1:5000/cart/checkout', {}, { withCredentials: true });
        
        this.$toast.success("Uspešno ste kupili!");
        location.reload();
    } catch (error) {
        this.$toast.error(error.response?.data?.error || "Došlo je do greške!");
    }
},


        

        

        
        
    },

    

    computed: {
        ukupnaCena() {
            return this.korpa.reduce((sum, item) => sum + (item.kolicina * item.cena), 0);
        }
    },

    mounted() {
        this.dohvati_korisnike(),
        this.dohvati_proizvod_za_korpu()
    },
}
</script>
<style>
.table{
    margin-left: 50em;
}

#kupi_korpa{
    width: 200px;
    margin-top: 2em;
    margin-left: 8em;
}
</style>