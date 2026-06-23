from flask import Blueprint, jsonify, request

from database import get_db_connection


comments_bp = Blueprint('comments', __name__)


@comments_bp.route('/comments', methods=['GET'])
def svi_komentari():
    mydb = get_db_connection()
    cursor = mydb.cursor(dictionary=True)
    cursor.execute("select * from komentari")
    komentari = cursor.fetchall()
    return jsonify(komentari)


@comments_bp.route('/products/<proizvod_id>/comments', methods=['GET'])
def dohvati_komentare(proizvod_id):
    mydb = get_db_connection()
    cursor = mydb.cursor(dictionary=True)
    query = "SELECT komentari.*, korisnici.username FROM komentari JOIN korisnici ON komentari.korisnik_id = korisnici.id WHERE komentari.proizvod_id = %s"
    cursor.execute(query, (proizvod_id,))
    rez = cursor.fetchall()
    return jsonify(rez)


@comments_bp.route('/products/<proizvod_id>/comments', methods=['POST'])
def proizvodi_komentari(proizvod_id):
    data = request.json
    mydb = get_db_connection()
    cursor = mydb.cursor(prepared=True)
    korisnik_id = data['korisnik_id']
    tekst_komentara = data['tekst_komentara']

    query = "INSERT INTO komentari (tekst_komentara, proizvod_id, korisnik_id) VALUES (%s, %s, %s)"
    params = (tekst_komentara, proizvod_id, korisnik_id)
    cursor.execute(query, params)
    mydb.commit()
    return jsonify(data)


@comments_bp.route('/products/<proizvod_id>/comments/<komentar_id>', methods=['DELETE'])
def obrisi_komentar(proizvod_id, komentar_id):
    mydb = get_db_connection()
    cursor = mydb.cursor(prepared=True)
    cursor.execute("DELETE FROM komentari WHERE komentar_id = %s AND proizvod_id = %s", (komentar_id, proizvod_id))
    mydb.commit()
    return jsonify({'message': 'Komentar uspesno obrisan'})


@comments_bp.route('/comments/details', methods=['GET'])
def dohvati_sve_komentare_sa_detaljima():
    mydb = get_db_connection()
    cursor = mydb.cursor(dictionary=True)
    query = "SELECT komentari.*, korisnici.username, proizvodi.naziv FROM komentari JOIN korisnici ON komentari.korisnik_id = korisnici.id JOIN proizvodi ON komentari.proizvod_id = proizvodi.proizvod_id"
    cursor.execute(query)
    rez = cursor.fetchall()
    return jsonify(rez)


@comments_bp.route('/admin/comments', methods=['GET'])
def admin_dohvati_sve_komentare():
    mydb = get_db_connection()
    cursor = mydb.cursor(dictionary=True)
    query = "SELECT komentari.*, korisnici.username, proizvodi.naziv_proizvoda FROM komentari JOIN korisnici ON komentari.korisnik_id = korisnici.id join proizvodi on proizvodi.proizvod_id = komentari.proizvod_id"
    cursor.execute(query)
    rez = cursor.fetchall()
    return jsonify(rez)


@comments_bp.route('/admin/comments/<id>', methods=['DELETE'])
def admin_obrisi_komentar(id):
    mydb = get_db_connection()
    cursor = mydb.cursor(prepared=True)
    query = "DELETE FROM komentari WHERE komentar_id = %s"
    cursor.execute(query, (id,))
    mydb.commit()
    return jsonify({'message': 'Komentar uspesno obrisan'})
