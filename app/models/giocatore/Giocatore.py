class Giocatore:
    def __init__(self,id = None, nome = None, cognome = None, data_di_nascita= None, squadra_id = None, nomero_di_maglia= None):
        self.id = id
        self.nome = nome
        self.cognome = cognome
        self.data_di_nascita = data_di_nascita
        self.squadra_id = squadra_id
        self.numero_di_maglia = nomero_di_maglia
        
    def __str__(self):
        return f"Giocatore [id={self.id}, nome={self.nome}, cognome={self.cognome}, data_di_nascita={self.data_di_nascita}, squadra_id={self.squadra_id}, numero_di_maglia={self.numero_di_maglia}]"