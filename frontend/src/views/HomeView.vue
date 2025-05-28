
<template>
	<h1>Svi proizvodi</h1>
	<div class="svi_proizvodi">
		<div class="proizvod" v-for="(item, index) in proizvodi" :key="item.proizvod_id">
		
		<div class="card" style="width: 18rem;">
			<div class="card-objava mt-2">
				<h5 class="card-title ms-3"> <b>Objavio:</b> {{ item.username }}</h5><img class="slika_profilna ms-1" :src="item.profilna_slika" alt="">
			</div>
		<img :src="item.proizvod_slika" class="card-img-top" alt="..." @click="odvedi_na_jedan_proizovd(item.proizvod_id)">
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
			<button id="kupi" @click="dodaj_u_korpu(item.proizvod_id)" class="btn btn-success mt-2" v-if="(korisnik.vrsta_korisnika == 'krojac' || korisnik.vrsta_korisnika == 'admin' || korisnik.vrsta_korisnika == 'kupac') && item.korisnik_id !== korisnik.id">Kupi</button>
			
			
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
        }, 

		async obrisi_proizvod(id) {
			await axios.delete(`http://127.0.0.1:5000/proizvodi/delete/${id}`)
			location.reload()
		},

		izmeni(id){
			this.$router.push(`/update-proizvoda/${id}`)
		},

		odvedi_na_jedan_proizovd(id){
			this.$router.push(`/jedan-proizvod/${id}`)
		},

		async dodaj_u_korpu(proizvod_id){
			await axios.post(`http://127.0.0.1:5000/cart/add/${proizvod_id}`,{
				kolicina: 1
			},)
			this.$toast.success('Uspesno ste dodali proizvod u korpu!')
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
	gap: 5em 5em;
	justify-content: center;
	flex-wrap: wrap;
	width: 60%;
	margin: 0 auto;
}

.slika_profilna{
	width: 30px;
	height: 30px;
	border-radius: 30px;
}

.card{
	height: 100%;
	/* box-shadow: 4px 10px; */
	box-shadow: rgba(240, 46, 170, 0.4) 5px 5px, rgba(240, 46, 170, 0.3) 10px 10px, rgba(240, 46, 170, 0.2) 15px 15px, rgba(240, 46, 170, 0.1) 20px 20px, rgba(240, 46, 170, 0.05) 25px 25px;
}

.card-objava{
	display: flex;
}

.dugimici{
	display: flex;
	flex-direction: column;
	gap: 0.5em;
}

#kupi{
	width: 100%;
	height: 50px;
}

h1{
	margin-left: 21em;
	margin-bottom: 1em;
	margin-top: 0.5em;
}

</style>

