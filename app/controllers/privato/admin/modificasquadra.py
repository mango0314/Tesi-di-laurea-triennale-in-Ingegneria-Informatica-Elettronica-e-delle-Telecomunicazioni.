# app/controllers/index.py

from flask import Blueprint, current_app, render_template, session, request, redirect, make_response, url_for
from app.models.giocatore.GiocatoreDAO import GiocatoreDAO
from app.models.giocatore.Giocatore import Giocatore
from app.models.squadra.SquadraDAO import SquadraDAO
from app.models.squadra.Squadra import Squadra
from datetime import datetime, date


# Creiamo un Blueprint dedicato alle rotte “pubbliche”
modificasquadra_bp = Blueprint('modificasquadra', __name__)

@modificasquadra_bp.route('/modificasquadra' , methods=['POST'])
def home():

    if 'autenticato' not in session:
        return redirect('/richiedilogin?errore=1')
    
    
    lista_nomisquadra = SquadraDAO.getNomi()
    
    errori = []
    squadra_id = request.form.get('squadra_id')
    nome_vecchio = SquadraDAO.getNome(squadra_id)
    
    torneo_id = session.get("torneo_id")
    logo = request.form.get('team_logo')

    nome_squadra = request.form.get('nome_squadra').strip()
    if nome_squadra != nome_vecchio and nome_squadra in lista_nomisquadra:
        errori.append("Il nome della squadra è già in uso")

    count = request.form.get('giocatori_count', type=int)

    if errori:
        squadra = SquadraDAO.getbyId(squadra_id)
        lista_giocatorisquadra = GiocatoreDAO.getAllbyId(squadra_id)

        return render_template('privato/admin/modifica_squadra.html', squadra=squadra, lista_giocatorisquadra=lista_giocatorisquadra, errori=errori, hide_navigation=True)
    


    listaGiocatori = []
    squadra = Squadra()
    squadra.id = squadra_id
    squadra.nome = nome_squadra
    squadra.torneo_id = torneo_id
    squadra.logo = logo

    successo1 = SquadraDAO.modifica(squadra)

   

    for i in range(count):
        # 1) Prelevo ogni campo
        id_param    = request.form.get(f'id_{i}')
        nome        = request.form.get(f'nome_{i}', '').strip()
        cognome     = request.form.get(f'cognome_{i}', '').strip()
        data_str    = request.form.get(f'data_nascita_{i}', '').strip()
        maglia_str  = request.form.get(f'numero_maglia_{i}', '').strip()

        # Validazione ID
        if not id_param:
            errori.append(f"Giocatore {i+1}: ID mancante")
            continue
        try:
            giocatore_id = int(id_param)
        except ValueError:
            errori.append(f"Giocatore {i+1}: ID non valido ({id_param})")
            continue

        # Validazione nome e cognome
        if not nome:
            errori.append(f"Giocatore {i+1}: nome mancante")
        if not cognome:
            errori.append(f"Giocatore {i+1}: cognome mancante")

        giocatore = Giocatore()
        giocatore.id = giocatore_id
        giocatore.nome = nome
        giocatore.cognome = cognome

        # 2) Parsing data di nascita + controllo età
        try:
            nascita = date.fromisoformat(data_str)
            oggi = date.today()
            anni = oggi.year - nascita.year - ((oggi.month, oggi.day) < (nascita.month, nascita.day))
            if anni < 18 or anni > 60:
                errori.append(f"Giocatore {i}: età non valida ({anni} anni)")
            giocatore.data_di_nascita = nascita
        except ValueError:
            errori.append(f"Giocatore {i}: formato data non valido (gg/MM/yyyy)")

        # 3) Validazione numero maglia
        if not maglia_str:
            errori.append(f"Giocatore {i+1}: numero di maglia mancante")
        else:
            try:
                maglia = int(maglia_str)
                if not (1 <= maglia <= 99):
                    raise ValueError()
                giocatore.numero_di_maglia = maglia
            except ValueError:
                errori.append(f"Giocatore {i+1}: numero di maglia non valido ({maglia_str})")

        giocatore.squadra_id = squadra_id

        listaGiocatori.append(giocatore)
    
    successo2 = GiocatoreDAO.modificaGiocatori(listaGiocatori)
    
    if errori:
        squadra = SquadraDAO.getbyId(squadra_id)

        lista_giocatorisquadra = GiocatoreDAO.getAllbyId(squadra_id)

        return render_template('privato/admin/modifica_squadra.html', errori = errori, squadra = squadra, lista_giocatorisquadra = lista_giocatorisquadra, hide_navigation=True)
    
            
    if successo1 and successo2:    
        return redirect('/privato?successo=1')
    else:
        return redirect('/privato?errore=1')
