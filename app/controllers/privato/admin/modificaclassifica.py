# app/controllers/index.py

from flask import Blueprint, current_app, render_template, session, request, redirect, make_response, url_for, abort
from app.models.scontro.ScontroDAO import ScontroDAO
from app.models.classifica.ClassificaDAO import ClassificaDAO
from app.models.torneo.TorneoDAO import TorneoDAO
from app.models.scontro.Scontro import Scontro  
from app.models.squadra.SquadraDAO import SquadraDAO
from app.models.sport.SportDAO import SportDAO
from datetime import datetime, date, timedelta
import re

# Creiamo un Blueprint dedicato alle rotte “pubbliche”
modificaclassifica_bp = Blueprint('modificaclassifica', __name__)

@modificaclassifica_bp.route('/modificaclassifica' , methods=['POST'])
def home():


     # ——— DEBUG: dump completo del form ———
    current_app.logger.debug("FORM KEYS:   %r", request.form.keys())
    current_app.logger.debug("FORM VALUES: %r", request.form.to_dict(flat=False))

    if 'autenticato' not in session:
        return redirect('/richiedilogin?errore=1')
    
    id_squadra_list = request.form.getlist('id_squadra')
    print(f"{id_squadra_list}")
    bonus_list = request.form.getlist('bonus')

    if not id_squadra_list or not bonus_list or len(id_squadra_list) != len(bonus_list):
        abort(400, "Parametri id_squadra e bonus mancanti o di lunghezza diversa")

    torneo_id = session.get("torneo_id")
    if not torneo_id:
        abort(400, "Torneo non specificato nella sessione")

    try:
        for i in range(len(id_squadra_list)):
            id_param = id_squadra_list[i]  
            bonus_param = bonus_list[i]    


            squadra_id = int(id_param)
            bonus = int(bonus_param)

            ClassificaDAO.updateBonus(squadra_id, torneo_id, bonus)

        return redirect(url_for('privato.home', successo=True))

    except Exception as e:
        print(f"Errore durante l'aggiornamento della classifica: {e}")
        abort(500, "Si è verificato un errore inaspettato durante l'aggiornamento della classifica.")