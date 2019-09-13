import os

from tinamit.envolt.bf import ModeloBF


class ModeloSWATPLUS(ModeloBF):
    """
    Envoltura para modelos SWAT+.
    """

    idioma_orig = 'en'  # La lengua de los nombres y descripción de los variables (y NO la del código aquí)

    def __init__(símismo, archivo, nombre='SWAT+'):

        símismo.archivo = archivo

        símismo.direc_trabajo = ''

        # Buscar la ubicación del modelo SWAT+.
        símismo.exe_SWATPLUS = símismo.obt_conf(
            'exe',
            cond=os.path.isfile,
            mnsj_err=_(
                'Debes especificar la ubicación del ejecutable SWATPLUS, p. ej.'
                '\n\tModeloSWATPLUS.estab_conf("exe", "C:\\Camino\\hacia\\mi\\SWATPLUSConsole.exe")'
                '\npara poder hacer simulaciones con modelos SWATPLUS.'
            )
        )

        variables = VariablesSWATPLUS(inic=símismo.dic_ingr)

        # Inicializar la clase pariente.
        super().__init__(variables, nombre=nombre)

    def incrementar(símismo, rebanada):
        super().incrementar(rebanada)

    def unidad_tiempo(símismo):
        return 'dias' #days
        return 'horas' #hours
        return 'Intervalos de 15 minutos' #15 minute intervals
        return 'minutos' #minutes
        return 'incrementos' #increments

