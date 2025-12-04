from flask import current_app
from app import mysql
from app.models.classifica.Classifica import Classifica

class ClassificaDAO:

    @staticmethod
    def get(classifica):
        query = 'SELECT * FROM classifica WHERE id = %s'

        cur = mysql.connection.cursor()
        try:
            cur.execute(query, (classifica.id))
            row = cur.fetchone()
            cur.close()
            if row:
                return Classifica(*row)
        except Exception as e:
            print(f"Errore durante la query: {e}")
            cur.close()
            return None
    
    @staticmethod
    def classificaEsiste(id_squadra, id_torneo):
        query = 'SELECT * FROM classifica WHERE id_squadra = %s AND id_torneo = %s'
        cur = mysql.connection.cursor()
        try:
            cur.execute(query, (id_squadra, id_torneo))
            row = cur.fetchone()
            cur.close()
            return row is not None
        except Exception as e:
            print(f"Errore durante la query: {e}")
            cur.close()
            return False




        
    @staticmethod
    def getAll():
        query = 'SELECT * FROM classifica'
        cur = mysql.connection.cursor()
        try:
            cur.execute(query)
            rows = cur.fetchall()
            cur.close()

            return [Classifica(*row) for row in rows]
        except Exception as e:
            print(f"Errore durante la query: {e}")
            cur.close()
            return []
        

    @staticmethod
    def getAllby_torneo_id(id_torneo):
        query = 'SELECT * FROM classifica where id_torneo = %s order by punteggio + bonus desc'
        cur = mysql.connection.cursor()
        try:
            cur.execute(query, (id_torneo,))
            rows = cur.fetchall()
            cur.close()

            return [Classifica(*row) for row in rows]
        except Exception as e:
            print(f"Errore durante la query: {e}")
            cur.close()
            return []
        
    @staticmethod
    def salva(classifica):
        query = ' INSERT INTO classifica (id_squadra, punteggio, id_torneo, pareggi, sconfitte, media, bonus) VALUES (%s, %s, %s, %s, %s, %s, %s)' \
        ' ON DUPLICATE KEY UPDATE id_squadra = values(id_squadra), punteggio = values(punteggio), id_torneo = values(id_torneo), pareggi = values(pareggi), sconfitte = values(sconfitte), media = values(media), bonus = values(bonus)'
        cur = mysql.connection.cursor()
        try:
            cur.execute(query, (classifica.id_squadra, classifica.punteggio, classifica.id_torneo, classifica.pareggi, classifica.sconfitte, classifica.media, classifica.bonus))
            mysql.connection.commit()
            cur.close()
            return True
        except Exception as e:
            print(f"Errore durante la query: {e}")
            mysql.connection.rollback()
            cur.close()
            return False
        
    @staticmethod
    def modifica(classifica):
        query = 'UPDATE classifica SET punteggio = %s, id_torneo = %s, vittorie = %s, pareggi = %s, sconfitte = %s, media = %s, bonus = %s WHERE id_squadra = %s'
        cur = mysql.connection.cursor()
        try:
            cur.execute(query, (classifica.punteggio, classifica.id_torneo, classifica.vittorie, classifica.pareggi, classifica.sconfitte, classifica.media, classifica.bonus, classifica.id_squadra))
            mysql.connection.commit()
            cur.close()
            return True
        except Exception as e:
            print(f"Errore durante la query: {e}")
            mysql.connection.rollback()
            cur.close()
            return False
        
    @staticmethod
    def modificaPunteggio(c):
        query = 'UPDATE classifica SET punteggio = %s WHERE id_squadra = %s'
        cur = mysql.connection.cursor()
        try:
            cur.execute(query, (c.punteggio, c.id_squadra))
            mysql.connection.commit()
            cur.close()
            return True
        except Exception as e:
            print(f"Errore durante la query: {e}")
            mysql.connection.rollback()
            cur.close()
            return False
        
    @staticmethod
    def getBonus(id_squadra, id_torneo):
        query = 'SELECT bonus FROM classifica WHERE id_squadra = %s AND id_torneo = %s'
        cur = mysql.connection.cursor()
        try:
            cur.execute(query, (id_squadra, id_torneo))
            row = cur.fetchone()
            cur.close()
            if row:
                return row[0]
            return 0
        except Exception as e:
            print(f"Errore durante la query: {e}")
            cur.close()
            return 0
        
    @staticmethod
    def updatePunteggi(lista_classifica):
        query = 'UPDATE classifica SET punteggio = %s, vittorie = %s, punteggi = %s, sconfitte = %s WHERE id_squadra = %s AND id_torneo = %s'
        cur = mysql.connection.cursor()
        try:
            for c in lista_classifica:
                cur.execute(query, (c.punteggio, c.vittorie, c.pareggi, c.sconfitte, c.id_squadra, c.id_torneo))
            mysql.connection.commit()
            cur.close()
            return True
        except Exception as e:
            print(f"Errore durante la query: {e}")
            mysql.connection.rollback()
            cur.close()
            return False
        
    @staticmethod
    def updateBonus(id_squadra, id_torneo, bonus):
        query = 'UPDATE classifica SET bonus = %s WHERE id_squadra = %s AND id_torneo = %s'
        cur = mysql.connection.cursor()
        try:
            cur.execute(query, (bonus, id_squadra, id_torneo))
            mysql.connection.commit()
            cur.close()
            return True
        except Exception as e:
            print(f"Errore durante la query: {e}")
            mysql.connection.rollback()
            cur.close()
            return False
        
    @staticmethod
    def updatePunteggioBonus(id_squadra, id_torneo, punteggio, bonus):
        query = 'UPDATE classifica SET punteggio = %s, bonus = %s WHERE id_squadra = %s AND id_torneo = %s'
        cur = mysql.connection.cursor()
        try:
            cur.execute(query, (punteggio, bonus, id_squadra, id_torneo))
            mysql.connection.commit()
            cur.close()
            return True
        except Exception as e:
            print(f"Errore durante la query: {e}")
            mysql.connection.rollback()
            cur.close()
            return False
        
    @staticmethod
    def updatePunteggieStatistiche(lista_classifica):
        query = 'UPDATE classifica SET punteggio = %s, vittorie = %s, pareggi = %s, sconfitte = %s, media = %s WHERE id_squadra = %s AND id_torneo = %s'
        cur = mysql.connection.cursor()
        try:
            for c in lista_classifica:
                cur.execute(query, (c.punteggio, c.vittorie, c.pareggi, c.sconfitte, c.id_squadra, c.id_torneo))
            mysql.connection.commit()
            cur.close()
            return True
        except Exception as e:
            print(f"Errore durante la query: {e}")
            mysql.connection.rollback()
            cur.close()
            return False
        
    @staticmethod
    def elimina(classifica):
        query = 'DELETE FROM classifica WHERE id_squadra = %s'
        cur = mysql.connection.cursor()
        try:
            cur.execute(query, (classifica.id_squadra,))
            mysql.connection.commit()
            cur.close()
            return True
        except Exception as e:
            print(f"Errore durante la query: {e}")
            mysql.connection.rollback()
            cur.close()
            return False
