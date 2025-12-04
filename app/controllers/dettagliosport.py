# app/controllers/index.py

from flask import Blueprint, render_template, request
from app.models.torneo.TorneoDAO import TorneoDAO

# Creiamo un Blueprint dedicato alle rotte “pubbliche”
dettagliosport_bp = Blueprint('dettagliosport', __name__)

@dettagliosport_bp.route('/dettagliosport')
def home():
    
    sport_id = request.args.get('sport_id', type=int)
    tornei = TorneoDAO.getAll_bySportid(sport_id)
   
  
        
      
    return render_template('dettagliosport.html', tornei=tornei, sport_id=sport_id)
