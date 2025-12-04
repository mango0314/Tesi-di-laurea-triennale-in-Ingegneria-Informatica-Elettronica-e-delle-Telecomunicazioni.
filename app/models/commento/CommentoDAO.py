from flask import current_app
from app import mysql
from app.models.commento.Commento import Commento

class CommentoDAO:

    @staticmethod
    def get(commento):
        query = 'SELECT * FROM commento WHERE id = %s'
        cur = mysql.connection.cursor()
        try:
            cur.execute(query, (commento.id,))
            row = cur.fetchone()
            cur.close()
            if row:
                return Commento(*row)
        except Exception as e:
            print(f"Errore durante la query: {e}")
            cur.close()
            return None
        
    @staticmethod
    def getById(id):
        query = 'SELECT * FROM commento WHERE id = %s'
        cur = mysql.connection.cursor()
        try:
            cur.execute(query, (id,))
            row = cur.fetchone()
            cur.close()
            if row:
                return Commento(*row)
        except Exception as e:
            print(f"Errore durante la query: {e}")
            cur.close()
            return None
 
 

    @staticmethod
    def getAll():
        query = 'SELECT * FROM commento'
        cur = mysql.connection.cursor()
        try:
            cur.execute(query)
            rows = cur.fetchall()
            cur.close()
            return [Commento(*row) for row in rows]
        except Exception as e:
            print(f"Errore durante la query: {e}")
            cur.close()
            return []

    @staticmethod
    def getAllby_Scontro(scontro_id):
        query = 'SELECT * FROM commento WHERE scontro_id = %s ORDER BY id'
        cur = mysql.connection.cursor()
        try:
            cur.execute(query, (scontro_id,))
            rows = cur.fetchall()
            cur.close()
            return [Commento(*row) for row in rows]
        except Exception as e:
            print(f"Errore durante la query: {e}")
            cur.close()
            return []
        
    @staticmethod
    def getCount(scontro_id):
        query='SELECT count(id) as numero_commenti from commento WHERE scontro_id = %s '
        cur = mysql.connection.cursor()
        try:
            cur.execute(query, (scontro_id,))
            row = cur.fetchone()
            cur.close()
            if row:
                return row[0]
        except Exception as e:
            print(f"Errore durante la query: {e}")
            cur.close()
            return None
        
    @staticmethod
    def get_by_scontro_paginated(scontro_id, page=1, per_page=10):
                """
                Pagina i commenti per scontro usando LIMIT/OFFSET.
                Ritorna (items_list_of_Commento, total_count).
                - page è 1-based
                - per_page default 10 (modificabile)
                """
                try:
                    page = max(1, int(page))
                    per_page = max(1, int(per_page))
                except (ValueError, TypeError):
                    page = 1
                    per_page = 10

                offset = (page - 1) * per_page

                # conta totale (esclude eventuali soft-deleted se presenti)
                count_sql = 'SELECT COUNT(*) FROM commento WHERE scontro_id = %s'
                select_sql = (
                    'SELECT * FROM commento '
                    'WHERE scontro_id = %s '
                    'ORDER BY id DESC '          # restituisce primi i più recenti; cambia se preferisci altro ordine
                    'LIMIT %s OFFSET %s'
                )

                cur = mysql.connection.cursor()
                try:
                    cur.execute(count_sql, (scontro_id,))
                    row = cur.fetchone()
                    total = int(row[0]) if row else 0

                    cur.execute(select_sql, (scontro_id, per_page, offset))
                    rows = cur.fetchall()
                    # mappa ogni row su oggetto Commento (assumendo costruttore Commento(*row) come usi altrove)
                    items = [Commento(*r) for r in rows] if rows else []
                    return items, total
                except Exception as e:
                    current_app.logger.exception(f"Errore get_by_scontro_paginated scontro_id={scontro_id}")
                    return [], 0
                finally:
                    try:
                        cur.close()
                    except:
                        pass

        

    @staticmethod
    def salva(commento):
        insert_sql = 'INSERT INTO commento ( nome, contenuto, scontro_id) VALUES ( %s, %s, %s)' 
        select_sql = 'SELECT created_at from commento where id=%s'
        cur = mysql.connection.cursor()
        try:
            cur.execute(insert_sql, (commento.nome, commento.contenuto, commento.scontro_id))
            mysql.connection.commit()
            commento.id = cur.lastrowid  # Imposta l'ID generato automaticamente
            cur.execute(select_sql, (commento.id,))
            row = cur.fetchone()
            if row:
                return row[0]
            cur.close()
            return True
        except Exception as e:
            print(f"Errore durante la query salva commento: {e}")
            mysql.connection.rollback()
            cur.close()
            return False

    @staticmethod
    def modifica(commento):
        query = 'UPDATE commento SET nome = %s, contenuto = %s, scontro_id = %s, created_at WHERE id = %s'
        cur = mysql.connection.cursor()
        try:
            cur.execute(query, (commento.nome, commento.contenuto, commento.scontro_id, commento.created_at, commento.id))
            mysql.connection.commit()
            cur.close()
            return True
        except Exception as e:
            print(f"Errore durante la query: {e}")
            mysql.connection.rollback()
            cur.close()
            return False

    @staticmethod
    def elimina(commento):
        query = 'DELETE FROM commento WHERE id = %s'
        cur = mysql.connection.cursor()
        try:
            cur.execute(query, (commento.id,))
            mysql.connection.commit()
            cur.close()
            return True
        except Exception as e:
            print(f"Errore durante la query: {e}")
            mysql.connection.rollback()
            cur.close()
            return False
