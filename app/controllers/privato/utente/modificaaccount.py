# app/controllers/index.py

from flask import Blueprint, current_app, render_template, session, request, redirect, make_response, url_for
from app.models.giocatore.GiocatoreDAO import GiocatoreDAO
from app.models.squadra.SquadraDAO import SquadraDAO
from app.models.squadra.Squadra import Squadra
from app.models.account.AccountDAO import AccountDAO
from app.models.account.Account import Account
from datetime import datetime, date
import re


# Creiamo un Blueprint dedicato alle rotte “pubbliche”
modificaaccount_bp = Blueprint('modificaaccount', __name__)

@modificaaccount_bp.route('/modificaaccount' , methods=['POST'])
def home():

    if 'autenticato' not in session:
        return redirect('/richiedilogin?errore=1')
    
    
    lista_nomisquadra = SquadraDAO.getNomi()
    
    errori = []
    username = request.form.get('username')
    vecchia_password = request.form.get('vpassword')
    if AccountDAO.getbyUsername_Password(username, vecchia_password) is None:
        errori.append("Password attuale errata")

    nuova_password = request.form.get('npassword')
    PASSWORD_PATTERN = re.compile(r'^(?=.*[!@#$%^&*(),.?":{}|<>]).{8,}$')
    if not nuova_password or not PASSWORD_PATTERN.match(nuova_password):
        errori.append("La nuova password deve contenere almeno 8 caratteri e un carattere speciale")

    squadra_id = request.form.get('squadra_id')
    nome_precedente = SquadraDAO.getNome(squadra_id)

    nome_squadra = request.form.get('nomesquadra').strip()
    if nome_squadra != nome_precedente and nome_squadra in lista_nomisquadra:
        errori.append("Il nome della squadra è già in uso")
    
    torneo_id = request.form.get("torneo_id")
    logo = request.form.get('team_logo')

    

    

    if errori:
        account = AccountDAO.getbyUsername(username)
        squadra = SquadraDAO.getbyId(squadra_id)
        

        return render_template('privato/utente/modificaaccount.html', squadra=squadra,account=account, errori=errori, hide_navigation=True)
    
    account = Account()
    account.username = username
    account.password = nuova_password
    account.ruolo = session.get('ruolo')
    account.id_Sq = squadra_id

    successo1 = AccountDAO.modifica(account)

    
    squadra = Squadra()
    squadra.id = squadra_id
    squadra.nome = nome_squadra
    squadra.torneo_id = torneo_id
    squadra.logo = logo

    successo2 = SquadraDAO.modifica(squadra)   
    
    
            
    if successo1 and successo2:    
        return redirect('/privato?successo=1')
    else:
        return redirect('/privato?errore=1')
