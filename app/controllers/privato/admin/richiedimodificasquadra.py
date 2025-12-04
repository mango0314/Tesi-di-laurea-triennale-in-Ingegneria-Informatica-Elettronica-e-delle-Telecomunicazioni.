# app/controllers/index.py

from flask import Blueprint, current_app, render_template, session, request, redirect, make_response
from app.models.scontro.ScontroDAO import ScontroDAO
from app.models.giocatore.GiocatoreDAO import GiocatoreDAO
from app.models.squadra.SquadraDAO import SquadraDAO

# Creiamo un Blueprint dedicato alle rotte “pubbliche”
richiedimodificasquadra_bp = Blueprint('richiedimodificasquadra', __name__)

@richiedimodificasquadra_bp.route('/richiedimodificasquadra')
def home():

    if 'autenticato' not in session:
        return redirect('/richiedilogin?errore=1')
    
    
    squadra_id = request.args.get('squadra_id', type= int)
    
    squadra = SquadraDAO.getbyId(squadra_id)

    lista_giocatorisquadra = GiocatoreDAO.getAllbyId(squadra_id)

            
        
    return render_template('privato/admin/modifica_squadra.html', squadra=squadra, lista_giocatorisquadra = lista_giocatorisquadra, hide_navigation=True)
