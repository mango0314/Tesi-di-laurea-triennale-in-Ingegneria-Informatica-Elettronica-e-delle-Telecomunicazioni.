# app/controllers/index.py

from flask import Blueprint, render_template, session, redirect, make_response
from app.models.squadra.SquadraDAO import SquadraDAO
from app.models.giocatore.GiocatoreDAO import GiocatoreDAO
from app.models.torneo.TorneoDAO import TorneoDAO
from app.models.scontro.ScontroDAO import ScontroDAO
from app.models.classifica.ClassificaDAO import ClassificaDAO
from app.models.classifica.Classifica import Classifica

# Creiamo un Blueprint dedicato alle rotte “pubbliche”
classificaprivato_bp = Blueprint('classificaprivato', __name__)

@classificaprivato_bp.route('/classificaprivato')
def home():
   
   if 'autenticato' not in session:
        return redirect('/richiedilogin?errore=1')
   
   ruolo = session.get('ruolo')

   squadra = None
   torneo_id = None
   if ruolo == 0:
          torneo_id = session.get('torneo_id')
   else:
          squadra_id = session.get('squadra_id')
          squadra = SquadraDAO.getbyId(squadra_id) if squadra_id else None
          torneo_id = squadra.torneo_id if squadra else None
   
   scontri = ScontroDAO.getAlleby_TorneoId(torneo_id)
   squadreIds = []

   for s in scontri:
          if (s.squadra1_id is not None and s.squadra1_id not in squadreIds):
               squadreIds.append(s.squadra1_id)
          if (s.squadra2_id is not None and s.squadra2_id not in squadreIds):
               squadreIds.append(s.squadra2_id)
     
   squadre = []
   for squadraId in squadreIds:
          sq = SquadraDAO.getbyId(squadraId)
          if sq is not None:
                squadre.append(sq)
     
   lista_classifica = []
   torneo = TorneoDAO.getById(torneo_id)
   Sportid = torneo.sport_id if torneo else None

   if ruolo == 0:
         for sq in squadre:
          somma_punti = ScontroDAO.getSomma_puntifatti(sq.id, torneo_id)
          numero_scontri_conclusi = int( ScontroDAO.getNumeroScontri_conclusi(sq.id, torneo_id))

          media = None
          if numero_scontri_conclusi > 0:
               media = somma_punti / numero_scontri_conclusi
          
          bonus = ClassificaDAO.getBonus(sq.id, torneo_id)
          lista_classifica.append(Classifica(sq.id, 0, torneo_id, 0, 0, 0, media, bonus))

          for s in scontri:
               p1 = s.punteggio1
               p2 = s.punteggio2
               if( p1 is None or p2 is None):
                    continue
               idx1 = -1
               idx2 = -1
               for i in range(len(lista_classifica)):
                    if lista_classifica[i].id_squadra == s.squadra1_id:
                         idx1 = i
                    if lista_classifica[i].id_squadra == s.squadra2_id:  
                         idx2 = i

               if idx1 == -1 or idx2 == -1:
                    continue  
               if p1 > p2:
                    old = lista_classifica[idx1].punteggio
                    old2 = lista_classifica[idx1].vittorie  
                    old3 = lista_classifica[idx2].sconfitte

                    if Sportid == 1:
                              lista_classifica[idx1].punteggio = old + 3
                              lista_classifica[idx1].vittorie = old2 + 1
                              lista_classifica[idx2].sconfitte = old3 + 1
                    elif Sportid == 2:
                              lista_classifica[idx1].punteggio = old + 2
                              lista_classifica[idx1].vittorie = old2 + 1
                              lista_classifica[idx2].sconfitte = old3 + 1
                    else:
                         if p2 == 2:
                              lista_classifica[idx1].punteggio = old + 2
                              lista_classifica[idx1].vittorie = old2 + 1
                              lista_classifica[idx2].punteggio = lista_classifica[idx2].punteggio + 1
                              lista_classifica[idx2].sconfitte = old3 + 1
                         else:
                                   lista_classifica[idx1].punteggio = old + 3
                                   lista_classifica[idx1].vittorie = old2 + 1
                                   lista_classifica[idx2].sconfitte = old3 + 1
               elif p2 > p1:
                         old = lista_classifica[idx2].punteggio
                         old2 = lista_classifica[idx2].vittorie  
                         old3 = lista_classifica[idx1].sconfitte
               
                         if Sportid == 1:
                                   lista_classifica[idx2].punteggio = old + 3
                                   lista_classifica[idx2].vittorie = old2 + 1
                                   lista_classifica[idx1].sconfitte = old3 + 1
                         elif Sportid == 2:
                                   lista_classifica[idx2].punteggio = old + 2
                                   lista_classifica[idx2].vittorie = old2 + 1
                                   lista_classifica[idx1].sconfitte = old3 + 1
                         else:
                              if p1 == 2:
                                   lista_classifica[idx2].punteggio = old + 2
                                   lista_classifica[idx2].vittorie = old2 + 1
                                   lista_classifica[idx1].punteggio = lista_classifica[idx1].punteggio + 1
                                   lista_classifica[idx1].sconfitte = old3 + 1
                              else:
                                   lista_classifica[idx2].punteggio = old + 3
                                   lista_classifica[idx2].vittorie = old2 + 1
                                   lista_classifica[idx1].sconfitte = old3 + 1
               elif Sportid == 1:  
                         lista_classifica[idx1].punteggio = lista_classifica[idx1].punteggio + 1
                         lista_classifica[idx2].punteggio = lista_classifica[idx2].punteggio + 1
                         lista_classifica[idx1].pareggi = lista_classifica[idx1].pareggi + 1
                         lista_classifica[idx2].pareggi = lista_classifica[idx2].pareggi + 1
               
               ClassificaDAO.salva(lista_classifica)        
   else:
      lista_classifica = ClassificaDAO.getAllby_torneo_id(torneo_id)

   # Ordina la classifica per punteggio totale decrescente
   lista_classifica.sort(key=lambda c: c.get_punteggio_totale(), reverse=True)

   if lista_classifica:
         lista_classifica_conimmagini = []
         for c in lista_classifica:
               s = SquadraDAO.getbyId(c.id_squadra)
               lista_classifica_conimmagini.append({
                    'squadra_id': c.id_squadra,
                    'nome': s.nome if s else '',
                    'logo': s.logo if s else '',
                    'punteggio': c.punteggio,
                    'torneo_id': c.id_torneo,
                    'vittorie': c.vittorie,
                    'sconfitte': c.sconfitte,
                    'pareggi': c.pareggi,
                    'media': c.media,
                    'bonus': c.bonus
               })

# Passa i dati al template
   response = make_response(render_template(
    'privato/classifica_privato.html',
    classifica=lista_classifica_conimmagini,
    torneo=torneo,
    sport_id=Sportid,
    ruolo=ruolo,
    hide_navigation=True,
    manual = True
    # aggiungi qui altri parametri se servono
   ))
   response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
   response.headers['Pragma'] = 'no-cache'
   response.headers['Expires'] = '0'
   return response
     
