from flask import current_app
from app import mysql
from app.models.account.Account import Account

class AccountDAO:

    @staticmethod
    def get(account):
        query = 'SELECT * FROM account WHERE username = %s'

        cur = mysql.connection.cursor()
        try:
            cur.execute(query, (account.username))
            row = cur.fetchone()
            cur.close()
            if row:
                return Account(*row)
        except Exception as e:
            print(f"Errore durante la query: {e}")
            cur.close()
            return None
        
    @staticmethod
    def getbyUsername(username):
        query = 'SELECT * FROM account WHERE username = %s'
        cur = mysql.connection.cursor()
        try:
            cur.execute(query, (username,))
            row = cur.fetchone()
            cur.close()
            if row:
                return Account(*row)
            else:
                return None
        except Exception as e:
            print(f"Errore durante la query: {e}")
            cur.close()
            return None
        
    @staticmethod
    def getbyUsername_Password(username, password):
        query = 'SELECT * FROM account WHERE username = %s and BINARY password = %s'
        cur = mysql.connection.cursor()
        try:
            cur.execute(query, (username,password,))
            row = cur.fetchone()
            cur.close()
            if row:
                return Account(*row)
            else:
                return None
        except Exception as e:
            print(f"Errore durante la query: {e}")
            cur.close()
            return None
    
    @staticmethod
    def getEsiste(account):
        query = 'SELECT * FROM account WHERE username = %s'
        cur = mysql.connection.cursor()
        try:
            cur.execute(query, (account.username,))
            exists = cur.fetchone() is not None   
            cur.close()
            return exists
        except Exception as e:
            print(f"Errore durante la query: {e}")
            cur.close()
            return False
        
    @staticmethod
    def getEsistebypassword(account):
        query = 'SELECT * FROM account WHERE username = %s AND BINARY password = %s'
        cur = mysql.connection.cursor()
        try:
            cur.execute(query, (account.username, account.password))
            exists = cur.fetchone() is not None
            cur.close()
            return exists
        except Exception as e:
            print(f"Errore durante la query: {e}")
            cur.close()
            return False
        
    @staticmethod
    def get_ruolo(username,password):
        query = ' SELECT ruolo FROM account WHERE username = %s AND BINARY password = %s'
        cur = mysql.connection.cursor()
        try:
            cur.execute(query, (username,password))
            row=cur.fetchone()
            cur.close()
            if row:
                return row[0]
            else:
                return -1
        except Exception as e:
            print(f"Errore durante la query: {e}")
            cur.close()
            return -1
        
    @staticmethod
    def getSq(username, password):
        query = ' SELECT id_Sq FROM account WHERE username = %s AND BINARY password = %s'
        cur = mysql.connection.cursor()
        try:
            cur.execute(query,(username, password))
            row= cur.fetchone()
            cur.close()
            if row:
                return row[0] 
            else:
                return -1
            
        except Exception as e:
            print(f"Errore durante la query: {e}")
            cur.close()
            return -1
        
    @staticmethod
    def getUsername():
        query = 'SELECT username FROM account'
        cur = mysql.connection.cursor()
        try:
            cur.execute(query)
            rows = cur.fetchall()
            cur.close()

            return [row[0] for row in rows]
        except Exception as e:
            print(f"Errore durante la query di getUsername: {e}")
            cur.close()
            return []
        
    @staticmethod
    def getAll():
        query = 'SELECT * FROM account'
        cur = mysql.connection.cursor()
        try:
            cur.execute(query)
            rows = cur.fetchall()
            cur.close()

            return [Account(*row) for row in rows]
        except Exception as e:
            print(f"Errore durante la query: {e}")
            cur.close()
            return []
        
    @staticmethod
    def salva(account):
        query = ' INSERT INTO account (username, password, ruolo, id_Sq) VALUES (%s, %s, %s, %s)'
        cur = mysql.connection.cursor()
        try:
            print(f"[AccountDAO] Salvo account: username={account.username}, ruolo={account.ruolo}, squadra_id={account.id_Sq}")
            cur.execute(query, (account.username, account.password, account.ruolo, account.id_Sq))
            print("[AccountDAO] Execute OK, commit in arrivo")
            mysql.connection.commit()
            cur.close()
            return True
        except Exception as e:
            print(f"Errore durante la query: {e}")
            mysql.connection.rollback()
            cur.close()
            return False
        
    @staticmethod
    def modifica(account):
        query = 'UPDATE account SET password = %s, ruolo = %s, id_Sq = %s WHERE username = %s'
        cur = mysql.connection.cursor()
        try:
            cur.execute(query, ( account.password, account.ruolo, account.id_Sq, account.username))
            mysql.connection.commit()
            cur.close()
            return True
        except Exception as e:
            print(f"Errore durante la query: {e}")
            mysql.connection.rollback()
            cur.close()
            return False
        
    @staticmethod
    def elimina(account):
        query = 'DELETE FROM account WHERE id = %s'
        cur = mysql.connection.cursor()
        try:
            cur.execute(query, (account.id,))
            mysql.connection.commit()
            cur.close()
            return True
        except Exception as e:
            print(f"Errore durante la query: {e}")
            mysql.connection.rollback()
            cur.close()
            return False
