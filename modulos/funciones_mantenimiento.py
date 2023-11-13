VERSION = '1.4.1.2303'
SHORT_VERSION = VERSION[:3]
TYPE_VERSION = 'RC'

ARCH_INI = "../databases/database.ini"
ARCH_LOG_ERROR = "../error.log"

AFIRMATIVO = ['S', 's', 'Si', 'SI', 'sI', 'si']
NEGATIVO = ['N', 'n', 'No', 'NO', 'nO', 'no']

import os
import psycopg2 as sql
import psycopg2.errors

from datetime import datetime
from getpass import getpass
from traceback import format_exc

import funciones_cuentas as ctas
import funciones_rendiciones as rend

os.system(f'TITLE Morella v{VERSION} - MF! Soluciones informáticas')
os.system('color 0a')   # Colores del módulo (Verde sobre negro)
os.system('mode con: cols=160 lines=9999')


def obtener_database() -> str:
    """Obtiene desde un archivo .ini la información necesaria para ingresar a la
    base de datos y la retorna en forma de cadena.

    :rtype: str
    """
    if not os.path.isfile(ARCH_INI):
        arch = open(ARCH_INI, "w")
        arch.close()
    with open(ARCH_INI, "r") as arch:
        db = arch.readline()
    return db


DATABASE = obtener_database()


def iniciar_sesion() -> tuple:
    """Permite al usuario ingresar al sistema a través de su usuario y contraseña.
    - En caso que la contraseña sea 0000 se le solicitará ingresar una contraseña nueva.
    - En caso de ingresar erroneamente la contraseña tres veces consecutivas se 
    bloqueará el usuario.
    - En caso de ingresar un usuario inactivo o bloqueado no se permitirá el ingreso.

    Se retorna una tupla con los datos del usuario. En cualquiera de los casos en que
    no se produzca un ingreso exitoso se retorna una tupla con cadenas vacías.

    :rtype: tuple
    """
    i_d = 0
    user = input("Usuario: ").lower()
    try:
        i_d, nom, ape, tel, dom, use, pas, pri, act = buscar_usuario_por_user(user)
        if i_d == 0 and nom == 0 and ape == 0:
            return 0, 0, 0, 0, 0, 0, 0, 0, 0
        if act == 1:
            counter = 0
            pw = getpass("Contraseña: ")
            while pw != pas:
                print("Contraseña incorrecta")
                print()
                counter += 1
                if counter == 3:
                    edit_registro('usuarios', 'activo', 2, i_d)
                    print("Su usuario ha sido bloqueado por repetición de claves incorrectas. Comuníquese con un administrador.")
                    i_d = -1
                    nom, ape, tel, dom, use, pas, pri, act = "", "", "", "", "", "", "", ""
                    return i_d, nom, ape, tel, dom, use, pas, pri, act
                print()
                print
                pw = getpass("Contraseña: ")
            if pw == pas:
                print()
                print(f"Bienvenido/a {nom}, que tengas un buen día.")
                print()
                while pw == "0000":
                    pw_new = str(getpass("Ingrese la nueva contraseña: "))
                    while len(pw_new) < 4:
                        print("La contraseña debe ser de 4 dígitos o más.")
                        pw_new = str(getpass("Ingrese la nueva contraseña: "))
                        print()
                    while pw_new == "0000":
                        print("La contraseña no puede ser 0000.")
                        pw_new = str(getpass("Ingrese la nueva contraseña: "))
                        print()
                    pw_conf = str(getpass("Repita la nueva contraseña: "))
                    print()
                    if pw_new == pw_conf:
                        edit_registro('usuarios', 'pass', str(pw_new), i_d)
                        print("Contraseña actualizada exitosamente.")
                        print()
                        return i_d, nom, ape, tel, dom, use, pw_new, pri, act
                    else:
                        pw = ""
                return i_d, nom, ape, tel, dom, use, pas, pri, act
        elif act == 2:
            print()
            print("Su usuario se encuentra bloqueado. Comuníquese con un administrador.")
            i_d = -1
            nom, ape, tel, dom, use, pas, pri, act = "", "", "", "", "", "", "", ""
            return i_d, nom, ape, tel, dom, use, pas, pri, act
        else:
            print()
            print("Usuario inactivo.")
            i_d = -1
            nom, ape, tel, dom, use, pas, pri, act = "", "", "", "", "", "", "", ""
            return i_d, nom, ape, tel, dom, use, pas, pri, act
    except TypeError:
        print()
        print("Usuario inexistente.")
        i_d = -1
        nom, ape, tel, dom, use, pas, pri, act = "", "", "", "", "", "", "", ""
        return i_d, nom, ape, tel, dom, use, pas, pri, act
    except sql.OperationalError:
        print()
        print("Usuario inexistente.")
        i_d = -1
        nom, ape, tel, dom, use, pas, pri, act = "", "", "", "", "", "", "", ""
        return i_d, nom, ape, tel, dom, use, pas, pri, act
    except:
        log_error()
        print()
        input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
        i_d = -1
        nom, ape, tel, dom, use, pas, pri, act = "", "", "", "", "", "", "", ""
        return i_d, nom, ape, tel, dom, use, pas, pri, act


def barra_progreso(progreso: int, total: int, titulo:str=None, solo_titulo=False):
    """Muestra el progreso durante la ejecución de un ciclo. Puede elegirse mostrar
    una barra de progreso impresa en pantalla junto con el porcentaje de progreso en
    el títuto de la ventana o sólo este último. 
    
    El progreso en el título puede mostrarse sólo o añadir el mismo a otro.

    :param progreso: Índice actual del ciclo (Se puede utilizar un contador de
    iteraciones)
    :type progreso: int

    :param total: Cantidad total de iteraciones (Se puede utilizar len())
    :type total: int

    :param titulo: Si desea mostrarse un título además del progreso se debe indicar
    en este parámetro. Si se indica se mostrará el progreso luego del mismo, en caso
    contrario, se mostrará sólo el progreso. Por defecto: Desactivado.
    :type titulo: str

    :param solo_titulo: Indica si se muestra el progreso sólo en el título (True) o
    si se muestra también la barra de progreso impresa en pantalla (False).
    Por defecto: False.
    :type solo_titulo: boolean
    """
    if total:
        porcentaje = 100 * (progreso / float(total))
    else:
        porcentaje = 100
    if solo_titulo:
        if titulo:
            os.system(f'TITLE {titulo}  -  PROGRESO: {porcentaje:.2f}%')
        else:
            os.system(f'TITLE PROGRESO: {porcentaje:.2f}%')
    else:
        barra = ('#' * int(porcentaje) + '-' * (100 - int(porcentaje)))
        print(f"\r [{barra}] {porcentaje:.2f}%", end='\r')
        if titulo:
            os.system(f'TITLE {titulo}  -  PROGRESO: {porcentaje:.2f}%')
        else:
            os.system(f'TITLE PROGRESO: {porcentaje:.2f}%')


def buscar_usuario_por_user(user: str) -> tuple:
    """Busca un usuario en la base de datos a partir del nombre de usuario
    y retorna una tupla con todos los datos del mismo. En caso de no poder
    conectarse con la BD, lo informa al usuario y retorna una tupla de nueve
    ceros.

    :param user: Nombre de usuario
    :type user: str

    :rtype: tuple
    """
    try:
        conn = sql.connect(DATABASE)
    except sql.OperationalError:
        log_error()
        print()
        print("         ERROR. La base de datos no responde. Asegurese de estar conectado a la red y que el servidor se encuentre encendido.")
        print()
        print("         Si es así y el problema persiste, comuníquese con el administrador del sistema.")
        print()
        return 0, 0, 0, 0, 0, 0, 0, 0, 0
    cursor = conn.cursor()
    instruccion = f"SELECT * FROM usuarios WHERE user_name = '{user}'"
    cursor.execute(instruccion)
    datos = cursor.fetchone()
    conn.commit()
    conn.close()

    i_d, nom, ape, tel, dom, use, pas, pri, act = datos
    return i_d, nom, ape, tel, dom, use, pas, pri, act


def buscar_usuario_por_id(idu: int) -> tuple:
    """Busca un usuario en la base de datos a partir del ID de usuario
    y retorna una tupla con todos los datos del mismo.

    :param user: ID de usuario
    :type user: int

    :rtype: tuple
    """
    with sql.connect(DATABASE) as conn:
        cursor = conn.cursor()
        instruccion = f"SELECT * FROM usuarios WHERE id = '{idu}'"
        cursor.execute(instruccion)
        datos = cursor.fetchone()

    i_d, nom, ape, tel, dom, use, pas, pri, act = datos
    return i_d, nom, ape, tel, dom, use, pas, pri, act


def log_error():
    """
    Recoge la información necesaria de la excepción producida, la fecha y la hora en que se produjo
    y lo vuelca en el Log de errores
    """
    exc = format_exc()
    with open(ARCH_LOG_ERROR, 'a') as log_error:
        log_error.write(f"{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}: \n")
        log_error.write(exc)
        log_error.write("\n_________________________________________________\n\n")


def reemplazar_comilla(cadena: str) -> str:
    """Recibe una cadena y la analiza en búsqueda de comillas
    simples. En caso de contener, reemplaza cada una de ellas
    por una tílde invertida y retorna la nueva cadena,de lo
    contrario retorna la cadena como fue recibida.

    :param cadena: Cadena a analizar
    :type cadena: str

    :rtype: str
    """
    if type(cadena) == str and "'" in cadena:
        cadena = cadena.replace("'", "´")
    else:
        cadena = cadena
    return cadena


def run_query(query: str):
    """Recibe una consulta SQL y la ejecuta en la base de datos

    :param query: Consulta SQL
    :type query: str
    """
    with sql.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute(query)


def run_query_w_par(query: str, parameters:tuple = ()):
    """Recibe una consulta SQL con parámetros y la ejecuta en la base de datos

    :param query: Consulta SQL
    :type query: str

    :param parameters: Tupla que contiene los parámetros a pasar en la consulta
    :type parameters: tuple
    """
    with sql.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute(query, parameters)


def delete_row(tabla: str, columna: str, valor: str|int|float|bool):
    """Elimina el o los renglones que cumplan una condición
    de una tabla específica en la base de datos.

    :param tabla: Tabla de donde se buscarán y eliminarán los renglones
    :type tabla: str
    
    :param columna: Columna donde se buscará el valor indicado
    :type columna: str
    
    :param valor: Valor que se buscará en la columna indicada
    :type valor: str or int or float or bool
    """
    valor = reemplazar_comilla(valor)

    with sql.connect(DATABASE) as conn:
        cursor = conn.cursor()
        instruccion = f"DELETE FROM {tabla} WHERE {columna} = '{valor}'"
        cursor.execute(instruccion)


def ult_reg(tabla: str, columna: str) -> list:
    """Busca en la base de datos el último registro de una tabla específica
    y retorna sus valores en forma de lista.

    :param tabla: Tabla donde se buscará el último registro.
    :type tabla: str

    :param columna: Columna que se utilizará para ordenar (generalmente ID)
    :type columna: str

    :rtype: list
    """
    with sql.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {tabla} ORDER BY {columna} DESC LIMIT 1")
        ult_registro = cursor.fetchall()

    ult_reg_list = list(ult_registro[0])
    return ult_reg_list


def buscar_op_por_nicho(cod_nicho: str) -> list:
    """Busca en la base de datos las operaciones que se encuentren relacionadas
    a un código de nicho específico.

    :param cod_nicho: Código de nicho
    :type cod_nicho: str

    :rtype: list
    """
    with sql.connect(DATABASE) as conn:
        cursor = conn.cursor()
        instruccion = f"SELECT * FROM operaciones WHERE nicho = '{cod_nicho}'"
        cursor.execute(instruccion)
        datos = cursor.fetchall()
    return datos


def truncate(n:float, decimals:int|float = 0) -> float:
    """Realiza el truncamiento de un número. Si se indican decimales negativos
    se redondea a un número con base 10 por el positivo del decimal indicado.
    Por ejemplo: si se indica decimal -2 se redondeará a un número múltipo de 100.

    :param n: Número a truncar
    :type n: int or float

    :param decimals: cantidad máxima de decimales (+) o cifras a eliminar (-). Por defecto: 0
    :type decimlas: int

    :rtype: int or float
    """
    multiplier = 10 ** decimals
    return int(n * multiplier) / multiplier


def mostrar_precios_venta(ret: bool = False):
    """Imprime en pantalla una tabla donde se muestran los precios
    de venta, ordeandos por ID, con sus respectivos datos.
    Si se le indica, retorna la cantidad de precios impresos.

    :param ret: Indica si se debe retornar la cantidad de precios impresos. 
    Por defecto: False
    :pram type: bool
    """
    counter = 0

    with sql.connect(DATABASE) as conn:
        cursor = conn.cursor()
        instruccion = f"SELECT * FROM precios_venta ORDER BY id"
        cursor.execute(instruccion)
        datos = cursor.fetchall()

    print("------------------------------------------------------------------------------------------")
    print("{:<4} {:<40} {:<15} {:<15} {:<15}".format('ID','DESCRIPCIÓN', '   PRECIO', '   ANTICIPO', 'CUOTAS (x10)'))
    print("------------------------------------------------------------------------------------------")

    for i in datos:
        counter += 1
        i_d, nom, pre, ant, cuo = i
        print("{:<4} {:<40} {:<15} {:<15} {:<15}".format(f'{i_d}'.rjust(2, " "), nom, f'{pre:.2f}'.rjust(11, ' '), f'{ant:.2f}'.rjust(11, ' '), f'{cuo:.2f}'.rjust(11, ' ')))

    print("------------------------------------------------------------------------------------------")
    print()

    if ret == False:
        input("Presione la tecla enter para continuar... ")
    elif ret == True:
        return counter


def mostrar_precios_mant(ret: bool = False):
    """Imprime en pantalla una tabla donde se muestran los precios
    de mantenimiento, ordeandos por ID, con sus respectivos datos.
    Si se le indica, retorna la cantidad de precios impresos.

    :param ret: Indica si se debe retornar la cantidad de precios impresos.
    Por defecto: False
    :pram type: bool
    """
    counter = 0

    with sql.connect(DATABASE) as conn:
        cursor = conn.cursor()
        instruccion = f"SELECT * FROM cat_nichos ORDER BY id"
        cursor.execute(instruccion)
        datos = cursor.fetchall()

    print("--------------------------------------------------------------------------")
    print("{:<4} {:<40} {:<15} {:<15}".format('ID','CATEGORÍA', 'PRECIO BICON', '  PRECIO NOB'))
    print("--------------------------------------------------------------------------")

    for i in datos:
        counter += 1
        i_d, cat, val_mant_bic, val_mant_nob = i
        print("{:<4} {:<40} {:<15} {:<15}".format(f'{i_d}'.rjust(2, " "), cat, f'{val_mant_bic:.2f}'.rjust(11, ' '), f'{val_mant_nob:.2f}'.rjust(11, ' ')))

    print("--------------------------------------------------------------------------")
    print()

    if ret == False:
        input("Presione la tecla enter para continuar... ")
    elif ret == True:
        return counter


def mostrar_cuentas_mail(ret: bool = False):
    """Imprime en pantalla una tabla donde se muestran las cuentas
    de email, ordeandas por ID, con sus respectivos datos.
    Si se le indica, retorna la cantidad de cuentas impresas.

    :param ret: Indica si se debe retornar la cantidad de cuentas impresas.
    Por defecto: False
    :pram type: bool
    """
    counter = 0

    with sql.connect(DATABASE) as conn:
        cursor = conn.cursor()
        instruccion = f"SELECT * FROM mail ORDER BY id"
        cursor.execute(instruccion)
        datos = cursor.fetchall()

    print("------------------------------------------------------------------------------------------------------------------------------------------------")
    print("{:<4} {:<20} {:<40} {:<40} {:<40}".format('ID','ETIQUETA','CUENTA EMAIL','SERVIDOR SMTP','USUARIO SMTP'))
    print("------------------------------------------------------------------------------------------------------------------------------------------------")

    for i in datos:
        counter += 1
        i_d, etiq, mail, server, user, pas = i
        print("{:<4} {:<20} {:<40} {:<40} {:<40}".format(f'{i_d}'.rjust(2, " "), etiq, mail, server, user))

    print("------------------------------------------------------------------------------------------------------------------------------------------------")
    print()

    if ret == False:
        input("Presione la tecla enter para continuar... ")
    elif ret == True:
        return counter


def buscar_mail(id: int) -> tuple:
    """Busca en la base de datos una cuenta de email a partir de su ID
    y retorna una tupla con los datos de la misma.

    :param id: ID de la cuenta a buscar
    :type id: int
    """
    with sql.connect(DATABASE) as conn:
        cursor = conn.cursor()
        instruccion = f"SELECT * FROM mail WHERE id = {id}"
        cursor.execute(instruccion)
        datos = cursor.fetchone()

    i_d, etiq, mail, server, user, pw = datos
    return i_d, etiq, mail, server, user, pw


def calcular_precio_venta_manual(precio_de_contado: int) -> tuple:
    """Recibe un precio de venta, calcula sus valores correspondientes
    de anticipo y cuota y retorna una tupla con estos.

    :param precio_de_contado: Precio de venta
    :type precio_de_contado: int

    :rtype: tuple
    """
    anticipo = precio_de_contado/2
    cuota = (anticipo*1.5)/10
    cuota_r = float(truncate(cuota, -2))
    return anticipo, cuota_r


def cambio_precio_venta_manual(id_precio: int, nuevo_valor: int):
    """Recibe un ID de precio de venta y un valor y, a partir de éste, calcula
    su respectivos valores de anticipo y cuota. Luego registra el cambio en la
    base de datos.

    :param id_precio: ID de precio de venta
    :type id_precio: int

    :param nuevo_valor: Nuevo precio de venta
    :type nuevo_valor: int
    """
    anticipo, cuota_r = calcular_precio_venta_manual(nuevo_valor)

    with sql.connect(DATABASE) as conn:
        cursor = conn.cursor()
        instruccion = f"UPDATE precios_venta SET precio = {nuevo_valor}, anticipo = {anticipo}, cuotas = {cuota_r} WHERE id = {id_precio}"
        cursor.execute(instruccion)


def cambio_precio_venta_porcentaje(porcentaje: int):
    """Recupera desde la BD los precios actuales de venta y los actualiza aumentándolos,
    de forma redondeada en valores múltiplos de 100, según el porcentaje indicado. A su
    vez, calcula y actualiza en la BD los valores correspondientes al anticipo y cuotas
    de cada uno, redondeándolos de la misma forma que los precios.

    :param porcentaje: Porcentaje a aumentar
    :type porcentaje: int
    """

    pcnt = 1+(porcentaje/100)

    # Recuperación de precios actuales
    with sql.connect(DATABASE) as conn:
        cursor = conn.cursor()
        instruccion = f"SELECT * FROM precios_venta ORDER BY id"
        cursor.execute(instruccion)
        datos = cursor.fetchall()

    # Actualización de precios
    for i in datos:
        i_d, nom, pre, ant, cuo = i

        # Precio
        n_pre = pre * pcnt
        n_pre_r = float(truncate(n_pre, -2))

        # Anticipo
        n_ant = n_pre_r/2

        # Cuota
        n_cuo = (n_ant*1.5)/10
        n_cuo_r = float(truncate(n_cuo, -2))

        # Registro de nuevos precios
        with sql.connect(DATABASE) as conn:
            cursor = conn.cursor()
            instruccion = f"UPDATE precios_venta SET precio = {n_pre_r}, anticipo = {n_ant}, cuotas = {n_cuo_r} WHERE id = {i_d}"
            cursor.execute(instruccion)


def cambio_precio_mant_manual(id_cat: int, nuevo_val_mant_bic: int, nuevo_val_mant_nob: int):
    """Recibe un ID de categoría de nicho y sus respectivos nuevos precios de mantenimiento
    y registra el cambio en la base de datos.

    :param id_cat: ID de categoría de nicho
    :type id_cat: int
    
    :param nuevo_val_mant_bic: Nuevo precio de mantenimiento para Bicon
    :type nuevo_val_mant_bic: int
    
    :param nuevo_val_mant_nob: Nuevo precio de mantenimiento para NOB
    :type nuevo_val_mant_nob: int
    """
    with sql.connect(DATABASE) as conn:
        cursor = conn.cursor()
        instruccion = f"UPDATE cat_nichos SET valor_mant_bicon = {nuevo_val_mant_bic}, valor_mant_nob = {nuevo_val_mant_nob} WHERE id = {id_cat}"
        cursor.execute(instruccion)


def cambio_precio_mant_porcentaje(facturacion: str, porcentaje: int):
    """Recupera desde la BD los precios actuales de mantenimiento correspondientes al tipo
    de facturación indicada y los actualiza aumentándolos, de forma redondeada en valores
    múltiplos de 100, según el porcentaje indicado.

    :param facturacion: Tipo de facturación a aumentar (puede ser 'todas', 'bicon' o 'nob')
    :type facturacion: str

    :param porcentaje: Porcentaje a aumentar
    :type porcentaje: int
    """

    pcnt = 1+(porcentaje/100)

    # Recuperación de precios actuales
    with sql.connect(DATABASE) as conn:
        cursor = conn.cursor()
        instruccion = f"SELECT * FROM cat_nichos ORDER BY id"
        cursor.execute(instruccion)
        datos = cursor.fetchall()

    # Actualización de precios
    for i in datos:
        i_d, cat, val_mant_bic, val_mant_nob = i

        # Cálculo precio BICON
        if facturacion == 'todas' or facturacion == 'bicon':
            n_vmb = val_mant_bic * pcnt
            n_vmb_t = float(truncate(n_vmb, -2))

        # Cálculo precio NOB
        if facturacion == 'todas' or facturacion == 'nob':
            n_vmn = val_mant_nob * pcnt
            n_vmn_t = float(truncate(n_vmn, -2))

        # Definición de la consulta SQL según facturación seleccionada
        if facturacion == 'todas':
            instruccion = f"UPDATE cat_nichos SET valor_mant_bicon = {n_vmb_t}, valor_mant_nob = {n_vmn_t} WHERE id = {i_d}"
        elif facturacion == 'bicon':
            instruccion = f"UPDATE cat_nichos SET valor_mant_bicon = {n_vmb_t} WHERE id = {i_d}"
        elif facturacion == 'nob':
            instruccion = f"UPDATE cat_nichos SET valor_mant_nob = {n_vmn_t} WHERE id = {i_d}"

        # Registro de nuevos precios
        with sql.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute(instruccion)


def edit_registro(tabla: str, columna: str, nuevo_valor: str|int|float|bool, id: int):
    """Modifica el valor de una columna específica de un registro en particular
    en la base de datos.

    :param tabla: Tabla de donde se buscará y modificará el registro
    :type tabla: str
    
    :param columna: Columna donde se modificará el valor indicado
    :type columna: str
    
    :param nuevo_valor: Nuevo valor que se registrará en la columna indicada
    :type nuevo_valor: str or int or float or bool

    :param id: ID del registro a modificar
    :type id: int
    """
    nuevo_valor = reemplazar_comilla(nuevo_valor)

    with sql.connect(DATABASE) as conn:
        cursor = conn.cursor()
        instruccion = f"UPDATE {tabla} SET {columna} = '{nuevo_valor}' WHERE id = '{id}'"
        cursor.execute(instruccion)


def set_null_registro(tabla: str, columna_null: str, columna_filtro: str, valor: str|int|float|bool):
    """Hace nulo el valor de una columna específica de un registro en particular,
    que cumpla una condición, en la base de datos.

    :param tabla: Tabla de donde se buscará y modificará el registro
    :type tabla: str
    
    :param columna_null: Columna donde se colocará valor nulo
    :type columna_null: str

    :param columna_filtro: Columna donde se buscará el valor indicado
    :type columna_filtro: str
    
    :param valor: Valor que se buscará en la columna indicada
    :type valor: str or int or float or bool
    """
    with sql.connect(DATABASE) as conn:
        cursor = conn.cursor()
        instruccion = f"UPDATE {tabla} SET {columna_null} = NULL WHERE {columna_filtro} = '{valor}'"
        cursor.execute(instruccion)


def edit_nicho(columna: str, nuevo_valor: str|int|float|bool, cod_nicho: str):
    """Modifica el valor de una columna específica de un registro en particular,
    a través de su Código de nicho, en la tabla nichos de la base de datos.

    :param columna: Columna donde se modificará el valor indicado
    :type columna: str
    
    :param nuevo_valor: Nuevo valor que se registrará en la columna indicada
    :type nuevo_valor: str or int or float or bool

    :param cod_nicho: Código de nicho del registro a modificar
    :type id: str
    """
    nuevo_valor = reemplazar_comilla(nuevo_valor)

    with sql.connect(DATABASE) as conn:
        cursor = conn.cursor()
        instruccion = f"UPDATE nichos SET {columna} = '{nuevo_valor}' WHERE codigo = '{cod_nicho}'"
        cursor.execute(instruccion)


def obtener_panteones() -> list:
    """Recupera de la base de datos todos los registros de la tabla panteones y
    los devuelve en una lista de tuplas que contienen todos los datos cada uno.

    :rtype: list
    """
    with sql.connect(DATABASE) as conn:
        cursor = conn.cursor()
        instruccion = f"SELECT * FROM panteones ORDER BY id"
        cursor.execute(instruccion)
        datos = cursor.fetchall()
    return datos


def obtener_cat_nichos() -> list:
    """Recupera de la base de datos todos los registros de la tabla categoria_nichos y
    los devuelve en una lista de tuplas que contienen todos los datos cada uno.

    :rtype: list
    """
    with sql.connect(DATABASE) as conn:
        cursor = conn.cursor()
        instruccion = f"SELECT * FROM cat_nichos ORDER BY id"
        cursor.execute(instruccion)
        datos = cursor.fetchall()
    return datos


def convertir_car_esp(letra: str) -> str:
    """Recibe una cadena compuesta por un caracter y, en caso de ser
    una vocal con tilde, la convierte a la misma vocal sin tilde y la
    retorna. De lo contrario la retorna sin modificaciones.

    :param letra: Letra a analizar
    :type letra: str

    :rtype: str
    """
    a = ['á','à','â','ä']
    e = ['é','è','ê','ë']
    i = ['í','ì','î','ï']
    o = ['ó','ò','ô','ö']
    u = ['ú','ù','û','ü']
    
    if letra in a:
        letra_n = 'a'
    elif letra in e:
        letra_n = 'e'
    elif letra in i:
        letra_n = 'i'
    elif letra in o:
        letra_n = 'o'
    elif letra in u:
        letra_n = 'u'
    else:
        return letra

    return letra_n


def generar_user(nombre: str, apellido: str) -> str:
    """Recibe dos cadenas con el nombre y el apellido respectivamente, luego las convierte
    a minúsculas, quita las tildes de las vocales, si las hubiera, y elimina los caracteres
    especiales, si los hubiera.
    Por último, retorna una cadena compuesta por los primeros tres caracteres del apellido
    resultante y los tres primeros caracteres del nombre resultante.

    :param nombre: Nombre del usuario
    :type nombre: str

    :param apellido: Apellido del usuario
    :type apellido: str

    :rtype: str
    """
    letras = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n',
                'ñ', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

    tildes = ['á', 'é', 'í', 'ó', 'ú', 'à', 'è', 'ì', 'ò',
                'ù', 'â', 'ê', 'î', 'ô', 'û', 'ä', 'ë', 'ï', 'ö', 'ü']

    nombre = str(nombre).lower()
    apellido = str(apellido).lower()
    nom = ape = ""
    
    contador = 0
    for n in nombre:
        if n in tildes:
            n = convertir_car_esp(n)
        if n in letras:
            contador += 1
            nom += str(n)
            if contador == 3:
                break

    contador = 0
    for a in apellido:
        if a in tildes:
            a = convertir_car_esp(a)
        if a in letras:
            contador += 1
            ape += str(a)
            if contador == 3:
                break
    
    return f"{ape}{nom}"


def opcion_menu() -> int:                                                                           # OPCIÓN MENÚ PRINCIPAL
    """Muestra al usuario un menú y luego le solicita ingresar una de las
    opciones mostradas a través del número correspondiente. En caso de no
    ingresar una opción correcta, se le volverá a solicitar.

    :rtype: int
    """
    print()
    print("********** Acciones disponibles **********")
    print()
    print("   1. Mantenimiento de usuarios")
    print("   2. Mantenimiento de panteones")
    print("   3. Mantenimiento de nichos")
    print("   4. Mantenimiento de cobradores")
    print("   5. Mantenimiento de centros de egresos")
    print("   6. Mantenimiento de precios")
    print("   7. Mantenimiento de mails")
    print("   8. Mantenimiento de datos de FiServ")
    print("   0. Salir")
    print()
    try:
        opcion = int(input("Ingrese una opción: "))
        while opcion < 0 or opcion > 8:
            print()
            print("Opción incorrecta.")
            print()
            opcion = int(input("Ingrese una opción: "))
    except ValueError: 
        print("Opción incorrecta.")
        opcion = -1
    except:
        log_error()
        print()
        input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
        opcion -1
    return opcion
    

def menu(idu: int):                                                                                 # MENÚ PRINCIPAL
    """Recibe el ID del usuario. Luego llama a la función donde se muestra las
    opciones y recibe, a través de ella, la opción ingresada por el usuario.
    Luego, según la opción ingresada, llama a la función correspondiente, a la
    cual le transmite el ID del usuario.

    :param idu: ID de usuario
    :type idu: int
    """
    opcion = -1
    while opcion != 0:
        opcion = opcion_menu()
        if opcion == 1:
            menu_usuarios(idu)
        elif opcion == 2:
            menu_panteones(idu)
        elif opcion == 3:
            menu_nichos(idu)
        elif opcion == 4:
            menu_cobradores(idu)
        elif opcion == 5:
            menu_centros_egresos(idu)
        elif opcion == 6:
            menu_precios(idu)
        elif opcion == 7: 
            menu_mails(idu)
        elif opcion == 8: 
            menu_fiserv(idu)
        elif opcion == 0:
            return


def opcion_menu_usuarios() -> int:                                                                  # OPCIÓN MENÚ DE USUARIOS
    """Muestra al usuario un menú y luego le solicita ingresar una de las
    opciones mostradas a través del número correspondiente. En caso de no
    ingresar una opción correcta, se le volverá a solicitar.

    :rtype: int
    """
    print()
    print("********** Acciones disponibles **********")
    print()
    print("   1. Ver usuarios")
    print("   2. Crear nuevo usuario")
    print("   3. Modificar usuario")
    print("   4. Activar usuario")
    print("   5. Inactivar usuario")
    print("   0. Volver")
    print()
    try:
        opcion = int(input("Ingrese una opción: "))
        while opcion < 0 or opcion > 5:
            print()
            print("Opción incorrecta.")
            print()
            opcion = int(input("Ingrese una opción: "))
    except ValueError: 
        print("Opción incorrecta.")
        opcion = -1
    except:
        log_error()
        print()
        input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
        opcion -1
    return opcion


def menu_usuarios(idu: int):                                                                        # MENÚ DE USUARIOS
    """Recibe el ID del usuario. Luego llama a la función donde se muestra las
    opciones y recibe, a través de ella, la opción ingresada por el usuario.
    Luego, según la opción ingresada, llama a la función correspondiente, a la
    cual le transmite el ID del usuario.

    :param idu: ID de usuario
    :type idu: int
    """
    opcion = -1
    while opcion != 0:
        opcion = opcion_menu_usuarios()
        if opcion == 1:
            mostrar_usuarios(idu)
        elif opcion == 2:
            crear_usuario(idu)
        elif opcion == 3:
            modificar_usuario(idu)
        elif opcion == 4:
            activar_usuario(idu)
        elif opcion == 5:
            inactivar_usuario(idu)
        elif opcion == 0:
            return


def mostrar_usuarios(idu: int):
    """Permite al usuario ver una tabla donde se muestran todos los usuarios
    que se encuentran registrados en la BD y sus respectivos datos, a
    excepción de la contraseña y el ID.

    Nivel de privilegios mínimo: 3

    :param idu: ID de usuario
    :type idu: int
    """
    i_d, nom, ape, tel, dom, use, pas, pri, act = buscar_usuario_por_id(idu)

    if pri < 3:
        print("No posee privilegios para realizar esta acción")
        print()

    elif pri >= 3:
        with sql.connect(DATABASE) as conn:
            cursor = conn.cursor()
            instruccion = f"SELECT * FROM usuarios ORDER BY user"
            cursor.execute(instruccion)
            datos = cursor.fetchall()
        
        print("-".rjust(113, '-'))
        print("{:<7} {:<30} {:<25} {:<30} {:<6} {:<10}".format('USER', 'NOMBRE', 'TELÉFONO', 'DOMICILIO', 'NIVEL', 'ESTADO'))
        print("-".rjust(113, '-'))

        for i in datos:
            id_us, nom, ape, tel, dom, use, pas, pri, act = i
            if act == 0:
                estado = "INACTIVO"
            elif act == 1:
                estado = "ACTIVO"
            elif act == 2:
                estado = "BLOQUEADO"
            print("{:<7} {:<30} {:<25} {:<30} {:<6} {:<10}".format(use, f"{ape} {nom}"[0:30], f"{tel}"[0:25], dom[0:30], f"  {pri}  ", estado))

        print("-".rjust(113, '-'))
        print()


def crear_usuario(idu: int):
    """Permite al usuario crear un nuevo usuario y registrarlo en la base de datos.
    Automáticamente se crea el nombre de usuario y la contraseña, siendo ésta 0000.
    El nivel de privilegios del nuevo usuario deberá ser siempre igual o inferior
    al del usuario que está realizando la acción.

    Nivel de privilegios mínimo: 3

    :param idu: ID de usuario
    :type idu: int
    """
    i_d, nom, ape, tel, dom, use, pas, pri, act = buscar_usuario_por_id(idu)

    if pri < 3:
        print("No posee privilegios para realizar esta acción")
        print()

    elif pri >= 3:
        print("Ingrese los datos del nuevo usuario:")
        print()

        nombre_usuario = input("Nombre: ")
        if len(nombre_usuario) < 3:
            print()
            print("         ERROR. El nombre debe contener al menos 3 caracteres. No se realizaron cambios en el registro.")
            print()
            return

        apellido_usuario = input("Apellido: ")
        if len(apellido_usuario) < 3:
            print()
            print("         ERROR. El apellido debe contener al menos 3 caracteres. No se realizaron cambios en el registro.")
            print()
            return
            
        telefono_usuario = input("Teléfono: ")
        domicilio_usuario = input("Domicilio: ")
        login_usuario = generar_user(nombre_usuario, apellido_usuario)
        pass_usuario = "0000"
        
        try:
            privilegios_usuario = int(input("Nivel de privilegios (1-4): "))

        except ValueError:
            print("         ERROR. Debe indicar un valor numérico entre el 1 y el 4")
            print()
            return
        except:
            log_error()
            print()
            input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
            return 

        while privilegios_usuario > pri:
            print()
            print("     ERROR. Los privilegios del nuevo usuario no pueden exceder los propios.")
            print()
            privilegios_usuario = input("Nivel de privilegios: ")
        print()

        activo_usuario = 1
        nombre_usuario = reemplazar_comilla(nombre_usuario)
        apellido_usuario = reemplazar_comilla(apellido_usuario)
        telefono_usuario = reemplazar_comilla(telefono_usuario)
        domicilio_usuario = reemplazar_comilla(domicilio_usuario)

        parameters = str((nombre_usuario, apellido_usuario, telefono_usuario, domicilio_usuario,
                            login_usuario, pass_usuario, privilegios_usuario, activo_usuario))
        query = f"INSERT INTO usuarios (nombre, apellido, telefono, domicilio, user_name, pass, privilegios, activo) VALUES {parameters}"

        try:
            run_query(query)

        except sql.errors.UniqueViolation:
            print()
            print(f"         ERROR. Ya existe un usuario con el nombre {login_usuario}.")
            print()
            return

        print(f"Usuario {login_usuario} creado exitosamente.")
        print()
        print("ANTENCIÓN: Al realizar su primer ingreso deberá colocar la contraseña 0000 y luego se le solicitará la creación de una contraseña.")
        print()
        getpass("Presione enter para continuar... ")
        print()


def opcion_modificar_usuarios() -> int:                                                             # OPCIÓN MENÚ MODIFICAR USUARIOS
    """Muestra al usuario un menú y luego le solicita ingresar una de las
    opciones mostradas a través del número correspondiente. En caso de no
    ingresar una opción correcta, se le volverá a solicitar.

    :rtype: int
    """
    print()
    print("********** Acciones disponibles **********")
    print()
    print("   1. Modificar nombre")
    print("   2. Modificar apellido")
    print("   3. Modificar teléfono")
    print("   4. Modificar domicilio")
    print("   5. Modificar contraseña")
    print("   6. Modificar privilegios")
    print("   0. Volver")
    print()
    try:
        opcion = int(input("Ingrese una opción: "))
        while opcion < 0 or opcion > 6:
            print()
            print("Opción incorrecta.")
            print()
            opcion = int(input("Ingrese una opción: "))
    except ValueError: 
        print("Opción incorrecta.")
        opcion = -1
    except:
        log_error()
        print()
        input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
        opcion -1
    return opcion


def modificar_usuario(idu: int):
    """Recibe el ID del usuario. Luego llama a la función donde se muestra las
    opciones y recibe, a través de ella, la opción ingresada por el usuario.
    Luego, según la opción ingresada, permite al usuario realizar alguna de las
    siguientes acciones:

    - Modificar el nombre del usuario
    - Modificar el apellido del usuario
    - Modificar el teléfono del usuario
    - Modificar el domicilio del usuario
    - Modificar la contraseña del usuario
    - Modificar el nivel de privilegios del usuario

    Luego, en caso de realizar la acción de manera correcta, se registra la
    modificación en la base de datos.

    Nivel de privilegios necesario: Sólo pueden modificarse los datos del
    usuario que está realizando la acción o de usuarios con nivel de
    privilegios inferior a éste.
    
    En caso de intentar modificar la contraseña se solicitará en primer lugar
    la contraseña actual y sólo se podrá modificar la contraseña del usuario
    que está intentando realizar la acción, a excepción de aquellos usuarios
    de nivel 4 o superior, quienes podrán modificar la contraseña de otros
    usuarios, siempre que éstos sean de nivel inferior al propio.

    Si al ingresar la contraseña actual se realizan tres intentos fallidos
    concecutivos el sistema bloqueará la cuenta del usuario y cerrará el
    programa.

    Al ingresar una nueva contraseña el sistema le solicitará al usuario
    que repita la misma con el objetivo de evitar ingresar una contraseña
    no deseada.

    Una nueva contraseña no puede ser nunca 0000, ya que ésta se utiliza
    de manera genérica al crear un nuevo usuario y no está permitido su uso.

    :param idu: ID de usuario
    :type idu: int
    """
    i_d, nom, ape, tel, dom, use, pas, pri, act = buscar_usuario_por_id(idu)

    opcion = -1
    while opcion != 0:
        opcion = opcion_modificar_usuarios()
        print()

        if opcion == 1:     # Modificar nombre
            usuario = str(input("Indique el usuario que desea modificar: "))
            print()
            
            try:
                i_d_m, nom_m, ape_m, tel_m, dom_m, use_m, pas_m, pri_m, act_m = buscar_usuario_por_user(usuario)
            
            except TypeError:
                print("         ERROR. Nombre de usuario inexistente")
                return
            except:
                log_error()
                print()
                input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
                return
            print()
            
            while pri <= pri_m and i_d != i_d_m:
                print("         ERROR. Sólo pueden modificarse los datos propios o de usuarios de niveles inferiores.")
                print()
            
                usuario = str(input("Indique el usuario que desea modificar o presione enter para volver: "))
                print()
            
                if usuario != "":
                    try:
                        i_d_m, nom_m, ape_m, tel_m, dom_m, use_m, pas_m, pri_m, act_m = buscar_usuario_por_user(usuario)
            
                    except TypeError:
                        print("         ERROR. Nombre de usuario inexistente")
                        return
                    except:
                        log_error()
                        print()
                        input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
                        return
            
                elif usuario == "":
                    return
            
            nuevo_nombre = str(input("Ingrese el nuevo nombre: "))
            
            if len(nuevo_nombre) < 3:
                print()
                print("         ERROR. El nombre debe contener al menos 3 caracteres. No se realizaron cambios en el registro.")
                print()
                return
            
            nuevo_user = generar_user(nuevo_nombre, ape_m)
            try:
                edit_registro('usuarios', 'user_name', nuevo_user, i_d_m)
            
            except sql.errors.UniqueViolation:
                print()
                print(f"         ERROR. Ya existe un usuario con el nombre {nuevo_user}.")
                print()
                return
            
            edit_registro('usuarios', 'nombre', nuevo_nombre, i_d_m)
            print()
            print(f"Nombre modificado correctamente. El nuevo nombre de usuario es: {nuevo_user}")
            print()
        
        elif opcion == 2:   # Modificar apellido
            usuario = str(input("Indique el usuario que desea modificar: "))
            print()
            
            try:
                i_d_m, nom_m, ape_m, tel_m, dom_m, use_m, pas_m, pri_m, act_m = buscar_usuario_por_user(usuario)
            
            except TypeError:
                print("         ERROR. Nombre de usuario inexistente")
                return
            except:
                log_error()
                print()
                input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
                return
            print()
            
            while pri <= pri_m and i_d != i_d_m:
                print("         ERROR. Sólo pueden modificarse los datos propios o de usuarios de niveles inferiores.")
                print()
            
                usuario = str(input("Indique el usuario que desea modificar o presione enter para volver: "))
                print()
            
                if usuario != "":
                    try:
                        i_d_m, nom_m, ape_m, tel_m, dom_m, use_m, pas_m, pri_m, act_m = buscar_usuario_por_user(usuario)
            
                    except TypeError:
                        print("         ERROR. Nombre de usuario inexistente")
                        return
                    except:
                        log_error()
                        print()
                        input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
                        return
            
                elif usuario == "":
                    return
            
            nuevo_apellido = str(input("Ingrese el nuevo apellido: "))
            
            if len(nuevo_apellido) < 3:
                print()
                print("         ERROR. El apellido debe contener al menos 3 caracteres. No se realizaron cambios en el registro.")
                print()
                return
            
            nuevo_user = generar_user(nom_m, nuevo_apellido)
            try:
                edit_registro('usuarios', 'user_name', nuevo_user, i_d_m)
            
            except sql.errors.UniqueViolation:
                print()
                print(f"         ERROR. Ya existe un usuario con el nombre {nuevo_user}.")
                print()
                return
            
            edit_registro('usuarios', 'apellido', nuevo_apellido, i_d_m)
            print()
            print(f"Apellido modificado correctamente. El nuevo nombre de usuario es: {nuevo_user}")
            print()
        
        elif opcion == 3:   # Modificar teléfono
            usuario = str(input("Indique el usuario que desea modificar: "))
            print()
            
            try:
                i_d_m, nom_m, ape_m, tel_m, dom_m, use_m, pas_m, pri_m, act_m = buscar_usuario_por_user(usuario)
            
            except TypeError:
                print("         ERROR. Nombre de usuario inexistente")
                return
            except:
                log_error()
                print()
                input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
                return
            print()
            
            while pri <= pri_m and i_d != i_d_m:
                print("         ERROR. Sólo pueden modificarse los datos propios o de usuarios de niveles inferiores.")
                print()
            
                usuario = str(input("Indique el usuario que desea modificar o presione enter para volver: "))
                print()
            
                if usuario != "":
                    try:
                        i_d_m, nom_m, ape_m, tel_m, dom_m, use_m, pas_m, pri_m, act_m = buscar_usuario_por_user(usuario)
            
                    except TypeError:
                        print("         ERROR. Nombre de usuario inexistente")
                        return
                    except:
                        log_error()
                        print()
                        input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
                        return
            
                elif usuario == "":
                    return
            
            nuevo_telefono = str(input("Ingrese el nuevo teléfono: "))
            edit_registro('usuarios', 'telefono', nuevo_telefono, i_d_m)
            print()
            print(f"Teléfono modificado correctamente.")
            print()
        
        elif opcion == 4:   # Modificar domicilio
            usuario = str(input("Indique el usuario que desea modificar: "))
            print()
            
            try:
                i_d_m, nom_m, ape_m, tel_m, dom_m, use_m, pas_m, pri_m, act_m = buscar_usuario_por_user(usuario)
            
            except TypeError:
                print("         ERROR. Nombre de usuario inexistente")
                return
            except:
                log_error()
                print()
                input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
                return
            print()
            
            while pri <= pri_m and i_d != i_d_m:
                print("         ERROR. Sólo pueden modificarse los datos propios o de usuarios de niveles inferiores.")
                print()
            
                usuario = str(input("Indique el usuario que desea modificar o presione enter para volver: "))
                print()
            
                if usuario != "":
                    try:
                        i_d_m, nom_m, ape_m, tel_m, dom_m, use_m, pas_m, pri_m, act_m = buscar_usuario_por_user(usuario)
            
                    except TypeError:
                        print("         ERROR. Nombre de usuario inexistente")
                        return
                    except:
                        log_error()
                        print()
                        input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
                        return
            
                elif usuario == "":
                    return
            
            nuevo_domicilio = str(input("Ingrese el nuevo domicilio: "))
            edit_registro('usuarios', 'domicilio', nuevo_domicilio, i_d_m)
            print()
            print(f"Domicilio modificado correctamente.")
            print()
        
        elif opcion == 5:   # Modificar contraseña
            if pri < 4:
                counter = 0

                pw_act = getpass("Ingrese su contraseña actual: ")
                print()

                while pw_act != pas:
                    print("Contraseña incorrecta")
                    print()
                    counter += 1

                    if counter == 3:
                        edit_registro('usuarios', 'activo', 2, i_d)
                        print("Su usuario ha sido bloqueado por repetición de claves incorrectas. Comuníquese con un administrador.")
                        exit()

                    pw_act = getpass("Ingrese su contraseña actual: ")
                    print()

                if pw_act == pas:
                    pw_new = str(getpass("Ingrese la nueva contraseña: "))
                    print()

                    while len(pw_new) < 4:
                        print("La contraseña debe ser de 4 dígitos o más.")
                        pw_new = str(getpass("Ingrese la nueva contraseña: "))
                        print()

                    while pw_new == "0000":
                        print("La contraseña no puede ser 0000.")
                        pw_new = str(getpass("Ingrese la nueva contraseña: "))
                        print()

                    pw_conf = str(getpass("Repita la nueva contraseña: "))
                    print()

                    if pw_new == pw_conf:
                        edit_registro('usuarios', 'pass', str(pw_new), i_d)
                        print("Contraseña actualizada exitosamente.")
                        print()
                    else:
                        print("         ERROR. Las contraseñas no coinciden.")
                        print()

            elif pri >= 4:
                counter = 0

                pw_act = getpass("Ingrese su contraseña actual: ")
                print()

                while pw_act != pas:
                    print("Contraseña incorrecta")
                    print()
                    counter += 1

                    if counter == 3:
                        edit_registro('usuarios', 'activo', 2, i_d)
                        print("Su usuario ha sido bloqueado por repetición de claves incorrectas. Comuníquese con un administrador.")
                        exit()

                    pw_act = getpass("Ingrese su contraseña actual: ")
                    print()

                if pw_act == pas:
                    usuario = str(input("Indique el usuario que desea modificar: "))
                    print()

                    try:
                        i_d_m, nom_m, ape_m, tel_m, dom_m, use_m, pas_m, pri_m, act_m = buscar_usuario_por_user(usuario)

                    except TypeError:
                        print("         ERROR. Nombre de usuario inexistente")
                        return
                    except:
                        log_error()
                        print()
                        input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
                        return
                    print()

                    if pri <= pri_m:
                        print("         ERROR. Sólo pueden modificarse la contraseña de usuarios de niveles inferiores.")
                        print()
                        return

                    pw_new = str(getpass("Ingrese la nueva contraseña: "))
                    print()

                    while len(pw_new) < 4:
                        print("La contraseña debe ser de 4 dígitos o más.")
                        pw_new = str(getpass("Ingrese la nueva contraseña: "))
                        print()

                    while pw_new == "0000" and i_d_m == i_d:
                        print("La contraseña no puede ser 0000.")
                        pw_new = str(getpass("Ingrese la nueva contraseña: "))
                        print()
                    pw_conf = str(getpass("Repita la nueva contraseña: "))
                    print()

                    if pw_new == pw_conf:
                        edit_registro('usuarios', 'pass', str(pw_new), i_d_m)
                        print("Contraseña actualizada exitosamente.")
                        print()
                    else:
                        print("         ERROR. Las contraseñas no coinciden.")
                        print()
        
        elif opcion == 6:   # Modificar privilegios
            if pri < 4:
                print("         ERROR. Los privilegios sólo pueden ser modificados por usuarios de nivel 4.")
            
            elif pri >= 4:
                usuario = str(input("Indique el usuario que desea modificar: "))
                print()
            
                try:
                    i_d_m, nom_m, ape_m, tel_m, dom_m, use_m, pas_m, pri_m, act_m = buscar_usuario_por_user(usuario)
            
                except TypeError:
                    print("         ERROR. Nombre de usuario inexistente")
                    return
                except:
                    log_error()
                    print()
                    input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
                    return
            
                while i_d_m == i_d or pri <= pri_m:
            
                    if i_d_m == i_d:
                        print("         ERROR. Un usuario no puede modificarse a si mismo sus privilegios.")
                        print()
            
                    elif pri <= pri_m:
                        print("         ERROR. Sólo pueden modificarse los datos de usuarios de niveles inferiores.")
                        print()
                    usuario = str(input("Indique el usuario que desea modificar o presione enter para volver: "))
                    print()
                    if usuario == "":
                        return
            
                    try:
                        i_d_m, nom_m, ape_m, tel_m, dom_m, use_m, pas_m, pri_m, act_m = buscar_usuario_por_user(usuario)
            
                    except TypeError:
                        print("         ERROR. Nombre de usuario inexistente")
                        print()
                        return
                    except:
                        log_error()
                        input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
                        print()
                        return
            
                try:
                    nuevo_privilegio = int(input("Ingrese el nuevo nivel de privilegios (1-4): "))
            
                except ValueError:
                    print("         ERROR. Debe indicar un valor numérico entre el 1 y el 4")
                    print()
                    return
                except:
                    log_error()
                    print()
                    input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
                    return
                print()
            
                while nuevo_privilegio < 1 or nuevo_privilegio > 4:
                    print("         ERROR. Debe indicar un valor numérico entre el 1 y el 4")
                    print()
            
                    try:
                        nuevo_privilegio = int(input("Ingrese el nuevo nivel de privilegios (1-4): "))
            
                    except ValueError:
                        print("         ERROR. Debe indicar un valor numérico entre el 1 y el 4")
                        print()
                        return
                    except:
                        log_error()
                        print()
                        input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
                        return
            
                edit_registro('usuarios', 'privilegios', nuevo_privilegio, i_d_m)
                print()
                print(f"Privilegios modificados correctamente.")
                print()


def activar_usuario(idu: int):
    """Permite al usuario activar cuentas de usuario que se encuentren inactivas
    o bloqueadas.

    Nivel de privilegios mínimo: 4

    :param idu: ID de usuario
    :type idu: int
    """
    i_d, nom, ape, tel, dom, use, pas, pri, act = buscar_usuario_por_id(idu)
    msj = " "

    if pri < 4:
        print("         ERROR. Los usuarios inactivados sólo pueden ser reactivados por usuarios de nivel 4.")

    elif pri >= 4:
        usuario = str(input("Indique el usuario que desea reactivar: "))
        print()

        try:
            i_d_m, nom_m, ape_m, tel_m, dom_m, use_m, pas_m, pri_m, act_m = buscar_usuario_por_user(usuario)

        except TypeError:
            print("         ERROR. Nombre de usuario inexistente")
            return
        except:
            log_error()
            print()
            input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
            return

        while i_d_m == i_d:
            print("         ERROR. Un usuario no puede reactivarse a si mismo.")

            try:
                usuario = str(input("Indique el usuario que desea reactivar: "))
                print()
                i_d_m, nom_m, ape_m, tel_m, dom_m, use_m, pas_m, pri_m, act_m = buscar_usuario_por_user(usuario)

            except TypeError:
                print("         ERROR. Nombre de usuario inexistente")
                return
            except:
                log_error()
                print()
                input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
                return

        msj = ""
        while msj != "S" and msj != "N":
            msj = input(f"¿Seguro que quiere reactivar el usuario <{use_m}>, perteneciente a {nom_m} {ape_m}? (S/N): ")

            if msj in AFIRMATIVO:
                msj = "S"
                edit_registro('usuarios', 'activo', 1, i_d_m)
                print()
                print("Usuario reactivado exitosamente.")
                print()
                return

            elif msj in NEGATIVO:
                msj = "N"
                print()
                print("No se han realizado cambios en el registro.")
                print()
                return

            else:
                print()
                print("         ERROR. Debe indicar S para inactivar o N para cancelar.")
                print()


def inactivar_usuario(idu: int):
    """Permite al usuario inactivar cuentas de usuarios.

    Nivel de privilegios mínimo: 4

    :param idu: ID de usuario
    :type idu: int
    """
    i_d, nom, ape, tel, dom, use, pas, pri, act = buscar_usuario_por_id(idu)
    msj = " "

    if pri < 4:
        print("         ERROR. Los usuarios sólo pueden ser dados de baja por usuarios de nivel 4.")

    elif pri >= 4:
        usuario = str(input("Indique el usuario que desea inactivar: "))
        print()

        try:
            i_d_m, nom_m, ape_m, tel_m, dom_m, use_m, pas_m, pri_m, act_m = buscar_usuario_por_user(usuario)

        except TypeError:
            print("         ERROR. Nombre de usuario inexistente")
            return
        except:
            log_error()
            print()
            input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
            return

        while i_d_m == i_d:
            print("         ERROR. Un usuario no puede darse de baja a si mismo.")

            try:
                usuario = str(input("Indique el usuario que desea inactivar: "))
                print()
                i_d_m, nom_m, ape_m, tel_m, dom_m, use_m, pas_m, pri_m, act_m = buscar_usuario_por_user(usuario)

            except TypeError:
                print("         ERROR. Nombre de usuario inexistente")
                return
            except:
                log_error()
                print()
                input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
                return

        msj = ""
        while msj != "S" and msj != "N":
            msj = input(f"¿Seguro que quiere dar de baja al usuario <{use_m}>, perteneciente a {nom_m} {ape_m}? (S/N): ")
            if msj in AFIRMATIVO:
                msj = "S"
                edit_registro('usuarios', 'activo', 0, i_d_m)
                print()
                print("Usuario inactivado exitosamente.")
                print()
                return

            elif msj in NEGATIVO:
                msj = "N"
                print()
                print("No se han realizado cambios en el registro.")
                print()
                return

            else:
                print()
                print("         ERROR. Debe indicar S para inactivar o N para cancelar.")
                print()



    opcion = -1
    while opcion != 0:
        opcion = opcion_menu()
        if opcion == 1:
            menu_usuarios(idu)
        elif opcion == 2:
            menu_panteones(idu)
        elif opcion == 3:
            return
            menu_nichos(idu)
        elif opcion == 4:
            return
            menu_cobradores(idu)
        elif opcion == 5:
            return
            menu_precios(idu)
        elif opcion == 6:
            return
            menu_mails(idu)
        elif opcion == 0:
            return    


def opcion_menu_panteones() -> int:                                                                 # OPCIÓN MENÚ DE PANTEONES
    """Muestra al usuario un menú y luego le solicita ingresar una de las
    opciones mostradas a través del número correspondiente. En caso de no
    ingresar una opción correcta, se le volverá a solicitar.

    :rtype: int
    """
    print()
    print("********** Acciones disponibles **********")
    print()
    print("   1. Agregar nuevo panteón")
    print("   2. Editar un panteón")
    print("   3. Eliminar un panteón")
    print("   0. Volver")
    print()
    try:
        opcion = int(input("Ingrese una opción: "))
        while opcion < 0 or opcion > 3:
            print()
            print("Opción incorrecta.")
            print()
            opcion = int(input("Ingrese una opción: "))
    except ValueError: 
        print("Opción incorrecta.")
        opcion = -1
    except:
        log_error()
        print()
        input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
        opcion = -1
    return opcion


def menu_panteones(idu: int):                                                                       # MENÚ DE PANTEONES
    """Recibe el ID del usuario. Luego llama a la función donde se muestra las
    opciones y recibe, a través de ella, la opción ingresada por el usuario.
    Luego, según la opción ingresada, llama a la función correspondiente, a la
    cual le transmite el ID del usuario.

    :param idu: ID de usuario
    :type idu: int
    """
    opcion = -1
    while opcion != 0:
        opcion = opcion_menu_panteones()
        if opcion == 1:
            agregar_panteon(idu)
        elif opcion == 2:
            editar_panteon(idu)
        elif opcion == 3:
            eliminar_panteon(idu)


def agregar_panteon(idu: int):
    """Permite al usuario registrar un nuevo panteon en la base de datos.
    El mismo es ingresado, también, en los archivos .mf auxiliares a la BD.

    Nivel de privilegios mínimo: 3

    :param idu: ID de usuario
    :type idu: int
    """
    i_d, nom, ape, tel, dom, use, pas, pri, act = buscar_usuario_por_id(idu)
    msj = " "
    print()

    if pri < 3:
        print("         ERROR. No posee los privilegios necesarios para realizar esta operación.")
        print()
        return

    elif pri >= 3:
        nuevo_panteon = input("Ingrese el nombre del nuevo panteon: ").title()
        print()
        print()

        msj = ""
        while msj != "S" and msj != "N":
            nuevo_panteon = reemplazar_comilla(nuevo_panteon)
            msj = str(input(f"¿Seguro que quiere dar de alta el panteón <{nuevo_panteon}>? (S/N): "))

            if msj in AFIRMATIVO:
                msj = "S"
                print()
                print("Agregando panteón. Aguarde un momento.")
                query = f"INSERT INTO panteones (panteon) VALUES ('{nuevo_panteon}')"
                try:
                    run_query(query)

                except sql.errors.UniqueViolation:
                    print()
                    print("         ERROR. Ya existe un panteón con ese nombre. No se realizaron cambios en el registro.")
                    print()
                    return
                except:
                    log_error()
                    print()
                    input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
                    return

                with open('../databases/categ_ing.mf', 'a', encoding='Utf-8') as archivo_categ:
                    archivo_categ.write(f"\nMantenimiento {nuevo_panteon}")
                
                with open("../databases/panteones.mf", 'a', encoding='Utf-8') as archivo_pant:
                    archivo_pant.write(f'\nMantenimiento {nuevo_panteon}')
                
                print()
                print("Panteón agregado exitosamente.")
                print()
                return

            elif msj in NEGATIVO:
                msj = "N"
                print()
                print("No se han realizado cambios en el registro.")
                print()
                return
            else:
                print()
                print("         ERROR. Debe indicar S para dar de alta el panteón o N para cancelar.")
                print()


def editar_panteon(idu: int):
    """Permite al usuario modificar un panteón existente en la base de datos.

    ##        --------- ATENCIÓN! ---------
    Ésta opción se encuentra deshabilitada hasta que se deje obsoleto el uso
    de archivos auxiliares .mf

    Nivel de privilegios mínimo: 3

    :param idu: ID de usuario
    :type idu: int
    """
    i_d, nom, ape, tel, dom, use, pas, pri, act = buscar_usuario_por_id(idu)
    print()
    if pri < 3:
        print("         ERROR. No posee los privilegios necesarios para realizar esta operación.")
        print()
        return
    elif pri >= 3:
        print("Esta opción no se encuentra disponible por el momento. Comuníquese con el administrador.")


def eliminar_panteon(idu):
    """Permite al usuario eliminar de la base de datos un panteón existente.

    ##        --------- ATENCIÓN! ---------
    Ésta opción se encuentra deshabilitada hasta que se deje obsoleto el uso
    de archivos auxiliares .mf

    Nivel de privilegios mínimo: 3

    :param idu: ID de usuario
    :type idu: int
    """
    i_d, nom, ape, tel, dom, use, pas, pri, act = buscar_usuario_por_id(idu)
    print()
    if pri < 3:
        print("         ERROR. No posee los privilegios necesarios para realizar esta operación.")
        print()
        return
    elif pri >= 3:
        print("Esta opción no se encuentra disponible por el momento. Comuníquese con el administrador.")


def opcion_menu_nichos() -> int:                                                                    # OPCIÓN MENÚ DE NICHOS
    """Muestra al usuario un menú y luego le solicita ingresar una de las
    opciones mostradas a través del número correspondiente. En caso de no
    ingresar una opción correcta, se le volverá a solicitar.

    :rtype: int
    """
    print()
    print("********** Acciones disponibles **********")
    print()
    print("   1. Agregar un nicho")
    print("   2. Ocupar un nicho")
    print("   3. Cambiar categoría de un nicho")
    print("   4. Eliminar un nicho")
    print("   5. Agregar una categoría")
    print("   6. Eliminar una categoría")
    print("   0. Volver")
    print()
    try:
        opcion = int(input("Ingrese una opción: "))
        while opcion < 0 or opcion > 6:
            print()
            print("Opción incorrecta.")
            print()
            opcion = int(input("Ingrese una opción: "))
    except ValueError: 
        print("Opción incorrecta.")
        opcion = -1
    except:
        log_error()
        print()
        input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
        opcion = -1
    return opcion


def menu_nichos(idu: int):                                                                          # MENÚ DE NICHOS
    """Recibe el ID del usuario. Luego llama a la función donde se muestra las
    opciones y recibe, a través de ella, la opción ingresada por el usuario.
    Luego, según la opción ingresada, llama a la función correspondiente, a la
    cual le transmite el ID del usuario.

    :param idu: ID de usuario
    :type idu: int
    """
    opcion = -1
    while opcion != 0:
        opcion = opcion_menu_nichos()
        if opcion == 1:
            alta_nicho(idu)
        elif opcion == 2:
            ocupar_nicho(idu)
        elif opcion == 3:
            cambiar_cat_nicho(idu)
        elif opcion == 4:
            eliminar_nicho(idu)
        elif opcion == 5:
            agregar_categoria(idu)
        elif opcion == 6:
            eliminar_categoria(idu)
        elif opcion == 0:
            return


def alta_nicho(idu: int, ret: bool = False):
    """Permite al usuario registrar un nuevo nicho en la base de datos. 

    Nivel de privilegios mínimo: 2

    :param idu: ID de usuario
    :type idu: int

    :param ret: Indica si se debe retornar el código de nicho.
    Por defecto: False
    :pram type: bool
    """
    msj = " "
    i_d, nom, ape, tel, dom, use, pas, pri, act = buscar_usuario_por_id(idu)

    if pri < 2:
        print()
        print("         ERROR. No posee los privilegios necesarios para realizar esta acción.")
        print()

    else:
        print("*** Alta nuevo nicho ***")
        print()
        print("Indique número de panteón: ")

        datos = obtener_panteones()
        counter = 0
        for i in datos:
            counter += 1
            i_d_pan, n_pan = i
            print(f"    * {i_d_pan}. {n_pan}")
        print()

        try:
            panteon = int(input("Panteón: "))

        except ValueError:
            print("         ERROR. Debe ingresar un dato de tipo numérico.")
            print()
            return
        except:
            log_error()
            print()
            input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
            return

        while panteon < 1 or panteon > counter:
            print("         ERROR. Debe indicar un nro. de panteón válido.")
            print()

            try:
                panteon = int(input("Panteón: "))

            except ValueError:
                print("         ERROR. Debe ingresar un dato de tipo numérico.")
                print()
                return
            except:
                log_error()
                print()
                input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
                return

        piso = input("Indique el piso: ").upper()
        if len(piso) < 1 or len(piso) > 2:
            print("         ERROR. No debe ocupar más de dos caracteres.")
            print()
            return

        if "'" in piso:
            print("         ERROR. No se puede utilizar comillas simples (').")
            print()
            return

        try:
            fila = int(input("Indique número de fila: "))
            if len(str(fila)) < 1 or len(str(fila)) > 2:
                print("         ERROR. No debe ocupar más de dos caracteres.")
                print()
                return

        except ValueError:
            print("         ERROR. Debe ingresar un dato de tipo numérico.")
            print()
            return
        except:
            log_error()
            print()
            input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
            return

        try:
            nicho = int(input("Indique número de nicho: "))
            if len(str(nicho)) < 1 or len(str(nicho)) > 4:
                print("         ERROR. No debe ocupar más de cuatro caracteres.")
                print()
                return

        except ValueError:
            print("         ERROR. Debe ingresar un dato de tipo numérico.")
            print()
            return
        except:
            log_error()
            print()
            input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
            return

        print("Indique categoría del nicho: ")

        datos = obtener_cat_nichos()
        counter = 0
        for i in datos:
            counter += 1
            i_d_cat_nichos, cat_nichos, val_mant_bic, val_mant_nob = i
            print(f"    * {i_d_cat_nichos}. {cat_nichos}")
        print()

        try:
            cat_nicho = int(input("Categoría: "))

        except ValueError:
            print("         ERROR. Debe ingresar un dato de tipo numérico.")
            print()
            return
        except:
            log_error()
            print()
            input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
            return

        while cat_nicho < 1 or cat_nicho > counter:
            print("         ERROR. Debe indicar una categoría de nicho válida.")
            print()

            try:
                cat_nicho = int(input("Categoría: "))
                print()

            except ValueError:
                print("         ERROR. Debe ingresar un dato de tipo numérico.")
                print()
                return
            except:
                log_error()
                print()
                input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
                return

        fallecido = input("Si se encuentra ocupado coloque los datos del fallecido de lo contrario presione enter: ")

        if fallecido == "":
            ocupado = 0
            fallecido = 'NULL'

        else:
            fallecido = reemplazar_comilla(fallecido)
            ocupado = 1

        cod_nicho = f"{str(panteon).rjust(2, '0')}{str(piso).rjust(2, '0')}{str(fila).rjust(2, '0')}{str(nicho).rjust(4, '0')}"
        print()

        msj = ""
        while msj != "S" and msj != "N":
            id_c, cat, val_mant_bic, val_mant_nob = rend.obtener_categoria(cat_nicho)
            msj = str(input(f"¿Seguro que quiere dar de alta el nicho {cat} <{cod_nicho}>? (S/N): "))

            if msj in AFIRMATIVO:
                msj = "S"
                print()
                print("Agregando nicho. Aguarde un momento.")

                parameters = str((cod_nicho, panteon, str(piso).rjust(2, '0'), str(fila).rjust(2, '0'), str(nicho).rjust(4, '0'), cat_nicho, ocupado, fallecido))
                query = f"INSERT INTO nichos VALUES {parameters}"

                try:
                    run_query(query)
                    print()
                    print("Nicho agregado exitosamente.")
                    print()
                    if ret == True:
                        return cod_nicho

                except sql.errors.UniqueViolation:
                    print()
                    print("         ERROR. El nicho ya se encuentra cargado en el sistema. No se realizaron cambios en el registro.")

                    if ret == False:
                        return
                    elif ret == True:
                        return cod_nicho

                except:
                    log_error()
                    print()
                    input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")

                    if ret == False:
                        return
                    elif ret == True:
                        return cod_nicho

            elif msj in NEGATIVO:
                msj = "N"
                print()
                print("No se han realizado cambios en el registro.")
                print()
                return
            else:
                print()
                print("         ERROR. Debe indicar S para dar de alta el nicho o N para cancelar.")
                print()


def ocupar_nicho(idu: int):
    """Permite al usuario registrar los datos de un fallecido en un nicho registrado
    en la base de datos. En caso que ya se encuentren datos de un fallecido, se le
    ofrece al usuario la opción de modificar o eliminar dicha información.

    Nivel de privilegios mínimo: 2

    :param idu: ID de usuario
    :type idu: int
    """
    msj = " "
    i_d, nom, ape, tel, dom, use, pas, pri, act = buscar_usuario_por_id(idu)

    if pri < 2:
        print()
        print("         ERROR. No posee los privilegios necesarios para realizar esta acción.")
        print()

    else:
        print()
        print("*** Ocupar nicho ***")
        print()

        cod_nicho = input("Ingrese el código de nicho: ").upper()
        print()
        
        try:
            cod, pan, pis, fil, num, cat, ocu, fall = rend.obtener_datos_nicho(cod_nicho)
        
        except TypeError:
            print("         ERROR. El nicho indicado no se encuentra dado de alta.")
            return
        except:
            log_error()
            print()
            input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
            return
        
        if ocu == 1:
            msj = ""
            while msj != "S" and msj != "N":
                msj = str(input(f"El nicho {cod_nicho} ya se encuentra ocupado por {fall} ¿Quiere modificar los datos del fallecido? (S/N): "))
                print()

                if msj in AFIRMATIVO:
                    msj = "S"
                    fallecido = input("Ingrese los nuevos datos del fallecido: ")
                    edit_nicho('fallecido', fallecido, cod_nicho)
                    print()
                    print("Datos modificados exitosamente.")
                    print()
                    return
                
                elif msj in NEGATIVO:
                    msj = ""
                    while msj != "S" and msj != "N":
                        msj = str(input(f"¿Quiere cambiar el estado a desocupado? (S/N): "))
                        print()
                        if msj in AFIRMATIVO:
                            msj = "S"
                            edit_nicho('ocupado', 0, cod_nicho)
                            edit_nicho('fallecido', '', cod_nicho)
                            print()
                            print("Datos modificados exitosamente.")
                            print()
                            return
                        elif msj in NEGATIVO:
                            msj = "N"
                            print()
                            print("No se han realizado cambios en el registro.")
                            print()
                            return
                        else:
                            print()
                            print("         ERROR. Debe indicar S para desocupar el nicho o N para cancelar.")
                            print()
                
                else:
                    print()
                    print("         ERROR. Debe indicar S para modificar los datos del fallecido o N para cancelar.")
                    print()

        else:
            fallecido = input("Ingrese los datos del fallecido: ")
            print()
            edit_nicho('ocupado', 1, cod_nicho)
            edit_nicho('fallecido', fallecido, cod_nicho)
            print()
            print("Datos modificados exitosamente.")
            print()
            return

            
def cambiar_cat_nicho(idu: int):
    """Permite al usuario cambiar la categoría de un nicho y lo registra en la BD.

    Nivel de privilegios mínimo: 2

    :param idu: ID de usuario
    :type idu: int
    """
    msj = " "
    i_d, nom, ape, tel, dom, use, pas, pri, act = buscar_usuario_por_id(idu)

    if pri < 2:
        print()
        print("         ERROR. No posee los privilegios necesarios para realizar esta acción.")
        print()
    
    else:
        print()
        print("*** Editar la categoría de un nicho ***")
        print()
    
        cod_nicho = input("Ingrese el código de nicho: ").upper()
        print()
    
        try:
            cod, pan, pis, fil, num, cat, ocu, fall = rend.obtener_datos_nicho(cod_nicho)
    
        except TypeError:
            print("         ERROR. El nicho indicado no se encuentra dado de alta.")
            return
        except:
            log_error()
            print()
            input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
            return
    
        i_d_ant, categ_nicho_ant, val_bic_ant, val_nob_ant = rend.obtener_categoria(cat)
        print(f"El nicho {cod_nicho} pertenece a la categoría {categ_nicho_ant}.")
        print("Indique la nueva categoría: ")
        
        datos = obtener_cat_nichos()
        
        counter = 0
        for i in datos:
            counter += 1
            i_d_cat_nichos, cat_nichos, val_mant_bic, val_mant_nob = i
            print(f"    * {i_d_cat_nichos}. {cat_nichos}")
        print()
        
        try:
            cat_nicho = int(input("Categoría: "))
        
        except ValueError:
            print("         ERROR. Debe ingresar un dato de tipo numérico.")
            print()
            return
        except:
            log_error()
            print()
            input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
            return
        
        while cat_nicho < 1 or cat_nicho > counter:
            print("         ERROR. Debe indicar una categoría de nicho válida.")
            print()
        
            try:
                cat_nicho = int(input("Categoría: "))
                print()
        
            except ValueError:
                print("         ERROR. Debe ingresar un dato de tipo numérico.")
                print()
                return
            except:
                log_error()
                print()
                input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
                return
        
        i_d_ant, nueva_categ_nicho, val_bic_ant, val_nob_ant = rend.obtener_categoria(cat_nicho)
        msj = ""
        while msj != "S" and msj != "N":
            msj = str(input(f"¿Seguro quiere cambiar la categoría del nicho {cod_nicho} de {categ_nicho_ant} a {nueva_categ_nicho}? (S/N): "))
            
            if msj in AFIRMATIVO:
                msj = "S"
                edit_nicho('categoria', cat_nicho, cod_nicho)
                print()
                print("Datos modificados exitosamente.")
                print()
                return
            
            elif msj in NEGATIVO:
                msj = "N"
                print()
                print("No se han realizado cambios en el registro.")
                print()
                return
            
            else:
                print()
                print("         ERROR. Debe indicar S para cambiar la categoría del nicho o N para cancelar.")
                print()


def eliminar_nicho(idu: int):
    """Permite al usuario eliminar un nicho de la base de datos en caso
    que no esté ocupado ni asociado a una operación.

    Nivel de privilegios mínimo: 2

    :param idu: ID de usuario
    :type idu: int
    """
    msj = " "
    i_d, nom, ape, tel, dom, use, pas, pri, act = buscar_usuario_por_id(idu)

    if pri < 2:
        print()
        print("         ERROR. No posee los privilegios necesarios para realizar esta acción.")
        print()
    
    else:
        print()
        print("*** Eliminar nicho ***")
        print()
    
        cod_nicho = input("Ingrese el código de nicho: ").upper()
        print()
    
        try:
            cod, pan, pis, fil, num, cat, ocu, fall = rend.obtener_datos_nicho(cod_nicho)
    
        except TypeError:
            print("         ERROR. El nicho indicado no se encuentra dado de alta.")
            return
        except:
            log_error()
            print()
            input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
            return
    
        operacion = buscar_op_por_nicho(cod_nicho)
        if ocu == 0 and len(operacion) == 0:
            msj = ""
        
            while msj != "S" and msj != "N":
                msj = str(input(f"¿Seguro quiere eliminar el nicho {cod_nicho}? (S/N): "))
        
                if msj in AFIRMATIVO:
                    msj = "S"
                    delete_row('nichos', 'codigo', cod_nicho)
                    print()
                    print("Datos eliminados exitosamente.")
                    print()
                    return
                elif msj in NEGATIVO:
                    msj = "N"
                    print()
                    print("No se han realizado cambios en el registro.")
                    print()
                    return
                else:
                    print()
                    print("         ERROR. Debe indicar S para eliminar el nicho o N para cancelar.")
                    print()
        
        elif len(operacion) == 1:
            i_d, soc, nic, fac, cob, tar, rut, ult, u_a, fec, mor, c_f, u_r, paga, op_cob, nom_alt, dom_alt = operacion[0]
            i_d, nom, dni, tel1, tel2, mail, dom, loc, c_p, f_n, f_a, act = rend.obtener_datos_socio(soc)
            print(f"         ERROR. El nicho {cod_nicho} se encuentra relacionado a la operación nro. {str(i_d).rjust(7, '0')} del asociado {str(soc).rjust(6, '0')} - {nom}")
            print()
            return
        
        elif ocu == 1:
            print(f"         ERROR. El nicho {cod_nicho} se encuentra ocupado. Cambie el estado antes de eliminarlo.")
            print()
            return


def agregar_categoria(idu: int):
    """Permite al usuario agregar una categoría de nicho y la registra en la BD.
    A la misma se le debe indicar precio de mantenimiento para Bicon y NOB.

    Nivel de privilegios mínimo: 3

    :param idu: ID de usuario
    :type idu: int
    """
    msj = " "
    i_d, nom, ape, tel, dom, use, pas, pri, act = buscar_usuario_por_id(idu)
    
    if pri < 3:
        print()
        print("         ERROR. No posee los privilegios necesarios para realizar esta acción.")
        print()
    
    else:
        print()
        print("*** Agregar categoría de nicho ***")
        print()
        categoria = input("Ingrese el nombre de la categoría: ").title()
        print()
    
        while len(categoria) < 3:
            print("El nombre de la categoría debe tener al menos 3 caracteres de largo.")
            categoria = input("Ingrese el nombre de la categoría: ").title()
    
        try:
            val_mant_bic = int(input("Indique el costo de mantenimiento para operaciones de Bicon: $ "))
    
        except ValueError:
            print("         ERROR. Se debe indicar un dato de tipo numérico.")
            return
        except:
            log_error()
            print()
            input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
            return
        print()
    
        try:
            val_mant_nob = int(input("Indique el costo de mantenimiento para operaciones de NOB: $ "))

        except ValueError:
            print("         ERROR. Se debe indicar un dato de tipo numérico.")
            return
        except:
            log_error()
            print()
            input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
            return
        print()

        parameters = str((categoria, float(val_mant_bic), float(val_mant_nob)))
        query = f"INSERT INTO cat_nichos (categoria, valor_mant_bicon, valor_mant_nob) VALUES {parameters}"

        try:
            run_query(query)
            print("Categoría agregada exitosamente. Recuerde agregar los precios de compra.")
            print()

        except sql.errors.UniqueViolation:
            print("         ERROR. Ya existe una categoría con ese nombre. No se realizaron cambios en el registro.")
            print()
        except:
            log_error()
            print()
            input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
            print()
        print()


def eliminar_categoria(idu: int):
    """Permite al usuario eliminar una categoría de nicho.
    
    Nivel de privilegios mínimo: 3

    :param idu: ID de usuario
    :type idu: int
    """
    msj = " "
    i_d, nom, ape, tel, dom, use, pas, pri, act = buscar_usuario_por_id(idu)
    
    if pri < 3:
        print()
        print("         ERROR. No posee los privilegios necesarios para realizar esta acción.")
        print()
    
    else:
        print()
        print("*** Eliminar categoría de nicho ***")
        print()
        print("Ingrese el código de categoría: ")
        
        datos = obtener_cat_nichos()        
        counter = 0
        for i in datos:
            counter += 1
            i_d_cat_nichos, cat_nichos, val_mant_bic, val_mant_nob = i
            print(f"    * {i_d_cat_nichos}. {cat_nichos}")
        print()
        
        try:
            cat_nicho = int(input("Categoría: "))
        
        except ValueError:
            print("         ERROR. Debe ingresar un dato de tipo numérico.")
            print()
            return
        except:
            log_error()
            print()
            input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
            return
        
        while cat_nicho < 1 or cat_nicho > counter:
            print("         ERROR. Debe indicar una categoría de nicho válida.")
            print()
        
            try:
                cat_nicho = int(input("Categoría: "))
                print()
        
            except ValueError:
                print("         ERROR. Debe ingresar un dato de tipo numérico.")
                print()
                return
            except:
                log_error()
                print()
                input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
                return
        
        i_d, cat, val_mant_bic, val_mant_nob = rend.obtener_categoria(cat_nicho)
        msj = ""
        while msj != "S" and msj != "N":
            msj = str(input(f"¿Seguro quiere eliminar la categoría {cat}? (S/N): "))
            if msj in AFIRMATIVO:
                msj = "S"
                delete_row('cat_nichos', 'id', cat_nicho)
                print()
                print("Categoría eliminada exitosamente.")
                print()
                return
            elif msj in NEGATIVO:
                msj = "N"
                print()
                print("No se han realizado cambios en el registro.")
                print()
                return
            else:
                print()
                print("         ERROR. Debe indicar S para eliminar la categoría o N para cancelar.")
                print()


def opcion_menu_cobradores() -> int:                                                                # OPCIÓN MENÚ DE COBRADORES
    """Muestra al usuario un menú y luego le solicita ingresar una de las
    opciones mostradas a través del número correspondiente. En caso de no
    ingresar una opción correcta, se le volverá a solicitar.

    :rtype: int
    """
    print()
    print("********** Acciones disponibles **********")
    print()
    print("   1. Agregar un cobrador")
    print("   2. Editar un cobrador")
    print("   3. Eliminar un cobrador")
    print("   0. Volver")
    print()
    try:
        opcion = int(input("Ingrese una opción: "))
        while opcion < 0 or opcion > 3:
            print()
            print("Opción incorrecta.")
            print()
            opcion = int(input("Ingrese una opción: "))
    except ValueError: 
        print("Opción incorrecta.")
        opcion = -1
    except:
        log_error()
        print()
        input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
        opcion = -1
    return opcion


def menu_cobradores(idu: int):                                                                      # MENÚ DE COBRADORES
    """Recibe el ID del usuario. Luego llama a la función donde se muestra las
    opciones y recibe, a través de ella, la opción ingresada por el usuario.
    Luego, según la opción ingresada, llama a la función correspondiente, a la
    cual le transmite el ID del usuario.

    :param idu: ID de usuario
    :type idu: int
    """
    opcion = -1
    while opcion != 0:
        opcion = opcion_menu_cobradores()
        if opcion == 1:
            alta_cobrador(idu)
        elif opcion == 2:
            editar_cobrador(idu)
        elif opcion == 3:
            eliminar_cobrador(idu)
        elif opcion == 0:
            return


def alta_cobrador(idu: int):
    """Permite al usuario registrar un nuevo cobrador en la base de datos.
    El mismo es ingresado, también, en los archivos .mf auxiliares a la BD.

    Nivel de privilegios mínimo: 3

    :param idu: ID de usuario
    :type idu: int
    """
    i_d, nom, ape, tel, dom, use, pas, pri, act = buscar_usuario_por_id(idu)
    msj = " "
    print()
    
    if pri < 3:
        print("         ERROR. No posee los privilegios necesarios para realizar esta operación.")
        print()
        return
    
    elif pri >= 3:
        nuevo_cobrador = input("Ingrese el nombre del nuevo cobrador: ").title()
        print()
        print()
        msj = ""
        
        while msj != "S" and msj != "N":
            nuevo_cobrador = reemplazar_comilla(nuevo_cobrador)
            msj = str(input(f"¿Seguro que quiere dar de alta el cobrador <{nuevo_cobrador}>? (S/N): "))
        
            if msj in AFIRMATIVO:
                msj = "S"
                print()
                print("Agregando cobrador. Aguarde un momento.")
                query = f"INSERT INTO cobradores (cobrador) VALUES ('{nuevo_cobrador}')"
        
                try:
                    run_query(query)
        
                except sql.errors.UniqueViolation:
                    print()
                    print("         ERROR. Ya existe un cobrador con ese nombre. No se realizaron cambios en el registro.")
                    print()
                    return
                except:
                    log_error()
                    print()
                    input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
                    return
        
                with open("../databases/cobradores.mf", 'a', encoding='Utf-8') as archivo_cob:
                    archivo_cob.write(f'\n{nuevo_cobrador}')
                
                print()
                print("Cobrador agregado exitosamente.")
                print()
                return

            elif msj in NEGATIVO:
                msj = "N"
                print()
                print("No se han realizado cambios en el registro.")
                print()
                return
            else:
                print()
                print("         ERROR. Debe indicar S para dar de alta el cobrador o N para cancelar.")
                print()


def editar_cobrador(idu: int):
    """Permite al usuario modificar un cobrador existente en la base de datos.

    ##        --------- ATENCIÓN! ---------
    Ésta opción se encuentra deshabilitada hasta que se deje obsoleto el uso
    de archivos auxiliares .mf

    Nivel de privilegios mínimo: 3

    :param idu: ID de usuario
    :type idu: int
    """
    i_d, nom, ape, tel, dom, use, pas, pri, act = buscar_usuario_por_id(idu)
    print()
    if pri < 3:
        print("         ERROR. No posee los privilegios necesarios para realizar esta operación.")
        print()
        return
    elif pri >= 3:
        print("Esta opción no se encuentra disponible por el momento. Comuníquese con el administrador.")


def eliminar_cobrador(idu: int):
    """Permite al usuario eliminar de la base de datos un cobrador existente.

    ##        --------- ATENCIÓN! ---------
    Ésta opción se encuentra deshabilitada hasta que se deje obsoleto el uso
    de archivos auxiliares .mf

    Nivel de privilegios mínimo: 3

    :param idu: ID de usuario
    :type idu: int
    """
    i_d, nom, ape, tel, dom, use, pas, pri, act = buscar_usuario_por_id(idu)
    print()
    if pri < 3:
        print("         ERROR. No posee los privilegios necesarios para realizar esta operación.")
        print()
        return
    elif pri >= 3:
        print("Esta opción no se encuentra disponible por el momento. Comuníquese con el administrador.")


def opcion_menu_centros_egresos() -> int:                                                           # OPCIÓN MENÚ DE CENTRO DE EGRESOS
    """Muestra al usuario un menú y luego le solicita ingresar una de las
    opciones mostradas a través del número correspondiente. En caso de no
    ingresar una opción correcta, se le volverá a solicitar.

    :rtype: int
    """
    print()
    print("********** Acciones disponibles **********")
    print()
    print("   1. Agregar centro de egreso")
    print("   2. Modificar centro de egreso")
    print("   2. Eliminar centro de egreso")
    print("   0. Volver")
    print()
    try:
        opcion = int(input("Ingrese una opción: "))
        while opcion < 0 or opcion > 3:
            print()
            print("Opción incorrecta.")
            print()
            opcion = int(input("Ingrese una opción: "))
    except ValueError: 
        print("Opción incorrecta.")
        opcion = -1
    except:
        log_error()
        print()
        input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
        opcion = -1
    return opcion


def menu_centros_egresos(idu: int):                                                                 # MENÚ DE CENTRO DE EGRESOS
    """Recibe el ID del usuario. Luego llama a la función donde se muestra las
    opciones y recibe, a través de ella, la opción ingresada por el usuario.
    Luego, según la opción ingresada, llama a la función correspondiente, a la
    cual le transmite el ID del usuario.

    :param idu: ID de usuario
    :type idu: int
    """
    opcion = -1
    while opcion != 0:
        opcion = opcion_menu_centros_egresos()
        if opcion == 1:
            alta_centro_egreso(idu)
        elif opcion == 2:
            editar_centro_egreso(idu)
        elif opcion == 3:
            eliminar_centro_egreso(idu)
        elif opcion == 0:
            return


def alta_centro_egreso(idu: int):
    """Permite al usuario registrar un nuevo centro de egresos en la base de datos.

    ##        --------- ATENCIÓN! ---------
    Ésta opción se encuentra deshabilitada hasta que se deje obsoleto el uso de
    archivos auxiliares .mf

    Nivel de privilegios mínimo: 3

    :param idu: ID de usuario
    :type idu: int
    """
    i_d, nom, ape, tel, dom, use, pas, pri, act = buscar_usuario_por_id(idu)
    print()
    if pri < 3:
        print("         ERROR. No posee los privilegios necesarios para realizar esta operación.")
        print()
        return
    elif pri >= 3:
        print("Esta opción no se encuentra disponible por el momento. Comuníquese con el administrador.")


def editar_centro_egreso(idu: int):
    """Permite al usuario editar un centro de egresos existente en la base de datos.

    ##        --------- ATENCIÓN! ---------
    Ésta opción se encuentra deshabilitada hasta que se deje obsoleto el uso de
    archivos auxiliares .mf

    Nivel de privilegios mínimo: 3

    :param idu: ID de usuario
    :type idu: int
    """
    i_d, nom, ape, tel, dom, use, pas, pri, act = buscar_usuario_por_id(idu)
    print()
    if pri < 3:
        print("         ERROR. No posee los privilegios necesarios para realizar esta operación.")
        print()
        return
    elif pri >= 3:
        print("Esta opción no se encuentra disponible por el momento. Comuníquese con el administrador.")


def eliminar_centro_egreso(idu: int):
    """Permite al usuario eliminar de la base de datos un centro de egresos existente.

    ##        --------- ATENCIÓN! ---------
    Ésta opción se encuentra deshabilitada hasta que se deje obsoleto el uso de
    archivos auxiliares .mf

    Nivel de privilegios mínimo: 3

    :param idu: ID de usuario
    :type idu: int
    """
    i_d, nom, ape, tel, dom, use, pas, pri, act = buscar_usuario_por_id(idu)
    print()
    if pri < 3:
        print("         ERROR. No posee los privilegios necesarios para realizar esta operación.")
        print()
        return
    elif pri >= 3:
        print("Esta opción no se encuentra disponible por el momento. Comuníquese con el administrador.")


def opcion_menu_precios() -> int:                                                                   # OPCIÓN MENÚ DE PRECIOS
    """Muestra al usuario un menú y luego le solicita ingresar una de las
    opciones mostradas a través del número correspondiente. En caso de no
    ingresar una opción correcta, se le volverá a solicitar.

    :rtype: int
    """
    print()
    print("********** Acciones disponibles **********")
    print()
    print("   1. Precios de venta")
    print("   2. Precios de mantenimiento")
    print("   0. Volver")
    print()
    try:
        opcion = int(input("Ingrese una opción: "))
        while opcion < 0 or opcion > 2:
            print()
            print("Opción incorrecta.")
            print()
            opcion = int(input("Ingrese una opción: "))
    except ValueError: 
        print("Opción incorrecta.")
        opcion = -1
    except:
        log_error()
        print()
        input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
        opcion = -1
    return opcion


def menu_precios(idu: int):                                                                         # MENÚ DE PRECIOS
    """Recibe el ID del usuario. Luego llama a la función donde se muestra las
    opciones y recibe, a través de ella, la opción ingresada por el usuario.
    Luego, según la opción ingresada, llama a la función correspondiente, a la
    cual le transmite el ID del usuario.

    :param idu: ID de usuario
    :type idu: int
    """
    opcion = -1
    while opcion != 0:
        opcion = opcion_menu_precios()
        if opcion == 1:
            menu_precios_venta(idu)
        elif opcion == 2:
            menu_precios_mant(idu)
        elif opcion == 0:
            return


def opcion_menu_precios_venta() -> int:                                                             # OPCIÓN MENÚ PRECIOS DE VENTA
    """Muestra al usuario un menú y luego le solicita ingresar una de las
    opciones mostradas a través del número correspondiente. En caso de no
    ingresar una opción correcta, se le volverá a solicitar.

    :rtype: int
    """
    print()
    print("********** Acciones disponibles **********")
    print()
    print("   1. Ver precios de venta")
    print("   2. Modificar manualmente")
    print("   3. Actualizar por porcentaje")
    print("   0. Volver")
    print()
    try:
        opcion = int(input("Ingrese una opción: "))
        while opcion < 0 or opcion > 3:
            print()
            print("Opción incorrecta.")
            print()
            opcion = int(input("Ingrese una opción: "))
    except ValueError: 
        print("Opción incorrecta.")
        opcion = -1
    except:
        log_error()
        print()
        input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
        opcio = -1
    return opcion


def menu_precios_venta(idu: int):                                                                   # MENÚ PRECIOS DE VENTA
    """Recibe el ID del usuario. Luego llama a la función donde se muestra las
    opciones y recibe, a través de ella, la opción ingresada por el usuario.
    Luego, según la opción ingresada, llama a la función correspondiente, a la
    cual le transmite el ID del usuario.

    :param idu: ID de usuario
    :type idu: int
    """
    opcion = -1
    while opcion != 0:
        opcion = opcion_menu_precios_venta()
        if opcion == 1:     # Mostrar precios de veneta
            mostrar_precios_venta()
        elif opcion == 2:   # Editar precios de venta manualmente
            editar_precios_venta_manual(idu)
        elif opcion == 3:   # Editar precios de venta por porcentaje
            editar_precios_venta_porcent(idu)
        elif opcion == 4:   # INAHABILITADO
            alta_precio(idu)    
        elif opcion == 5:   # INAHABILITADO
            eliminar_precio(idu)
        elif opcion == 0:   # Volver
            return


def editar_precios_venta_manual(idu: int):
    """Permite al usuario modificar de manera manual un precio de venta
    registrado en la base de datos.

    Nivel de privilegios mínimos: 2

    :param idu: ID de usuario
    :type idu: int
    """
    i_d, nom, ape, tel, dom, use, pas, pri, act = buscar_usuario_por_id(idu)
    print()
    
    if pri < 2:
        print("         ERROR. No posee los privilegios necesarios para realizar esta operación.")
        print()
        return
    
    elif pri >= 2:
        print("*** Cambio de precios manual ***")
        print()
        print("Indique el ID de precio que desea modificar: ")
        cant = mostrar_precios_venta(True)

        try:
            id_precio = int(input("ID: "))
            print()

            while id_precio < 1 or id_precio > cant:
                print("         ERROR. Indique un ID válido o presione enter para volver al menú anterior.")
                print()
                id_precio = int(input("ID: "))
                print()

        except ValueError:
            print("         ERROR. El dato solicitado debe ser de tipo numérico.")
            return

        try:
            precio_nuevo = int(input("Indique el nuevo precio de compra en un pago: $ "))

        except ValueError:
            print("         ERROR. El dato solicitado debe ser de tipo numérico.")
            return
        except:
            log_error()
            print()
            input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
            return

        print()
        print("Actualizado precio...")
        cambio_precio_venta_manual(id_precio, precio_nuevo)
        print()
        print("Precio actualizado exitosamiente")
        return


def editar_precios_venta_porcent(idu: int):
    """Permite al usuario actualizar los precios de venta a partir de un porcentaje.

    Nivel de privilegios mínimo: 2

    :param idu: ID de usuario
    :type idu: int
    """
    i_d, nom, ape, tel, dom, use, pas, pri, act = buscar_usuario_por_id(idu)
    print()
    
    if pri < 2:
        print("         ERROR. No posee los privilegios necesarios para realizar esta operación.")
        print()
        return
    
    elif pri >= 2:
        print("*** Actualizar precios por porcentaje ***")
        print()
    
        try:
            porcentaje = int(input("Indique el porcentaje de aumento a realizar: "))
            print()
    
        except ValueError:
            print("         ERROR. El dato solicitado debe ser de tipo numérico.")
            print()
            return
        except:
            log_error()
            print()
            input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
            return
    
        if porcentaje <= 0:
            print("         ERROR. El porcentaje debe ser mayor a cero.")
            print()
            return
    
        print("Actualizando precios. No interrumpa el proceso ni apague el sistema...")
        print()
        cambio_precio_venta_porcentaje(porcentaje)
        print("Lista de precios actualizada exitosamente.")
        print()


def alta_precio(idu: int):       # OPCIÓN INAHABILITADA
    """Permite al usuario registrar un nuevo precio de venta en la base de datos.

    ##        --------- ATENCIÓN! ---------
    Ésta opción se encuentra deshabilitada hasta que se deje obsoleto el uso de
    archivos auxiliares .mf

    Nivel de privilegios mínimo: 3

    :param idu: ID de usuario
    :type idu: int
    """
    if False:
        i_d, nom, ape, tel, dom, use, pas, pri, act = buscar_usuario_por_id(idu)
        print()
        
        if pri < 3:
            print("         ERROR. No posee los privilegios necesarios para realizar esta operación.")
            print()
            return
        
        elif pri >= 3:
            print("*** Alta de precios de venta ***")
            print() 
        
            nombre = input("Indique el nombre del precio: [ Piso/s - Categoría (fila/s) ] " ).title()
            nombre = reemplazar_comilla(nombre)
            print()
        
            try:
                precio = int(input("Indique el precio de compra en un pago: $ "))
        
            except ValueError:
                print("         ERROR. El dato solicitado es de tipo numérico")
                print()
                return
            except:
                log_error()
                print()
                input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
                return
        
            print("Registrando nuevo precio...")
            parameters = str((nombre, precio, 1, 1))
            query = f"INSERT INTO precios_venta (nombre, precio, anticipo, cuotas) VALUES {parameters}"
            run_query(query)
        
            print("Calculando anticipo y cuotas...")
            id_precio, nomb_pr, pr_ft, pr_ant, pr_cuot = ult_reg('precios_venta', 'id')
            cambio_precio_venta_manual(id_precio, precio)
        
            print()
            print("Precio agregado exitosamente.")
            return


def eliminar_precio(idu):   # OPCIÓN INAHABILITADA
    """Permite al usuario eliminar de la base de datos un precio de venta existente.

    ##        --------- ATENCIÓN! ---------
    Ésta opción se encuentra deshabilitada hasta que se deje obsoleto el uso de
    archivos auxiliares .mf

    Nivel de privilegios mínimo: 3

    :param idu: ID de usuario
    :type idu: int
    """
    if False:
        i_d, nom, ape, tel, dom, use, pas, pri, act = buscar_usuario_por_id(idu)
        print()
        
        if pri < 3:
            print("         ERROR. No posee los privilegios necesarios para realizar esta operación.")
            print()
            return
        
        elif pri >= 3:
            print("*** Eliminar un precio de venta ***")
            print()
            print("Indique el precio que desea eliminar: ")
            mostrar_precios_venta()
        
            try:
                precio = int(input("ID de precio: "))
                print()
        
            except ValueError:
                print("         ERROR. El dato solicitado debe ser de tipo numérico.")
                print()
                return
            except:
                log_error()
                print()
                input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
                return
        
            msj = ""
            while msj != "S" and msj != "N":
                msj = str(input(f"¿Seguro quiere eliminar este precio? (S/N): "))
                
                if msj in AFIRMATIVO:
                    msj = "S"
                    delete_row('precios_venta', 'id', precio)
                    print()
                    print("Precio eliminado exitosamente.")
                    print()
                    return
        
                elif msj in NEGATIVO:
                    msj = "N"
                    print()
                    print("No se han realizado cambios en el registro.")
                    print()
                    return
                else:
                    print()
                    print("         ERROR. Debe indicar S para eliminar el precio o N para cancelar.")
                    print()


def opcion_menu_precios_mant() -> int:                                                              # OPCIÓN MENÚ PRECIOS DE MANTENIMIENTO
    """Muestra al usuario un menú y luego le solicita ingresar una de las
    opciones mostradas a través del número correspondiente. En caso de no
    ingresar una opción correcta, se le volverá a solicitar.

    :rtype: int
    """    
    print()
    print("********** Acciones disponibles **********")
    print()
    print("   1. Ver precios de mantenimiento")
    print("   2. Modificar manualmente")
    print("   3. Actualizar por porcentaje")
    print("   0. Volver")
    print()
    try:
        opcion = int(input("Ingrese una opción: "))
        while opcion < 0 or opcion > 3:
            print()
            print("Opción incorrecta.")
            print()
            opcion = int(input("Ingrese una opción: "))
    except ValueError: 
        print("Opción incorrecta.")
        opcion = -1
    except:
        log_error()
        print()
        input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
        opcion = -1
    return opcion


def menu_precios_mant(idu: int):                                                                    # MENÚ PRECIOS DE MANTENIMIENTO
    """Recibe el ID del usuario. Luego llama a la función donde se muestra las
    opciones y recibe, a través de ella, la opción ingresada por el usuario.
    Luego, según la opción ingresada, llama a la función correspondiente, a la
    cual le transmite el ID del usuario.

    :param idu: ID de usuario
    :type idu: int
    """
    opcion = -1
    while opcion != 0:
        opcion = opcion_menu_precios_mant()
        if opcion == 1:
            mostrar_precios_mant()
        elif opcion == 2:
            editar_precios_mant_manual(idu)
        elif opcion == 3:
            editar_precios_mant_porcent(idu)
        elif opcion == 0:
            return


def editar_precios_mant_manual(idu: int):
    """Permite al usuario modificar de manera manual los precios de mantenimiento
    de Bicon y NOB para una categoría de nichos.

    Nivel de privilegios mínimos: 2

    :param idu: ID de usuario
    :type idu: int
    """
    i_d, nom, ape, tel, dom, use, pas, pri, act = buscar_usuario_por_id(idu)
    print()
    
    if pri < 2:
        print("         ERROR. No posee los privilegios necesarios para realizar esta operación.")
        print()
        return
    
    elif pri >= 2:
        print("*** Cambio de precios de mantenimiento manual ***")
        print()
        print("Indique el ID de precio que desea modificar: ")
        cant = mostrar_precios_mant(True)
    
        try:
            id_precio = int(input("ID: "))
            print()
    
            while id_precio < 1 or id_precio > cant:
                print("         ERROR. Indique un ID válido o presione enter para volver al menú anterior.")
                print()
                id_precio = int(input("ID: "))
                print()
    
        except ValueError:
            print("         ERROR. El dato solicitado debe ser de tipo numérico.")
            return
        except:
            log_error()
            print()
            input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
            return
    
        try:
            precio_bic_nuevo = int(input("Indique el nuevo precio de mantenimiento para BICON: $ "))
    
        except ValueError:
            print("         ERROR. El dato solicitado debe ser de tipo numérico.")
            return
        except:
            log_error()
            print()
            input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
            return
    
        try:
            precio_nob_nuevo = int(input("Indique el nuevo precio de mantenimiento para NOB: $ "))
    
        except ValueError:
            print("         ERROR. El dato solicitado debe ser de tipo numérico.")
            return
        except:
            log_error()
            print()
            input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
            return
        print()
    
        print("Actualizado precios de mantenimiento...")
        cambio_precio_mant_manual(id_precio, precio_bic_nuevo, precio_nob_nuevo)
        print()
        print("Precio actualizado exitosamiente")
        return


def editar_precios_mant_porcent(idu: int):
    """Permite al usuario actualizar los precios de mantenimiento a partir de un porcentaje. El usuario
    puede elegir hacerlo sólo para una distribución de facturación o para todos los precios a la vez.

    Nivel de privilegios mínimo: 2

    :param idu: ID de usuario
    :type idu: int
    """
    i_d, nom, ape, tel, dom, use, pas, pri, act = buscar_usuario_por_id(idu)
    print()

    if pri < 2:
        print("         ERROR. No posee los privilegios necesarios para realizar esta operación.")
        print()
        return
    
    elif pri >= 2:
        print("*** Actualizar precios de mantenimiento por porcentaje ***")
        print()
        print()
        print("Elija una distribución:")
        print()
        print("   1. Bicon")
        print("   2. NOB")
        print("   3. Todas")
        print("   0. Volver")
        print()
    
        opcion = -1
        while opcion == -1:
            try:
                opcion = int(input("Ingrese una opción: "))
    
                if opcion < 0 or opcion > 3:
                    print()
                    print("Opción incorrecta.")
                    print()
                    opcion = -1
    
                elif opcion == 1:
                    facturacion = 'bicon'
    
                elif opcion == 2:
                    facturacion = 'nob'
    
                elif opcion == 3:
                    facturacion = 'todas'
    
                elif opcion == 0:
                    return
    
            except ValueError: 
                print("Opción incorrecta.")
                opcion = -1
            except:
                log_error()
                print()
                input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
                print()
                opcion = -1
    
        try:
            porcentaje = int(input("Indique el porcentaje de aumento a realizar: "))
            print()
    
        except ValueError:
            print("         ERROR. El dato solicitado debe ser de tipo numérico.")
            print()
            return
        except:
            log_error()
            print()
            input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
            return
    
        if porcentaje <= 0:
            print("         ERROR. El porcentaje debe ser mayor a cero.")
            print()
            return
    
        print("Actualizando precios. No interrumpa el proceso ni apague el sistema...")
        print()
        cambio_precio_mant_porcentaje(facturacion, porcentaje)
        print("Lista de precios actualizada exitosamente.")
        print()
        

def opcion_menu_mails() -> int:                                                                     # OPCIÓN MENÚ DE MAILS
    """Muestra al usuario un menú y luego le solicita ingresar una de las
    opciones mostradas a través del número correspondiente. En caso de no
    ingresar una opción correcta, se le volverá a solicitar.

    :rtype: int
    """
    print()
    print("********** Acciones disponibles **********")
    print()
    print("   1. Ver cuentas de mail")
    print("   2. Agregar una cuenta de mail")
    print("   3. Editar una cuenta de mail")
    print("   4. Eliminar una cuenta de mail")
    print("   0. Volver")
    print()
    try:
        opcion = int(input("Ingrese una opción: "))
        while opcion < 0 or opcion > 4:
            print()
            print("Opción incorrecta.")
            print()
            opcion = int(input("Ingrese una opción: "))
    except ValueError: 
        print("Opción incorrecta.")
        opcion = -1
    except:
        log_error()
        print()
        input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
        opcion = -1
    return opcion


def menu_mails(idu: int):                                                                           # MENÚ DE MAILS
    """Recibe el ID del usuario. Luego llama a la función donde se muestra las
    opciones y recibe, a través de ella, la opción ingresada por el usuario.
    Luego, según la opción ingresada, llama a la función correspondiente, a la
    cual le transmite el ID del usuario.

    :param idu: ID de usuario
    :type idu: int
    """
    opcion = -1
    while opcion != 0:
        opcion = opcion_menu_mails()
        if opcion == 1:
            mostrar_cuentas_mail()
        elif opcion == 2:
            alta_mail(idu)
        elif opcion == 3:
            editar_mail(idu)
        elif opcion == 4:
            eliminar_mail(idu)
        elif opcion == 0:
            return


def alta_mail(idu: int):
    """Permite al usuario registrar un email de la empresa en la base de datos.

    Nivel de privilegios mínimo: 3

    :param idu: ID de usuario
    :type idu: int
    """
    i_d, nom, ape, tel, dom, use, pas, pri, act = buscar_usuario_por_id(idu)
    print()
    
    if pri < 3:
        print("         ERROR. No posee los privilegios necesarios para realizar esta operación.")
        print()
        return
    
    elif pri >= 3:
        print("*** Agregar una cuenta de mail ***")
        print()
    
        nueva_etiq = input("Ingrese un nombre para la nueva cuenta de mail: ").lower()
        nueva_etiq = reemplazar_comilla(nueva_etiq)
        print()
    
        if nueva_etiq == "":
            print("         ERROR. El campo no puede quedar vacío.")
            return
    
        nuevo_mail = input("Ingrese la cuenta de email: ").lower()
        print()
    
        if nuevo_mail == "":
            print("         ERROR. El campo no puede quedar vacío.")
            print()
            return
    
        if type(nuevo_mail) == str and "'" in nuevo_mail:
            print("         ERROR. No se pueden utilizar comillas simples (').")
            print()
            return
    
        nuevo_server = input("Ingrese el servidor SMTP: ").lower()
        print()
    
        if nuevo_server == "":
            print("         ERROR. El campo no puede quedar vacío.")
            print()
            return
    
        if type(nuevo_server) == str and "'" in nuevo_server:
            print("         ERROR. No se pueden utilizar comillas simples (').")
            print()
            return
    
        nuevo_usuario = input("Ingrese el usuario SMTP: ").lower()
        print()
    
        if nuevo_usuario == "":
            print("         ERROR. El campo no puede quedar vacío.")
            print()
            return
    
        if type(nuevo_usuario) == str and "'" in nuevo_usuario:
            print("         ERROR. No se pueden utilizar comillas simples (').")
            print()
            return
    
        nuevo_pw = getpass("Ingrese la contraseña del email: ")
        print()
    
        if nuevo_pw == "":
            print("         ERROR. El campo no puede quedar vacío.")
            return
    
        if type(nuevo_pw) == str and "'" in nuevo_pw:
            print("         ERROR. No se pueden utilizar comillas simples (').")
            print()
            return
    
        nuevo_pw_conf = getpass("Vuelva a ingresar la contraseña: ")
        print()
    
        if nuevo_pw == nuevo_pw_conf:
            parameters = str((nueva_etiq, nuevo_mail, nuevo_server, nuevo_usuario, nuevo_pw))
            query = f"INSERT INTO mail (etiqueta, mail, smtp_server, smtp_user, smtp_pass) VALUES {parameters}"
    
            try:
                run_query(query)
                print("Cuenta de email agregada exitosamente.")
                print()
    
            except sql.errors.UniqueViolation:
                print("         ERROR. La cuenta que está intentando ingresar ya existe en la base de datos.")
                print()
            except:
                log_error()
                print()
                input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
                print()
    
        else:
            print("         ERROR. Las contraseñas no coinciden.")
            print()
            return


def opcion_editar_mail() -> int:                                                                    # OPCIÓN MENÚ EDITAR MAIL
    """Muestra al usuario un menú y luego le solicita ingresar una de las
    opciones mostradas a través del número correspondiente. En caso de no
    ingresar una opción correcta, se le volverá a solicitar.

    :rtype: int
    """
    print()
    print("********** Acciones disponibles **********")
    print()
    print("   1. Modificar etiqueta")
    print("   2. Modificar cuenta mail")
    print("   3. Modificar servidor SMTP")
    print("   4. Modificar usuario SMTP")
    print("   5. Modificar contraseña")
    print("   0. Volver")
    print()
    try:
        opcion = int(input("Ingrese una opción: "))
        while opcion < 0 or opcion > 5:
            print()
            print("Opción incorrecta.")
            print()
            opcion = int(input("Ingrese una opción: "))
    except ValueError: 
        print("Opción incorrecta.")
        opcion = -1
    except:
        log_error()
        print()
        input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
        opcion = -1
    return opcion


def editar_mail(idu: int):                                                                          # MENÚ EDITAR MAIL
    """Recibe el ID del usuario. Luego llama a la función donde se muestra las
    opciones y recibe, a través de ella, la opción ingresada por el usuario.
    Luego, según la opción ingresada, permite al usuario realizar alguna de las
    siguientes acciones:

    - Modificar la etiqueta (nombre identificador de la cuenta de email)
    - Modificar la cuenta de email (cuenta SMTP)
    - Modificar el servidor SMTP
    - Modificar el usuario de acceso al servidor SMTP
    - Modificar la contraseña de acceso al servidor SMTP

    Luego, en caso de realizar la acción de manera correcta, se registra la
    modificación en la base de datos.

    Nivel de privilegios necesario: 3 (Excepto para modificar la contraeña
    de acceso al servidor SMTP, para lo cual se necesita, como mínimo, nivel
    de privilegios 4)

    En caso de modificar la contraseña el sistema le solicitará al usuario
    que la repita, con el objetivo de evitar el ingreso de una contraseña
    no deseada.

    :param idu: ID de usuario
    :type idu: int
    """
    opcion = -1
    i_d, nom, ape, tel, dom, use, pas, pri, act = buscar_usuario_por_id(idu)
    print()
    
    if pri < 3:
        print("         ERROR. No posee los privilegios necesarios para realizar esta operación.")
        print()
        return
    
    elif pri >= 3:
        while opcion != 0:
            opcion = opcion_editar_mail()
            print()
    
            if opcion == 1:     # Editar etiqueta
                mostrar_cuentas_mail()
                print()
                
                try:
                    id_mail = int(input("Indique el ID de la cuenta que desea modificar: "))
                    i_d, etiq, mail, server, user, pw = buscar_mail(id_mail)
                
                except ValueError:
                    print("         ERROR. El dato solicitado debe ser de tipo numérico.")
                    print()
                    return
                except TypeError:
                    print("         ERROR. ID de mail inexistente")
                    return
                except:
                    log_error()
                    print()
                    input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
                    return
                print()
                
                nueva_etiq = str(input("Ingrese la nueva etiqueta: "))
                edit_registro('mail', 'etiqueta', nueva_etiq, id_mail)
                print()
                print(f"Etiqueta modificada correctamente. La nueva etiqueta es: {nueva_etiq}")
                print()
            
            elif opcion == 2:   # Editar cuenta
                mostrar_cuentas_mail()
                print()
                
                try:
                    id_mail = int(input("Indique el ID de la cuenta que desea modificar: "))
                    i_d, etiq, mail, server, user, pw = buscar_mail(id_mail)
                
                except ValueError:
                    print("         ERROR. El dato solicitado debe ser de tipo numérico.")
                    print()
                    return
                except TypeError:
                    print("         ERROR. ID de mail inexistente")
                    return
                except:
                    log_error()
                    print()
                    input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
                    return
                print()
                
                nueva_cuenta = str(input("Ingrese la nueva cuenta: "))
                edit_registro('mail', 'mail', nueva_cuenta, id_mail)
                print()
                print(f"Cuenta modificada correctamente. La nueva cuenta es: {nueva_cuenta}")
                print()
            
            elif opcion == 3:   # Editar server
                mostrar_cuentas_mail()
                print()
                
                try:
                    id_mail = int(input("Indique el ID de la cuenta que desea modificar: "))
                    i_d, etiq, mail, server, user, pw = buscar_mail(id_mail)
               
                except ValueError:
                    print("         ERROR. El dato solicitado debe ser de tipo numérico.")
                    print()
                    return
                except TypeError:
                    print("         ERROR. ID de mail inexistente")
                    return
                except:
                    log_error()
                    print()
                    input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
                    return
                print()
                
                nueva_server = str(input("Ingrese el nuevo servidor SMTP: "))
                edit_registro('mail', 'smtp_server', nueva_server, id_mail)
                print()
                print(f"Servidor modificado correctamente. El nuevo servidor es: {nueva_server}")
                print()
            
            elif opcion == 4:   # Editar user
                mostrar_cuentas_mail()
                print()
                
                try:
                    id_mail = int(input("Indique el ID de la cuenta que desea modificar: "))
                    i_d, etiq, mail, server, user, pw = buscar_mail(id_mail)
                
                except ValueError:
                    print("         ERROR. El dato solicitado debe ser de tipo numérico.")
                    print()
                    return
                except TypeError:
                    print("         ERROR. ID de mail inexistente")
                    return
                print()
                
                nuevo_user = str(input("Ingrese el nuevo usuario SMTP: "))
                edit_registro('mail', 'smtp_user', nuevo_user, id_mail)
                print()
                print(f"Usuario modificado correctamente. El nuevo usuario es: {nuevo_user}")
                print()
            
            elif opcion == 5:   # Editar pass
                
                if pri < 4:
                    print("         ERROR. No posee los privilegios necesarios para realizar esta operación.")
                    print()
                    return  
                
                mostrar_cuentas_mail()
                print()
                
                try:
                    id_mail = int(input("Indique el ID de la cuenta que desea modificar: "))
                    i_d, etiq, mail, server, user, pw = buscar_mail(id_mail)
                
                except ValueError:
                    print("         ERROR. El dato solicitado debe ser de tipo numérico.")
                    print()
                    return
                except TypeError:
                    print("         ERROR. ID de mail inexistente")
                    return
                except:
                    log_error()
                    print()
                    input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
                    return
                print()
                
                nuevo_pw = str(getpass("Ingrese la nueva contraseña: "))
                print()
                conf_pw = str(getpass("Ingrese nuevamente la nueva contraseña: "))
                print()
                
                if nuevo_pw == conf_pw:
                    edit_registro('mail', 'smtp_pass', nuevo_pw, id_mail)
                    print()
                    print(f"Contraseña modificada correctamente.")
                    print()
                
                else:
                    print("         ERROR. Las contraseñas no coinciden")
                    print()
                    return
            

def eliminar_mail(idu: int):
    """Permite al usuario eliminar de la base de datos un email de la empresa existente.

    Nivel de privilegios mínimo: 4

    :param idu: ID de usuario
    :type idu: int
    """
    i_d, nom, ape, tel, dom, use, pas, pri, act = buscar_usuario_por_id(idu)
    print()
    
    if pri < 4:
        print("         ERROR. No posee los privilegios necesarios para realizar esta operación.")
        print()
        return
    
    else:
        print("*** Eliminar una cuenta de mail ***")
        print()
        print("Indique el ID de la cuenta que desea eliminar: ")
        mostrar_cuentas_mail()
    
        try:
            id_mail = int(input("ID de cuenta: "))
            print()
    
        except ValueError:
            print("         ERROR. El dato solicitado debe ser de tipo numérico.")
            print()
            return
        except:
            log_error()
            print()
            input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
            return
    
        msj = ""
        while msj != "S" and msj != "N":
            msj = str(input(f"¿Seguro quiere eliminar esta cuenta? (S/N): "))
    
            if msj in AFIRMATIVO:
                msj = "S"
                delete_row('mail', 'id', id_mail)
                print()
                print("Cuenta eliminada exitosamente.")
                print()
                return
    
            elif msj in NEGATIVO:
                msj = "N"
                print()
                print("No se han realizado cambios en el registro.")
                print()
                return
            else:
                print()
                print("         ERROR. Debe indicar S para eliminar la cuenta o N para cancelar.")
                print()


def opcion_menu_fiserv() -> int:                                                                    # OPCIÓN MENÚ FISERV
    """Muestra al usuario un menú y luego le solicita ingresar una de las
    opciones mostradas a través del número correspondiente. En caso de no
    ingresar una opción correcta, se le volverá a solicitar.

    :rtype: int
    """
    print()
    print("********** Acciones disponibles **********")
    print()
    print("   1. Modificar número de comercio")
    print("   0. Volver")
    print()
    try:
        opcion = int(input("Ingrese una opción: "))
        while opcion < 0 or opcion > 1:
            print()
            print("Opción incorrecta.")
            print()
            opcion = int(input("Ingrese una opción: "))
    except ValueError: 
        print("Opción incorrecta.")
        opcion = -1
    except:
        log_error()
        print()
        input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
        opcion = -1
    return opcion


def menu_fiserv(idu: int):                                                                          # MENÚ FISERV
    """Recibe el ID del usuario. Luego llama a la función donde se muestra las
    opciones y recibe, a través de ella, la opción ingresada por el usuario.
    Luego, según la opción ingresada, llama a la función correspondiente, a la
    cual le transmite el ID del usuario.

    :param idu: ID de usuario
    :type idu: int
    """
    opcion = -1
    while opcion != 0:
        opcion = opcion_menu_fiserv()
        if opcion == 1:
            editar_nro_comercio_fiserv()
        elif opcion == 0:
            return


def editar_nro_comercio_fiserv():
    """Permite al usuario modificar el número de comercio de FiServ.
    """
    loop = -1
    
    while loop == -1:
        try:
            print()
            loop = nro_comercio = int(input("Indique el nuevo número de comercio o presione indique 0 para volver: "))
    
        except ValueError:
            print()
            print("         ERROR. El dato solicitado debe ser de tipo numérico.")
            print()
            loop= -1
        
    if loop == 0:
        return
    
    else:
        try:
            with sql.connect(DATABASE) as conn:
                cursor = conn.cursor()
                cursor.execute(f"UPDATE comercio_fiserv SET nro_comercio = '{nro_comercio}';")
        
        except sql.OperationalError:
            log_error()
            print()
            print("         ERROR. La base de datos no responde. Asegurese de estar conectado a la red y que el servidor se encuentre encendido.")
            print()
            print("         Si es así y el problema persiste, comuníquese con el administrador del sistema.")
            print()
            return
        except:
            log_error()
            print()
            input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
            return

        print()
        print("Número de comercio de FiServ modificado exitosamente.")
        print()


def obtener_nro_comercio_fiserv() -> int:
    """Recupera de la base de datos el número de comercio de FiServ y lo retorna

    :rtype: int
    """
    with sql.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute(f"SELECT nro_comercio FROM comercio_fiserv WHERE id = 1;")
        datos = cursor.fetchone()
    return datos[0]


# INICIO FUNCIONES OCULTAS

def mant_restaurar_admin():
    """Permite restaurar la cuenta del administrador del sistema en caso que sea bloqueado
    por intentos fallidos de ingreso con su cuenta.
    
    Esta función se encuentra dentro de un menú secreto al que sólo debe tener acceso el
    administrador.
    """
    with sql.connect(DATABASE) as conn:
        telefono = input("Teléfono: ")
        cursor = conn.cursor()
        instruccion = f"UPDATE usuarios SET nombre = 'Manuel', apellido = 'Ferrero', telefono = '{telefono}', domicilio = 'ADMIN', user_name = 'ferman', pass = '155606038', privilegios = 5, activo = 1 WHERE id = 1"
        cursor.execute(instruccion)

    print("Cuenta ADMIN restaurada exitosamente.")
    print()
    getpass("Presione enter para salir...")
    print()


def revisar_host(host: str) -> str:
    """Recibe una cadena conteniendo una dirección IP y valida su formato.
    En caso de ser correcta la retorna, de lo contrario retorna una cadena
    conteniendo la palabra error.

    La función admite la dirección localhost como válida.

    :param host: Dirección IP
    :type host: str

    :rtype: str
    """
    counter = 0

    if type(host) != str:
        return 'error'

    if host == 'localhost':
        return 'localhost'

    for i in host:
        if i == '.':
            counter += 1

    if counter != 3:
        return 'error'

    ip_s1, ip_s2, ip_s3, ip_s4 = host.split(sep='.')

    try:
        if int(ip_s1) < 0 or int(ip_s1) > 255:
            return 'error'

        if int(ip_s2) < 0 or int(ip_s2) > 255:
            return 'error'

        if int(ip_s3) < 0 or int(ip_s3) > 255:
            return 'error'

        if int(ip_s4) < 0 or int(ip_s4) > 255:
            return 'error'

        host = f"{int(ip_s1)}.{int(ip_s2)}.{int(ip_s3)}.{int(ip_s4)}"

    except ValueError:
        return 'error'

    return host


def mant_database():
    """Permite modificar la información de acceso a la base de datos. La misma
    se registra en un archivo .ini siguiendo el modelo correspondiente para el 
    posterior mediante el uso de la librería psycopg2. En caso de no existir el
    archivo, éste se crea a partir de esta función.

    Esta función se encuentra dentro de un menú secreto al que sólo debe tener acceso el
    administrador.

    En ella se solicitan los siguientes datos:

    - Host: Dirección IP del servidor donde se encuentra alojada la base de datos.
    - Database: Nombre de la base de datos
    - User: Usuario de acceso a la base de datos
    - Password: Contraseña de acceso a la base de datos (la misma debe ser provista dos
    veces para evitar registrar una contraseña no deseada).
    - Port: Puerto de conexión al servidor donde se encuentra alojada la base de datos.

    El sistema permite el completado rápido de los datos: Al presionar enter sin haber
    ingresado alguno de los datos solicitados, éste se completará automáticamente con
    los datos por defecto (los mismos se encuentral entre corchetes al momento de la 
    solicitud de los datos).
    """
    loop = -1
    while loop == -1:
        loop = host = input("Host [192.168.100.100]: ").lower()
        print()
    
        if host == "":
            host = '192.168.100.100'
    
        host = revisar_host(host)
    
        if host == 'error':
            print("         ERROR. Ingrese una dirección de host válida.")
            print()
            loop = -1
    
    dbname = input("Database [bicon]: ")
    if dbname == "":
        dbname = 'bicon'
    print()
    
    user = input("User [postgres]: ")
    if user == "":
        user = 'postgres'
    print()
    
    password = ""
    while password == "":
        password = getpass("Password: ")
        print()
    
        pw_conf = getpass("Repetir password: ")
        print()
    
        if password != pw_conf:
            print("         ERROR. Las contraseñas no coinciden. Vuelva a intentarlo.")
            print()
            password = ""        
    
    loop = -1
    while loop == -1:
        try:
            loop = port = input("Port [5432]: ")
    
            if port == "":
                port = 5432
    
            else:
                port = int(port)
            print()
    
        except ValueError:
            print("         ERROR. El dato solicitado debe ser de tipo numérico.")
            print()
            loop= -1
    
    conexion = f"host={host} dbname={dbname} user={user} password={password} port={port}"
    
    with open(ARCH_INI, 'w') as archivo:
        archivo.write(conexion)
    
    print("Ruta a base de datos actualizada exitosamente.")
    print()
    getpass("Presione enter para salir...")
    print()
    
# FIN FUNCIONES OCULTAS


def cerrar_consola():
    """Imprime en pantalla una gran cantidad de saltos de línea
    y un cartel que comunica al usuario que puede cerrar la consola,
    para que, en caso que el usuario inicie el sistema a través de
    la consola y no iniciando el archivo ejecutable, el mismo sepa
    que ya finalizó la ejecución.
    """
    print()
    print()
    print()
    print()
    print()
    print()
    print()
    print()
    print()
    print()
    print()
    print()
    print()
    print()
    print()
    print()
    print()
    print()
    print()
    print()
    print()
    print()
    print()
    print()
    print()
    print()
    print()
    print()
    print()
    print()
    print()
    print()
    print()
    print()
    print()
    print()
    print()
    print()
    print()
    print(" -----------------------------")
    print("| Ya puede cerrar la consola. |")
    print(" -----------------------------")
    print()
    print()
    print()
    print()


