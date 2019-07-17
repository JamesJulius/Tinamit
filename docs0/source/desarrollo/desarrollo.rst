.. _desarrollo:

Desarrollo
==========
Tinamït tiene una estructura modular, así que es muy fácil agregar más funcionalidades. En particular, por el desarrollo
de envolturas específicas, se puede agregar compatibilidad con varios programas de modelos
**de dinámicas de sistemas (DS)** y modelos **biofísicos (BF)**. También se pueden contribuir **traducciones** del
interfaz y de la documentación.

Además, Tinamït permite incorporar los resultados de modelos de **predicción climática** en las corridas de modelos
apropiados.

Modelos DS
----------
Tinamït queda compatible con modelos escritos con los programas siguientes. Siempre puedes
:ref:`escribir más <des_mds>`.

* **Vensim**: Un programa de MDS bastante popular. Desafortunadamente, requiere la versión pagada (DSS) para conectar
  con Tinamït. Ver su `página oficial <http://vensim.com/>`_ y la :class:`envoltura <tinamit.EnvolturaMDS.ModeloVensim>`.
* **Stella**: Otro programa bastante popular. Ver su `página oficial <https://www.iseesystems.com/
  store/products/stella-architect.aspx>`_ aquí. Envoltura todavía en trabajo.

Modelos BF
----------
Cada envoltura agrega compatibilidad con un tipo de modelo biofísico distinto. Notar que Tinamït no viene con estos
models incluidos pero simplemente *conecta* con ellos; los tienes que instalar separadamente. Siempre puedes
:ref:`agregar una nueva envoltura <des_bf>` para tu modelo BF preferido. Por el momento, tenemos:

* **SAHYSMOD**: Un modelo de salinidad de suelos. Descargar el `ejecutable <https://github.com/AzharInam/Sahysmod-SourceCode/releases>`_ compatible con Tinamït, o ver la `documentación completa <https://www.waterlog.info
  /sahysmod.htm>`_ y la :mod:`envoltura <tinamit.EnvolturaBF.en.SAHYSMOD.SAHYSMOD_Wrapper>`.
* **DSSAT**: Un modelo de cultivos, que toma en cuenta semilla, clima, suelo y manejo humano. Ver la `documentación
  completa <https://dssat.net/>`_. (:mod:`Envoltura <tinamit.EnvolturaBF.es.DSSAT.envoltDSSAT>` en trabajo.)

Modelos de Clima
----------------
Tinamït, por el paquete :py:ref:`taqdir`, ofrece la posibilidad de correr análisis de impactos de cambios climáticos.
Igual que para envolturas de modelos BF, simplemente conecta con estos modelos, no los incluye. Así que los tendrás
que instalar ti misma.

* **Marksim CMIP 5**: Marksim v2 permite generar predicciones climáticas con varios escenarios de cambios climáticos
  para cualquier región del mundo. Para más información, ver su
  `documentación oficial <http://www.ccafs-climate.org/pattern_scaling/>`_.
* **Marksim CMIP 3**: ¿Por qué usar CMIP 3 cuando tienes CMIP 5? Bueno, justo en caso, estamos trabajando en
  agregar compatibilidad con `Marksim <http://www.ccafs-climate.org/pattern_scaling/>`_ v1.

Traducciones
------------
¡Siempre querremos traducciones para hacer de Tinamït una herramienta aún más accesible! Se pueden
:ref:`traducir <des_trad>` el interfaz y la documentación de Tinamït en tu lengua preferida.


Cómo compartir tus inovaciones
------------------------------
La manera más fácil (para mi) es que te inscribas en GitHub, creas una nueva rama de Tinamït, le agreges tu contribución
y después la combinemos con la rama central del proyecto.
La manera más fácil para ti es probablemente mandarme tu nuevo código por correo electrónico (|correo|).

Unos apuntos para cuándo vas a compartir una nueva envoltura:

* Incluir instrucciones, si necesario, para que tus usuarios puedan conseguir modelos externos necesarios, si hay.
* Incluir tantos comentarios como posible en tu código (el código fuente de Tinamït es un ejemplo).
* Se recomienda escribir nuevas envolturas en castellano, pero aceptamos envolturas escritas en todos idiomas. Apoyamos
  particularmente esfuerzos para escribir el código en el idioma nativo del lugar donde estás trabajando.


Para más información...
-----------------------
.. toctree::
   :maxdepth: 1

   Desarrollar envolturas MDS <des_mds>
   Desarrollar envolturas BF <des_bf>
   Contribuir traducciones <des_trad>
