# app/controllers/index.py

from flask import Blueprint, render_template, request, redirect, session, url_for, current_app
from app.models.account.AccountDAO import AccountDAO 
from app.models.squadra.SquadraDAO import SquadraDAO 
from app.models.torneo.TorneoDAO import TorneoDAO
from app.models.giocatore.GiocatoreDAO import GiocatoreDAO
from app.models.giocatore.Giocatore import Giocatore
from app.models.squadra.Squadra import Squadra
from app.models.account.Account import Account
import re
from datetime import datetime, date
import os
import uuid
from werkzeug.utils import secure_filename
import magic

ALLOWED_EXT = {'pdf', 'png', 'jpg', 'jpeg'}

def file_permessi(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXT

def validazione_file(file_stream, allowed_mimes):
    head = file_stream.read(2048)
    file_stream.seek(0)
    mime = magic.from_buffer(head, mime=True)
    return mime in allowed_mimes

ALLOWED_MIMES = {'image/png','image/jpeg','application/pdf'}

registrazione_bp = Blueprint('registrazione', __name__)

@registrazione_bp.route('/registrazione', methods=['POST'])
def home():
    
    errori = []
    lista_nomisquadra = SquadraDAO.getNomi()
    lista_username = AccountDAO.getUsername()

    username= request.form.get('username', '').strip()
    password = request.form.get('password', '').strip()
    nome_squadra = request.form.get('nomesquadra', '').strip()
    torneo = request.form.get('torneo', '')
    file = request.files.get('logoUpload', '')
    logo_filename = None

    if username in lista_username:
        errori.append("Username già in uso")

    # controllo la password
    PASSWORD_PATTERN = re.compile(r'^(?=.*[!@#$%^&*(),.?":{}|<>]).{8,}$')
    password = request.form.get('password', '')
    if not password or not PASSWORD_PATTERN.match(password):
        errori.append("La password deve contenere almeno 8 caratteri e un carattere speciale")


    if file and file.filename:
        filename = secure_filename(file.filename)
        if not file_permessi(filename):
            errori.append("Estensione non permessa.")
        elif not validazione_file(file.stream, ALLOWED_MIMES):
            errori.append("Contenuto file non valido.")
        else:
            name = f"{uuid.uuid4().hex}_{filename}"
            upload_folder = current_app.config['UPLOAD_FOLDER']
            path = os.path.join(upload_folder, name)
            file.save(path)
            logo_filename = name
    


    # controllo nome squadra
    if nome_squadra in lista_nomisquadra:
        errori.append("Il nome della squadra è già in uso")
    
    # controllo date di nascite
    for i in range(1, 8):
        data_str = request.form.get(f'dataNascita_{i}', '')
        try:
            nascita = date.fromisoformat(data_str)
            oggi = date.today()
            anni = oggi.year - nascita.year - ((oggi.month, oggi.day) < (nascita.month, nascita.day))
            if anni < 18 or anni > 60:
                errori.append(f"Giocatore {i}: età non valida ({anni} anni)")
        except ValueError:
            errori.append(f"Giocatore {i}: formato data non valido (gg/MM/yyyy)")

    if errori:
    # Recupera la lista dei tornei dal DAO
        lista_tornei = TorneoDAO.getAll()

        # Ritorna il template di registrazione con errori e dati già inseriti
        return render_template(
            'richiediregistrazione.html',
            errori=errori,
            lista_tornei=lista_tornei,
            username=username,
            nome_squadra=nome_squadra,
            torneo=torneo,
            logo=logo_filename,
            # aggiungi altri dati del form se vuoi ripopolarli
            hide_navigation=True
        )


    squadra = Squadra()

    squadra.nome = nome_squadra
    squadra.torneo_id = torneo
    squadra.logo = logo_filename

    SquadraDAO.salva(squadra)
    print(f"[DEBUG] Idgenerato = {squadra.id!r}")
    Idgenerato = squadra.id

    account = Account()
    account.username = username
    account.password = password
    account.ruolo = 1
    account.id_Sq = Idgenerato
    

    AccountDAO.salva(account)

    # Ottieni l'ultimo ID dei giocatori
    base_id = GiocatoreDAO.UltimoId()

    lista_giocatori = []
    for i in range(1, 8):
        giocatore = Giocatore()  # Assicurati che la classe Giocatore sia importata
        base_id += 1
        giocatore.id = base_id
        nome_giocatore = request.form.get(f'nome_{i}', '').strip()
        if not re.match(r'^[a-zA-Z\s]+$', nome_giocatore):
            errori.append(f"Giocatore {i}: nome non valido")
            
        giocatore.nome = nome_giocatore
        cognome_giocatore = request.form.get(f'cognome_{i}', '').strip()
        if not re.match(r'^[a-zA-Z\s]+$', cognome_giocatore):
            errori.append(f"Giocatore {i}: cognome non valido")
        giocatore.cognome =cognome_giocatore
        data_str = request.form.get(f'dataNascita_{i}', '')
        giocatore.data_di_nascita = data_str
        giocatore.squadra_id = Idgenerato
        giocatore.numero_di_maglia = int(request.form.get(f'numeroMaglia_{i}', '0'))
        lista_giocatori.append(giocatore)

        
    GiocatoreDAO.salvaGiocatori(lista_giocatori)


   
    

    
   

    # Redirect all'area privata
    return redirect(url_for('richiedilogin.home'))

