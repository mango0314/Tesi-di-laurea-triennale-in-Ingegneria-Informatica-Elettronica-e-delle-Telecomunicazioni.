# app/controllers/index.py

from flask import Blueprint, current_app, render_template, session, request, redirect, make_response, url_for, flash
from app.models.scontro.ScontroDAO import ScontroDAO
from app.models.torneo.TorneoDAO import TorneoDAO
from app.models.commento.CommentoDAO import CommentoDAO
from app.models.commento.Commento import Commento
from app.models.sport.SportDAO import SportDAO


# Creiamo un Blueprint dedicato alle rotte “pubbliche”
aggiungicommento_privato_bp = Blueprint('aggiungicommento_privato', __name__)

@aggiungicommento_privato_bp.route('/aggiungicommento_privato' , methods=['POST'])
def home():
 
    
    
    errori = []
    ruolo = session.get('ruolo')
    if ruolo == 1:
        autore = session.get('username')
    else:
        autore = request.form.get('nome').strip()
    contenuto = request.form.get('commento')
    scontro_id = request.args.get('scontro_id', type=int)
    torneo_id = session.get('torneo_id')
    
    if len(contenuto) > 500:
        errori.append("Commento troppo lungo")


    

   
    if errori:
        # flash di ogni errore (categoria 'danger' o 'error')
        for e in errori:
            flash(e, 'danger')
        # PRG: redirect alla pagina di dettaglio (che caricherà i dati necessari)
        return redirect(f'/scontri?torneo_id={torneo_id}')

    commento = Commento()
    
    commento.nome = autore
    commento.contenuto = contenuto
    commento.scontro_id= scontro_id

    successo= CommentoDAO.salva(commento)
            
        
    if successo :    
        return redirect('/scontri?successo=1')
    else:
        return redirect('/scontri?errore=1')
