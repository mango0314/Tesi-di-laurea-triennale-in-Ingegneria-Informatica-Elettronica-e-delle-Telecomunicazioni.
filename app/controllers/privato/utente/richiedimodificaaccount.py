# app/controllers/index.py

from flask import Blueprint, current_app, render_template, session, request, redirect, make_response
from app.models.squadra.SquadraDAO import SquadraDAO
from app.models.account.AccountDAO import AccountDAO

# Creiamo un Blueprint dedicato alle rotte “pubbliche”
richiedimodificaaccount_bp = Blueprint('richiedimodificaaccount', __name__)

@richiedimodificaaccount_bp.route('/richiedimodificaaccount')
def home():

    if 'autenticato' not in session:
        return redirect('/richiedilogin?errore=1')
    
    
    username = session.get('username')
    
    account = AccountDAO.getbyUsername(username)

    squadra = SquadraDAO.getbyId(account.id_Sq)


    
            
        
    return render_template('privato/utente/modificaaccount.html', account = account, squadra = squadra, hide_navigation=True)
