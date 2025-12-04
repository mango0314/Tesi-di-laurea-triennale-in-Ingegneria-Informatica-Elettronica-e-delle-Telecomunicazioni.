from flask import current_app
from app import mysql
from app.models.squadra.Squadra import Squadra

class SquadraDAO:

    @staticmethod
    def get(squadra):
        query = 'SELECT * FROM squadra WHERE id = %s'
        cur = mysql.connection.cursor()
        try:
            cur.execute(query, (squadra.id,))
            row = cur.fetchone()
            cur.close()
            if row:
                return Squadra(*row)
        except Exception as e:
            print(f"Errore durante la query: {e}")
            cur.close()
            return None
        
    @staticmethod
    def getbyId(id):
        query = 'SELECT * FROM squadra WHERE id = %s'
        cur = mysql.connection.cursor()
        try:
            cur.execute(query, (id,))
            row = cur.fetchone()
            cur.close()
            if row:
                return Squadra(*row)
        except Exception as e:
            print(f"Errore durante la query: {e}")
            cur.close()
            return None
        
    @staticmethod
    def getNome(squadra_id):
        query = 'SELECT nome FROM squadra where id = %s'
        cur = mysql.connection.cursor()
        try:
            cur.execute(query, (squadra_id,))
            row = cur.fetchone()
            cur.close()
            if row:
                return row[0]
        except Exception as e:
            print(f"Errore durante la query in getnomi: {e}")
            cur.close()
            return []
        
    @staticmethod
    def getNomi():
        query = 'SELECT nome FROM squadra'
        cur = mysql.connection.cursor()
        try:
            cur.execute(query)
            rows = cur.fetchall()
            cur.close()
            return [row[0] for row in rows]
        except Exception as e:
            print(f"Errore durante la query in getnomi: {e}")
            cur.close()
            return []
        
    @staticmethod
    def getbyTorneoId(torneo_id):
        query = 'SELECT * FROM squadra WHERE torneo_id = %s'
        cur = mysql.connection.cursor()
        try:
            cur.execute(query, (torneo_id,))
            row = cur.fetchone()
            cur.close()
            if row:
                return Squadra(*row)
        except Exception as e:
            print(f"Errore durante la query: {e}")
            cur.close()
            return None
        
    @staticmethod
    def getUltimoId():
        query = 'SELECT id FROM squadra ORDER BY id DESC LIMIT 1'
        cur = mysql.connection.cursor()
        try:
            cur.execute(query)
            row = cur.fetchone()
            cur.close()
            if row:
                return row[0]
        except Exception as e:
            print(f"Errore durante la query di getUltimoId: {e}")
            cur.close()
            return -1

    @staticmethod
    def getAll():
        query = 'SELECT * FROM squadra ORDER BY id'
        cur = mysql.connection.cursor()
        try:
            cur.execute(query)
            rows = cur.fetchall()
            cur.close()
            return [Squadra(*row) for row in rows]
        except Exception as e:
            print(f"Errore durante la query: {e}")
            cur.close()
            return []

    @staticmethod
    def getAllby_torneo_id(torneo_id):
        query = 'SELECT * FROM squadra WHERE torneo_id = %s ORDER BY id'
        cur = mysql.connection.cursor()
        try:
            cur.execute(query, (torneo_id,))
            rows = cur.fetchall()
            cur.close()
            return [Squadra(*row) for row in rows]
        except Exception as e:
            print(f"Errore durante la query: {e}")
            cur.close()
            return []



    @staticmethod
    def salva(squadra):
    # Inserisco solo nome, torneo_id e logo (id viene gestito da MySQL come AUTO_INCREMENT)
        query = 'INSERT INTO squadra (nome, torneo_id, logo) VALUES (%s, %s, %s)'
        cur = mysql.connection.cursor()
        try:
            # Gestione del campo torneo_id che può essere None (NULL in MySQL)
            cur.execute(query, (
                squadra.nome,
                squadra.torneo_id if squadra.torneo_id is not None else None,
                squadra.logo
            ))
            mysql.connection.commit()
            # Recupero l'id generato da MySQL
            squadra.id = cur.lastrowid
            cur.close()
            return True
        except Exception as e:
            print(f"Errore durante la query: {e}")
            mysql.connection.rollback()
            cur.close()
            return False

    @staticmethod
    def modifica(squadra):
        query = 'UPDATE squadra SET nome = %s, torneo_id = %s, logo = %s WHERE id = %s'
        cur = mysql.connection.cursor()
        try:
            cur.execute(query, (squadra.nome, squadra.torneo_id, squadra.logo, squadra.id))
            mysql.connection.commit()
            cur.close()
            return True
        except Exception as e:
            print(f"Errore durante la query: {e}")
            mysql.connection.rollback()
            cur.close()
            return False

    @staticmethod
    def elimina(squadra):
        query = 'DELETE FROM squadra WHERE id = %s'
        cur = mysql.connection.cursor()
        try:
            cur.execute(query, (squadra.id,))
            mysql.connection.commit()
            cur.close()
            return True
        except Exception as e:
            print(f"Errore durante la query: {e}")
            mysql.connection.rollback()
            cur.close()
            return False