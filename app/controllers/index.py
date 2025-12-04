# app/controllers/index.py

from flask import Blueprint, render_template
from app.models.sport.SportDAO import SportDAO

# Creiamo un Blueprint dedicato alle rotte “pubbliche”
index_bp = Blueprint('index', __name__)

@index_bp.route('/')
def home():
    """
    Equivalente al doGet della tua servlet Java:
      1) recupera la listaSport da DB via DAO
      2) passa listaSport al template Jinja2
      3) restituisce la pagina renderizzata
    """
    listaSport = SportDAO.get_all()  # usa il tuo metodo DAO Python
    if listaSport is None or len(listaSport) == 0:
        # Se la lista è vuota, restituisce un messaggio di errore
        print("DEBUG listaSport è vuota")
        return render_template('index.html', listaSport=listaSport, error="Nessuno sport trovato.")
        
      
    return render_template('index.html', listaSport=listaSport)
