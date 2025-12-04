# app/controllers/index.py

from flask import Blueprint, current_app, render_template, session, request, redirect, make_response, url_for
from app.models.scontro.ScontroDAO import ScontroDAO
from app.models.scontro.Scontro import Scontro
from app.models.torneo.TorneoDAO import TorneoDAO
from app.models.torneo.Torneo import Torneo
from app.models.squadra.SquadraDAO import SquadraDAO

# Creiamo un Blueprint dedicato alle rotte “pubbliche”
eliminascontro_bp = Blueprint('eliminascontro', __name__)

@eliminascontro_bp.route('/eliminascontro')
def home():

    if 'autenticato' not in session:
        return redirect('/richiedilogin?errore=1')
    
    
    scontro_id = request.args.get('scontro_id', type=int)
    

    scontro = Scontro()
    scontro.id = scontro_id

    successo = ScontroDAO.elimina(scontro)
            
    if successo:     
        return redirect('/privato?successo=1')
    else:
        return redirect('/privato?errore=1')
