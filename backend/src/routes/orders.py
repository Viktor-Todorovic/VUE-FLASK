from flask import Blueprint, jsonify, session

from database import get_db_connection


orders_bp = Blueprint('orders', __name__)


@orders_bp.route('/orders', methods=['POST'])
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
            return jsonify({'error': 'Vasa korpa je prazna!'}), 400

        ukupna_cena = sum([proizvod[5] for proizvod in proizvodi_u_korpi])

        cursor.execute("SELECT trenutno_stanje_novca FROM korisnici WHERE id = %s", (korisnik_id,))
        saldo_rez = cursor.fetchone()
        if not saldo_rez or saldo_rez[0] < ukupna_cena:
            return jsonify({'error': 'Nemate dovoljno novca za kupovinu!'}), 400

        for proizvod in proizvodi_u_korpi:
            kolicina_za_kupovinu = proizvod[1]
            dostupna_kolicina = proizvod[4]

            if kolicina_za_kupovinu > dostupna_kolicina:
                return jsonify({'error': f'Proizvoda nema dovoljno na stanju! Dostupno: {dostupna_kolicina}, a vi pokusavate da kupite {kolicina_za_kupovinu}.'}), 400

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

        return jsonify({'message': f'Kupovina uspesno zavrsena! Ukupno potroseno: {ukupna_cena} RSD'}), 200

    except Exception as e:
        mydb.rollback()
        return jsonify({'error': str(e)}), 500

    finally:
        cursor.close()
        mydb.close()
