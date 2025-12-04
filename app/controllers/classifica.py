# app/controllers/index.py

from flask import Blueprint, current_app, render_template, session, request,redirect
from app.models.scontro.ScontroDAO import ScontroDAO
from app.models.torneo.TorneoDAO import TorneoDAO
from app.models.squadra.SquadraDAO import SquadraDAO
from app.models.classifica.ClassificaDAO import ClassificaDAO

# Creiamo un Blueprint dedicato alle rotte “pubbliche”
classifica_bp = Blueprint('classifica', __name__)

@classifica_bp.route('/classifica')
def home():

    if 'sport_id' not in session or 'torneo_id' not in session:
        return redirect('dettagliotorneo.html')
                        
    torneo_id = session.get('torneo_id')
    sport_id = session.get('sport_id')
    
   
    
    torneo = TorneoDAO.getById(torneo_id)
    classifica = ClassificaDAO.getAllby_torneo_id(torneo_id)
    classifica.sort(key=lambda c: c.get_punteggio_totale(), reverse=True)
    classifica_con_immagini = []
    for c in classifica:
        squadra = SquadraDAO.getbyId(c.id_squadra)
        if squadra:
            classifica_con_immagini.append({
                'id_squadra': c.id_squadra,
                'nome': squadra.nome,
                'logo': squadra.logo,
                'punteggio_totale': c.get_punteggio_totale(),
                'vittorie': c.vittorie,
                'pareggi': c.pareggi,
                'sconfitte': c.sconfitte
            })
   
            
        
    return render_template('classifica.html', torneo=torneo, classifica= classifica_con_immagini, sport_id= sport_id, hide_navigation=True)
