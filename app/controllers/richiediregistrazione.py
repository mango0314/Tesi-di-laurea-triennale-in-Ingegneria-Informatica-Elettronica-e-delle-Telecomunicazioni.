# app/controllers/index.py

from flask import Blueprint, render_template
from app.models.torneo.TorneoDAO import TorneoDAO
from app.models.sport.SportDAO import SportDAO


# Creiamo un Blueprint dedicato alle rotte “pubbliche”
richiediregistrazione_bp = Blueprint('richiediregistrazione', __name__)

@richiediregistrazione_bp.route('/richiediregistrazione')
def home():
    
    

    lista_tornei = TorneoDAO.getAll()
    lista_sport = SportDAO.get_all()
    
        
      
    return render_template('richiediregistrazione.html', hide_navigation=True, lista_tornei=lista_tornei, lista_sport=lista_sport)
