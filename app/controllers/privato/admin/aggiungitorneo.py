# app/controllers/index.py

from flask import Blueprint, current_app, render_template, session, request, redirect, make_response, url_for
from app.models.scontro.ScontroDAO import ScontroDAO
from app.models.torneo.TorneoDAO import TorneoDAO
from app.models.torneo.Torneo import Torneo
from app.models.sport.SportDAO import SportDAO

# Creiamo un Blueprint dedicato alle rotte “pubbliche”
aggiungitorneo_bp = Blueprint('aggiungitorneo', __name__)

@aggiungitorneo_bp.route('/aggiungitorneo' , methods=['POST'])
def home():

    if 'autenticato' not in session:
        return redirect('/richiedilogin?errore=1')
    
    
    
    lista_nomiTornei = TorneoDAO.getNomi()
    errore = None
    nome_torneo = request.form.get('nome_torneo').strip()
    sport_id = request.form.get('sport')
    logo = request.form.get('teamLogo')


    if nome_torneo in lista_nomiTornei:
        errore = "Il nome del torneo è già in uso."

    if errore:
        lista_sport = SportDAO.get_all()

        return render_template('privato/admin/modifica_torneo.html', lista_sport = lista_sport, errore=errore, hide_navigation=True)

    torneo = Torneo()
    
    torneo.nome = nome_torneo
    torneo.sport_id = sport_id
    torneo.logo = logo

    successo= TorneoDAO.salva(torneo)
            
        
    if successo :    
        return redirect('/privato?successo=1')
    else:
        return redirect('/privato?errore=1')
