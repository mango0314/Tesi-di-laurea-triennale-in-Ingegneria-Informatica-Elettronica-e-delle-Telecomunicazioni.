class Torneo:
    def __init__(self, id= None, nome = None, sport_id = None,logo = None):
        self.id = id                # Identificativo del torneo (int)
        self.nome = nome            # Nome del torneo (stringa)
        self.sport_id = sport_id    # Identificativo dello sport associato (int)
        self.logo = logo            # Logo del torneo (stringa, URL o percorso del file)

    def __str__(self):
        return f"Torneo [id={self.id}, nome={self.nome}, sport_id={self.sport_id}, logo={self.logo}]"