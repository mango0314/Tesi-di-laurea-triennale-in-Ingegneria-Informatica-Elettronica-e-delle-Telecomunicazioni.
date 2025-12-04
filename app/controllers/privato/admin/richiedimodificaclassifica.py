# app/controllers/index.py

from flask import Blueprint, current_app, render_template, session, request, redirect, make_response
from app.models.scontro.ScontroDAO import ScontroDAO
from app.models.torneo.TorneoDAO import TorneoDAO
from app.models.squadra.SquadraDAO import SquadraDAO
from app.models.classifica.ClassificaDAO import ClassificaDAO

# Creiamo un Blueprint dedicato alle rotte “pubbliche”
richiedimodificaclassifica_bp = Blueprint('richiedimodificaclassifica', __name__)

@richiedimodificaclassifica_bp.route('/richiedimodificaclassifica')
def home():

    if 'autenticato' not in session:
        return redirect('/richiedilogin?errore=1')

    torneo_id = request.args.get('torneo_id', type=int)
    print(f"ID torneo ricevuto: {torneo_id}")
    sport_id = request.args.get('sport_id', type=int)
    classifica = ClassificaDAO.getAllby_torneo_id(torneo_id)

    classifica.sort(key=lambda c: c.get_punteggio_totale(), reverse=True)
    
    session['torneo_id'] = torneo_id
    session['sport_id'] = sport_id

    if classifica:
         lista_classifica_conimmagini = []
         for c in classifica:
               print(f"ID SQUADRA: {c.id_squadra}")
               s = SquadraDAO.getbyId(c.id_squadra)

               lista_classifica_conimmagini.append({
                    'id_squadra': c.id_squadra,
                    'nome': s.nome if s else '',
                    'logo': s.logo if s else '',
                    'punteggio': c.punteggio,
                    'torneo_id': c.id_torneo,
                    'vittorie': c.vittorie,
                    'pareggi': c.pareggi,
                    'sconfitte': c.sconfitte,
                    'media': c.media,
                    'bonus': c.bonus
               })

               print(f"ecco gli sqaudra_id pirma di mandarli al form. {lista_classifica_conimmagini[-1]['id_squadra']}")
            
    
    
            
        
    return render_template('privato/admin/modifica_classifica.html', classifica = lista_classifica_conimmagini, hide_navigation=True)
