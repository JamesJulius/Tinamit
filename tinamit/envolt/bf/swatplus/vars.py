from tinamit.mod.var import Variable
from tinamit.mod.vars_mod import VariablesMod

class VarSWATPLUS(Variable):
    def __init__(símismo, nombre, unid, ingr, egr, inic=0, líms=None, info=''):

class VarModBFSWATPLUS(VarSWATPLUS):


class VariablesSAHYSMOD(VariablesMod):
    def


info_vars = {
'harv_bm_min':{'nombre':'Minimum biomass to allow harvest','unid':'kg/ha','ingr':True,'egr':True},
'lat_sed':{'nombre':'Sediment concentration in lateral flow','unid':'g/L','ingr':True,'egr':True},
'min_n':{'nombre':'Inorganic N in soil surface','unid':'ppm','ingr':True,'egr':True},
'bm_e':{'nombre':'Biomass-energy ratio','unid':'(kg/ha)/(MJ/m2)','ingr':True,'egr':True},
'drain':{'nombre':'Drainage coefficient','unid':'mm/day','ingr':True,'egr':True},
'tmp_max_ave':{'nombre':'The average or mean daily maximum air temperature','unid':'C','ingr':True,'egr':True},
'spec_yld':{'nombre':'Specific yield for shallow aquifer','unid':'m3/m3','ingr':True,'egr':True},
'no3_n':{'nombre':'Nitrate concentration in shallow aquifer converted to kg/ha','unid':'ppm NO3-N','ingr':True,'egr':True},
'lat_orgn':{'nombre':'Organic N concentration in lateral flow','unid':'mg/L','ingr':True,'egr':True},
'amt_mm':{'nombre':'Irrigation amount','unid':'mm','ingr':True,'egr':True}
}