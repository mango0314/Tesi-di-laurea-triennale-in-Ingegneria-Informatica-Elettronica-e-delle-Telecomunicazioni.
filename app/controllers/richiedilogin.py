# app/controllers/index.py

from flask import Blueprint, render_template


# Creiamo un Blueprint dedicato alle rotte “pubbliche”
richiedilogin_bp = Blueprint('richiedilogin', __name__)

@richiedilogin_bp.route('/richiedilogin')
def home():
    """
    Equivalente al doGet della tua servlet Java:
      1) recupera la listaSport da DB via DAO
      2) passa listaSport al template Jinja2
      3) restituisce la pagina renderizzata
    """
    
        
      
    return render_template('richiedilogin.html', hide_navigation=True)
