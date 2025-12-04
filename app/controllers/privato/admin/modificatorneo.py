# app/controllers/index.py

from flask import Blueprint, current_app, render_template, session, request, redirect, make_response, url_for
from app.models.scontro.ScontroDAO import ScontroDAO
from app.models.torneo.TorneoDAO import TorneoDAO
from app.models.torneo.Torneo import Torneo
from app.models.squadra.SquadraDAO import SquadraDAO

# Creiamo un Blueprint dedicato alle rotte “pubbliche”
modificatorneo_bp = Blueprint('modificatorneo', __name__)

@modificatorneo_bp.route('/modificatorneo' , methods=['POST'])
def home():

    if 'autenticato' not in session:
        return redirect('/richiedilogin?errore=1')
    
    
    torneo_id = session.get('torneo_id')
    lista_nomiTornei = TorneoDAO.getNomi()
    errore = None
    nome_torneo = request.form.get('nome_torneo').strip()

    if nome_torneo in lista_nomiTornei:
        errore = "Il nome del torneo è già in uso."

    if errore:
        torneo = Torneo()

        return render_template('privato/admin/modifica_torneo.html', torneo=torneo, errore=errore, hide_navigation=True)

    torneo = Torneo()
    torneo.id = torneo_id
    torneo.nome = nome_torneo

    successo= TorneoDAO.modifica(torneo)
            
    if successo:    
        return redirect('/privato?successo=1')
    else:
        return redirect('/privato?errore=1')
