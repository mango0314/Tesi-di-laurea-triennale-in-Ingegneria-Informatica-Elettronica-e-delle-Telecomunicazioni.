# app/controllers/index.py

from flask import Blueprint, current_app, render_template, session, request
from app.models.giocatore.GiocatoreDAO import GiocatoreDAO
from app.models.squadra.SquadraDAO import SquadraDAO

# Creiamo un Blueprint dedicato alle rotte “pubbliche”
dettagliosquadra_bp = Blueprint('dettagliosquadra', __name__)

@dettagliosquadra_bp.route('/dettagliosquadra')
def home():
    
    
    squadra_id = request.args.get('squadra_id')
    
    squadra = SquadraDAO.getbyId(squadra_id)
    giocatori = GiocatoreDAO.getAllbyId(squadra_id)
    

            
        
    return render_template('dettagliosquadra.html', squadra= squadra, giocatori= giocatori, hide_navigation=True)
