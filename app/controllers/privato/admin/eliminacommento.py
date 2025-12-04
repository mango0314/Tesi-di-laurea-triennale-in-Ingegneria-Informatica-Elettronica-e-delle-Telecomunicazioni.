# app/controllers/index.py

from flask import Blueprint, current_app, render_template, session, request, redirect, make_response, url_for, jsonify
from app.models.commento.CommentoDAO import CommentoDAO
from app.models.commento.Commento import Commento

# Creiamo un Blueprint dedicato alle rotte “pubbliche”
eliminacommento_bp = Blueprint('eliminacommento', __name__)

@eliminacommento_bp.route('/eliminacommento', methods=['POST'])
def home():

    if 'autenticato' not in session:
        return redirect('/richiedilogin?errore=1')
    
    
    data = request.get_json(silent=True) or {}

    comment_id = data.get('comment_id')
    if not comment_id:
        return jsonify({'ok': False, 'error': 'comment_id mancante'}), 400
    
    commento = Commento()
    commento.id = comment_id

    try:
        CommentoDAO.elimina(commento)
                
        current_app.logger.info(f"L'admin ha eliminato commento {comment_id}")
        return jsonify({'ok': True})
    except Exception as e:
            current_app.logger.exception(f"Errore eliminazione commento id={comment_id}")
            return jsonify({'ok': False, 'error': 'errore interno'}), 50
