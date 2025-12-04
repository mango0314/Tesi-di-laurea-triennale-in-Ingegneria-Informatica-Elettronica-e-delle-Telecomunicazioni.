# app/controllers/index.py

from flask import Blueprint, current_app, render_template, session, request, redirect, make_response, url_for
from app.models.scontro.ScontroDAO import ScontroDAO
from app.models.torneo.TorneoDAO import TorneoDAO
from app.models.account.Account import Account
from app.models.account.AccountDAO import AccountDAO

# Creiamo un Blueprint dedicato alle rotte “pubbliche”
eliminaaccount_bp = Blueprint('eliminaaccount', __name__)

@eliminaaccount_bp.route('/eliminaaccount')
def home():

    if 'autenticato' not in session:
        return redirect('/richiedilogin?errore=1')
    
    
    username = session.get('username')
    

    account = Account()
    account.username = username

    successo= AccountDAO.elimina(account)
            
    if successo:     
        return redirect('/privato?successo=1')
    else:
        return redirect('/privato?errore=1')
