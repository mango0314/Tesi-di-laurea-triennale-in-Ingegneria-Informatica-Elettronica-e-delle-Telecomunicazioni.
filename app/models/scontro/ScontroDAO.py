from flask import current_app
from app import mysql
from app.models.scontro.Scontro import Scontro

class ScontroDAO:

    @staticmethod
    def get(scontro):
        query = 'SELECT * FROM scontro WHERE id = %s'
        cur = mysql.connection.cursor()
        try:
            cur.execute(query, (scontro.id,))
            row = cur.fetchone()
            cur.close()
            if row:
                return Scontro(*row)
        except Exception as e:
            print(f"Errore durante la query: {e}")
            cur.close()
            return None
        
    @staticmethod
    def getById(id):
        query = 'SELECT * FROM scontro WHERE id = %s'
        cur = mysql.connection.cursor()
        try:
            cur.execute(query, (id,))
            row = cur.fetchone()
            cur.close()
            if row:
                return Scontro(*row)
        except Exception as e:
            print(f"Errore durante la query: {e}")
            cur.close()
            return None
        
    @staticmethod
    def getUltimoScontro(torneo_id):
        query = 'SELECT * FROM SCONTRO WHERE torneo_id = %s AND punteggio1 IS NOT NULL ORDER BY DATA DESC, ORARIO DESC LIMIT 1'
        cur = mysql.connection.cursor()
        try:
            cur.execute(query, (torneo_id,))
            row = cur.fetchone()
            cur.close()
            if row:
                return Scontro(*row)
        except Exception as e:
            print(f"Errore durante la query: {e}")
            cur.close()
            return None
        
    @staticmethod
    def getNumeroScontri_conclusi(squadra_id, torneo_id):
        query = 'SELECT COUNT(*) as partite_giocate FROM scontro WHERE (squadra1_id = %s or squadra2_id = %s) AND (punteggio1 IS NOT NULL or punteggio2 IS NOT NULL) AND torneo_id = %s'
        cur = mysql.connection.cursor()
        try:
            cur.execute(query, (squadra_id, squadra_id, torneo_id))
            row = cur.fetchone()
            cur.close()
            return row[0] if row else 0
        except Exception as e:
            print(f"Errore durante la query: {e}")
            cur.close()
            return 0
        
    @staticmethod
    def getSomma_puntifatti(squadra_id, torneo_id):
        query = ' SELECT   SUM( CASE  WHEN squadra1_id = %s THEN punteggio1    WHEN squadra2_id = %s THEN punteggio2 ELSE 0 END  ) AS totale_goal  FROM scontro WHERE (squadra1_id = %s OR squadra2_id = %s) AND (punteggio1 IS NOT NULL OR punteggio2 IS NOT NULL) AND torneo_id = %s'
        cur = mysql.connection.cursor()
        try:
            cur.execute(query, (squadra_id, squadra_id, squadra_id, squadra_id, torneo_id))
            result = cur.fetchone()
            cur.close()
            return result[0] if result else 0
        except Exception as e:
            print(f"Errore durante la query: {e}")
            cur.close()
            return -1
        
    @staticmethod
    def getNomesquadra(id_squadra):
        query = 'SELECT sq.nome as nome_squadra FROM scontro sc JOIN squadra sq ON sq.id = sc.squadra1_id WHERE sq.id = %s'
        cur = mysql.connection.cursor()
        try:
            cur.execute(query, (id_squadra,))
            row = cur.fetchone()
            cur.close()
            if row:
                return row['nome']
        except Exception as e:
            print(f"Errore durante la query: {e}")
            cur.close()
            return None
        
    @staticmethod
    def UltimoId():
        query = 'SELECT id FROM scontro ORDER BY id DESC LIMIT 1'
        cur = mysql.connection.cursor()
        try:
            cur.execute(query)
            row = cur.fetchone()
            cur.close()
            if row:
                return row['id']
        except Exception as e:
            print(f"Errore durante la query: {e}")
            cur.close()
            return -1
    
 

    @staticmethod
    def getAll():
        query = 'SELECT * FROM scontro'
        cur = mysql.connection.cursor()
        try:
            cur.execute(query)
            rows = cur.fetchall()
            cur.close()
            return [Scontro(*row) for row in rows]
        except Exception as e:
            print(f"Errore durante la query: {e}")
            cur.close()
            return []

    @staticmethod
    def getAllby_Torneo(torneo):
        query = 'SELECT * FROM scontro WHERE id_torneo = %s ORDER BY id'
        cur = mysql.connection.cursor()
        try:
            cur.execute(query, (torneo.id,))
            rows = cur.fetchall()
            cur.close()
            return [Scontro(*row) for row in rows]
        except Exception as e:
            print(f"Errore durante la query: {e}")
            cur.close()
            return []
        
    @staticmethod
    def getAllDateScontri(torneo_id):
        query = 'SELECT data FROM scontro WHERE id_torneo = %s ORDER BY id'
        cur = mysql.connection.cursor()
        try:
            cur.execute(query, (torneo_id,))
            rows = cur.fetchall()
            cur.close()
            return [row['data'] for row in rows]
        except Exception as e:
            print(f"Errore durante la query: {e}")
            cur.close()
            return []
        
    @staticmethod
    def getScontriBySquadra(squadra_id):
        query = 'SELECT s.* FROM scontro s JOIN squadra sq1 ON s.squadra1_id = sq1.id JOIN squadra sq2 ON s.squadra2_id = sq2.id WHERE (sq1.id = %s OR sq2.id = %s) '
        cur = mysql.connection.cursor()
        try:
            cur.execute(query, (squadra_id, squadra_id))
            rows = cur.fetchall()
            cur.close()
            return [Scontro(*row) for row in rows]
        except Exception as e:
            print(f"Errore durante la query: {e}")
            cur.close()
            return []
    
    @staticmethod
    def getAlleby_TorneoId(torneo_id):
        query = 'SELECT * FROM scontro WHERE torneo_id = %s ORDER BY data asc, orario asc'
        cur = mysql.connection.cursor()
        try:
            cur.execute(query, (torneo_id,))
            rows = cur.fetchall()
            cur.close()
            return [Scontro(*row) for row in rows]
        except Exception as e:
            print(f"Errore durante la query: {e}")
            cur.close()
            return []
        
    @staticmethod
    def getAllby_idSquadra(squadra_id):
        query = 'SELECT * FROM scontro WHERE id_squadra = %s  ORDER BY id'
        cur = mysql.connection.cursor()
        try:
            cur.execute(query, (squadra_id, squadra_id))
            rows = cur.fetchall()
            cur.close()
            return [Scontro(*row) for row in rows]
        except Exception as e:
            print(f"Errore durante la query: {e}")
            cur.close()
            return []

    @staticmethod
    def salva(scontro):
        query = 'INSERT INTO scontro ( torneo_id, squadra1_id, squadra2_id, punteggio1, punteggio2, data, orario) VALUES ( %s, %s, %s, %s, %s, %s, %s)' 
        cur = mysql.connection.cursor()
        try:
            cur.execute(query, (scontro.torneo_id, scontro.squadra1_id, scontro.squadra2_id, scontro.punteggio1, scontro.punteggio2, scontro.data, scontro.orario))
            mysql.connection.commit()
            scontro.id = cur.lastrowid  # Imposta l'ID generato automaticamente
            cur.close()
            return True
        except Exception as e:
            print(f"Errore durante la query: {e}")
            mysql.connection.rollback()
            cur.close()
            return False

    @staticmethod
    def modifica(scontro):
        query = 'UPDATE scontro SET torneo_id = %s, punteggio1 = %s, punteggio2 = %s, data = %s, orario = %s WHERE id = %s'
        cur = mysql.connection.cursor()
        try:
            cur.execute(query, (scontro.torneo_id, scontro.punteggio1, scontro.punteggio2, scontro.data, scontro.orario, scontro.id))
            mysql.connection.commit()
            cur.close()
            return True
        except Exception as e:
            print(f"Errore durante la query: {e}")
            mysql.connection.rollback()
            cur.close()
            return False

    @staticmethod
    def elimina(scontro):
        query = 'DELETE FROM scontro WHERE id = %s'
        cur = mysql.connection.cursor()
        try:
            cur.execute(query, (scontro.id,))
            mysql.connection.commit()
            cur.close()
            return True
        except Exception as e:
            print(f"Errore durante la query: {e}")
            mysql.connection.rollback()
            cur.close()
            return False
