<template >
    <div class="table">
        <h1>Svi komentari</h1>
        <thead>
            <tr>
                <th>Korisnik</th>
                <th>Tekst komentara</th>
                <th>Proizvod</th>
                <th>Opcije</th>
            </tr>
        </thead>
        <tbody>
            <tr v-for="(komentar, index) in komentari" :key="komentar.komentar_id">
                <td>{{ komentar.username }}</td>
                <td>{{ komentar.tekst_komentara }}</td>
                <td>{{ komentar.naziv_proizvoda }}</td>
                <td><button @click="obrisiKomentar(komentar.komentar_id)" class="btn btn-danger">Obrisi</button></td>
            </tr>
        </tbody>
    </div>
</template>
<script>
import axios from 'axios';

export default {
    props:['id'],
    data() {
        return {
            komentari: [],
            proizvod:{}
        }
    },


    methods: {
        async dohvati_komentare() {
            const data = await axios.get('http://127.0.0.1:5000/dohvati_komentare')
            this.komentari = data.data
        }, 

        

        async obrisiKomentar(id){
            await axios.delete(`http://127.0.0.1:5000/admin/comments/delete/${id}`);
            this.$toast.success("Komentar uspesno obrisan");
            this.dohvati_komentare()
            
            
        },


    },

    mounted() {
        this.dohvati_komentare()
        
    },
}
</script>
<style scoped>
.table{
    margin-left: 48em;
}
</style>