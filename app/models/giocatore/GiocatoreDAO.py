from flask import current_app
from app import mysql
from app.models.giocatore.Giocatore import Giocatore

class GiocatoreDAO:

    @staticmethod
    def get(giocatore):
        query = 'SELECT * FROM giocatore WHERE id = %s'

        cur = mysql.connection.cursor()
        try:
            cur.execute(query, (giocatore.id))
            row = cur.fetchone()
            cur.close()
            if row:
                return Giocatore(*row)
        except Exception as e:
            print(f"Errore durante la query: {e}")
            cur.close()
            return None
        
    @staticmethod
    def getAll():
        query = 'SELECT * FROM giocatore order by id'
        cur = mysql.connection.cursor()
        try:
            cur.execute(query)
            rows = cur.fetchall()
            cur.close()

            return [Giocatore(*row) for row in rows]
        except Exception as e:
            print(f"Errore durante la query: {e}")
            cur.close()
            return []
        
    @staticmethod
    def getAllbyId(squadra_id):
        query = 'SELECT * FROM giocatore where squadra_id = %s order by id'
        cur = mysql.connection.cursor()
        try:
            cur.execute(query, (squadra_id,))
            rows = cur.fetchall()
            cur.close()

            return [Giocatore(*row) for row in rows]
        except Exception as e:
            print(f"Errore durante la query: {e}")
            cur.close()
            return []
        

    def UltimoId():
        query = 'SELECT id from Giocatore order by id desc limit 1'
        cur = mysql.connection.cursor()
        try:
            cur.execute(query)
            row = cur.fetchone()
            cur.close()
            if row:
                return row[0]
        except Exception as e:
            print(f"Errore durante la query di Ultimoid: {e}")
            cur.close()
            return -1

        

    @staticmethod
    def salvaGiocatori(giocatori):
        query = 'INSERT INTO giocatore (nome, cognome, data_di_nascita, squadra_id, numero_di_maglia) VALUES (%s, %s, %s, %s, %s)' 
        cur = mysql.connection.cursor()
        try:
            for g in giocatori:
                cur.execute(query, (g.nome, g.cognome,g.data_di_nascita, g.squadra_id, g.numero_di_maglia))
            mysql.connection.commit()
            g.id = cur.lastrowid  # Ottieni l'ultimo ID generato
            cur.close()
            return True
        except Exception as e:
            print(f"Errore durante la query: {e}")
            mysql.connection.rollback()
            cur.close()
            return False
        
    @staticmethod
    def salva(giocatore):
        query = ' INSERT INTO giocatore VALUES (%s, %s, %s, %s, %s, %s, %s)' 
        cur = mysql.connection.cursor( )
        try:
            cur.execute(query, (giocatore.id_squadra, giocatore.nome, giocatore.cognome, giocatore.data_di_nascita, giocatore.numero_di_maglia))
            mysql.connection.commit()
            cur.close()
            return True
        except Exception as e:
            print(f"Errore durante la query: {e}")
            mysql.connection.rollback()
            cur.close()
            return False
        
    @staticmethod
    def modifica(giocatore):
        query = 'UPDATE giocatore SET nome = %s, cognome = %s, data_di_nascita = %s, squadra_id = %s, numero_di_maglia = %s WHERE id = %s'
        cur = mysql.connection.cursor()
        try:
            cur.execute(query, (giocatore.nome, giocatore.cognome, giocatore.data_di_nascita, giocatore.squadra_id, giocatore.numero_di_maglia, giocatore.id))
            mysql.connection.commit()
            cur.close()
            return True
        except Exception as e:
            print(f"Errore durante la query: {e}")
            mysql.connection.rollback()
            cur.close()
            return False
    
    @staticmethod
    def modificaGiocatori(giocatori):
        query = 'UPDATE giocatore SET nome = %s, cognome = %s, data_di_nascita = %s, squadra_id = %s, numero_di_maglia = %s WHERE id = %s'
        cur = mysql.connection.cursor()
        try:
            for g in giocatori:
                cur.execute(query, (g.nome, g.cognome, g.data_di_nascita, g.squadra_id, g.numero_di_maglia, g.id))
            mysql.connection.commit()
            cur.close()
            return True
        except Exception as e:
            print(f"Errore durante la query: {e}")
            mysql.connection.rollback()
            cur.close()
            return False
        

        
    @staticmethod
    def elimina(giocatore):
        query = 'DELETE FROM giocatore WHERE id = %s'
        cur = mysql.connection.cursor()
        try:
            cur.execute(query, (giocatore.id))
            mysql.connection.commit()
            cur.close()
            return True
        except Exception as e:
            print(f"Errore durante la query: {e}")
            mysql.connection.rollback()
            cur.close()
            return False
