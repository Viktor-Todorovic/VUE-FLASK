from flask import Blueprint, jsonify, request, session


sessions_bp = Blueprint('sessions', __name__)


@sessions_bp.route('/sessions', methods=['POST'])
def login():
    data = request.json
    session['korisnik'] = data
    return ""


@sessions_bp.route('/session', methods=['GET'])
def ulogovan_korisnik():
    if 'korisnik' in session:
        return jsonify(session['korisnik'])
    return ""


@sessions_bp.route('/session', methods=['DELETE'])
def logout():
    session.pop("korisnik", None)
    return ""
