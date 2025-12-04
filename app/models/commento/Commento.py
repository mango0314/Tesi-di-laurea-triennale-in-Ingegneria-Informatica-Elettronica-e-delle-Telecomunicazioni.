class Commento:
    def __init__(self, id = None, nome = None, contenuto = None, scontro_id = None, created_at = None):
        self.id = id
        self.nome = nome
        self.contenuto = contenuto
        self.scontro_id = scontro_id
        self.created_at = created_at

    def __str__(self):
        return (f"Commento [id={self.id}, nome={self.nome}, contenuto={self.contenuto}, "
                f"scontro_id={self.scontro_id}, created_at={self.created_at}]")