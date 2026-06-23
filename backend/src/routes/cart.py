from flask import Blueprint, jsonify, request, session

from database import get_db_connection


cart_bp = Blueprint('cart', __name__)


@cart_bp.route('/cart/items', methods=['GET'])
def korpa():
    korisnik_id = session.get('korisnik', {}).get('id')
    if not korisnik_id:
        return jsonify({'error': 'Niste prijavljeni!'}), 401

    try:
        mydb = get_db_connection()
        cursor = mydb.cursor(dictionary=True)

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


@cart_bp.route('/cart/items/<int:proizvod_id>', methods=['POST'])
def dodaj_u_korpu(proizvod_id):
    korisnik_id = session.get('korisnik', {}).get('id')
    if not korisnik_id:
        return jsonify({'error': 'Niste prijavljeni!'})

    data = request.json
    kolicina = data.get('kolicina', 1)
    mydb = get_db_connection()
    cursor = mydb.cursor(prepared=True)

    query = 'INSERT INTO korpa (proizvod_id,korisnik_id,kolicina) VALUES (%s,%s,%s)'
    params = (proizvod_id, korisnik_id, kolicina)
    cursor.execute(query, params)
    mydb.commit()
    return jsonify(data)


@cart_bp.route('/cart/items/<int:proizvod_id>', methods=['PATCH'])
def update_cart(proizvod_id):
    korisnik_id = session.get('korisnik', {}).get('id')
    if not korisnik_id:
        return jsonify({'error': 'Niste prijavljeni'}), 401

    data = request.json
    try:
        nova_kolicina = int(data.get('kolicina'))
    except (TypeError, ValueError):
        return jsonify({'error': 'Neispravna kolicina'}), 400

    if nova_kolicina < 1:
        return jsonify({'error': 'Neispravna kolicina'}), 400

    try:
        mydb = get_db_connection()
        cursor = mydb.cursor(prepared=True)

        cursor.execute(
            "SELECT * FROM korpa WHERE korisnik_id = %s AND proizvod_id = %s",
            (korisnik_id, proizvod_id)
        )
        proizvod = cursor.fetchone()
        if not proizvod:
            return jsonify({'error': 'Proizvod nije pronadjen u korpi'}), 404

        cursor.execute(
            "UPDATE korpa SET kolicina = %s WHERE korisnik_id = %s AND proizvod_id = %s",
            (nova_kolicina, korisnik_id, proizvod_id)
        )
        mydb.commit()
        return jsonify({'message': 'Kolicina uspesno azurirana'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        mydb.close()


@cart_bp.route('/cart/items/<proizvod_id>', methods=['DELETE'])
def obrisi_iz_korpe(proizvod_id):
    korisnik_id = session.get('korisnik', {}).get('id')
    if not korisnik_id:
        return jsonify({'error': 'Niste prijavljeni!'}), 401

    mydb = get_db_connection()
    cursor = mydb.cursor(prepared=True)
    cursor.execute('DELETE FROM korpa WHERE korisnik_id = %s and proizvod_id = %s', (korisnik_id, proizvod_id))
    mydb.commit()
    return jsonify({'message': 'Proizvod uklonjen iz korpe!'})


@cart_bp.route('/cart/items/<int:korpa_id>/quantity', methods=['PATCH'])
def dodaj_kolicinu_korpe(korpa_id):
    try:
        data = request.json
        mydb = get_db_connection()
        cursor = mydb.cursor(dictionary=True)

        if 'kolicina' not in data:
            return jsonify({'error': 'Nedostaju podaci o kolicini ili ID proizvoda'}), 400

        nova_kolicina = int(data['kolicina'])

        cursor.execute('SELECT kolicina FROM korpa WHERE korpa_id = %s', (korpa_id,))
        result = cursor.fetchone()
        if result is None:
            return jsonify({'error': 'Proizvod nije pronadjen'}), 404

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
