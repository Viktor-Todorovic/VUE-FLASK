<template>
    <h1>Svi proizvodi</h1>
    <div class="svi_proizvodi">
		<div class="proizvod" v-for="(item, index) in proizvodi" :key="index">
		
		<div class="card" style="width: 18rem;">
		<h5 class="card-title ms-3" ><b>Objavio:</b> {{ item.username }}</h5>
		<img :src="item.proizvod_slika" class="card-img-top" alt="...">
		<div class="card-body">
			<h5 class="card-title"><b>Naziv:</b> {{ item.naziv_proizvoda }}</h5>
			<p class="card-text"><b>Opis:</b> {{ item.opis }}</p>
			<hr>
			<p class="card-text"><b>Materijal:</b> {{ item.materijal }}</p>
			<p class="card-text"><b>Mere: </b> {{ item.mere }}cm</p>
			<hr>
			<p class="card-text"><b>Kolicina: </b> {{ item.kolicina }}</p>
			<p class="card-text"><b>Cena: </b> {{ item.cena }} din.</p>
			<hr>
			<div class="dugimici" v-if="item.korisnik_id == korisnik.id || korisnik.vrsta_korisnika == 'admin'">
				<button @click="izmeni(item.proizvod_id)" class="btn btn-primary">Izmeni</button>
				<button @click="obrisi_proizvod(item.proizvod_id)" class="btn btn-danger">Obrisi</button>
			</div>
			
		</div>
		</div>
	</div>
	</div>
</template>
<script>
import axios from 'axios'
export default {
    data() {
        return {
            proizvodi: [],
			korisnik:{},
			proizvod: {}
        }
    },

    methods: {
		async dohvati_proizvode() {
            const data = await axios.get('http://127.0.0.1:5000/proizvodi')
            this.proizvodi = data.data
        },

		async dohvati_korisnike() {
            const data = await axios.get('http://127.0.0.1:5000/ulogovan_korisnik')
            this.korisnik = data.data
			this.izbaci_ako_nije_admin()
        }, 

		async obrisi_proizvod(id) {
			await axios.delete(`http://127.0.0.1:5000/proizvodi/delete/${id}`)
			location.reload()
		},

		izmeni(id){
			this.$router.push(`/update-proizvoda/${id}`)
		},

		izbaci_ako_nije_admin(){
            if(this.korisnik.vrsta_korisnika != 'admin'){
                this.$router.push('/')
                this.$toast.error('Morate biti admin da bi pristupili ovoj stranici!')
            }
        }

		

	},

    mounted() {
		this.dohvati_proizvode(),
		this.dohvati_korisnike()
		
	},
}
</script>
<style scoped>
    .svi_proizvodi{
	display: flex;
	gap: 1em;
	justify-content: center;
	flex-wrap: wrap;
}

.card{
	height: 100%;
}

.dugimici{
	display: flex;
	flex-direction: column;
	gap: 0.5em;
}
</style>