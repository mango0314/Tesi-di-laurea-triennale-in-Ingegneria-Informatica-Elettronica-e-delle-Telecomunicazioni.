class Squadra:
    def __init__(self, id= None, nome = None, torneo_id= None, logo= None):
        self.id = id                # Identificativo della squadra (int)
        self.nome = nome            # Nome della squadra (stringa)
        self.torneo_id = torneo_id    # Identificativo dello sport associato (int)
        self.logo = logo            # Logo della squadra (stringa, URL o percorso del file)

    def __str__(self):
        return f"Squadra [id={self.id}, nome={self.nome}, torneo_id={self.torneo_id}, logo={self.logo}]"