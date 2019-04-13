import inspect
import os
import sys
import traceback
from importlib import import_module as importar_mod
from warnings import warn as avisar

from ._envolt import EnvolturaBF


def gen_bf(mod):
    if isinstance(mod, EnvolturaBF):
        return mod
    elif callable(mod):
        if issubclass(mod, EnvolturaBF):
            return mod()
    elif isinstance(mod, str):
        return _extraer_de_archivo(mod)
    raise TypeError(
        _('Debes dar o una instancia o subclase de `EnvolturaMDS`, o la dirección de un archivo que contiene una.')
    )


def _extraer_de_archivo(archivo):
    if not os.path.isfile(archivo):
        raise FileNotFoundError(_('El archivo siguiente no existe... :(\n\t{}').format(archivo))

    if os.path.splitext(archivo)[1] != '.py':
        raise ValueError(_('El archivo siguiente no parece ser un archivo Python.').format(archivo))

    dir_mod, nombre_mod = os.path.split(archivo)
    sys.path.append(dir_mod)
    módulo = importar_mod(os.path.splitext(nombre_mod)[0])
    instancias = {nmb: cls for nmb, cls in inspect.getmembers(módulo, lambda x: isinstance(x, EnvolturaBF))}
    clases = {
        nmb: cls for nmb, cls in inspect.getmembers(
            módulo, lambda x: (inspect.isclass(x) and issubclass(x, EnvolturaBF))
        )
    }
    if instancias:
        if 'Envoltura' in instancias:
            return instancias['Envoltura']
        return list(instancias.values())[0]

    potenciales = {}
    errores = {}
    for nmb, cls in clases:
        # noinspection PyBroadException
        try:
            potenciales[nmb] = cls()
        except NotImplementedError:
            continue
        except Exception:
            errores[nmb] = traceback.format_exc()
            continue

    if len(potenciales) == 1:
        return list(potenciales.values())[0]
    elif 'Envoltura' in potenciales:
        return potenciales['Envoltura']
    elif potenciales:
        elegida = list(potenciales.values())[0]
        avisar(_('\nHabía más de una instancia de "EnvolturaBF" en el fuente'
                 '\n\t{}'
                 '\n...y ninguna se llamaba "Envoltura". Tomaremos "{}" como la envoltura'
                 '\ny esperaremos que funcione. Si no te parece, asegúrate que la definición de clase o el'
                 '\nobjeto correcto se llame "Envoltura".').format(archivo, elegida))
        return elegida

    raise AttributeError(_(
        'El archivo especificado: \n\t{}\nno contiene subclase o instancia de "EnvolturaBF" utilizable. '
        '\nErrores encontrados:{}'
    ).format(archivo, ''.join(['\n\n\t{}: \n{}'.format(nmb, e) for nmb, e in errores.items()])))
