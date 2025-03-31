<template>
    <div class="forma">
        <img class="slika" :src="korisnik.profilna_slika" alt="">
        <h1>Moj profil</h1>
        <p>
            Username
            <input type="text" v-model="korisnik.username" >
        </p>
        <p>
            Password
            <input type="text"v-model="korisnik.password" >
        </p>
        <p>
            Email
            <input type="text"v-model="korisnik.email" >
        </p>
        <p>
            Godina rodjenja
            <input type="number"v-model="korisnik.godina_rodjenja" > 
        </p>
        <p>
            Vrsta korisnika
            <select name="vrsta_korisnika" v-model="korisnik.vrsta_korisnika" >
                <option value="krojac" >Krojac</option>
                <option value="kupac">Kupac</option>
            </select>
        </p>
        <p class="file_upload">
            Dodaj sliku
            <input type="file" id="dodaj_sliku" @change="handleFileUpload">
        </p>

        <p>
            Dodaj pare
            <input type="text"v-model="korisnik.trenutno_stanje_novca" >
        </p>

        <button class="btn btn-primary" @click="izmeni">Izmeni</button>

    </div>
    <h2>Istorija kupovina</h2>
    <div class="table">
            <thead>
                <tr>
                    <th>Proizvod</th>
                    <th>Kolicina</th>
                    <th>Ukupna cena</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="(istorija, index) in istorija_uplata" :key="index">
                    <td>{{ istorija.naziv_proizvoda }}</td>
                    <td>{{ istorija.kolicina }}</td>
                    <td>{{ istorija.ukupna_cena }} din.</td>
                </tr>
            </tbody>
        </div>

    <div class="donja_strana">

        <h2>Moji proizvodi</h2>
    
        <div class="svi_proizvodi">
            <div class="proizvod" v-for="(item, index) in filter" :key="index">
            
            <div class="card" style="width: 18rem;">
            <h5 class="card-title ms-3" ><b>Objavio:</b> {{ item.username }}</h5>
            <img :src="item.proizvod_slika" class="card-img-top" alt="..." @click="odvedi_na_jedan_proizovd(item.proizvod_id)">
            <div class="card-body">
                <h5 class="card-title"><b>Naziv:</b> {{ item.naziv_proizvoda }}</h5>
                <p class="card-text"><b>Opis:</b> {{ item.opis }}</p>
                <hr>
                <p class="card-text"><b>Materijal:</b> {{ item.materijal }}</p>
                <p class="card-text"><b>Mere: </b> {{ item.mere }}cm</p>
                <hr>
                <p class="card-text"><b>Cena: </b> {{ item.cena }} din.</p>
                <hr>
                <div class="dugimici" v-if="item.korisnik_id == korisnik.id || korisnik.vrsta_korisnika == 'admin'">
                    <button @click="izmeni_proizvod(item.proizvod_id)" class="btn btn-primary">Izmeni</button>
                    <button @click="obrisi_proizvod(item.proizvod_id)" class="btn btn-danger">Obrisi</button>
                </div>
                
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
            korisnik:{
                username: "",
                password: "",
                email: "",
                godina_rodjenja: "",
                trenutno_stanje_novca: 0,
                vrsta_korisnika: ""
            },
            proizvodi: [],
            profilna_slika: null,
            istorija_uplata: []

        }
    },

    methods: {

        handleFileUpload(event){
            this.profilna_slika = event.target.files[0]
        },

        async dohvati_korisnike() {
            const data = await axios.get('http://127.0.0.1:5000/ulogovan_korisnik')
            this.korisnik = data.data
        },

        async dohvati_proizvode() {
            const data = await axios.get('http://127.0.0.1:5000/proizvodi')
            this.proizvodi = data.data
        },

        async dohvati_istoriju_kupovina(){
            const data = await axios.get('http://127.0.0.1:5000/dohvati_kupljene_proizvode')
            this.istorija_uplata = data.data
        },
 

        async izmeni() {

            if(this.korisnik.username == "" || this.korisnik.password == "" || this.korisnik.email == "" || this.korisnik.godina_rodjenja == "" || this.korisnik.vrsta_korisnika == "") {
                this.$toast.error("Sva polja moraju biti popunjena!")
                return
            }

            if(!this.korisnik.email.includes('@')){
                this.$toast.error("Email mora imati @ u sebi!")
                return
            }

            if(this.korisnik.password.length < 6){
                this.$toast.error("Password mora imati vise od 6 karaktera!")
                return
            }

            if(this.korisnik.username.length < 3){
                this.$toast.error("Duzina usernamea mora biti iznad 3 karaktera!")
                return
            }

            // const data = await axios.put('http://127.0.0.1:5000/update_korisnika',this.korisnik)
            // this.korisnik = data.data
            // location.reload()
            // this.$toast.success("Uspesno ste izmenili svoj profil!")
            // this.$router.push('/')
            const formData = new FormData();
            formData.append('id', this.korisnik.id);
            formData.append('username', this.korisnik.username);
            formData.append('email', this.korisnik.email);
            formData.append('password', this.korisnik.password);
            formData.append('godina_rodjenja', this.korisnik.godina_rodjenja);
            formData.append('trenutno_stanje_novca', this.korisnik.trenutno_stanje_novca);
            formData.append('vrsta_korisnika', this.korisnik.vrsta_korisnika);
            if (this.profilna_slika) {
                formData.append('profilna_slika', this.profilna_slika);
            }

            try {
                const response = await axios.put('http://127.0.0.1:5000/update_korisnika', formData, {
                    headers: {
                        'Content-Type': 'multipart/form-data'
                    }
                });

                if (response.data.user) {
                    this.korisnik = response.data.user;
                }

                this.$toast.success('Profil uspesno izmenjen!');
                setTimeout(() => {
                    this.$router.push('/').then(() => {
                        window.location.reload();
                    });
                }, 500);
            } catch (error) {
                this.$toast.error('Greska prilikom izmene profila.');
            }
        },
        
        async obrisi_proizvod(id) {
			await axios.delete(`http://127.0.0.1:5000/proizvodi/delete/${id}`)
			location.reload()
		},
        izmeni_proizvod(id){
			this.$router.push(`/update-proizvoda/${id}`)
		},
        odvedi_na_jedan_proizovd(id){
			this.$router.push(`/jedan-proizvod/${id}`)
		}
    },

    computed: {
        filter(){
            return this.proizvodi.filter(proizvod =>
                proizvod.korisnik_id == this.korisnik.id
            )
        }

        
    },

    mounted() {
        this.dohvati_korisnike(),
        this.dohvati_proizvode(),
        this.dohvati_istoriju_kupovina()
    },
}


</script>

<style scoped>
.slika{
    width: 130px;
    height: 130px;
    border-radius: 30px;
}

#dodaj_sliku{
    border: 0;
    background: transparent;
    /* margin-left: 5em; */
}

.file_upload{
    margin-left: 7.2em;
}

h2{
    margin-left: 26em;
    margin-top: 2em;
}
.donja_strana{
    display: flex;
    flex-direction: column;
}
.forma{
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
    .svi_proizvodi{
	display: flex;
    /* flex-direction: column; */
	gap: 3em;
	justify-content: center;
    margin-top: 3em;
}

.card{
	height: 100%;
    box-shadow: rgba(240, 46, 170, 0.4) 5px 5px, rgba(240, 46, 170, 0.3) 10px 10px, rgba(240, 46, 170, 0.2) 15px 15px, rgba(240, 46, 170, 0.1) 20px 20px, rgba(240, 46, 170, 0.05) 25px 25px;

}

.dugimici{
	display: flex;
	flex-direction: column;
	gap: 0.5em;
}

.card-text{
    color: black;
    
}

.table{
    margin-left: 51em;
    margin-top: 3em;
    
}


</style>