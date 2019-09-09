from tinamit.envolt.bf import ModeloBF


class ModeloSwatPlus(ModeloBF):
    def __init__(símismo, archivo, nombre='SWAT+'):
        super().__init__(variables, nombre=nombre)

    def incrementar(símismo, rebanada):
        super().incrementar(rebanada)

    def unidad_tiempo(símismo):
        return 'mes' #months
