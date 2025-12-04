class Classifica:
    def __init__(self, id_squadra=None, punteggio=0, id_torneo=None, vittorie=0, pareggi=0, sconfitte=0, media=0.0, bonus=0):
        self.id_squadra = id_squadra
        self.punteggio = punteggio
        self.id_torneo = id_torneo
        self.vittorie = vittorie
        self.pareggi = pareggi
        self.sconfitte = sconfitte
        self.media = media
        self.bonus = bonus

    def __str__(self):
        return (f"Classifica [id_squadra={self.id_squadra}, punteggio={self.punteggio}, id_torneo={self.id_torneo}, "
                f"vittorie={self.vittorie}, pareggi={self.pareggi}, sconfitte={self.sconfitte}, "
                f"media={self.media}, bonus={self.bonus}]")

    def get_punteggio_totale(self):
        return self.punteggio + self.bonus