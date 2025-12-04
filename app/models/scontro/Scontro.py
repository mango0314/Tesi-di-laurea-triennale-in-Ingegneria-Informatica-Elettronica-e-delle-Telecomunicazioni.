class Scontro:
    def __init__(self,id= None , torneo_id = None, squadra1_id = None, squadra2_id = None, punteggio1 = None, punteggio2 = None, data = None, orario =None):
        self.id = id
        self.torneo_id = torneo_id
        self.squadra1_id = squadra1_id
        self.squadra2_id = squadra2_id
        
        self.punteggio1 = punteggio1
        self.punteggio2 = punteggio2
        self.data = data
        self.orario = orario

    def __str__(self):
        return f"Scontro [id={self.id},  torneo_id={self.torneo_id}, squadra1_id={self.squadra1_id}, squadra2_id={self.squadra2_id}, punteggio1={self.punteggio1}, punteggio2={self.punteggio2}, data={self.data}, orario={self.orario}]"
