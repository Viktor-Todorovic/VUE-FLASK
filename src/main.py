
from flask import Flask,render_template,request,session,jsonify
import mysql.connector
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename
app = Flask(__name__)
app.config['SECRET_KEY'] = "RAF2021-2022"
app.config['SESSION_COOKIE_SAMESITE'] = 'None'
app.config['SESSION_COOKIE_SECURE'] = True
CORS(app,supports_credentials=True)
SLIKA = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../frontend/src/assets/slike_korisnici"))
PROIZVODI = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../frontend/src/assets/slike_proizvodi"))
app.config['UPLOAD_FOLDER'] = SLIKA
app.config['UPLOAD_FOLDER_PROIZVODI'] = PROIZVODI
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'svg', 'webp'}



def get_db_connection():
    return mysql.connector.connect(
	host="localhost",
	user="root",
	password="", 
	database="krojacki_salon"
    )

@app.route('/upload-profilna-slika', methods=['POST'])
def upload_profilna_slika():
    if 'profilna_slika' not in request.files or 'id' not in request.form:
        return jsonify({'error': 'Nema fajla ili ID korisnika nije prosleđen'}), 400
    
    file = request.files['profilna_slika']
    user_id = request.form.get('id')

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        relative_path = f"/src/assets/slike_korisnici/{filename}"

        file.save(file_path)
        try:
            mydb = get_db_connection()
            cursor = mydb.cursor(prepared=True)
            query = "UPDATE korisnici SET profilna_slika = ? WHERE id = ?"
            cursor.execute(query, (relative_path, user_id))
            mydb.commit()

            return jsonify({
                'message': 'Slika uspešno sačuvana',
                'image_path': relative_path
            })
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'error': 'Nedozvoljen format fajla'}), 400
    
@app.route('/upload-proizvod-slika', methods=['POST'])
def upload_proizvod_slika():
    if 'proizvod_slika' not in request.files or 'proizvod_id' not in request.form:
        return jsonify({'error': 'Nema fajla ili ID korisnika nije prosleđen'}), 400
    
    file = request.files['proizvod_slika']
    slika_id = request.form.get('proizvod_id')

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER_PROIZVODI'], filename)
        relative_path = f"/src/assets/slike_proizvodi/{filename}"

        file.save(file_path)
        try:
            mydb = get_db_connection()
            cursor = mydb.cursor(prepared=True)
            query = "UPDATE proizvodi SET proizvod_slika = ? WHERE proizvod_id = ?"
            cursor.execute(query, (relative_path, slika_id))
            mydb.commit()

            return jsonify({
                'message': 'Slika uspešno sačuvana',
                'image_path': relative_path
            })
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'error': 'Nedozvoljen format fajla'}), 400


@app.route('/korisnici')
def svi_korisnici():
    mydb = get_db_connection()
    cursor = mydb.cursor(dictionary=True)
    cursor.execute("select * from korisnici")
    korisnici = cursor.fetchall()
    return jsonify(korisnici)
############################################KOMENTARI#######################################
@app.route('/komentari')
def svi_komentari():
    mydb = get_db_connection()
    cursor = mydb.cursor(dictionary=True)
    cursor.execute("select * from komentari")
    komentari = cursor.fetchall()
    return jsonify(komentari)

@app.route('/dohvatiKomentare/<proizvod_id>')
def dohvati_komentare(proizvod_id):
    mydb = get_db_connection()
    cursor = mydb.cursor(dictionary=True)
    query = "SELECT komentari.*, korisnici.username FROM komentari JOIN korisnici ON komentari.korisnik_id = korisnici.id WHERE komentari.proizvod_id = %s"
    cursor.execute(query, (proizvod_id,))
    rez = cursor.fetchall()
    print(rez)
    return jsonify(rez)

@app.route('/dohvati_komentare')
def dohvati_sve_komentare():
    mydb = get_db_connection()
    cursor = mydb.cursor(dictionary=True)
    query = "SELECT komentari.*, korisnici.username, proizvodi.naziv_proizvoda FROM komentari JOIN korisnici ON komentari.korisnik_id = korisnici.id join proizvodi on proizvodi.proizvod_id = komentari.proizvod_id"
    cursor.execute(query)
    rez = cursor.fetchall()
    return jsonify(rez)

# @app.route('/obrisi_komentar_admin/<komentar_id>', methods =['DELETE'])
# def obrisi_komentar_admin(komentar_id):
#     mydb = get_db_connection()
#     cursor = mydb.cursor(dictionary=True)
#     query = "DELETE FROM komentari where komentar_id = %s"
#     cursor.execute(query,(komentar_id, ))
#     rez = cursor.fetchall()
#     return jsonify(rez)

@app.route('/admin/comments/delete/<id>', methods=['DELETE'])
def admin_obrisi_komentar(id):
    mydb = get_db_connection()
    cursor = mydb.cursor(prepared=True)
    query = "DELETE FROM komentari WHERE komentar_id = %s"
    cursor.execute(query, (id,))
    mydb.commit()
    return jsonify({'message': 'Komentar uspesno obrisan'})


@app.route('/proizvod/<proizvod_id>/komentar/obrisi/<komentar_id>', methods=['DELETE'])
def obrisi_komentar(proizvod_id, komentar_id):
    mydb = get_db_connection()
    cursor = mydb.cursor(prepared=True)
    cursor.execute("DELETE FROM komentari WHERE komentar_id = %s AND proizvod_id = %s", (komentar_id, proizvod_id))
    mydb.commit()
    return jsonify({'message': 'Komentar uspesno obrisan'})

@app.route('/dohvatiSveKomentare')
def dohvatiSveKomentare():
    mydb = get_db_connection()
    cursor = mydb.cursor(dictionary=True)
    query = "SELECT komentari.*, korisnici.username, proizvodi.naziv FROM komentari JOIN korisnici ON komentari.korisnik_id = korisnici.id JOIN proizvodi ON komentari.proizvod_id = proizvodi.proizvod_id"
    cursor.execute(query)
    rez = cursor.fetchall()
    return jsonify(rez)

@app.route('/proizvodi/komentari', methods =['POST'])
def proizvodi_komentari():
    data = request.json
    mydb = get_db_connection()
    cursor = mydb.cursor(prepared=True)
    print(data)
    proizvod_id = data['proizvod_id']
    korisnik_id = data['korisnik_id']
    tekst_komentara = data['tekst_komentara']
    
    query = "INSERT INTO komentari (tekst_komentara, proizvod_id, korisnik_id) VALUES (%s, %s, %s)"
    params = (tekst_komentara,proizvod_id,korisnik_id)
    cursor.execute(query,params)
    mydb.commit()
    return jsonify(data)





###############################################KOMENTARI##################################
###############################################KORPA##################################


# @app.route('/cart/add/<int:product_id>', methods=['POST'])
# def add_to_cart(product_id):

#     if 'korisnik' not in session:
#         return jsonify({'error': 'Morate biti prijavljeni da biste dodali proizvod u korpu.'}), 401

#     korisnik_id = session['korisnik']['id']
#     kolicina = request.json.get('kolicina', 1)  

#     try:
#         mydb = get_db_connection()
#         cursor = mydb.cursor(prepared=True)


#         cursor.execute("SELECT * FROM proizvodi WHERE proizvod_id = %s", (product_id,))
#         proizvod = cursor.fetchone()
#         if not proizvod:
#             return jsonify({'error': 'Proizvod ne postoji.'}), 404


#         cursor.execute("SELECT * FROM korpa WHERE proizvod_id = %s AND korisnik_id = %s", ( product_id,korisnik_id))
#         postojeca_stavka = cursor.fetchone()

#         if postojeca_stavka:
#             cursor.execute(
#                 "UPDATE korpa SET kolicina = kolicina + %s WHERE korisnik_id = %s AND proizvod_id = %s",
#                 (kolicina, korisnik_id, product_id),
#             )
#         else:
#             cursor.execute(
#                 "INSERT INTO korpa ( proizvod_id, korisnik_id, kolicina) VALUES (%s, %s, %s)",
#                 (korisnik_id, product_id, kolicina),
#             )

#         mydb.commit()
#         return jsonify({'message': 'Proizvod uspešno dodat u korpu.'}), 201
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500
#     finally:
#         cursor.close()
#         mydb.close()

# @app.route('/cart/add/<int:product_id>', methods=['POST'])
# def add_to_cart(proizvod_id):
#     data = request.json
#     mydb = get_db_connection()
#     cursor = mydb.cursor(prepared=True)
#     kolicina = data.get('kolicina')
#     korisnik_id = session.get['korisnik']
#     proizvod_id = data.get('proizvod_id')
#     cursor.execute("INSERT INTO korisnici (id, username, email, password, godina_rodjenja, trenutno_stanje_novca, vrsta_korisnika) VALUES (?, ?, ?, ?, ?, ?, ?)")
#     mydb.commit()
#     return data  



# @app.route('/cart/add/<int:proizvod_id>', methods=['POST'])
# def dodaj_u_korpu(proizvod_id):
#     korisnik_id = session.get('korisnik', {}).get('id')
#     if not korisnik_id:
#         return jsonify({'error' : 'Niste prijavljeni!'})
    
#     data = request.json
#     kolicina = data.get('kolicina', 1)
#     mydb = get_db_connection()
#     cursor = mydb.cursor(prepared=True)
#     cursor.execute('SELECT kolicina from korpa where korisnik_id = %s AND proizvod_id = %s',(korisnik_id,proizvod_id))
#     rez = cursor.fetchone()
#     if rez:
#         nova_kolicina = rez[0] + kolicina
#         cursor.execute('UPDATE korpa SET  kolicina = %s WHERE korisnik_id = %s AND proizvod_id = %s',(nova_kolicina,korisnik_id,proizvod_id))
#     else:
#         cursor.execute('INSERT INTO korpa (proizvod_id,korisnik_id,kolicina) VALUES (%s,%s,%s)',(proizvod_id,korisnik_id,kolicina))
#     mydb.commit()
#     return jsonify({'message' : 'Proizvod_dodat_u_korpu'})

@app.route('/cart/add/<int:proizvod_id>', methods=['POST'])
def dodaj_u_korpu(proizvod_id):
    korisnik_id = session.get('korisnik', {}).get('id')
    if not korisnik_id:
        return jsonify({'error' : 'Niste prijavljeni!'})
    data = request.json
    kolicina = data.get('kolicina', 1)
    mydb = get_db_connection()
    cursor = mydb.cursor(prepared=True)
    
    query ='INSERT INTO korpa (proizvod_id,korisnik_id,kolicina) VALUES (%s,%s,%s)'
    params = (proizvod_id,korisnik_id,kolicina)
    cursor.execute(query,params)
    mydb.commit()
    return jsonify(data)


# @app.route('/korpa', methods = ['GET'])
# def korpa():
#     korisnik_id = session.get('korisnik', {}).get('id')
#     if not korisnik_id:
#         return jsonify({'error' : 'Niste prijavljeni!'})
    
#     mydb = get_db_connection()
#     cursor = mydb.cursor(dictionary=True)
#     cursor.execute('SELECT *, korisnik.id, proizvod.proizvod_id from korpa join korisnici on korpa.korisnik_id = korisnici.id join proizvodi on korpa.proizvod_id = proizvod.proizvod_id where korpa.korisnik_id = %s',(korisnik_id, ))
#     rez = cursor.fetchall()
#     return jsonify(rez)

@app.route('/korpa', methods=['GET'])
def korpa():
    korisnik_id = session.get('korisnik', {}).get('id')
    if not korisnik_id:
        return jsonify({'error': 'Niste prijavljeni!'}), 401

    try:
        mydb = get_db_connection()
        cursor = mydb.cursor(dictionary=True)

        # SQL upit koji dohvaća proizvode i korisnike
        query = """
        SELECT 
            korpa.korpa_id AS korpa_id,
            korpa.kolicina,
            proizvodi.proizvod_id,
            proizvodi.naziv_proizvoda,
            proizvodi.cena,
            korisnici.username AS korisnik_username
        FROM korpa
        JOIN korisnici ON korpa.korisnik_id = korisnici.id
        JOIN proizvodi ON korpa.proizvod_id = proizvodi.proizvod_id
        WHERE korpa.korisnik_id = %s
        """
        cursor.execute(query, (korisnik_id,))
        rez = cursor.fetchall()

        return jsonify(rez), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        mydb.close()

# @app.route('/cart/update/<int:proizvod_id>', methods=['POST'])
# def update_cart(proizvod_id):
#     korisnik_id = session.get('user', {}).get('id')
#     if not korisnik_id:
#         return jsonify({'error': 'Niste prijavljeni'}), 401
#     data = request.json
#     nova_kolicina = data.get('kolicina')
#     mydb = get_db_connection()
#     cursor = mydb.cursor(prepared=True)
#     cursor.execute("UPDATE korpa SET kolicina = %s WHERE korisnik_id = %s AND proizvod_id = %s",(nova_kolicina, korisnik_id, proizvod_id))
#     mydb.commit()
#     return jsonify({'message': 'Količina ažurirana'})

@app.route('/korpa/obrisi/<proizvod_id>', methods =['DELETE'])
def obrisi_iz_korpe(proizvod_id):
    korisnik_id = session.get('korisnik', {}).get('id')
    if not korisnik_id:
        return jsonify({'error': 'Niste prijavljeni!'}), 401
    
    mydb = get_db_connection()
    cursor = mydb.cursor(prepared=True)
    cursor.execute('DELETE FROM korpa WHERE korisnik_id = %s and proizvod_id = %s',(korisnik_id,proizvod_id))
    mydb.commit()
    return jsonify({'message': 'Proizvod uklonjen iz korpe!'})


@app.route('/dodaj_kolicinu_korpe', methods=['POST'])
def dodaj_kolicinu_korpe():
    try:
        data = request.json
        mydb = get_db_connection()
        cursor = mydb.cursor(dictionary=True)
        
        
        if 'kolicina' not in data or 'korpa_id' not in data:
            return jsonify({'error': 'Nedostaju podaci o količini ili ID proizvoda'}), 400
        
        nova_kolicina = int(data['kolicina'])
        korpa_id = int(data['korpa_id'])
        
        
        cursor.execute('SELECT kolicina FROM korpa WHERE korpa_id = %s', (korpa_id,))
        result = cursor.fetchone()
        if result is None:
            return jsonify({'error': 'Proizvod nije pronađen'}), 404
        
        trenutna_kolicina = result['kolicina']
        ukupno = trenutna_kolicina + nova_kolicina
        
        
        cursor.execute('UPDATE korpa SET kolicina = %s WHERE korpa_id = %s', (ukupno, korpa_id))
        mydb.commit()
        
        return jsonify({'ukupno': ukupno}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        mydb.close()


@app.route('/cart/update/<int:proizvod_id>', methods=['POST'])
def update_cart(proizvod_id):
    korisnik_id = session.get('korisnik', {}).get('id')
    if not korisnik_id:
        return jsonify({'error': 'Niste prijavljeni'}), 401

    data = request.json
    nova_kolicina = data.get('kolicina')

    if not nova_kolicina or not isinstance(nova_kolicina, int) or nova_kolicina < 1:
        return jsonify({'error': 'Neispravna količina'}), 400

    try:
        mydb = get_db_connection()
        cursor = mydb.cursor(prepared=True)

        cursor.execute(
            "SELECT * FROM korpa WHERE korisnik_id = %s AND proizvod_id = %s",
            (korisnik_id, proizvod_id)
        )
        proizvod = cursor.fetchone()
        if not proizvod:
            return jsonify({'error': 'Proizvod nije pronađen u korpi'}), 404

        cursor.execute(
            "UPDATE korpa SET kolicina = %s WHERE korisnik_id = %s AND proizvod_id = %s",
            (nova_kolicina, korisnik_id, proizvod_id)
        )
        mydb.commit()
        return jsonify({'message': 'Količina uspešno ažurirana'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        mydb.close()








# @app.route('/cart/checkout', methods=['POST'])
# def checkout():
#     korisnik_id = session.get('korisnik', {}).get('id')
#     if not korisnik_id:
#         return jsonify({'error': 'Niste prijavljeni!'}), 401

#     try:
#         mydb = get_db_connection()
#         cursor = mydb.cursor(prepared=True)

        
#         query = """
#         SELECT 
#             korpa.proizvod_id AS proizvod_id,
#             korpa.kolicina AS kolicina,
#             proizvodi.cena AS cena_po_komadu,
#             proizvodi.korisnik_id AS krojac_id, 
#             (korpa.kolicina * proizvodi.cena) AS ukupna_cena
#         FROM korpa
#         JOIN proizvodi ON korpa.proizvod_id = proizvodi.proizvod_id
#         WHERE korpa.korisnik_id = %s
#         """
#         cursor.execute(query, (korisnik_id,))
#         proizvodi_u_korpi = cursor.fetchall()

#         if not proizvodi_u_korpi:
#             return jsonify({'error': 'Vaša korpa je prazna!'}), 400

#         ukupna_cena = sum([proizvod[4] for proizvod in proizvodi_u_korpi])

        
#         cursor.execute("SELECT trenutno_stanje_novca FROM korisnici WHERE id = %s", (korisnik_id,))
#         saldo_rez = cursor.fetchone()
#         if not saldo_rez or saldo_rez[0] < ukupna_cena:
#             return jsonify({'error': 'Nemate dovoljno novca za kupovinu!'}), 400

        
#         cursor.execute(
#             "UPDATE korisnici SET trenutno_stanje_novca = trenutno_stanje_novca - %s WHERE id = %s",
#             (ukupna_cena, korisnik_id)
#         )

        
#         for proizvod in proizvodi_u_korpi:
#             proizvod_id = proizvod[0]
#             kolicina = proizvod[1]
#             krojac_id = proizvod[3]
#             ukupna_cena_proizvoda = proizvod[4]

            
#             cursor.execute(
#                 """
#                 INSERT INTO istorija_kupovina (proizvod_id, korisnik_id, kolicina, ukupna_cena)
#                 VALUES (%s, %s, %s, %s)
#                 """,
#                 (proizvod_id, korisnik_id, kolicina, ukupna_cena_proizvoda)
#             )

            
#             cursor.execute(
#                 "UPDATE korisnici SET trenutno_stanje_novca = trenutno_stanje_novca + %s WHERE id = %s",
#                 (ukupna_cena_proizvoda, krojac_id)
#             )

            
#             cursor.execute(
#                 "UPDATE proizvodi SET kolicina = kolicina - %s WHERE proizvod_id = %s",
#                 (kolicina, proizvod_id)
#             )

        
#         cursor.execute("DELETE FROM korpa WHERE korisnik_id = %s", (korisnik_id,))

#         mydb.commit()

#         return jsonify({'message': f'Kupovina uspešno završena! Ukupno potrošeno: {ukupna_cena} RSD'}), 200

#     except Exception as e:
#         mydb.rollback()
#         return jsonify({'error': str(e)}), 500

#     finally:
#         cursor.close()
#         mydb.close()

@app.route('/cart/checkout', methods=['POST'])
def checkout():
    korisnik_id = session.get('korisnik', {}).get('id')
    if not korisnik_id:
        return jsonify({'error': 'Niste prijavljeni!'}), 401

    try:
        mydb = get_db_connection()
        cursor = mydb.cursor(prepared=True)

        query = """
        SELECT 
            korpa.proizvod_id AS proizvod_id,
            korpa.kolicina AS kolicina,
            proizvodi.cena AS cena_po_komadu,
            proizvodi.korisnik_id AS krojac_id, 
            proizvodi.kolicina AS dostupna_kolicina,
            (korpa.kolicina * proizvodi.cena) AS ukupna_cena
        FROM korpa
        JOIN proizvodi ON korpa.proizvod_id = proizvodi.proizvod_id
        WHERE korpa.korisnik_id = %s
        """
        cursor.execute(query, (korisnik_id,))
        proizvodi_u_korpi = cursor.fetchall()

        if not proizvodi_u_korpi:
            return jsonify({'error': 'Vaša korpa je prazna!'}), 400

        ukupna_cena = sum([proizvod[5] for proizvod in proizvodi_u_korpi])

        cursor.execute("SELECT trenutno_stanje_novca FROM korisnici WHERE id = %s", (korisnik_id,))
        saldo_rez = cursor.fetchone()
        if not saldo_rez or saldo_rez[0] < ukupna_cena:
            return jsonify({'error': 'Nemate dovoljno novca za kupovinu!'}), 400

       
        for proizvod in proizvodi_u_korpi:
            proizvod_id = proizvod[0]
            kolicina_za_kupovinu = proizvod[1]
            dostupna_kolicina = proizvod[4]

            if kolicina_za_kupovinu > dostupna_kolicina:
                return jsonify({'error': f'Proizvoda nema dovoljno na stanju! Dostupno: {dostupna_kolicina}, a vi pokušavate da kupite {kolicina_za_kupovinu}.'}), 400

    
        cursor.execute(
            "UPDATE korisnici SET trenutno_stanje_novca = trenutno_stanje_novca - %s WHERE id = %s",
            (ukupna_cena, korisnik_id)
        )

    
        cursor.execute("SELECT trenutno_stanje_novca FROM korisnici WHERE id = %s", (korisnik_id,))
        novo_stanje = cursor.fetchone()[0]
        session['korisnik']['trenutno_stanje_novca'] = novo_stanje  


     
        for proizvod in proizvodi_u_korpi:
            proizvod_id = proizvod[0]
            kolicina = proizvod[1]
            krojac_id = proizvod[3]
            ukupna_cena_proizvoda = proizvod[5]

            cursor.execute(
                """
                INSERT INTO istorija_kupovina (proizvod_id, korisnik_id, kolicina, ukupna_cena)
                VALUES (%s, %s, %s, %s)
                """,
                (proizvod_id, korisnik_id, kolicina, ukupna_cena_proizvoda)
            )

            cursor.execute(
                "UPDATE korisnici SET trenutno_stanje_novca = trenutno_stanje_novca + %s WHERE id = %s",
                (ukupna_cena_proizvoda, krojac_id)
            )

            cursor.execute(
                "UPDATE proizvodi SET kolicina = kolicina - %s WHERE proizvod_id = %s",
                (kolicina, proizvod_id)
            )

        cursor.execute("DELETE FROM korpa WHERE korisnik_id = %s", (korisnik_id,))
        mydb.commit()

        return jsonify({'message': f'Kupovina uspešno završena! Ukupno potrošeno: {ukupna_cena} RSD'}), 200

    except Exception as e:
        mydb.rollback()
        return jsonify({'error': str(e)}), 500

    finally:
        cursor.close()
        mydb.close()








@app.route('/dohvati_kupljene_proizvode', methods=['GET'])
def dohvati_kupljene_proizvode():
    
    korisnik_id = session.get('korisnik', {}).get('id')
    if not korisnik_id:
        return jsonify({'error': 'Niste prijavljeni!'}), 401
    
    mydb = get_db_connection()
    cursor = mydb.cursor(dictionary=True)
    query = "SELECT istorija_kupovina.*,istorija_kupovina.korisnik_id,istorija_kupovina.proizvod_id,proizvodi.naziv_proizvoda  FROM istorija_kupovina join proizvodi on proizvodi.proizvod_id = istorija_kupovina.proizvod_id join korisnici on korisnici.id = istorija_kupovina.korisnik_id WHERE istorija_kupovina.korisnik_id = %s"
    cursor.execute(query,(korisnik_id, ))
    rez = cursor.fetchall()
    return jsonify(rez)














###############################################KORPA##################################





@app.route('/proizvodi')
def svi_proizvodi():
    mydb = get_db_connection()
    cursor = mydb.cursor(dictionary=True)
    cursor.execute("select * from proizvodi join korisnici on korisnici.id = proizvodi.korisnik_id")
    proizvodi = cursor.fetchall()
    return jsonify(proizvodi)

@app.route('/dodaj_proizvod', methods=['POST'])
def dodaj_proizvod():
    mydb = get_db_connection()
    cursor = mydb.cursor(prepared=True)
    proizvod_id = 'NULL'
    korisnik_id = session['korisnik'].get('id')
    naziv_proizvoda = request.form.get('naziv_proizvoda')
    opis = request.form.get('opis')
    materijal = request.form.get('materijal')
    mere = request.form.get('mere')
    cena = request.form.get('cena')
    kolicina = request.form.get('kolicina')
    proizvod_slika = None
    if 'proizvod_slika' in request.files and request.files['proizvod_slika'].filename != '':
        file = request.files['proizvod_slika']
        
        if file and allowed_file(file.filename):
            print(proizvod_slika)
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER_PROIZVODI'], filename)
            file.save(file_path)
            proizvod_slika = f"/src/assets/slike_proizvodi/{filename}"
            

            query = "INSERT INTO proizvodi (proizvod_id, korisnik_id,naziv_proizvoda,opis,materijal,mere,cena,kolicina,proizvod_slika) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
            params = (proizvod_id,korisnik_id,naziv_proizvoda, opis, materijal, mere, cena,kolicina, proizvod_slika)
            
        else:
            return jsonify({'error': 'Neispravan format slike'}), 400
    else:
        query = "INSERT INTO proizvodi (proizvod_id, korisnik_id,naziv_proizvoda,opis,materijal,mere,cena,kolicina) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
        params = (proizvod_id,korisnik_id,naziv_proizvoda, opis, materijal, mere, cena,kolicina)

    cursor.execute(query, params)
    mydb.commit()
    print(cursor.rowcount)
    cursor = mydb.cursor(dictionary=True)
    updated_user = cursor.fetchone()
    
    return jsonify({'message': 'Profil uspešno ažuriran', 'korisnik': updated_user})

# "INSERT INTO proizvodi (proizvod_id, korisnik_id,naziv_proizvoda,opis,materijal,mere,cena,kolicina) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"

@app.route('/proizvodi/delete/<id>', methods=['DELETE'])
def obrisi_proizvod(id):
    mydb = get_db_connection()
    cursor = mydb.cursor(prepared=True)
    query = "delete from proizvodi where proizvod_id =%s"
    cursor.execute(query, (id, ))
    mydb.commit()
    return ""

@app.route('/korisnici/delete/<id>', methods=['DELETE'])
def obrisi_korisnika(id):
    mydb = get_db_connection()
    cursor = mydb.cursor(prepared=True)
    query = "delete from korisnici where id =%s"
    cursor.execute(query, (id, ))
    mydb.commit()
    return ""
# -----------------------
@app.route('/proizvodi/update', methods=['PUT'])
def update_proizvoda():
   
    mydb = get_db_connection()
    cursor = mydb.cursor(prepared=True)
    id = request.form.get('proizvod_id')
    naziv_proizvoda = request.form.get('naziv_proizvoda')
    opis = request.form.get('opis')
    materijal = request.form.get('materijal')
    mere = request.form.get('mere')
    cena = request.form.get('cena')
    kolicina = request.form.get('kolicina')
    proizvod_slika = None
    if 'proizvod_slika' in request.files and request.files['proizvod_slika'].filename != '':
        file = request.files['proizvod_slika']
        
        if file and allowed_file(file.filename):
            print(proizvod_slika)
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER_PROIZVODI'], filename)
            file.save(file_path)
            proizvod_slika = f"/src/assets/slike_proizvodi/{filename}"
            

            query = "UPDATE proizvodi SET naziv_proizvoda = %s, opis = %s, materijal = %s, mere = %s, cena = %s,kolicina = %s, proizvod_slika = %s WHERE proizvod_id = %s"
            params = (naziv_proizvoda, opis, materijal, mere, cena,kolicina, proizvod_slika, id)
            
        else:
            return jsonify({'error': 'Neispravan format slike'}), 400
    else:
        query = "UPDATE proizvodi SET naziv_proizvoda = %s, opis = %s, materijal = %s, mere = %s, cena = %s, kolicina = %s  WHERE proizvod_id = %s"
        params = (naziv_proizvoda, opis, materijal, mere, cena,kolicina, id)

    cursor.execute(query, params)
    mydb.commit()
    print(cursor.rowcount)
    cursor = mydb.cursor(dictionary=True)
    cursor.execute("SELECT * FROM proizvodi WHERE proizvod_id = %s", (id,))
    updated_user = cursor.fetchone()
    
    return jsonify({'message': 'Profil uspešno ažuriran', 'korisnik': updated_user})

@app.route('/dodaj_kolicinu', methods=['POST'])
def dodaj_kolicinu():
    try:
        data = request.json
        mydb = get_db_connection()
        cursor = mydb.cursor(dictionary=True)
        
        
        if 'kolicina' not in data or 'proizvod_id' not in data:
            return jsonify({'error': 'Nedostaju podaci o količini ili ID proizvoda'}), 400
        
        nova_kolicina = int(data['kolicina'])
        proizvod_id = int(data['proizvod_id'])
        
        
        cursor.execute('SELECT kolicina FROM proizvodi WHERE proizvod_id = %s', (proizvod_id,))
        result = cursor.fetchone()
        if result is None:
            return jsonify({'error': 'Proizvod nije pronađen'}), 404
        
        trenutna_kolicina = result['kolicina']
        ukupno = trenutna_kolicina + nova_kolicina
        
        
        cursor.execute('UPDATE proizvodi SET kolicina = %s WHERE proizvod_id = %s', (ukupno, proizvod_id))
        mydb.commit()
        
        return jsonify({'ukupno': ukupno}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        mydb.close()



@app.route('/dohvati_proizvod_po_idu/<id>')
def dohvati_proizvod_po_idu(id):
    mydb = get_db_connection()
    cursor = mydb.cursor(dictionary=True)
    query = "select * from proizvodi where proizvod_id = %s"
    cursor.execute(query, (id, ))
    rez = cursor.fetchone()
    
    return jsonify(rez)

@app.route('/dohvati_korisnika_po_idu/<id>')
def dohvati_korisnika_po_idu(id):
    mydb = get_db_connection()
    cursor = mydb.cursor(dictionary=True)
    query = "select * from korisnici where id = %s"
    cursor.execute(query, (id, ))
    rez = cursor.fetchone()
    
    return jsonify(rez)


@app.route('/register', methods=['POST'])
def register():
      data = request.json
      mydb = get_db_connection()
      cursor = mydb.cursor(prepared=True)
      id = 'NULL'
      username = data.get('username')
      email = data.get('email')
      password = data.get('password')
      godina_rodjenja = data.get('godina_rodjenja')
      trenutno_stanje_novca = data.get('trenutno_stanje_novca')
      vrsta_korisnika = data.get('vrsta_korisnika')
      params = (id, username, email, password, godina_rodjenja, trenutno_stanje_novca, vrsta_korisnika)
      query = "INSERT INTO korisnici (id, username, email, password, godina_rodjenja, trenutno_stanje_novca, vrsta_korisnika) VALUES (?, ?, ?, ?, ?, ?, ?)"
      cursor.execute(query, params)
      mydb.commit()
      return data  

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    session['korisnik'] = data
    return ""

@app.route('/ulogovan_korisnik')
def ulogovan_korisnik():
    if 'korisnik' in session:
        return jsonify(session['korisnik'])
    return ""





@app.route('/update_korisnika', methods=['PUT'])
def update_korisnika():
    mydb = get_db_connection()
    cursor = mydb.cursor(prepared=True)

    id = request.form.get('id')
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    godina_rodjenja = request.form.get('godina_rodjenja')
    trenutno_stanje_novca = request.form.get('trenutno_stanje_novca')
    vrsta_korisnika = request.form.get('vrsta_korisnika')
    if 'profilna_slika' in request.files and request.files['profilna_slika'].filename != '':
        file = request.files['profilna_slika']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            profilna_slika = f"/src/assets/slike_korisnici/{filename}"

            query = "UPDATE korisnici SET username = ?, email = ?, password = ?, godina_rodjenja = ?, trenutno_stanje_novca = ?, vrsta_korisnika = ?, profilna_slika = ? WHERE id = ?"
            params = (username, email, password, godina_rodjenja, trenutno_stanje_novca, vrsta_korisnika, profilna_slika, id)
        else:
            return jsonify({'error': 'Neispravan format slike'}), 400
    else:
        query = "UPDATE korisnici SET username = ?, email = ?, password = ?, godina_rodjenja = ?, trenutno_stanje_novca = ?, vrsta_korisnika = ? WHERE id = ?"
        params = (username, email, password, godina_rodjenja, trenutno_stanje_novca, vrsta_korisnika, id)

    cursor.execute(query, params)
    mydb.commit()
    cursor = mydb.cursor(dictionary=True)
    cursor.execute("SELECT * FROM korisnici WHERE id = %s", (id,))
    updated_user = cursor.fetchone()
    session['korisnik'] = updated_user

    return jsonify({'message': 'Profil uspešno ažuriran', 'korisnik': updated_user})


       

@app.route('/update_korisnika_admin/<id>', methods=['PUT'])
def update_korisnika_admin():
      data = request.json
      mydb = get_db_connection()
      cursor = mydb.cursor(prepared=True)
      id = data.get('id')
      username = data.get('username')
      email = data.get('email')
      password = data.get('password')
      godina_rodjenja = data.get('godina_rodjenja')
      trenutno_stanje_novca = data.get('trenutno_stanje_novca')
      vrsta_korisnika = data.get('vrsta_korisnika')
      params = (username, password, email, godina_rodjenja, trenutno_stanje_novca, vrsta_korisnika,id)
      query = "update korisnici set username=?,password=?, email=?, godina_rodjenja = ?, trenutno_stanje_novca = ?,vrsta_korisnika=? where id=%s"
      cursor.execute(query, params)
      mydb.commit()
      return data 

@app.route('/logout')
def logout():

    session.pop("korisnik",None)
    return ""


@app.route('/')
def index():
    return 'Hello world'


app.run(debug=True)
