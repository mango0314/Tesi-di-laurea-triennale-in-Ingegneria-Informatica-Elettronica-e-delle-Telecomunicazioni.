# app/controllers/index.py

from flask import Blueprint, current_app, render_template, session, request, redirect, make_response
from app.models.scontro.ScontroDAO import ScontroDAO
from app.models.scontro.Scontro import Scontro
from app.models.squadra.SquadraDAO import SquadraDAO

# Creiamo un Blueprint dedicato alle rotte “pubbliche”
richiediaggiungiscontro_bp = Blueprint('richiediaggiungiscontro', __name__)

@richiediaggiungiscontro_bp.route('/richiediaggiungiscontro')
def home():

    if 'autenticato' not in session:
        return redirect('/richiedilogin?errore=1')
    
    
    
    torneo_id = request.args.get('torneo_id', type=int)
    
    scontro = Scontro()
    scontro = None
    lista_squadretorneo = SquadraDAO.getAllby_torneo_id(torneo_id)

    
            
        
    return render_template('privato/admin/modifica_scontro.html', scontro=scontro,lista_squadretorneo= lista_squadretorneo, hide_navigation=True)
