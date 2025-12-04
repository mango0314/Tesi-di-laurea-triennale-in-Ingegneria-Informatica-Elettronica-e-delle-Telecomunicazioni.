# app/controllers/index.py

from flask import Blueprint, render_template, session, redirect, make_response
from app.models.squadra.SquadraDAO import SquadraDAO
from app.models.giocatore.GiocatoreDAO import GiocatoreDAO
from app.models.torneo.TorneoDAO import TorneoDAO

# Creiamo un Blueprint dedicato alle rotte “pubbliche”
privato_bp = Blueprint('privato', __name__)

@privato_bp.route('/privato')
def home():
   
   if 'autenticato' not in session:
        return redirect('/richiedilogin?errore=1')
   
   ruolo = session.get('ruolo')
   username = session.get('username')
   squadra_id = session.get('squadra_id')
   

   squadra = SquadraDAO.getbyId(squadra_id)
   giocatori = GiocatoreDAO.getAllbyId(squadra_id)
   lista_tuttitornei = TorneoDAO.getAll()

   
        
      
    # Impedisce la cache delle pagine private
   response = make_response(render_template(
        'privato/index_privato.html',
        giocatori=giocatori,
        squadra=squadra,
        ruolo=ruolo,
        username = username,
        lista_tuttitornei=lista_tuttitornei,
        hide_navigation=True
    ))
   response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
   response.headers['Pragma'] = 'no-cache'
   response.headers['Expires'] = '0'
   return response
