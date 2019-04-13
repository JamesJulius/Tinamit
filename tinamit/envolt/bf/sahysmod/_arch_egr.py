import re

import numpy as np


def leer_arch_egr(archivo, n_est, n_polí, años):
    años = [años] if isinstance(años, int) else años

    dic_datos = {}
    for k, v in dic_datos.items():
        v[:] = -1

    with open(archivo, 'r') as d:

        for a in años:
            _avanzar_a_año(a, d)

            for e in range(1, n_est + 1):
                _avanzar_a_estación(e, d)

                for p in range(1, n_polí + 1):
                    _avanzar_a_polígono(p, d)

                    f = d.readline()

                    while not _fin_sección(f):

                        for var, val in _extraer_vars(f):
                            if var not in dic_datos:
                                dic_datos[var] = np.full((len(años), n_est, n_polí), np.nan)
                            if len(val):
                                dic_datos[var][a, e, p] = val

                        f = d.readline()

    return dic_datos


def procesar_cr(dic):
    # Estos variables, si faltan en el egreso, deberían ser 0 y no NaN
    for cr in ['CrA#', 'CrB#', 'CrU#', 'Cr4#', 'A#', 'B#', 'U#']:
        dic[cr][np.isnan(dic[cr])] = 0

    # Ajustar la salinidad por la presencia de varios cultivos
    kr = dic['Kr#']

    salin_suelo = np.zeros_like(dic['Kr#'])

    # Crear una máscara boleana para cada valor potencial de Kr y llenarlo con la salinidad correspondiente
    kr0 = (kr == 0)
    salin_suelo[kr0] = \
        dic['A#'][kr0] * dic['CrA#'][kr0] + dic['B#'][kr0] * dic['CrB#'][kr0] + dic['U#'][kr0] * dic['CrU#'][kr0]

    kr1 = (kr == 1)
    salin_suelo[kr1] = dic['CrU#'][kr1] * dic['U#'][kr1] + dic['C1*#'][kr1] * (1 - dic['U#'][kr1])

    kr2 = (kr == 2)
    salin_suelo[kr2] = dic['CrA#'][kr2] * dic['A#'][kr2] + dic['C2*#'][kr2] * (1 - dic['A#'][kr2])

    kr3 = (kr == 3)
    salin_suelo[kr3] = dic['CrB#'][kr3] * dic['B#'][kr3] + dic['C3*#'][kr3] * (1 - dic['B#'][kr3])

    kr4 = (kr == 4)
    salin_suelo[kr4] = dic['Cr4#'][kr4]

    para_llenar = [
        {'másc': kr0, 'cr': ['Cr4#']},
        {'másc': kr1, 'cr': ['CrA#', 'CrB#', 'Cr4#']},
        {'másc': kr2, 'cr': ['CrB#', 'CrU#', 'Cr4#']},
        {'másc': kr3, 'cr': ['CrA#', 'CrU#', 'Cr4#']},
        {'másc': kr4, 'cr': ['CrA#', 'CrB#', 'CrU#']}
    ]

    for d in para_llenar:
        l_cr = d['cr']
        másc = d['másc']

        for cr in l_cr:
            dic[cr][másc] = salin_suelo[másc]

    # Aseguarse que no quedamos con áreas que faltan
    for k in ["A", "B"]:
        dic[k][dic[k] == -1] = 0


def _avanzar_a_año(año, d):
    f = d.readline()
    while re.match(r'\W*YEAR:\W+%i\W' % año, f) is None:
        f = d.readline()


def _avanzar_a_estación(estación, d):
    f = d.readline()
    while re.match(r'\W*Season:\W+%i\W' % estación, f) is None:
        f = d.readline()


def _avanzar_a_polígono(polígono, d):
    f = d.readline()
    while re.match(r'\W*Polygon:\W+%i\W' % polígono, f) is None:
        f = d.readline()


def _fin_sección(f):
    return re.match(r' #$', f) is not None


def _extraer_vars(f):
    return re.search(r'([A-Za-z0-9*#]+)\W+=\W+([0-9.E\-]+)?', f)
