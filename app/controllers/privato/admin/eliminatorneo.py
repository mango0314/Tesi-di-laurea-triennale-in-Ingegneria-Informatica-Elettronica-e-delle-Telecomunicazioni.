# app/controllers/index.py

from flask import Blueprint, current_app, render_template, session, request, redirect, make_response, url_for
from app.models.scontro.ScontroDAO import ScontroDAO
from app.models.torneo.TorneoDAO import TorneoDAO
from app.models.torneo.Torneo import Torneo
from app.models.squadra.SquadraDAO import SquadraDAO

# Creiamo un Blueprint dedicato alle rotte “pubbliche”
eliminatorneo_bp = Blueprint('eliminatorneo', __name__)

@eliminatorneo_bp.route('/eliminatorneo')
def home():

    if 'autenticato' not in session:
        return redirect('/richiedilogin?errore=1')
    
    
    torneo_id = request.args.get('torneo_id', type=int)
    

    torneo = Torneo()
    torneo.id = torneo_id

    successo= TorneoDAO.elimina(torneo)
            
    if successo:     
        return redirect('/privato?successo=1')
    else:
        return redirect('/privato?errore=1')
