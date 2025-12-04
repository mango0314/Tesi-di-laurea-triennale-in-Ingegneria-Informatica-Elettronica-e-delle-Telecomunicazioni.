# app/controllers/index.py

from flask import Blueprint, current_app, render_template, session, request, redirect, make_response, render_template_string
from app.models.scontro.ScontroDAO import ScontroDAO
from app.models.torneo.TorneoDAO import TorneoDAO
from app.models.squadra.SquadraDAO import SquadraDAO
from app.models.commento.CommentoDAO import CommentoDAO
import json

# Creiamo un Blueprint dedicato alle rotte “pubbliche”
dettagliotorneo_admin_bp = Blueprint('dettagliotorneo_admin', __name__)

@dettagliotorneo_admin_bp.route('/dettagliotorneo_admin')
def home():

    if 'autenticato' not in session:
        return redirect('/richiedilogin?errore=1')
    
    sport_id = request.args.get('sportid', type=int)
    torneo_id = request.args.get('torneo_id', type=int)
    
    torneo = TorneoDAO.getById(torneo_id)
    scontri = ScontroDAO.getAlleby_TorneoId(torneo_id)
    ultimo_scontro = ScontroDAO.getUltimoScontro(torneo_id)
    nome1, nome2 = '', ''
    logo1, logo2 = '', ''
    scontri_con_immagini = []
    commenti = {} 

    if ultimo_scontro:
        # Chiamo il DAO una volta per ciascuna squadra
        squadra1 = SquadraDAO.getbyId(ultimo_scontro.squadra1_id) if ultimo_scontro.squadra1_id else None
        squadra2 = SquadraDAO.getbyId(ultimo_scontro.squadra2_id) if ultimo_scontro.squadra2_id else None
        current_app.logger.warning(f"Squadra con id {ultimo_scontro.squadra2_id} trovata: {squadra2}")

        # Solo se il DAO ha restituito un oggetto Squadra valido
        if squadra1:
            nome1 = squadra1.nome
            logo1 = squadra1.logo
        if squadra2:
            nome2 = squadra2.nome
            logo2 = squadra2.logo

        if not squadra1:
            current_app.logger.warning(f"Squadra con id {ultimo_scontro.squadra1_id} non trovata")



    for s in scontri:
            t1 = SquadraDAO.getbyId(s.squadra1_id) if s.squadra1_id else None
            t2 = SquadraDAO.getbyId(s.squadra2_id) if s.squadra2_id else None
            commenti_per_scontro = CommentoDAO.getAllby_Scontro(s.id) or []
            count_commenti = CommentoDAO.getCount(s.id) or None


            scontri_con_immagini.append({
                'scontro': s,
                'id': s.id,
                'squadra1_id': s.squadra1_id,
                'squadra2_id': s.squadra2_id,
                'nome_team1': t1.nome if t1 else '',
                'nome_team2': t2.nome if t2 else '',
                'img_squadra1': t1.logo if t1 else '',
                'img_squadra2': t2.logo if t2 else '',
                'punteggio1': s.punteggio1,
                'punteggio2': s.punteggio2,
                'data': s.data,
                'orario': s.orario,
                'numero_commenti': count_commenti,
                
            })


  
    
    session['sport_id'] = sport_id  # Salva lo sport_id nella sessione
    print(f"Sport ID salvato nella sessione: {sport_id}")
    session['torneo_id'] = torneo_id
            
        
    return render_template('privato/admin/dettagliotorneo_admin.html', torneo=torneo, ultimo_scontro=ultimo_scontro, img_squadra1_ultimo=logo1, img_squadra2_ultimo = logo2, nomeTeam1_ultimo=nome1, nomeTeam2_ultimo=nome2, 
                           scontri_con_immagini = scontri_con_immagini, hide_navigation=True, manual=True)
