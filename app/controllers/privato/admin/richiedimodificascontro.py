# app/controllers/index.py

from flask import Blueprint, current_app, render_template, session, request, redirect, make_response
from app.models.scontro.ScontroDAO import ScontroDAO
from app.models.torneo.TorneoDAO import TorneoDAO
from app.models.squadra.SquadraDAO import SquadraDAO

# Creiamo un Blueprint dedicato alle rotte “pubbliche”
richiedimodificascontro_bp = Blueprint('richiedimodificascontro', __name__)

@richiedimodificascontro_bp.route('/richiedimodificascontro')
def home():

    if 'autenticato' not in session:
        return redirect('/richiedilogin?errore=1')
    
    
    scontro_id = request.args.get('scontro_id', type=int)
    print(f"ID scontro ricevuto: {scontro_id}")
    torneo_id = request.args.get('torneo_id', type=int)
    print(f"ID torneo ricevuto: {torneo_id}")
    
    scontro = ScontroDAO.getById(scontro_id)
    print(f"la data dello scontro è: {scontro.data if scontro else 'Nessuno scontro trovato'}")
    lista_squadretorneo = SquadraDAO.getAllby_torneo_id(torneo_id)

    

    
            
        
    return render_template('privato/admin/modifica_scontro.html', scontro=scontro,  lista_squadretorneo= lista_squadretorneo, hide_navigation=True)
