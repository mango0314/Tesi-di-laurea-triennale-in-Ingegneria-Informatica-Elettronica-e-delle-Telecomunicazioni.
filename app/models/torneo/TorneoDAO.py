from flask import current_app
from app import mysql
from app.models.torneo.Torneo import Torneo

class TorneoDAO:

    @staticmethod
    def get(torneo):
        query = 'SELECT * FROM torneo WHERE id = %s'
        cur = mysql.connection.cursor()
        try:
            cur.execute(query, (torneo.id,))
            row = cur.fetchone()
            cur.close()
            if row:
                return Torneo(*row)
        except Exception as e:
            print(f"Errore durante la query: {e}")
            cur.close()
            return None
    
    @staticmethod
    def getById(id):
        query = 'SELECT * FROM torneo WHERE id = %s'
        cur = mysql.connection.cursor()
        try:
            cur.execute(query, (id,))
            row = cur.fetchone()
            cur.close()
            if row:
                return Torneo(*row)
        except Exception as e:
            print(f"Errore durante la query: {e}")
            cur.close()
            return None
    
    @staticmethod
    def getNome(torneo_id):
        query = 'SELECT nome FROM torneo where id = %s'
        cur = mysql.connection.cursor()
        try:
            cur.execute(query, (torneo_id,))
            rows = cur.fetchone()
            cur.close()
            if rows:
                return rows[0]
        except Exception as e:
            print(f"Errore durante la query: {e}")
            cur.close()
            return []
    
    @staticmethod
    def getNomi():
        query = 'SELECT nome FROM torneo'
        cur = mysql.connection.cursor()
        try:
            cur.execute(query)
            rows = cur.fetchall()
            cur.close()
            return [row[0] for row in rows]
        except Exception as e:
            print(f"Errore durante la query: {e}")
            cur.close()
            return []
    
    @staticmethod
    def getSportId(torneo_id):
        query = 'SELECT sport_id FROM torneo WHERE id = %s'
        cur = mysql.connection.cursor()
        try:
            cur.execute(query, (torneo_id,))
            row = cur.fetchone()
            cur.close()
            if row:
                return row['sport_id']
        except Exception as e:
            print(f"Errore durante la query: {e}")
            cur.close()
            return None
    
    @staticmethod
    def getUltimoId():
        query = 'SELECT id FROM torneo ORDER BY id DESC LIMIT 1'
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
        query = 'SELECT * FROM torneo ORDER BY id'
        cur = mysql.connection.cursor()
        try:
            cur.execute(query)
            rows = cur.fetchall()
            cur.close()
            return [Torneo(*row) for row in rows]
        except Exception as e:
            print(f"Errore durante la query: {e}")
            cur.close()
            return []

    @staticmethod
    def getAll_bySport(sport):
        query = 'SELECT * FROM torneo WHERE sport_id = %s ORDER BY id'
        cur = mysql.connection.cursor()
        try:
            cur.execute(query, (sport.id,))
            rows = cur.fetchall()
            cur.close()
            return [Torneo(*row) for row in rows]
        except Exception as e:
            print(f"Errore durante la query: {e}")
            cur.close()
            return []
        
    @staticmethod
    def getAll_bySportid(sport_id):
        query = 'SELECT * FROM torneo WHERE sport_id = %s ORDER BY id'
        cur = mysql.connection.cursor()
        try:
            cur.execute(query, (sport_id,))
            rows = cur.fetchall()
            cur.close()
            return [Torneo(*row) for row in rows]
        except Exception as e:
            print(f"Errore durante la query di getallbysportid: {e}")
            cur.close()
            return []
        
    @staticmethod
    def getAll_bySquadraidra(squadra_id):
        query = 'SELECT * from torneo t join squadra s on t.id = s.torneo_id where s.id = ?'
        cur = mysql.connection.cursor()
        try:
            cur.execute(query, (squadra_id,))
            rows = cur.fetchall()
            cur.close()
            return [Torneo(*row) for row in rows]
        except Exception as e:
            print(f"Errore durante la query: {e}")
            cur.close()
            return []

    @staticmethod
    def salva(torneo):
        query = 'INSERT INTO torneo (nome, sport_id, logo) VALUES ( %s, %s, %s)'
        cur = mysql.connection.cursor()
        try:
            cur.execute(query, (
                 
                torneo.nome,
                torneo.sport_id,
                torneo.logo
            ))
            mysql.connection.commit()
            torneo.id = cur.lastrowid
            cur.close()
            return True
        except Exception as e:
            print(f"Errore durante la query salva: {e}")
            mysql.connection.rollback()
            cur.close()
            return False

    @staticmethod
    def modifica(torneo):
        query = 'UPDATE torneo SET nome = %s WHERE id = %s'
        cur = mysql.connection.cursor()
        try:
            cur.execute(query, (torneo.nome, torneo.id))
            mysql.connection.commit()
            cur.close()
            return True
        except Exception as e:
            print(f"Errore durante la query: {e}")
            mysql.connection.rollback()
            cur.close()
            return False

    @staticmethod
    def elimina(torneo):
        query = 'DELETE FROM torneo WHERE id = %s'
        cur = mysql.connection.cursor()
        try:
            cur.execute(query, (torneo.id,))
            mysql.connection.commit()
            cur.close()
            return True
        except Exception as e:
            print(f"Errore durante la query: {e}")
            mysql.connection.rollback()
            cur.close()
            return False