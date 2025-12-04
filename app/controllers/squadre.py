# app/controllers/index.py

from flask import Blueprint, render_template, request, session, redirect
from app.models.torneo.TorneoDAO import TorneoDAO
from app.models.squadra.SquadraDAO import SquadraDAO

# Creiamo un Blueprint dedicato alle rotte “pubbliche”
squadre_bp = Blueprint('squadre', __name__)

@squadre_bp.route('/squadre')
def home():
    
    if 'torneo_id' not in session:
        return redirect('dettagliotorneo.html')
    
    torneo_id = session.get('torneo_id')
    torneo = TorneoDAO.getById(torneo_id)
    squadre = SquadraDAO.getAllby_torneo_id(torneo_id)
   
  
        
      
    return render_template('squadre.html', squadre=squadre, torneo=torneo, hide_navigation=True)
