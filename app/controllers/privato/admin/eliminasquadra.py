# app/controllers/index.py

from flask import Blueprint, current_app, render_template, session, request, redirect, make_response, url_for
from app.models.scontro.ScontroDAO import ScontroDAO
from app.models.torneo.TorneoDAO import TorneoDAO
from app.models.squadra.Squadra import Squadra
from app.models.squadra.SquadraDAO import SquadraDAO

# Creiamo un Blueprint dedicato alle rotte “pubbliche”
eliminasquadra_bp = Blueprint('eliminasquadra', __name__)

@eliminasquadra_bp.route('/eliminasquadra')
def home():

    if 'autenticato' not in session:
        return redirect('/richiedilogin?errore=1')
    
    
    squadra_id = request.args.get('squadra_id', type=int)
    

    squadra = Squadra()
    squadra.id = squadra_id

    successo= SquadraDAO.elimina(squadra)
            
    if successo:     
        return redirect('/privato?successo=1')
    else:
        return redirect('/privato?errore=1')
