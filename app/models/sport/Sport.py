class Sport:
    def __init__(self, id, nome):
        self.id = id          # Identificativo dello sport (int)
        self.nome = nome      # Nome dello sport (stringa)

    def __str__(self):
        return f"Sport [id={self.id}, nome={self.nome}]"