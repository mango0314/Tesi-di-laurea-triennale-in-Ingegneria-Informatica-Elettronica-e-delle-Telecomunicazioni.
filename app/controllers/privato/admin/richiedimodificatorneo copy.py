# app/controllers/index.py

from flask import Blueprint, current_app, render_template, session, request, redirect, make_response
from app.models.scontro.ScontroDAO import ScontroDAO
from app.models.torneo.TorneoDAO import TorneoDAO
from app.models.squadra.SquadraDAO import SquadraDAO

# Creiamo un Blueprint dedicato alle rotte “pubbliche”
richiedimodificatorneo_bp = Blueprint('richiedimodificatorneo', __name__)

@richiedimodificatorneo_bp.route('/richiedimodificatorneo')
def home():

    if 'autenticato' not in session:
        return redirect('/richiedilogin?errore=1')
    
    
    torneo_id = request.args.get('torneo_id', type= int)
    
    torneo = TorneoDAO.getById(torneo_id)

    session['torneo_id'] = torneo_id
            
        
    return render_template('privato/admin/modifica_torneo.html', torneo=torneo, hide_navigation=True)
