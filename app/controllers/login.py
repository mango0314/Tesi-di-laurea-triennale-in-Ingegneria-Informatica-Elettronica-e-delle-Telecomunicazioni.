# app/controllers/index.py

from flask import Blueprint, render_template, request, redirect, session, url_for
from app.models.account.AccountDAO import AccountDAO  


# Creiamo un Blueprint dedicato alle rotte “pubbliche”
login_bp = Blueprint('login', __name__)

@login_bp.route('/login', methods=['POST'])
def home():
    
    username= request.form.get('username', '').strip()
    password = request.form.get('password', '').strip()

    ruolo = AccountDAO.get_ruolo(username, password)
    if ruolo == -1:
        return render_template('richiedilogin.html', errore='Credenziali non valide', hide_navigation=True)
    
    squadraid = AccountDAO.getSq(username, password)
    

    
    # Gestione sessione Flask (cookie httpOnly gestito da Flask)
    session['autenticato'] = True
    session['squadra_id'] = squadraid
    session['ruolo'] = ruolo
    session['username'] = username

    # Redirect all'area privata
    return redirect(url_for('privato.home'))

