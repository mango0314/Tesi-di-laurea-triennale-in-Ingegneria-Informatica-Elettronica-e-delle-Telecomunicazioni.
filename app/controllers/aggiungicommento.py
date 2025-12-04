

from flask import Blueprint, session, request, redirect, flash
from app.models.commento.CommentoDAO import CommentoDAO
from app.models.commento.Commento import Commento
import bleach
import re

aggiungicommento_bp = Blueprint('aggiungicommento', __name__)

@aggiungicommento_bp.route('/aggiungicommento', methods=['POST'])
def home():
    errori = []
    ruolo = session.get('ruolo')

    if ruolo == 1:
        autore = session.get('username')
    else:
        autore = request.form.get('nome', '').strip()
        if not autore or len(autore) < 2:
            errori.append("Il nome inserito non è valido")

    contenuto = request.form.get('commento', '')
    scontro_id = request.args.get('scontro_id', type=int)
    torneo_id = session.get('torneo_id')

    if not contenuto:
        errori.append("Il commento non può essere vuoto")
    if len(contenuto) > 500:
        errori.append("Il commento è troppo lungo (max 500 caratteri)")

    if re.search(r'<[^>]*>', contenuto):
     errori.append("Il commento non deve contenere tag HTML")
    contenuto = bleach.clean(
         contenuto,
        tags=[],               
        attributes={},          
        strip=True              
    )

    if errori:
        for e in errori:
          flash(e, 'danger')
        return redirect(f'/dettagliotorneo?torneo_id={torneo_id}')

    commento = Commento()
    commento.nome = autore
    commento.contenuto = contenuto
    commento.scontro_id = scontro_id

    successo = CommentoDAO.salva(commento)

    if successo:
        return redirect('/dettagliotorneo?successo=1')
    else:
        return redirect('/dettagliotorneo?errore=1')
