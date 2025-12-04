# app/controllers/index.py

from flask import Blueprint, current_app, render_template, session, request, redirect
from app.models.giocatore.GiocatoreDAO import GiocatoreDAO
from app.models.squadra.SquadraDAO import SquadraDAO

# Creiamo un Blueprint dedicato alle rotte “pubbliche”
dettagliosquadra_privato_bp = Blueprint('dettagliosquadra_privato', __name__)

@dettagliosquadra_privato_bp.route('/dettagliosquadra_privato')
def home():
    
    if 'autenticato' not in session:
        return redirect('/richiedilogin?errore=1')
    
    squadra_id = request.args.get('squadra_id')
    
    squadra = SquadraDAO.getbyId(squadra_id)
    giocatori = GiocatoreDAO.getAllbyId(squadra_id)

    ruolo = session.get('ruolo')
    

            
        
    return render_template('privato/utente/dettagliosquadra_privato.html', ruolo= ruolo, squadra= squadra, giocatori= giocatori, hide_navigation=True)
