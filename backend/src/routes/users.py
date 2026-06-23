import os

from flask import Blueprint, current_app, jsonify, request, session
from werkzeug.utils import secure_filename

from database import get_db_connection
from utils import allowed_file


users_bp = Blueprint('users', __name__)


@users_bp.route('/users', methods=['GET'])
def svi_korisnici():
    mydb = get_db_connection()
    cursor = mydb.cursor(dictionary=True)
    cursor.execute("select * from korisnici")
    korisnici = cursor.fetchall()
    return jsonify(korisnici)


@users_bp.route('/users/<id>', methods=['GET'])
def dohvati_korisnika_po_idu(id):
    mydb = get_db_connection()
    cursor = mydb.cursor(dictionary=True)
    query = "select * from korisnici where id = %s"
    cursor.execute(query, (id,))
    rez = cursor.fetchone()
    return jsonify(rez)


@users_bp.route('/users', methods=['POST'])
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


@users_bp.route('/users/<id>', methods=['DELETE'])
def obrisi_korisnika(id):
    mydb = get_db_connection()
    cursor = mydb.cursor(prepared=True)
    query = "delete from korisnici where id =%s"
    cursor.execute(query, (id,))
    mydb.commit()
    return ""


@users_bp.route('/users/me', methods=['PUT'])
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
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
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

    return jsonify({'message': 'Profil uspesno azuriran', 'korisnik': updated_user})


@users_bp.route('/admin/users/<id>', methods=['PUT'])
def update_korisnika_admin(id):
    data = request.json
    mydb = get_db_connection()
    cursor = mydb.cursor(prepared=True)
    id = data.get('id', id)
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    godina_rodjenja = data.get('godina_rodjenja')
    trenutno_stanje_novca = data.get('trenutno_stanje_novca')
    vrsta_korisnika = data.get('vrsta_korisnika')
    params = (username, password, email, godina_rodjenja, trenutno_stanje_novca, vrsta_korisnika, id)
    query = "update korisnici set username=?,password=?, email=?, godina_rodjenja = ?, trenutno_stanje_novca = ?,vrsta_korisnika=? where id=%s"
    cursor.execute(query, params)
    mydb.commit()
    return data


@users_bp.route('/users/me/purchases', methods=['GET'])
def dohvati_kupljene_proizvode():
    korisnik_id = session.get('korisnik', {}).get('id')
    if not korisnik_id:
        return jsonify({'error': 'Niste prijavljeni!'}), 401

    mydb = get_db_connection()
    cursor = mydb.cursor(dictionary=True)
    query = "SELECT istorija_kupovina.*,istorija_kupovina.korisnik_id,istorija_kupovina.proizvod_id,proizvodi.naziv_proizvoda  FROM istorija_kupovina join proizvodi on proizvodi.proizvod_id = istorija_kupovina.proizvod_id join korisnici on korisnici.id = istorija_kupovina.korisnik_id WHERE istorija_kupovina.korisnik_id = %s"
    cursor.execute(query, (korisnik_id,))
    rez = cursor.fetchall()
    return jsonify(rez)


@users_bp.route('/users/<int:user_id>/profile-image', methods=['POST'])
def upload_profilna_slika(user_id):
    if 'profilna_slika' not in request.files:
        return jsonify({'error': 'Nema fajla ili ID korisnika nije prosledjen'}), 400

    file = request.files['profilna_slika']

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        relative_path = f"/src/assets/slike_korisnici/{filename}"

        file.save(file_path)
        try:
            mydb = get_db_connection()
            cursor = mydb.cursor(prepared=True)
            query = "UPDATE korisnici SET profilna_slika = ? WHERE id = ?"
            cursor.execute(query, (relative_path, user_id))
            mydb.commit()

            return jsonify({
                'message': 'Slika uspesno sacuvana',
                'image_path': relative_path
            })
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    return jsonify({'error': 'Nedozvoljen format fajla'}), 400
