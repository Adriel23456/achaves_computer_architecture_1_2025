class PipeLine:

#TODO>>>>>> el hazard unit tiene las condiciones para checkear cuando hacer los stalls y lo demas, faltan las definiciones de pipelines que tienen los argumentos que estos condicionales necesitan, tratar de implementarlos para que el control de riesgos funcione
    def __init__(self):
        self.stall = False

    def stall(self):
        self.stall = True
        return None

