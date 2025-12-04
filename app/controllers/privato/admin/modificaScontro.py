# app/controllers/index.py

from flask import Blueprint, current_app, render_template, session, request, redirect, make_response, url_for
from app.models.scontro.ScontroDAO import ScontroDAO
from app.models.torneo.TorneoDAO import TorneoDAO
from app.models.scontro.Scontro import Scontro  
from app.models.squadra.SquadraDAO import SquadraDAO
from app.models.sport.SportDAO import SportDAO
from datetime import datetime, date, timedelta

# Creiamo un Blueprint dedicato alle rotte “pubbliche”
modificaScontro_bp = Blueprint('modificaScontro', __name__)

@modificaScontro_bp.route('/modificaScontro' , methods=['POST'])
def home():

    if 'autenticato' not in session:
        return redirect('/richiedilogin?errore=1')
    
    errori = []
    torneo_id = session.get('torneo_id')
    sport_idtorneo = session.get('sport_id')
    print(f"Sport ID torneo: {sport_idtorneo}")
    lista_scontritorneo = ScontroDAO.getAlleby_TorneoId(torneo_id)
    scontro_id = request.form.get('scontro_id', type=int)
    idSquadra1 = request.form.get('squadra1id', type=int)
    idSquadra2 = request.form.get('squadra2id', type=int)
    if (idSquadra1 == idSquadra2):
        errori.append("Non si possono scontrare due squadre identiche.")

    punteggio1_param = request.form.get('punteggio1', '').strip()
    punteggio2_param = request.form.get('punteggio2', '').strip()

    punteggio1 = None
    punteggio2 = None

    # Provo a convertirli in interi, segnalando errori se non validi
    if punteggio1_param:
        try:
            punteggio1 = int(punteggio1_param)
        except ValueError:
            errori.append("Punteggio 1 non è un numero valido.")

    if punteggio2_param:
        try:
            punteggio2 = int(punteggio2_param)
        except ValueError:
            errori.append("Punteggio 2 non è un numero valido.")

    if ( punteggio1 is not None and punteggio2 is not None):
        if(sport_idtorneo == 3 and punteggio1 != 3 and punteggio2 != 3):
            errori.append("Nella pallavolo si vince a 3 set.")

        if( sport_idtorneo == 2 or sport_idtorneo==3):
            if(punteggio1 == punteggio2):
                errori.append("Non è possibile il pareggio in questo sport.")

        if(punteggio1 < 0 or punteggio2 < 0):
            errori.append("I punteggi non possono essere negativi.")
         
        
    scontro = Scontro()
    scontro.id = scontro_id
    scontro.torneo_id = torneo_id
    scontro.squadra1_id = idSquadra1
    scontro.squadra2_id = idSquadra2
    scontro.punteggio1 = punteggio1
    scontro.punteggio2 = punteggio2

    # data (HTML5 date manda sempre ISO)
    try:
        data_obj = date.fromisoformat(request.form.get('data'))
        scontro.data = data_obj
    except (KeyError, ValueError):
        errori.append("Formato data non valido")

    # orario (se HTML5 time manda HH:mm:ss o HH:mm)
    orario_str = request.form.get('orario')
    try:
        # .fromisoformat non esiste per time; se finisce in %H:%M:%S fallback a %H:%M
        parsed = datetime.fromisoformat(f"1970-01-01T{orario_str}")
        orario_obj = parsed.time()
        scontro.orario = orario_obj
    except ValueError:
        errori.append("Formato orario non valido") 

    if scontro in lista_scontritorneo:
        errori.append("Scontro già esistente.")
    
    for s in lista_scontritorneo:
        stesse_squadre = (
            (scontro.squadra1_id == s.squadra1_id and scontro.squadra2_id == s.squadra2_id)
            or
            (scontro.squadra1_id == s.squadra2_id and scontro.squadra2_id == s.squadra1_id)
        )
        if not stesse_squadre:
            continue

        if scontro.data != s.data:
            continue

        
    
    if errori:
        lista_squadretorneo = SquadraDAO.getAllby_torneo_id(torneo_id)

        return render_template(
            'privato/admin/modifica_scontro.html',
            errori=errori,
            scontro=None,
            lista_squadretorneo=lista_squadretorneo,
            hide_navigation=True
        )
    
    successo= ScontroDAO.modifica(scontro)
       
    if successo:    
        return redirect('/privato?successo=1')
    else:
        return redirect('/privato?errore=1')
