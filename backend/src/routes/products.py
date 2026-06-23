import os

from flask import Blueprint, current_app, jsonify, request, session
from werkzeug.utils import secure_filename

from database import get_db_connection
from utils import allowed_file


products_bp = Blueprint('products', __name__)


@products_bp.route('/products', methods=['GET'])
def svi_proizvodi():
    mydb = get_db_connection()
    cursor = mydb.cursor(dictionary=True)
    cursor.execute("select * from proizvodi join korisnici on korisnici.id = proizvodi.korisnik_id")
    proizvodi = cursor.fetchall()
    return jsonify(proizvodi)


@products_bp.route('/products/<id>', methods=['GET'])
def dohvati_proizvod_po_idu(id):
    mydb = get_db_connection()
    cursor = mydb.cursor(dictionary=True)
    query = "select * from proizvodi where proizvod_id = %s"
    cursor.execute(query, (id,))
    rez = cursor.fetchone()
    return jsonify(rez)


@products_bp.route('/products', methods=['POST'])
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
            filename = secure_filename(file.filename)
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER_PROIZVODI'], filename)
            file.save(file_path)
            proizvod_slika = f"/src/assets/slike_proizvodi/{filename}"

            query = "INSERT INTO proizvodi (proizvod_id, korisnik_id,naziv_proizvoda,opis,materijal,mere,cena,kolicina,proizvod_slika) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
            params = (proizvod_id, korisnik_id, naziv_proizvoda, opis, materijal, mere, cena, kolicina, proizvod_slika)
        else:
            return jsonify({'error': 'Neispravan format slike'}), 400
    else:
        query = "INSERT INTO proizvodi (proizvod_id, korisnik_id,naziv_proizvoda,opis,materijal,mere,cena,kolicina) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
        params = (proizvod_id, korisnik_id, naziv_proizvoda, opis, materijal, mere, cena, kolicina)

    cursor.execute(query, params)
    mydb.commit()
    cursor = mydb.cursor(dictionary=True)
    updated_user = cursor.fetchone()

    return jsonify({'message': 'Proizvod uspesno dodat', 'korisnik': updated_user})


@products_bp.route('/products/<id>', methods=['PUT'])
def update_proizvoda(id):
    mydb = get_db_connection()
    cursor = mydb.cursor(prepared=True)
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
            filename = secure_filename(file.filename)
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER_PROIZVODI'], filename)
            file.save(file_path)
            proizvod_slika = f"/src/assets/slike_proizvodi/{filename}"

            query = "UPDATE proizvodi SET naziv_proizvoda = %s, opis = %s, materijal = %s, mere = %s, cena = %s,kolicina = %s, proizvod_slika = %s WHERE proizvod_id = %s"
            params = (naziv_proizvoda, opis, materijal, mere, cena, kolicina, proizvod_slika, id)
        else:
            return jsonify({'error': 'Neispravan format slike'}), 400
    else:
        query = "UPDATE proizvodi SET naziv_proizvoda = %s, opis = %s, materijal = %s, mere = %s, cena = %s, kolicina = %s  WHERE proizvod_id = %s"
        params = (naziv_proizvoda, opis, materijal, mere, cena, kolicina, id)

    cursor.execute(query, params)
    mydb.commit()
    cursor = mydb.cursor(dictionary=True)
    cursor.execute("SELECT * FROM proizvodi WHERE proizvod_id = %s", (id,))
    updated_user = cursor.fetchone()

    return jsonify({'message': 'Proizvod uspesno azuriran', 'korisnik': updated_user})


@products_bp.route('/products/<id>', methods=['DELETE'])
def obrisi_proizvod(id):
    mydb = get_db_connection()
    cursor = mydb.cursor(prepared=True)
    query = "delete from proizvodi where proizvod_id =%s"
    cursor.execute(query, (id,))
    mydb.commit()
    return ""


@products_bp.route('/products/<int:proizvod_id>/quantity', methods=['PATCH'])
def dodaj_kolicinu(proizvod_id):
    try:
        data = request.json
        mydb = get_db_connection()
        cursor = mydb.cursor(dictionary=True)

        if 'kolicina' not in data:
            return jsonify({'error': 'Nedostaju podaci o kolicini ili ID proizvoda'}), 400

        nova_kolicina = int(data['kolicina'])

        cursor.execute('SELECT kolicina FROM proizvodi WHERE proizvod_id = %s', (proizvod_id,))
        result = cursor.fetchone()
        if result is None:
            return jsonify({'error': 'Proizvod nije pronadjen'}), 404

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


@products_bp.route('/products/<int:proizvod_id>/image', methods=['POST'])
def upload_proizvod_slika(proizvod_id):
    if 'proizvod_slika' not in request.files:
        return jsonify({'error': 'Nema fajla ili ID proizvoda nije prosledjen'}), 400

    file = request.files['proizvod_slika']

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER_PROIZVODI'], filename)
        relative_path = f"/src/assets/slike_proizvodi/{filename}"

        file.save(file_path)
        try:
            mydb = get_db_connection()
            cursor = mydb.cursor(prepared=True)
            query = "UPDATE proizvodi SET proizvod_slika = ? WHERE proizvod_id = ?"
            cursor.execute(query, (relative_path, proizvod_id))
            mydb.commit()

            return jsonify({
                'message': 'Slika uspesno sacuvana',
                'image_path': relative_path
            })
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    return jsonify({'error': 'Nedozvoljen format fajla'}), 400
