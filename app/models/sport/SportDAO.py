from flask import current_app
from app import mysql
from app.models.sport.Sport import Sport


class SportDAO:

    @staticmethod
    def get(sport):
        query = 'SELECT * FROM sport WHERE id = %s'

        cur = mysql.connection.cursor()
        try:
            cur.execute(query, (sport.id,))
            row = cur.fetchone()
            cur.close()
            if row:
                return Sport(*row)
        except Exception as e:
            print(f"Errore durante la query: {e}")
            cur.close()
            return None
        
    @staticmethod
    def get_all():
        query = 'SELECT * FROM sport order by id'
        cur = mysql.connection.cursor()
        try:
            cur.execute(query)
            rows = cur.fetchall()
            cur.close()

            return [Sport(*row) for row in rows]
        except Exception as e:
            print(f"Errore durante la query: {e}")
            cur.close()
            return []
        

        
    