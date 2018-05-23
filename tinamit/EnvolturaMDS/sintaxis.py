import math as mat

import numpy as np
import regex
import theano
from lark import Lark, Transformer
from pkg_resources import resource_filename

from tinamit import _

try:
    import pymc3 as pm
except ImportError:
    pm = None


l_dialectos_potenciales = [resource_filename('tinamit.EnvolturaMDS', 'gram_ec_tinamït.g')]


def cortar_líns(texto, máx_car, lín_1=None, lín_otras=None):
    lista = []

    while len(texto):
        if len(texto) <= máx_car:
            l = texto
        else:
            dif = máx_car - texto

            l = regex.search(r'(.*)\W.[%s,]' % dif, texto).groups()[0]

        lista.append(l)
        texto = texto[len(l):]

    if lín_1 is not None:
        lista[0] = lín_1 + lista[0]

    if lín_otras is not None:
        for n, l in enumerate(lista[1:]):
            lista[n] = lín_otras + l

    return lista


class _Transformador(Transformer):
    @staticmethod
    def num(x):
        return float(x[0])

    @staticmethod
    def neg(x):
        return {'neg': x[0]}

    @staticmethod
    def var(x):
        return {'var': x[0]}

    @staticmethod
    def nombre(x):
        return str(x[0])

    @staticmethod
    def cadena(x):
        return str(x[0])

    @staticmethod
    def func(x):
        return {'func': x}

    @staticmethod
    def pod(x):
        return {'func': ['^', x]}

    @staticmethod
    def mul(x):
        return {'func': ['*', x]}

    @staticmethod
    def div(x):
        return {'func': ['/', x]}

    @staticmethod
    def suma(x):
        return {'func': ['+', x]}

    @staticmethod
    def sub(x):
        return {'func': ['-', x]}

    args = list
    ec = list


class Ecuación(object):
    def __init__(símismo, ec, dialecto=None):
        símismo.ec = ec

        if dialecto is None:
            dialecto = l_dialectos_potenciales
        elif isinstance(dialecto, str):
            dialecto = [dialecto]

        anlzdr = None
        errores = []
        for dial in dialecto:
            try:
                with open(dial) as gm:
                    anlzdr = Lark(gm, parser='lalr', start='ec')
                símismo.árbol = _Transformador().transform(anlzdr.parse(ec))[0]
                símismo.dialecto = dial.lower()
                break
            except BaseException as e:
                errores.append(e)
        if anlzdr is None:
            raise ValueError('Error en la ecuación "{}". Detalles: {}'.format(ec, errores))

    def variables(símismo):

        def _obt_vars(á):
            if isinstance(á, dict):

                for ll, v in á.items():

                    if ll == 'func':
                        if v[0] in ['+', '-', '/', '*', '^']:
                            vrs = _obt_vars(v[1][0])
                            vrs.update(_obt_vars(v[1][1]))

                            return vrs

                        else:
                            return set([i for x in v[1] for i in _obt_vars(x)])

                    elif ll == 'var':
                        return {v}

                    elif ll == 'neg':
                        return set()

                    else:
                        raise TypeError('')

            elif isinstance(á, list):
                return {z for x in á for z in _obt_vars(x)}
            elif isinstance(á, int) or isinstance(á, float):
                return set()
            else:
                raise TypeError('{}'.format(type(á)))

        return _obt_vars(símismo.árbol)

    def gen_func_python(símismo, paráms, otras_ecs=None):

        if otras_ecs is None:
            otras_ecs = {}

        dialecto = símismo.dialecto

        def _a_python(á, l_prms=paráms):

            if isinstance(á, dict):

                for ll, v in á.items():

                    if ll == 'func':

                        if v[0] == '+':
                            comp_1 = _a_python(v[1][0], l_prms=l_prms)
                            comp_2 = _a_python(v[1][1], l_prms=l_prms)
                            return lambda p, vr: comp_1(p=p, vr=vr) + comp_2(p=p, vr=vr)
                        elif v[0] == '/':
                            comp_1 = _a_python(v[1][0], l_prms=l_prms)
                            comp_2 = _a_python(v[1][1], l_prms=l_prms)
                            return lambda p, vr: comp_1(p=p, vr=vr) / comp_2(p=p, vr=vr)
                        elif v[0] == '-':
                            comp_1 = _a_python(v[1][0], l_prms=l_prms)
                            comp_2 = _a_python(v[1][1], l_prms=l_prms)
                            return lambda p, vr: comp_1(p=p, vr=vr) - comp_2(p=p, vr=vr)
                        elif v[0] == '*':
                            comp_1 = _a_python(v[1][0], l_prms=l_prms)
                            comp_2 = _a_python(v[1][1], l_prms=l_prms)
                            return lambda p, vr: comp_1(p=p, vr=vr) * comp_2(p=p, vr=vr)
                        elif v[0] == '^':
                            comp_1 = _a_python(v[1][0], l_prms=l_prms)
                            comp_2 = _a_python(v[1][1], l_prms=l_prms)
                            return lambda p, vr: comp_1(p=p, vr=vr) ** comp_2(p=p, vr=vr)
                        else:
                            fun = conv_fun(v[0], dialecto, 'python')
                            comp = _a_python(v[1][1], l_prms=l_prms)

                            return lambda p, vr: fun(*comp(p=p, vr=vr))

                    elif ll == 'var':
                        try:
                            í_var = l_prms.index(v)

                            return lambda p, vr: p[í_var]

                        except ValueError:
                            # Si el variable no es un parámetro calibrable, debe ser un valor observado, al menos
                            # que esté espeficado por otra ecuación.
                            if v in otras_ecs:

                                ec = otras_ecs[v]
                                if isinstance(ec, Ecuación):
                                    árb = ec.árbol
                                else:
                                    árb = Ecuación(ec).árbol
                                return _a_python(á=árb, l_prms=l_prms)

                            else:
                                return lambda p, vr: vr[v]

                    elif ll == 'neg':
                        comp = _a_python(v[1][1], l_prms=l_prms)
                        return lambda p, vr: -comp(p=p, vr=vr)
                    else:
                        raise TypeError('')

            elif isinstance(á, list):
                return [_a_python(x) for x in á]
            elif isinstance(á, int) or isinstance(á, float):
                return lambda p, vr: á
            else:
                raise TypeError('{}'.format(type(á)))

        return _a_python(símismo.árbol)

    def gen_mod_bayes(símismo, paráms, líms_paráms, obs_x, obs_y, aprioris=None, binario=False, otras_ecs=None):

        if pm is None:
            return ImportError(_('Hay que instalar PyMC3 para poder utilizar modelos bayesianos.'))

        if obs_x is None:
            obs_x = {}
        if obs_y is None:
            obs_y = {}

        if otras_ecs is None:
            otras_ecs = {}

        dialecto = símismo.dialecto

        d_vars_obs = {}

        def _a_bayes(á, d_pm=None):
            if d_pm is None:
                d_pm = {}

            if isinstance(á, dict):

                for ll, v in á.items():

                    if ll == 'func':

                        if v[0] == '+':
                            return _a_bayes(v[1][0], d_pm=d_pm) + _a_bayes(v[1][1], d_pm=d_pm)
                        elif v[0] == '/':
                            return _a_bayes(v[1][0], d_pm=d_pm) / _a_bayes(v[1][1], d_pm=d_pm)
                        elif v[0] == '-':
                            return _a_bayes(v[1][0], d_pm=d_pm) - _a_bayes(v[1][1], d_pm=d_pm)
                        elif v[0] == '*':
                            return _a_bayes(v[1][0], d_pm=d_pm) * _a_bayes(v[1][1], d_pm=d_pm)
                        elif v[0] == '^':
                            return _a_bayes(v[1][0], d_pm=d_pm) ** _a_bayes(v[1][1], d_pm=d_pm)
                        else:
                            return conv_fun(v[0], dialecto, 'pm')(
                                *_a_bayes(v[1], d_pm=d_pm))

                    elif ll == 'var':
                        try:
                            if v in d_pm:
                                return d_pm[v]
                            else:
                                í_var = paráms.index(v)
                                líms = líms_paráms[í_var]

                                if aprioris is None:
                                    if líms[0] is None:
                                        if líms[1] is None:
                                            dist_pm = pm.Flat(v, testval=0)
                                        else:
                                            dist_pm = líms[1] - pm.HalfFlat(v, testval=1)
                                    else:
                                        if líms[1] is None:
                                            dist_pm = líms[0] + pm.HalfFlat(v, testval=1)
                                        else:
                                            dist_pm = pm.Uniform(name=v, lower=líms[0], upper=líms[1])
                                else:
                                    dist, prms = aprioris[í_var]
                                    if (líms[0] is not None or líms[1] is not None) and dist != pm.Uniform:
                                        acotada = pm.Bound(dist, lower=líms[0], upper=líms[1])
                                        dist_pm = acotada(v, **prms)
                                    else:
                                        if dist == pm.Uniform:
                                            prms['lower'] = max(prms['lower'], líms[0])
                                            prms['upper'] = min(prms['upper'], líms[1])
                                        dist_pm = dist(v, **prms)

                                d_pm[v] = dist_pm
                                return dist_pm

                        except ValueError:

                            # Si el variable no es un parámetro calibrable, debe ser un valor observado, al menos
                            # que haya otra ecuación que lo describa
                            if v in otras_ecs:
                                ec = otras_ecs[v]
                                if isinstance(ec, Ecuación):
                                    árb = ec.árbol
                                else:
                                    árb = Ecuación(ec).árbol
                                return _a_bayes(á=árb, d_pm=d_pm)

                            else:
                                # Si no se especificó otra ecuación para este variable, debe ser un valor observado.
                                try:
                                    return obs_x[v]
                                except KeyError:
                                    d_vars_obs[v] = theano.shared()
                                    return d_vars_obs[v]
                    elif ll == 'neg':
                        return -_a_bayes(v, d_pm=d_pm)
                    else:
                        raise ValueError(_('Llave "{ll}" desconocida en el árbol sintático de la ecuación "{ec}". '
                                           'Éste es un error de programación en Tinamït.').format(ll=ll, ec=símismo))

            elif isinstance(á, list):
                return [_a_bayes(x, d_pm=d_pm) for x in á]
            elif isinstance(á, int) or isinstance(á, float):
                return á
            else:
                raise TypeError('')

        modelo = pm.Model()
        with modelo:
            mu = _a_bayes(símismo.árbol)
            sigma = pm.HalfNormal(name='sigma', sd=max(obs_y) / 3)

            if binario:
                x = pm.Normal(name='logit_prob', mu=mu, sd=sigma, shape=obs_y.shape, testval=np.full(obs_y.shape, 0))
                pm.Bernoulli(name='Y_obs', p=pm.invlogit(-x), observed=obs_y)  #

            else:
                pm.Normal(name='Y_obs', mu=mu, sd=sigma, observed=obs_y)

        return modelo, d_vars_obs

    def gen_texto(símismo, paráms=None):

        dialecto = símismo.dialecto
        if paráms is None:
            paráms = []

        def _a_tx(á, d_v):

            if isinstance(á, dict):
                for ll, v in á.items():
                    if ll == 'func':
                        if v[0] == '+':
                            return '({} + {})'.format(_a_tx(v[1][0], d_v=d_v), _a_tx(v[1][1], d_v=d_v))
                        elif v[0] == '/':
                            return '({} / {})'.format(_a_tx(v[1][0], d_v=d_v), _a_tx(v[1][1], d_v=d_v))
                        elif v[0] == '-':
                            return '({} - {})'.format(_a_tx(v[1][0], d_v=d_v), _a_tx(v[1][1], d_v=d_v))
                        elif v[0] == '*':
                            return '({} * {})'.format(_a_tx(v[1][0], d_v=d_v), _a_tx(v[1][1], d_v=d_v))
                        elif v[0] == '^':
                            return '({} ^ {})'.format(_a_tx(v[1][0], d_v=d_v), _a_tx(v[1][1], d_v=d_v))
                        else:
                            return '{nombre}({args})'.format(nombre=dic_funs_inv[dialecto][v[0]],
                                                             args=_a_tx(v[1], d_v=d_v))
                    elif ll == 'var':
                        try:
                            nmbr = 'p[{}]'.format(paráms.index(v))
                        except ValueError:
                            if v in d_v:
                                return d_v[v]
                            else:
                                nmbr = "d_x['v{}']".format(len(d_v))

                        d_v[v] = nmbr
                        return nmbr
                    elif ll == 'neg':
                        return '-{}'.format(_a_tx(v, d_v=d_v))
                    else:
                        raise TypeError('')

            elif isinstance(á, list):
                return ', '.join([_a_tx(x, d_v=d_v) for x in á])
            elif isinstance(á, int) or isinstance(á, float):
                return str(á)
            else:
                raise TypeError('')

        d_vars = {}
        return _a_tx(símismo.árbol, d_v=d_vars), d_vars

    def __str__(símismo):
        return símismo.gen_texto()[0]


dic_funs = {
    'mín': {'vensim': 'MIN', 'pm': pm.math.minimum if pm is not None else None, 'python': min},
    'máx': {'vensim': 'MAX', 'pm': pm.math.maximum if pm is not None else None, 'python': max},
    'abs': {'vensim': 'ABS', 'pm': pm.math.abs_ if pm is not None else None, 'python': abs},
    'exp': {'vensim': 'EXP', 'pm': pm.math.exp if pm is not None else None, 'python': mat.exp},
    'ent': {'vensim': 'INTEGER', 'pm': pm.math.floor if pm is not None else None, 'python': int},
    'rcd': {'vensim': 'SQRT', 'pm': pm.math.sqrt if pm is not None else None, 'python': mat.sqrt},
    'ln': {'vensim': 'LN', 'pm': pm.math.log if pm is not None else None, 'python': mat.log},
    'log': {'vensim': 'LOG', 'pm': None if pm is None else lambda x: pm.math.log(x) / mat.log(10), 'python': mat.log10},
    'sin': {'vensim': 'SIN', 'pm': pm.math.sin if pm is not None else None, 'python': mat.sin},
    'cos': {'vensim': 'COS', 'pm': pm.math.cos if pm is not None else None, 'python': mat.cos},
    'tan': {'vensim': 'TAN', 'pm': pm.math.tan if pm is not None else None, 'python': mat.tan},
    'sinh': {'vensim': 'SINH', 'pm': pm.math.sinh if pm is not None else None, 'python': mat.sinh},
    'cosh': {'vensim': 'COSH', 'pm': pm.math.cosh if pm is not None else None, 'python': mat.cosh},
    'tanh': {'vensim': 'TANH', 'pm': pm.math.tanh if pm is not None else None, 'python': mat.tanh},
    'asin': {'vensim': 'ARCSIN', 'python': mat.asin},
    'acos': {'vensim': 'ARCCOS', 'python': mat.acos},
    'atan': {'vensim': 'ARCTAN', 'python': mat.atan},

    '+': {'vensim': '+'},
    '-': {'vensim': '-'},
    '*': {'vensim': '*'},
    '^': {'vensim': '^'},
    '/': {'vensim': '/'}
}

dic_funs_inv = {}
for f, d_fun in dic_funs.items():
    for tipo, d in d_fun.items():
        if tipo not in dic_funs_inv:
            dic_funs_inv[tipo] = {}
        dic_funs_inv[tipo][d] = f


def conv_fun(fun, dialecto_0, dialecto_1):
    if dialecto_0 == 'tinamït':
        return dic_funs[fun][dialecto_1]
    else:
        return dic_funs[dic_funs_inv[dialecto_0][fun]][dialecto_1]
