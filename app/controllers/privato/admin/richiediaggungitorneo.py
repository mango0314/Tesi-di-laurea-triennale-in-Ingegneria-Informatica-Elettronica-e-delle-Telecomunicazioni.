# app/controllers/index.py

from flask import Blueprint, current_app, render_template, session, request, redirect, make_response
from app.models.sport.SportDAO import SportDAO
from app.models.torneo.Torneo import Torneo


# Creiamo un Blueprint dedicato alle rotte “pubbliche”
richiediaggiungitorneo_bp = Blueprint('richiediaggiungitorneo', __name__)

@richiediaggiungitorneo_bp.route('/richiediaggiungitorneo')
def home():

    if 'autenticato' not in session:
        return redirect('/richiedilogin?errore=1')
    
    
    torneo = Torneo()
    torneo = None
    lista_sport = SportDAO.get_all()
            
        
    return render_template('privato/admin/modifica_torneo.html', torneo=torneo, lista_sport= lista_sport, hide_navigation=True)
