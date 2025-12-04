from flask import Blueprint, current_app, render_template, session, request, render_template_string
from app.models.scontro.ScontroDAO import ScontroDAO
from app.models.torneo.TorneoDAO import TorneoDAO
from app.models.squadra.SquadraDAO import SquadraDAO
from app.models.commento.CommentoDAO import CommentoDAO
import json

dettagliotorneo_bp = Blueprint('dettagliotorneo', __name__)

@dettagliotorneo_bp.route('/dettagliotorneo')
def home():
    sport_id = request.args.get('sportid', type=int) or session.get('sport_id')
    torneo_id = request.args.get('torneo_id', type=int) or session.get('torneo_id')

    torneo = None
    scontri = []
    ultimo_scontro = None
    nome1 = nome2 = logo1 = logo2 = ''
    scontri_con_immagini = []

    try:
        if torneo_id:
            torneo = TorneoDAO.getById(torneo_id)
            scontri = ScontroDAO.getAlleby_TorneoId(torneo_id) or []
            ultimo_scontro = ScontroDAO.getUltimoScontro(torneo_id)

        if ultimo_scontro:
            squadra1 = SquadraDAO.getbyId(ultimo_scontro.squadra1_id) if ultimo_scontro.squadra1_id else None
            squadra2 = SquadraDAO.getbyId(ultimo_scontro.squadra2_id) if ultimo_scontro.squadra2_id else None
            if squadra1:
                nome1 = squadra1.nome
                logo1 = squadra1.logo
            if squadra2:
                nome2 = squadra2.nome
                logo2 = squadra2.logo

        for s in scontri:
            t1 = SquadraDAO.getbyId(s.squadra1_id) if s.squadra1_id else None
            t2 = SquadraDAO.getbyId(s.squadra2_id) if s.squadra2_id else None

            count_commenti = CommentoDAO.getCount(s.id) or 0

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
                'numero_commenti': count_commenti
            })

    except Exception as e:
        current_app.logger.exception("Errore caricamento dettagli torneo")

    session['sport_id'] = sport_id
    session['torneo_id'] = torneo_id

    return render_template(
        'dettagliotorneo.html',
        torneo=torneo,
        ultimo_scontro=ultimo_scontro,
        img_squadra1_ultimo=logo1,
        img_squadra2_ultimo=logo2,
        nomeTeam1_ultimo=nome1,
        nomeTeam2_ultimo=nome2,
        scontri_con_immagini=scontri_con_immagini,
        hide_navigation=True
    )
