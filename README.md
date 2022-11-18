# Morella v1

Este repositorio corresponde a la versión 1 de Morella, un sistema de gestión desarrollado para una empresa de Rosario (Argentina), la cual se dedica a la administración de panteones sociales.

## Módulos
El sistema consiste de 6 módulos:

Caja (caja.py):
  > Módulo destinado al registro de ingresos y egresos en la caja diaria y su impresión. También ofrece la impresión de la caja mensual de forma detallada, comprimida o dividida por cobradores.

Cuentas (cuentas.py):
  > Módulo destinado a la búsqueda de los estados de cuenta de los asociados y que permite generar un reporte con el estado de cuenta deseado.

Mantenimiento de tablas (mantenimiento.py):
  > Módulo destinado al mantenimiento de tablas en el cual se pueden crear o editar usuarios, panteones, nichos, cobradores, centros de egresos, precios y mails.
  > El mismo contiene un menú secreto para uso exclusivo del administrador de sistema, al cual se ingresa generando un error de tipo KeboardInterrupt (Ctrl+C) al momento en el que el sistema solicita el nombre de usuario y escribiendo la palabra admin seguido de presionar la tecla enter. Desde ese menú el administrador tiene la posibilidad de restaurar su cuenta, en caso de haber sido bloqueada por varios intentos de login fallidos, y de modificar los datos de conexión con la base de datos.

Rendiciones (rendiciones.py):
  > Módulo destinado a la cobranza de las cuotas de compra y mantenimiento de los nichos y a la emisión de recibos para los cobradores. 

Reporteador (reporteador.py):
  > Módulo destinado a la generación de diferentes reportes en PDF y XLSX como el listado de socios, listado de morosos (detallado y comprimido), listado de modificaciones de caja, listado de ingresos por débito automático, listado de panteones y listado de cobradores.

Ventas (ventas.py):
  > Módulo destinado a la venta de nichos y la creación y edición tanto de socios como de operaciones.


Para ingresar a cada uno de los módulos es necesario contar con un usuario y una contraseña, que pueden crearse a través del módulo de mantenimiento de tablas.
Dependiendo del nivel de privilegios de cada usuario, éste podrá realizar ciertas acciones y otras estarán bloqueadas.

## Admin Tools
Es una herramienta creada para que el usuario pueda arreglar errores en los pagos de los clientes, está pensada para ser utilizada durante un primer período ya que éstos fueron cargados uno por uno de forma manual debido que no fue posible extraer esa información del sistema predecesor. 

Consiste en una ventana divida en dos sectores: sector de búsqueda y sector de registro. 

En el sector de búsqueda se debe indicar el número de operación utilizado en el antiguo programa desarrollado en Cobol y al presionar el botón <Buscar> se mostrarán en la tabla los datos de relevancia de la/s operación/es que tengan ese número de operación en el sistema anterior.

En el sector de registro se debe indicar el nuevo número de operación y sistema de facturación correspondiente y el mes y año de la última cuota paga. Luego, al presionar el botón <Registrar pago>, la herramienta calcula la cantidad de cuotas que debe o tiene a favor dicha operación y modifica la base de datos para que coincida con esto.

Esta herramienta no requiere de usuario y contraseña y está planificada su obsolescencia a partir del segundo semestre de 2023.

## Base de datos
La base de datos se encuentra en un servidor de PostgreSQL alojado en Ubuntu.
Mediante la utilización de bash y cronejobs se realiza automáticamente un respaldo diario de la base de datos, éstos se guardan en una carpeta sincronizada a la nube mediante el servicio de Dropbox. 

Para ahorrar espacio sólo se almacenan 15 respaldos, luego, cada vez que se crea uno nuevo, se elimina el más antiguo. 

También es posible realizar un respaldo de forma manual a través de un ícono en el menú de aplicaciones de Ubuntu, al cual puede accederse a través de RDP.

## Documentación
En la documentación del programa (./docs/Manual de usuario - Morella.pdf) se puede encontrar de forma detallada los pasos a seguir para realizar cada acción posible, sus respectivos privilegios de usuario necesarios e información acerca del historial de versiones.
