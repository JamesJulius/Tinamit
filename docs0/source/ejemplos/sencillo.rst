.. _ejemplo_senc:

Ejemplo muy básico
------------------
También es un ejemplo un poco estúpido. Pero demuestra muy bien cómo funciona Tinamït, y no tienes que instalar
cualquier modelo biofísico externo para que te funcione, así que empecemos con este. ::

    import os
    from tinamit.Conectado import Conectado

    modelo = Conectado()
    directorio = os.path.dirname(__file__)
    modelo.estab_mds(os.path.join(directorio, "Prueba dll.vpm"))
    modelo.estab_bf(os.path.join(directorio, 'Prueba bf.py'))
    modelo.conectar(var_mds='Lluvia', var_bf='Lluvia', mds_fuente=False)
    modelo.conectar(var_mds='Bosques', var_bf='Bosque', mds_fuente=True)
    modelo.simular(paso=1, tiempo_final=100, nombre_corrida='Corrida_Tinamït')

Tomémoslo línea por línea. Primero, importamos Tinamït. ::

   import os
   from tinamit.Conectado import Conectado

Segundo, conectamos los variables biofísicos y de DS::

   directorio = os.path.dirname(__file__)
   modelo.estab_mds(os.path.join(directorio, "Prueba dll.vpm"))
   modelo.estab_bf(os.path.join(directorio, 'Prueba bf.py'))

Tenemos unos modelos muy sencillos. El modelo DS determina, dado la lluvia, la cantidad de pesca posible y su impacto
en la necesidad de explotar recursos del bosque.

.. image:: ../imágenes/Ejemplos/Ejemplo_básico_modelo_VENSIM.png
   :align: center
   :alt: Modelo Vensim.

Del otro lado, el "modelo" biofísico nos da la precipitación según la cubertura forestal. Vamos a conectar los variables
necesarios::

   modelo.conectar(var_mds='Lluvia', var_bf='Lluvia', mds_fuente=False)
   modelo.conectar(var_mds='Bosques', var_bf='Bosque', mds_fuente=True)

Y corremos la simulación para 100 meses. ¡Allí está! Ya puedes visualizar los resultados directamente en Vensim.
¿Ves que cambió la lluvia?::

   modelo.simular(paso=1, tiempo_final=100, nombre_corrida='Corrida_Tinamït')
