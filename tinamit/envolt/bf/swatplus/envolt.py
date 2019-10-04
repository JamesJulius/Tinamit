from tinamit.envolt.bf import ModeloBF

class ModeloSWATPLUS(ModeloBF):
    idioma_orig = 'en'
    def __init__(símismo, variables, nombre = 'SWATPLUS'):
        símismo.variables = variables
        símismo.nombre = nombre
        símismo.corrida = 1
        símismo.vars_clima = {}

        super.__init__(variables,nombre)


    def unidad_tiempo(símismo):
        if STEP = 0: #we have to first import the variables file.
            return "Dias"
        else if STEP = 1:
            return "Incrementos"
        else if STEP = 24:
            return "Horas"
        else if STEP = 96:
            return "Incrementos de 15 minutos"
        else if STEP = 1440:
            return 'minutos'


    def incrementar(símismo, rebanada):


        super().incrementar(rebanada)

    def paralelizable(símismo):
        return True

    def iniciar_modelo(símismo, corrida):
        símismo.corrida=corrida

        super().iniciar_modelo(corrida)

    def cerrar(símismo):

    def _correr_hasta_final(símismo):
        return None
    #TODO


    @classmethod
    def instalado(cls):
        return True

    @classmethod
    def prb_egreso(cls):

    @classmethod
    def prb_ingreso(cls):

    @classmethod
    def prb_simul(cls):

#class method should be defined
