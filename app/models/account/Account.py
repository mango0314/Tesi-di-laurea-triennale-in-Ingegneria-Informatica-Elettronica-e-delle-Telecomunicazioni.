class Account:
    def __init__(self, username = None, password = None, ruolo = None, id_Sq = None):
        
        self.username = username    # Nome utente (stringa)
        self.password = password    # Password (stringa)
        self.ruolo = ruolo          # Ruolo dell'account (stringa)
        self.id_Sq= id_Sq      # Squadra associata all'account (stringa)

    def __str__(self):
        return f"Account [ username={self.username}, password={self.password}, ruolo={self.ruolo}, id_Sq={self.id_Sq} ]"
    