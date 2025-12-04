# app/controllers/index.py

from flask import Blueprint, current_app, render_template, session, request, redirect, make_response
from app.models.scontro.ScontroDAO import ScontroDAO
from app.models.torneo.TorneoDAO import TorneoDAO
from app.models.squadra.SquadraDAO import SquadraDAO

# Creiamo un Blueprint dedicato alle rotte “pubbliche”
squadreadmin_bp = Blueprint('squadreadmin', __name__)

@squadreadmin_bp.route('/squadreadmin')
def home():

    if 'autenticato' not in session:
        return redirect('/richiedilogin?errore=1')
    
    
    torneo_id = session.get('torneo_id')

    torneo = TorneoDAO.getById(torneo_id)
    squadre = SquadraDAO.getAllby_torneo_id(torneo_id)
    
    
    ruolo = session.get('ruolo')
            
        
    return render_template('privato/admin/squadre_torneo_admin.html', torneo=torneo, ruolo=ruolo, squadre= squadre, hide_navigation=True, manual = True)
