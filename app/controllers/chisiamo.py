

from flask import Blueprint, render_template


# Creiamo un Blueprint dedicato alle rotte “pubbliche”
chisiamo_bp = Blueprint('chisiamo', __name__)
print(chisiamo_bp.deferred_functions)

@chisiamo_bp.route('/chisiamo')
def home():
    """
    Equivalente al doGet della tua servlet Java:
      1) recupera la listaSport da DB via DAO
      2) passa listaSport al template Jinja2
      3) restituisce la pagina renderizzata
    """
    
        
      
    return render_template('chisiamo.html', hide_navigation=True)
