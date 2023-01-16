import os
import psycopg2 as sql
import psycopg2.errors

from colorama import init, Fore, Back
from datetime import datetime
from getpass import getpass

import funciones_mantenimiento as mant
import reporter as rep

os.system(f'TITLE Morella v{mant.VERSION} - MF! Soluciones informáticas')
os.system('color 0E')   # Colores del módulo (Amarillo sobre negro)
os.system('mode con: cols=160 lines=9999')


def obtener_saldo_inicial() -> float:
    """Recupera desde la base de datos el saldo de la caja

    :rtype: float
    """
    with sql.connect(mant.DATABASE) as conn:
        cursor = conn.cursor()
        instruccion = f"SELECT saldo FROM saldo_caja ORDER BY nro_caja DESC LIMIT 1"
        cursor.execute(instruccion)
        datos = cursor.fetchone()
    return datos[0]


def obtener_contador() -> int:
    """Recupera desde la base de datos el número de la caja
    anterior y retorna el número actual

    :rtype: int
    """
    with sql.connect(mant.DATABASE) as conn:
        cursor = conn.cursor()
        instruccion = f"SELECT nro_caja FROM saldo_caja ORDER BY nro_caja DESC LIMIT 1"
        cursor.execute(instruccion)
        datos = cursor.fetchone()
    return datos[0]+1


def obtener_cobradores() -> list:
    """Recupera desde la base de datos todos los cobradores
    y los retorna en una lista

    :rtype: list
    """
    with sql.connect(mant.DATABASE) as conn:
        cursor = conn.cursor()
        instruccion = f"SELECT * FROM cobradores ORDER BY id"
        cursor.execute(instruccion)
        datos = cursor.fetchall()
    return datos


def iniciar_caja() -> float:
    """Muestra al usuario la fecha, el número de caja y el saldo inicial de
    la misma. Luego retorna el saldo inicial.
    
    En caso que hubiera un error al intentar obtener el saldo inicial o el
    mismo fuera negativo se da aviso al usuario y se le solicita que lo 
    ingrese de manera manual.

    :rtype: float
    """
    saldo_inicial = obtener_saldo_inicial()
    fecha = obtener_fecha()
    
    if saldo_inicial >= 0:
        print(f"Fecha: {fecha}")
        print("")
        print(f"Número de caja: {str(obtener_contador()).rjust(6, '0')}")
        print("")
        print(f"El saldo inicial es $ {saldo_inicial:.2f}")
        print("")
    
    else:
        print("")
        print(" *** ERROR. No ha sido posible leer el saldo final de la caja anterior.*** ")
        print("")
    
        loop = -1
        while loop == -1:
            try:
                loop = saldo_inicial = float(input("Por favor ingrese el saldo actual de la caja: $ "))
                print()
                
                with sql.connect(mant.DATABASE) as conn:
                    cursor = conn.cursor()
                    instruccion = f"UPDATE saldo_caja SET saldo = {saldo_inicial} WHERE saldo = -1"
                    cursor.execute(instruccion)
                print()
                
                print(f"Fecha: {fecha}")
                print("")
                print(f"Número de caja: {str(obtener_contador()).rjust(6, '0')}")
                print("")
                print(f"El saldo inicial es $ {saldo_inicial:.2f}")
                print("")
            
            except ValueError:
                print(" *** ERROR. EL MONTO DEBE SER NUMÉRICO ***")
                print()
                loop = -1
            except:
                mant.log_error()
                input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
                print()
                loop = -1
    
    return saldo_inicial


def obtener_dia() -> str:
    """Retorna una cadena con el día actual (número de dos dígitos).

    :rtype: str
    """
    return datetime.now().strftime('%d')


def obtener_mes() -> str:
    """Retorna una cadena con el mes actual (número de dos dígitos).

    :rtype: str
    """
    return datetime.now().strftime('%m')


def obtener_año() -> str:
    """Retorna una cadena con el año actual (número de cuatro dígitos).

    :rtype: str
    """
    return datetime.now().strftime('%Y')


def obtener_fecha() -> str:
    """Retorna una cadena con la fecha actual (formato DD/MM/AAAA).

    :rtype: str
    """
    return datetime.now().strftime('%d/%m/%Y')


def obtener_categ_ing() -> list:
    """Recupera desde el archivo .mf correspondiente las categorías de
    ingresos de caja y las retorna en una lista.

    :rtype: list
    """
    categ_ing = []

    with open("../databases/categ_ing.mf", 'r', encoding='Utf-8') as archivo:
        for i in archivo.readlines():
            categ_ing.append(i.rstrip())

    return categ_ing


def obtener_categ_egr() -> list:
    """Recupera desde el archivo .mf correspondiente las categorías de
    egresos de caja y las retorna en una lista.

    :rtype: list
    """
    categ_egr = []
    
    with open("../databases/categ_egr.mf", 'r', encoding='Utf-8') as archivo:
        for i in archivo.readlines():
            categ_egr.append(i.rstrip())

    return categ_egr


"---------------------------- Funciones inhabilitadas hasta dejar obsoletos los archivos .mf ----------------------------"

# def obtener_categ_ing() -> list:
#     """Recupera desde la base de datos las categorías de ingresos de caja
#     y las retorna en una lista.

#     :rtype: list
#     """
#     with sql.connect(mant.DATABASE) as conn:
#         cursor = conn.cursor()
#         instruccion = f"SELECT categoria FROM categorias_ingresos ORDER BY id"
#         cursor.execute(instruccion)
#         datos = cursor.fetchall()
#     return datos


# def obtener_categ_ing() -> list:
#     """Recupera desde la base de datos las categorías de egresos de caja
#     y las retorna en una lista.

#     :rtype: list
#     """
#     with sql.connect(mant.DATABASE) as conn:
#         cursor = conn.cursor()
#         instruccion = f"SELECT categoria FROM categorias_egresos ORDER BY id"
#         cursor.execute(instruccion)
#         datos = cursor.fetchall()
#     return datos

"------------------------------------------------------------------------------------------------------------------------"


def obtener_cobrador() -> list:
    """Recupera desde el archivo .mf correspondiente los cobradores y los
    retorna en una lista
    
    :rtype: list
    """
    cobradores = []
    
    with open("../databases/cobradores.mf", 'r', encoding='Utf-8') as archivo:
        for i in archivo.readlines():
            cobradores.append(i.rstrip())

    return cobradores


def obtener_nom_cobrador(id_cobrador: int) -> str:
    """Recibe el ID de cobrador y retorna el nombre

    :id_cobrador: ID de cobrador
    :type id_cobrador: int

    :rtype: str
    """
    with sql.connect(mant.DATABASE) as conn:
        cursor = conn.cursor()
        instruccion = f"SELECT cobrador FROM cobradores WHERE id = '{id_cobrador}'"
        cursor.execute(instruccion)
        datos = cursor.fetchone()
    return datos[0]


def obtener_panteon() -> list:
    """Recupera desde el archivo .mf correspondiente los panteones y los
    retorna en una lista
    
    :rtype: list
    """
    panteones = []

    with open("../databases/panteones.mf", 'r', encoding='Utf-8') as archivo:
        for i in archivo.readlines():
            panteones.append(i.rstrip())

    return panteones


def obtener_fecha_reg(id: int) -> tuple:
    """Recupera desde la base de datos la fecha de un registro de caja específico
    y la retorna en una tupla conteniendo dia (cadena, dos dígitos), mes (cadena,
    dos dígitos) y año (cadena, cuatro dígitos).

    :param id: ID del registro de caja
    :type id: int

    :rtype: tuple
    """
    with sql.connect(mant.DATABASE) as conn:
        cursor = conn.cursor()
        instruccion = f"SELECT * FROM caja WHERE id = '{id}'"
        cursor.execute(instruccion)
        datos = cursor.fetchall()

    i_d, cat, des, tra, ing, egr, obs, dia, mes, año, cer, use = datos[0]

    return dia, mes, año


def obtener_comisiones(rendicion: str | int) -> list:
    """Recupera desde la base de datos las comisiones correspondientes a
    una rendición específica y las retorna en una lista.

    :param rendicion: Número de rendición
    :type: str or int

    :rtype: list
    """
    with sql.connect(mant.DATABASE) as conn:
        cursor = conn.cursor()
        instrucción = f"SELECT * FROM comisiones WHERE rendicion = '{rendicion}'"
        cursor.execute(instrucción)
        datos = cursor.fetchall()
    return datos


def eliminar_comisiones(rendicion: str | int):
    """Elimina de la base de datos todas las comisiones correspondientes
    a una rendición específica.

    :param rendicion: Número de rendición
    :type rendición: str or int
    """
    with sql.connect(mant.DATABASE) as conn:
        cursor = conn.cursor()
        instrucción = f"DELETE FROM comisiones WHERE rendicion = '{rendicion}'"
        cursor.execute(instrucción)


def es_cerrada(id: int) -> int:
    """Recupera desde la base de datos si un registro de caja específico
    pertenece a una caja cerrada (1) o no (0) y lo retorna.

    :param id: ID del movimiento de caja
    :type id: int

    :rtype: int
    """
    with sql.connect(mant.DATABASE) as conn:
        cursor = conn.cursor()
        instruccion = f"SELECT * FROM caja WHERE id = '{id}'"
        cursor.execute(instruccion)
        datos = cursor.fetchall()

    i_d, cat, des, tra, ing, egr, obs, dia, mes, año, cer, use = datos[0]

    return cer


def ult_reg() -> list:
    """Recupera de la base de datos el último movimiento de caja y retorna
    toda la información del mismo en una lista.

    :rtype: list
    """
    with sql.connect(mant.DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM caja ORDER BY id DESC LIMIT 1")
        ult_registro = cursor.fetchall()

    return list(ult_registro[0])


def total_ing_por_cob(cobrador: str, mes:str, año: str) -> float | int:
    """Suma todos los cobros de un cobrador específico en un mes específico y
    los retorna.

    :param cobrador: Nombre del cobrador
    :type cobrador: str

    :param mes: Mes a buscar (cadena, dos dígitos).
    :type mes: str

    :param año: Año a buscar (cadena, cuatro dígitos).
    :type año: str

    :rtype: float or int
    """
    panteones = tuple(obtener_panteon())

    with sql.connect(mant.DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute(f"SELECT SUM(ingreso) FROM caja WHERE descripcion = '{cobrador}' AND mes='{mes}' AND año='{año}' AND categoria IN {panteones}")
        datos = cursor.fetchone()
    
    if datos[0] == None:
        return 0

    return float(datos[0])


def opcion_menu() -> int:                                                                           # OPCIÓN MENÚ PRINCIPAL
    """Muestra al usuario un menú y luego le solicita ingresar una de las
    opciones mostradas a través del número correspondiente. En caso de no
    ingresar una opción correcta, se le volverá a solicitar.

    :rtype: int
    """
    print("")
    print("********** Acciones disponibles **********")
    print("")
    print("   1. Registrar gasto de oficina")
    print("   2. Registrar pago de alquiler")
    print("   3. Registrar pago de sueldo")
    print("   4. Registrar pago de comisión")
    print("   5. Registrar alivio de caja")
    print("   6. Registrar ingreso extraordinario")
    print("   7. Operar con rendiciones")
    print("   8. Operar con los registros")
    print("   9. Caja mensual")
    print("   10. Registrar cobros de Federación")
    print("   0. Realizar cierre de caja")
    print("")
    try:
        opcion = int(input("Ingrese una opción: "))
        while opcion < 0 or opcion > 10:
            print("")
            print("Opción incorrecta.")
            print("")
            opcion = int(input("Ingrese una opción: "))
    except ValueError: 
        print("Opción incorrecta.")
        opcion = -1
    except:
        mant.log_error()
        input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
        print()
        opcion = -1
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
        if opcion == 1:     # Registrar gasto de oficina
            reg_gastos_of(idu)
        elif opcion == 2:   # Registrar pago de alquiler
            reg_pago_alquiler(idu)
        elif opcion == 3:   # Registrar pago de sueldo
            reg_pago_sueldo(idu)
        elif opcion == 4:   # Registrar pago de comisión
            reg_pago_comision(idu)
        elif opcion == 5:   # Registrar alivio de caja
            reg_alivio(idu)
        elif opcion == 6:   # Registrar ingreso extraordinario
            reg_ingreso_extraordinario(idu)
        elif opcion == 7:   # Operar con rendiciones
            menu_rendiciones(idu)
        elif opcion == 8:   # Operar con los registros
            menu_edit(idu)
        elif opcion == 9:   # Caja mensual
            menu_caja_mensual()
        elif opcion == 10:  # Registrar cobros de Federación
            reg_cobros_federacion(idu)
        elif opcion == 0:   # Realizar cierre de caja
            cierre_caja()


def menu_oficinas() -> int:                                                                         # MENÚ OFICINAS
    """Muestra al usuario un menú y luego le solicita ingresar una de las
    opciones mostradas a través del número correspondiente. En caso de no
    ingresar una opción correcta, se le volverá a solicitar.

    :rtype: int
    """
    print("")
    print("Seleccione una oficina")
    print("")
    print("   1. Córdoba 2915")
    print("   2. Gálvez")
    print("   3. Arroyo")
    print("   4. Panteón NOB")
    print("   0. Volver")
    print("")
    oficina = -1
    try:
        oficina = int(input("Ingrese una opción: "))
        while oficina < 0 or oficina > 4:
            print("")
            print("Opción incorrecta.")
            print("")
            oficina = int(input("Ingrese una opción: "))
    except ValueError: 
        print("Opción incorrecta.")
        oficina = -1
    except:
        mant.log_error()
        input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
        print()
        oficina -1
    return oficina


def reg_gastos_of(idu: int):
    """Recibe el ID del usuario. Luego llama a la función donde se muestra las
    opciones y recibe, a través de ella, la opción ingresada por el usuario.
    
    Luego permite al usuario registrar un gasto de oficina en la base de datos.
    Los campos a completar por el usuario son los siguientes:
    - Oficina: La elije a partir del menú de opciones desplegado y se guarda en
    la columna categoria de la base de datos.
    - Número de ticket: Se guarda en la columna transaccion de la base de datos.
    - Descripción: Se guarda en la columna descripcion de la base de datos.
    - Monto: Se guarda en la columna egreso de la base de datos.
    - Observaciones: Se guarda en la columna observacion de la base de datos.

    :param idu: ID de usuario
    :type idu: int
    """
    print("********** Registrar gasto de oficina **********")
    print("")
    
    oficina = -1
    transaccion = ""
    categoria = ""
    descripcion = ""
    egreso = 0
    observacion = ""
    dia = obtener_dia()
    mes = obtener_mes()
    año = obtener_año()
    
    while oficina != 0:
        oficina = menu_oficinas()
    
        if oficina == 1:    # Gastos oficina Córdoba 2915
            categoria = "Gastos oficina Córdoba 2915"
            
            while transaccion == "":
                print("")
                transaccion = input("Número de ticket: ")
                print("")
            
            while descripcion == "":
                descripcion = input("Descripción: ")
                print("")
            
            try:
                while egreso == 0:
                    egreso = float(input("Monto: $ "))
                    print("")
            
            except ValueError:
                print("")
                print("         ERROR. El monto debe ser numérico. No se registró ningún movimiento.")
                print("")
                return
            except:
                mant.log_error()
                input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
                print()
                return
            
            observacion = input("Observaciones: ")
            print("")
            
            descripcion = mant.reemplazar_comilla(descripcion)
            transaccion = mant.reemplazar_comilla(transaccion)
            observacion = mant.reemplazar_comilla(observacion)
            
            parameters = str((categoria, descripcion, transaccion, egreso, observacion, dia, mes, año, idu))
            query = f"INSERT INTO caja (categoria, descripcion, transaccion, egreso, observacion, dia, mes, año, id_user) VALUES {parameters}"
            
            try:
                mant.run_query(query)
            
            except:
                mant.log_error()
                input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
                print()
                return
            
            ult_reg_list = ult_reg()
            print("Se registró: ", ult_reg_list[1], " - ", ult_reg_list[2], " - ","$", ult_reg_list[5], " - ", ult_reg_list[6], " - " "NÚMERO DE REGISTRO: ", f"{ult_reg_list[0]}".rjust(8, '0'))
            
            return
        
        elif oficina == 2:  # Gastos oficina Gálvez
            categoria = "Gastos oficina Gálvez"
            
            while transaccion == "":
                print("")
                transaccion = input("Número de ticket: ")
                print("")
            
            while descripcion == "":
                descripcion = input("Descripción: ")
                print("")
            
            try:
                while egreso == 0:
                    egreso = float(input("Monto: $ "))
                    print("")
            
            except ValueError:
                print("")
                print("         ERROR. El monto debe ser numérico. No se registró ningún movimiento.")
                print("")
                return
            except:
                mant.log_error()
                input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
                print()
                return
            
            observacion = input("Observaciones: ")
            print("")
            
            descripcion = mant.reemplazar_comilla(descripcion)
            transaccion = mant.reemplazar_comilla(transaccion)
            observacion = mant.reemplazar_comilla(observacion)
            
            parameters = str((categoria, descripcion, transaccion, egreso, observacion, dia, mes, año, idu))
            query = f"INSERT INTO caja (categoria, descripcion, transaccion, egreso, observacion, dia, mes, año, id_user) VALUES {parameters}"
            
            try:
                mant.run_query(query)
            
            except:
                mant.log_error()
                input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
                print()
                return
            
            ult_reg_list = ult_reg()
            print("Se registró: ", ult_reg_list[1], " - ", ult_reg_list[2], " - ","$", ult_reg_list[5], " - ", ult_reg_list[6], " - " "NÚMERO DE REGISTRO: ", f"{ult_reg_list[0]}".rjust(8, '0'))
            
            return
        
        elif oficina == 3:  # Gastos oficina Arroyo
            categoria = "Gastos oficina Arroyo"
            
            while transaccion == "":
                print("")
                transaccion = input("Número de ticket: ")
                print("")
            
            while descripcion == "":
                descripcion = input("Descripción: ")
                print("")
            
            try:
                while egreso == 0:
                    egreso = float(input("Monto: $ "))
                    print("")
            
            except ValueError:
                print("")
                print("         ERROR. El monto debe ser numérico. No se registró ningún movimiento.")
                print("")
                return
            except:
                mant.log_error()
                input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
                print()
                return
            
            observacion = input("Observaciones: ")
            print("")
            
            descripcion = mant.reemplazar_comilla(descripcion)
            transaccion = mant.reemplazar_comilla(transaccion)
            observacion = mant.reemplazar_comilla(observacion)
            
            parameters = str((categoria, descripcion, transaccion, egreso, observacion, dia, mes, año, idu))
            query = f"INSERT INTO caja (categoria, descripcion, transaccion, egreso, observacion, dia, mes, año, id_user) VALUES {parameters}"
            
            try:
                mant.run_query(query)
            
            except:
                mant.log_error()
                input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
                print()
                return
            
            ult_reg_list = ult_reg()
            print("Se registró: ", ult_reg_list[1], " - ", ult_reg_list[2], " - ","$", ult_reg_list[5], " - ", ult_reg_list[6], " - " "NÚMERO DE REGISTRO: ", f"{ult_reg_list[0]}".rjust(8, '0'))
            
            return
        
        elif oficina == 4:  # Gastos panteón NOB
            categoria = "Gastos panteón NOB"
            
            while transaccion == "":
                print("")
                transaccion = input("Número de ticket: ")
                print("")
            
            while descripcion == "":
                descripcion = input("Descripción: ")
                print("")
            
            try:
                while egreso == 0:
                    egreso = float(input("Monto: $ "))
                    print("")
            
            except ValueError:
                print("")
                print("         ERROR. El monto debe ser numérico. No se registró ningún movimiento.")
                print("")
                return
            except:
                mant.log_error()
                input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
                print()
                return
            
            observacion = input("Observaciones: ")
            print("")
            
            descripcion = mant.reemplazar_comilla(descripcion)
            transaccion = mant.reemplazar_comilla(transaccion)
            observacion = mant.reemplazar_comilla(observacion)
            
            parameters = str((categoria, descripcion, transaccion, egreso, observacion, dia, mes, año, idu))
            query = f"INSERT INTO caja (categoria, descripcion, transaccion, egreso, observacion, dia, mes, año, id_user) VALUES {parameters}"
            
            try:
                mant.run_query(query)
            
            except:
                mant.log_error()
                input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
                print()
                return
            
            ult_reg_list = ult_reg()
            print("Se registró: ", ult_reg_list[1], " - ", ult_reg_list[2], " - ","$", ult_reg_list[5], " - ", ult_reg_list[6], " - " "NÚMERO DE REGISTRO: ", f"{ult_reg_list[0]}".rjust(8, '0'))
            
            return
    

def reg_pago_alquiler(idu: int):
    """Permite al usuario registrar un pago de alquiler en la base de datos.
    Los campos a completar por el usuario son los siguientes:
    - Número de ticket / recibo: Se guarda en la columna transaccion de la 
    base de datos.
    - Descripción: Se guarda en la columna descripcion de la base de datos.
    - Monto: Se guarda en la columna egreso de la base de datos.
    - Observaciones: Se guarda en la columna observacion de la base de datos.

    :param idu: ID de usuario
    :type idu: int
    """
    print("********** Registrar gasto de oficina **********")
    print("")
    
    transaccion = ""
    categoria = "Pago de alquileres"
    descripcion = ""
    egreso = 0
    observacion = ""
    dia = obtener_dia()
    mes = obtener_mes()
    año = obtener_año()
    
    while transaccion == "":
        print("")
        transaccion = input("Número de ticket / recibo: ")
        print("")
    
    while descripcion == "":
        descripcion = input("Descripción: ")
        print("")
    
    try:
        while egreso == 0:
            egreso = float(input("Monto: $ "))
            print("")
    
    except ValueError:
        print("")
        print("         ERROR. El monto debe ser numérico. No se registró ningún movimiento.")
        print("")
        return
    except:
        mant.log_error()
        input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
        print()
        return
    
    observacion = input("Observaciones: ")
    print("")
    
    descripcion = mant.reemplazar_comilla(descripcion)
    transaccion = mant.reemplazar_comilla(transaccion)
    observacion = mant.reemplazar_comilla(observacion)
    
    parameters = str((categoria, descripcion, transaccion, egreso, observacion, dia, mes, año, idu))
    query = f"INSERT INTO caja (categoria, descripcion, transaccion, egreso, observacion, dia, mes, año, id_user) VALUES {parameters}"
    
    try:
        mant.run_query(query)
    
    except:
        mant.log_error()
        input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
        print()
        return
    
    ult_reg_list = ult_reg()
    print("Se registró: ", ult_reg_list[1], " - ", ult_reg_list[2], " - ","$", ult_reg_list[5], " - ", ult_reg_list[6], " - " "NÚMERO DE REGISTRO: ", f"{ult_reg_list[0]}".rjust(8, '0'))
    
    return


def reg_pago_sueldo(idu: int):
    """Permite al usuario registrar un pago de sueldo en la base de datos.
    Los campos a completar por el usuario son los siguientes:
    - Número de recibo: Se guarda en la columna transaccion de la 
    base de datos.
    - Empleado/a: Se guarda en la columna descripcion de la base de datos.
    - Monto: Se guarda en la columna egreso de la base de datos.
    - Observaciones: Se guarda en la columna observacion de la base de datos.

    :param idu: ID de usuario
    :type idu: int
    """    
    print("********** Registrar pago de sueldo **********")
    print("")
    
    transaccion = ""
    categoria = "Pago de sueldos"
    descripcion = ""
    egreso = 0
    observacion = ""
    dia = obtener_dia()
    mes = obtener_mes()
    año = obtener_año()
    
    while transaccion == "":
        print("")
        transaccion = input("Número de recibo: ")
        print("")
    
    while descripcion == "":
        descripcion = input("Empleado/a: ")
        print("")
    
    try:
        while egreso == 0:
            egreso = float(input("Monto: $ "))
            print("")
    
    except ValueError:
        print("")
        print("         ERROR. El monto debe ser numérico. No se registró ningún movimiento.")
        print("")
        return
    except:
        mant.log_error()
        input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
        print()
        return
    
    observacion = input("Observaciones: ")
    print("")
    
    descripcion = mant.reemplazar_comilla(descripcion)
    transaccion = mant.reemplazar_comilla(transaccion)
    observacion = mant.reemplazar_comilla(observacion)

    parameters = str((categoria, descripcion, transaccion, egreso, observacion, dia, mes, año, idu))
    query = f"INSERT INTO caja (categoria, descripcion, transaccion, egreso, observacion, dia, mes, año, id_user) VALUES {parameters}"

    try:
        mant.run_query(query)

    except:
        mant.log_error()
        input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
        print()
        return

    ult_reg_list = ult_reg()
    print("Se registró: ", ult_reg_list[1], " - ", ult_reg_list[2], " - ","$", ult_reg_list[5], " - ", ult_reg_list[6], " - " "NÚMERO DE REGISTRO: ", f"{ult_reg_list[0]}".rjust(8, '0'))

    return


def reg_pago_comision(idu: int):
    """Permite al usuario registrar un pago de comisión en la base de datos.
    Los campos a completar por el usuario son los siguientes:
    - Rendición: Número de rendición de la cual se extraerán las comisiones.
    Se guarda en la columna transaccion de la base de datos.
    - Observaciones: Se guarda en la columna observacion de la base de datos.

    Una vez que fue registrado el pago de las comisiones, éstas se borran de
    la tabla de comisiones de la base de datos.

    En caso que una rendición posea cobros de más de un cobrador se le avisa
    al usuario, a quien se le solicitará que indique a que cobrador se le
    deberá registrar el pago.    

    :param idu: ID de usuario
    :type idu: int
    """
    print("********** Registrar pago de comisión **********")
    print("")
    
    try:
        rendicion = int(input("Indique el número de rendición: "))
        print()
    
        datos = obtener_comisiones(rendicion)
    
        if datos == []:
            print("         ERROR. Indique un número de rendición válido.")
            print()
            return
        
        total_com = 0
        total_cob = 0
        
        for i in datos:
            cob, ren, rec, imp, com = i
            total_com += com
            total_cob += cob
        
        categoria = "Pago de comisiones"
        
        # Confirmar si todos los cobros de la rendición son del mismo cobrador
        if total_cob == cob * len(datos):
            pass
        
        else:
            print("                                                                *** ATENCIÓN ***")
            print("                                                     La rendición posee varios cobradores.")
            print()
            
            print("Indique el ID del cobrador que cobra la comisión: ")
            datos = obtener_cobradores()
            counter = 0
            
            for i in datos:
                counter += 1
                id_cob, n_cob = i
                print(f"    * {id_cob}. {n_cob}")
            print()
            
            loop = -1
            while loop == -1:
                try:
                    loop = cob = int(input("Cobrador: "))
                    print()
            
                    while cob < 1 or cob > counter:
                        print("         ERROR. Debe indicar un ID de cobrador válido.")
                        print()
                        cob = int(input("Cobrador: "))
            
                except ValueError:
                    print("         ERROR. Debe ingresar un dato de tipo numérico.")
                    print()
                    loop = -1
                except:
                    mant.log_error()
                    print("")
                    input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
                    print()
                    return
        
        cobrador = obtener_nom_cobrador(cob)
        
        observacion = input("Observaciones: ")
        print("")
        
        dia = obtener_dia()
        mes = obtener_mes()
        año = obtener_año()
        
        observacion = mant.reemplazar_comilla(observacion)
        
        parameters = str((categoria, cobrador, rendicion, total_com, observacion, dia, mes, año, idu))
        query = f"INSERT INTO caja (categoria, descripcion, transaccion, egreso, observacion, dia, mes, año, id_user) VALUES {parameters}"

        mant.run_query(query)

        ult_reg_list = ult_reg()
        print("Se registró: ", ult_reg_list[1], " - ", ult_reg_list[2], " - ","$", ult_reg_list[5], " - ", ult_reg_list[6], " - " "NÚMERO DE REGISTRO: ", f"{ult_reg_list[0]}".rjust(8, '0'))
        print("")
        
        # Eliminando las comisiones pagas de la base de datos
        eliminar_comisiones(rendicion)

        return

    except ValueError:
        print()
        print("         ERROR. El dato solicitado debe ser de tipo numérico.")
        return
    except:
        mant.log_error()
        print()
        input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
        print()
        return


def reg_alivio(idu: int):
    """Permite al usuario registrar un alivio de caja en la base de datos.
    Los campos a completar por el usuario son los siguientes:
    - Número de caja: Se guarda en la columna transaccion de la 
    base de datos.
    - ¿Quién realiza el alivio?: Se guarda en la columna descripcion de la base de datos.
    - ¿A quién se lo entrega?: Se guarda en la columna descripcion de la base de datos.
    - Monto: Se guarda en la columna egreso de la base de datos.
    - Observaciones: Se guarda en la columna observacion de la base de datos.

    :param idu: ID de usuario
    :type idu: int
    """
    print("********** Registar alivio de caja **********")
    print("")
    
    transaccion = ""
    categoria = "Alivios de caja"
    descripcion = ""
    egreso = 0
    observacion =""
    dia = obtener_dia()
    mes = obtener_mes()
    año = obtener_año()
    
    while transaccion == "":
        print("")
        transaccion = input("Número de caja: ")
        print("")
    
    while descripcion == "":
        des1 = input("¿Quién realiza el alivio?: ")
        print("")
    
        des2 = input("¿A quién se lo entrega?: ")
        print("")
    
        descripcion = "A " + des2 + " de " + des1  
    
    try:
        while egreso == 0:
            egreso = float(input("Monto: $ "))
            print("")
    
    except ValueError:
        print("")
        print("         ERROR. El monto debe ser numérico. No se registró ningún movimiento.")
        print("")
        return
    
    except:
        mant.log_error()
        input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
        print()
        return
    
    observacion = input("Observaciones: ")
    print("")
    
    descripcion = mant.reemplazar_comilla(descripcion)
    transaccion = mant.reemplazar_comilla(transaccion)
    observacion = mant.reemplazar_comilla(observacion)

    parameters = str((categoria, descripcion, transaccion, egreso, observacion, dia, mes, año, idu))
    query = f"INSERT INTO caja (categoria, descripcion, transaccion, egreso, observacion, dia, mes, año, id_user) VALUES {parameters}"
    
    mant.run_query(query)
    
    ult_reg_list = ult_reg()
    print("Se registró: ", ult_reg_list[1], " - ", ult_reg_list[2], " - ","$", ult_reg_list[5], " - ", ult_reg_list[6], " - " "NÚMERO DE REGISTRO: ", f"{ult_reg_list[0]}".rjust(8, '0'))
    
    return


def reg_ingreso_extraordinario(idu: int):
    """Permite al usuario registrar un ingreso extraordinario en la base de
    datos.
    Los campos a completar por el usuario son los siguientes:
    - Número de ticket / recibo: Se guarda en la columna transaccion de la 
    base de datos.
    - Descripción: Se guarda en la columna descripcion de la base de datos.
    - Monto: Se guarda en la columna ingreso de la base de datos.
    - Observaciones: Se guarda en la columna observacion de la base de datos.

    :param idu: ID de usuario
    :type idu: int
    """
    print("********** Registrar ingreso extraordinario **********")
    print("")
    
    transaccion = ""
    categoria = "Ingresos extraordinarios"
    descripcion = ""
    ingreso = 0
    observacion = ""
    dia = obtener_dia()
    mes = obtener_mes()
    año = obtener_año()
    
    while transaccion == "":
        print("")
        transaccion = input("Número de ticket / recibo: ")
        print("")
    
    while descripcion == "":
        descripcion = input("Descripción: ")
        print("")
    
    try:
        while ingreso == 0:
            ingreso = float(input("Monto: $ "))
            print("")
    
    except ValueError:
        print("")
        print("         ERROR. El monto debe ser numérico. No se registró ningún movimiento.")
        print("")
        return
    except:
        mant.log_error()
        input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
        print()
        return
    
    observacion = input("Observaciones: ")
    print("")
    
    descripcion = mant.reemplazar_comilla(descripcion)
    transaccion = mant.reemplazar_comilla(transaccion)
    observacion = mant.reemplazar_comilla(observacion)
    
    parameters = str((categoria, descripcion, transaccion, ingreso, observacion, dia, mes, año, idu))
    query = f"INSERT INTO caja (categoria, descripcion, transaccion, ingreso, observacion, dia, mes, año, id_user) VALUES {parameters}"
    
    mant.run_query(query)
    
    ult_reg_list = ult_reg()
    print("Se registró: ", ult_reg_list[1], " - ", ult_reg_list[2], " - ","$", ult_reg_list[4], " - ", ult_reg_list[6], " - " "NÚMERO DE REGISTRO: ", f"{ult_reg_list[0]}".rjust(8, '0'))
    
    return


def opcion_menu_rendiciones() -> int:                                                               # OPCIÓN MENÚ RENDICIONES
    """Muestra al usuario un menú y luego le solicita ingresar una de las
    opciones mostradas a través del número correspondiente. En caso de no
    ingresar una opción correcta, se le volverá a solicitar.

    :rtype: int
    """
    print("")
    print("********** Acciones disponibles **********")
    print("")
    print("   1. Registrar un monto a rendir (-)")
    print("   2. Registrar pago de rendición adeudada (+)")
    print("   3. Registrar entrega de dinero sin listado (+)")
    print("   4. Registrar entrega de listado adeudado (-)")
    print("   0. Volver")
    print("")
    try:
        opcion = int(input("Ingrese una opción: "))
        while opcion < 0 or opcion > 4:
            print("")
            print("Opción incorrecta.")
            print("")
            opcion = int(input("Ingrese una opción: "))
    except ValueError: 
        print("Opción incorrecta.")
        opcion = -1
    except:
        mant.log_error()
        input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
        print()
        opcion = -1
    return opcion


def menu_rendiciones(idu: int):                                                                     # MENÚ RENDICIONES
    """Recibe el ID del usuario. Luego llama a la función donde se muestra las
    opciones y recibe, a través de ella, la opción ingresada por el usuario.
    Luego, según la opción ingresada, llama a la función correspondiente, a la
    cual le transmite el ID del usuario.

    :param idu: ID de usuario
    :type idu: int
    """
    opcion = -1
    while opcion != 0:
        opcion = opcion_menu_rendiciones()
        if opcion == 1:
            a_rendir(idu)
        elif opcion == 2:
            rend_adeudada(idu)
        elif opcion == 3:
            sin_listado(idu)
        elif opcion == 4:
            listado_adeudado(idu)


def a_rendir(idu: int):
    """Permite al usuario registrar un monto a rendir en la base de datos.
    Los campos a completar por el usuario son los siguientes:
    - Número de rendición: Se guarda en la columna transaccion de la 
    base de datos.
    - Cobrador: Se guarda en la columna descripcion de la base de datos.
    - Monto a rendir: Se guarda en la columna egreso de la base de datos.
    - Observaciones: Se guarda en la columna observacion de la base de datos.

    Esta opción se realiza cuando un cobrador entrega una rendición pero no
    realiza la entrega del dinero correspondiente. Por este motivo se registra
    el egreso de dicho dinero que ya fue ingresado al realizar el ingreso de
    los recibos al sistema.

    Su acción complementaria es Registrar pago de rendición adeudada (+).

    :param idu: ID de usuario
    :type idu: int
    """
    print("********** Registrar monto a rendir (-) **********")
    print("")
    
    transaccion = ""
    categoria = "A rendir"
    descripcion = ""
    egreso = 0
    observacion = ""
    dia = obtener_dia()
    mes = obtener_mes()
    año = obtener_año()
    
    while transaccion == "":
        print("")
        transaccion = input("Número de rendición: ")
        print("")
    
        print("Indique el ID de cobrador: ")
    
        datos = obtener_cobradores()
        counter = 0
       
        for i in datos:
            counter += 1
            id_cob, n_cob = i
            print(f"    * {id_cob}. {n_cob}")
        print()
       
        loop = -1
        while loop == -1:
            try:
                loop = cobrador = int(input("Cobrador: "))
                print()
                while cobrador < 1 or cobrador > counter:
                    print("         ERROR. Debe indicar un ID de cobrador válido.")
                    print()
                    cobrador = int(input("Cobrador: "))
       
            except ValueError:
                print("         ERROR. Debe ingresar un dato de tipo numérico.")
                print()
                loop = -1
       
            except:
                mant.log_error()
                print("")
                input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
                print()
                return
        print("")
    
    try:
        while egreso == 0:
            egreso = float(input("Monto a rendir: $ "))
            print("")
    
    except ValueError:
        print("")
        print("         ERROR. El monto debe ser numérico. No se registró ningún movimiento.")
        print("")
        return
    except:
        mant.log_error()
        input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
        print()
        return
    
    observacion = input("Observaciones: ")
    print("")
    
    descripcion = obtener_nom_cobrador(cobrador)
    
    descripcion = mant.reemplazar_comilla(descripcion)
    transaccion = mant.reemplazar_comilla(transaccion)
    observacion = mant.reemplazar_comilla(observacion)
    
    parameters = str((categoria, descripcion, transaccion, egreso, observacion, dia, mes, año, idu))
    query = f"INSERT INTO caja (categoria, descripcion, transaccion, egreso, observacion, dia, mes, año, id_user) VALUES {parameters}"
    
    try:
        mant.run_query(query)
    
    except:
        mant.log_error()
        input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
        print()
        return
    
    ult_reg_list = ult_reg()
    print("Se registró: ", ult_reg_list[1], " - ", ult_reg_list[2], " - ","$", ult_reg_list[5], " - ", ult_reg_list[6], " - " "NÚMERO DE REGISTRO: ", f"{ult_reg_list[0]}".rjust(8, '0'))
    
    return


def rend_adeudada(idu: int):
    """Permite al usuario registrar el pago de una rendición adeudada en la
    base de datos.
    Los campos a completar por el usuario son los siguientes:
    - Número de rendición: Se guarda en la columna transaccion de la 
    base de datos.
    - Cobrador: Se guarda en la columna descripcion de la base de datos.
    - Monto: Se guarda en la columna ingreso de la base de datos.
    - Observaciones: Se guarda en la columna observacion de la base de datos.

    Esta opción se realiza cuando un cobrador entrega el dinero de una
    rendición que ya había sido entregada. Se realiza para impactar en caja
    en ingreso de dicho dinero.
    
    Es la acción complementaria a Registrar monto a rendir (-).

    :param idu: ID de usuario
    :type idu: int
    """
    print("********** Registrar pago de rendición adeudada (+) **********")
    print("")
    
    transaccion = ""
    categoria = "Rendiciones adeudadas"
    descripcion = ""
    ingreso = 0
    observacion = ""
    dia = obtener_dia()
    mes = obtener_mes()
    año = obtener_año()
    
    while transaccion == "":
        print("")
        transaccion = input("Número de rendición: ")
        print("")
    
    print("Indique el ID de cobrador: ")
    
    datos = obtener_cobradores()
    counter = 0
    
    for i in datos:
        counter += 1
        id_cob, n_cob = i
        print(f"    * {id_cob}. {n_cob}")
    print()
    
    loop = -1
    while loop == -1:
        try:
            loop = cobrador = int(input("Cobrador: "))
            print()
    
            while cobrador < 1 or cobrador > counter:
                print("         ERROR. Debe indicar un ID de cobrador válido.")
                print()
                cobrador = int(input("Cobrador: "))
    
        except ValueError:
            print("         ERROR. Debe ingresar un dato de tipo numérico.")
            print()
            loop = -1
        except:
            mant.log_error()
            print("")
            input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
            print()
            return
        print("")
    
    try:
        while ingreso == 0:
            ingreso = float(input("Monto: $ "))
            print("")
    
    except ValueError:
        print("")
        print("         ERROR. El monto debe ser numérico. No se registró ningún movimiento.")
        print("")
        return
    except:
        mant.log_error()
        input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
        print()
        return
    
    observacion = input("Observaciones: ")
    print("")
    
    descripcion = obtener_nom_cobrador(cobrador)
    
    descripcion = mant.reemplazar_comilla(descripcion)
    transaccion = mant.reemplazar_comilla(transaccion)
    observacion = mant.reemplazar_comilla(observacion)
    
    parameters = str((categoria, descripcion, transaccion, ingreso, observacion, dia, mes, año, idu))
    query = f"INSERT INTO caja (categoria, descripcion, transaccion, ingreso, observacion, dia, mes, año, id_user) VALUES {parameters}"
    
    try:
        mant.run_query(query)
    
    except:
        mant.log_error()
        input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
        print()
        return
    
    ult_reg_list = ult_reg()
    print("Se registró: ", ult_reg_list[1], " - ", ult_reg_list[2], " - ","$", ult_reg_list[4], " - ", ult_reg_list[6], " - " "NÚMERO DE REGISTRO: ", f"{ult_reg_list[0]}".rjust(8, '0'))

    return


def sin_listado(idu: int):
    """Permite al usuario registrar la entrega de dinero sin listado en la
    base de datos.
    Los campos a completar por el usuario son los siguientes:
    - Cobrador: Se guarda en la columna descripcion de la base de datos.
    - Monto: Se guarda en la columna ingreso de la base de datos.
    - Observaciones: Se guarda en la columna observacion de la base de datos.

    Esta opción se realiza cuando un cobrador entrega el dinero de una
    rendición sin entregar el listado de recibos cobrados. Por este motivo se
    realiza en ingreso del dinero ya que los recibos no fueron ingresados al
    sistema.

    Su acción complementaria es Registrar entrega de listado adeudado (-).

    :param idu: ID de usuario
    :type idu: int
    """
    print("********** Registrar entrega de dinero sin listado (+) **********")
    print("")
    
    transaccion = "S/L"
    categoria = "Sin listado (+)"
    descripcion = ""
    ingreso = 0
    observacion = ""
    dia = obtener_dia()
    mes = obtener_mes()
    año = obtener_año()
    
    print("Indique el ID de cobrador: ")
    datos = obtener_cobradores()
    counter = 0
    
    for i in datos:
        counter += 1
        id_cob, n_cob = i
        print(f"    * {id_cob}. {n_cob}")
    print()
    
    loop = -1
    while loop == -1:
        try:
            loop = cobrador = int(input("Cobrador: "))
            print()
    
            while cobrador < 1 or cobrador > counter:
                print("         ERROR. Debe indicar un ID de cobrador válido.")
                print()
                cobrador = int(input("Cobrador: "))
    
        except ValueError:
            print("         ERROR. Debe ingresar un dato de tipo numérico.")
            print()
            loop = -1
        except:
            mant.log_error()
            print("")
            input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
            print()
            return
        print("")
    
    try:
        while ingreso == 0:
            ingreso = float(input("Monto: $ "))
            print("")
    
    except ValueError:
        print("")
        print("         ERROR. El monto debe ser numérico. No se registró ningún movimiento.")
        print("")
        return
    except:
        mant.log_error()
        input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
        print()
        return
    
    observacion = input("Observaciones: ")
    print("")
    
    descripcion = obtener_nom_cobrador(cobrador)
    
    descripcion = mant.reemplazar_comilla(descripcion)
    transaccion = mant.reemplazar_comilla(transaccion)
    observacion = mant.reemplazar_comilla(observacion)
    
    parameters = str((categoria, descripcion, transaccion, ingreso, observacion, dia, mes, año, idu))
    query = f"INSERT INTO caja (categoria, descripcion, transaccion, ingreso, observacion, dia, mes, año, id_user) VALUES {parameters}"
    
    try:
        mant.run_query(query)
    
    except:
        mant.log_error()
        input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
        print()
        return
    
    ult_reg_list = ult_reg()
    print("Se registró: ", ult_reg_list[1], " - ", ult_reg_list[2], " - ","$", ult_reg_list[4], " - ", ult_reg_list[6], " - " "NÚMERO DE REGISTRO: ", f"{ult_reg_list[0]}".rjust(8, '0'))
    
    return


def listado_adeudado(idu: int):
    """Permite al usuario registrar la entrega de un listado adeudado en
    la base de datos.
    Los campos a completar por el usuario son los siguientes:
    - Número de rendición: Se guarda en la columna transaccion de la 
    base de datos.
    - Cobrador: Se guarda en la columna descripcion de la base de datos.
    - Monto del listado: Se guarda en la columna egreso de la base de datos.
    - Observaciones: Se guarda en la columna observacion de la base de datos.

    Esta opción se realiza cuando un cobrador realiza la entrega de un listado
    de recibos cobrados por el cual ya había entregado el dinero. Por este
    motivo se registra el egreso del dinero ya que, al ingresar los recibos al
    sistema, se generaría un ingreso de dinero no existente en el momento.

    Es la acción complementaria a Registrar entrega de dinero sin listado (+).

    :param idu: ID de usuario
    :type idu: int
    """
    print("********** Registrar entrega de listado adeudado (-) **********")
    print("")
    
    transaccion = ""
    categoria = "Sin listado (-)"
    descripcion = ""
    egreso = 0
    observacion = ""
    dia = obtener_dia()
    mes = obtener_mes()
    año = obtener_año()
    
    while transaccion == "":
        print("")
        transaccion = input("Número de rendición: ")
        print("")
    
        print("Indique el ID de cobrador: ")
        datos = obtener_cobradores()
        counter = 0
    
        for i in datos:
            counter += 1
            id_cob, n_cob = i
            print(f"    * {id_cob}. {n_cob}")
        print()
    
        loop = -1
        while loop == -1:
            try:
                loop = cobrador = int(input("Cobrador: "))
                print()
    
                while cobrador < 1 or cobrador > counter:
                    print("         ERROR. Debe indicar un ID de cobrador válido.")
                    print()
                    cobrador = int(input("Cobrador: "))
    
            except ValueError:
                print("         ERROR. Debe ingresar un dato de tipo numérico.")
                print()
                loop = -1
            except:
                mant.log_error()
                print("")
                input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
                print()
                return
        print("")
    
    try:
        while egreso == 0:
            egreso = float(input("Monto del listado: $ "))
            print("")
    
    except ValueError:
        print("")
        print("         ERROR. El monto debe ser numérico. No se registró ningún movimiento.")
        print("")
        return
    except:
        mant.log_error()
        input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
        print()
        return
    
    observacion = input("Observaciones: ")
    print("")
    
    descripcion = obtener_nom_cobrador(cobrador)
    
    descripcion = mant.reemplazar_comilla(descripcion)
    transaccion = mant.reemplazar_comilla(transaccion)
    observacion = mant.reemplazar_comilla(observacion)
    
    parameters = str((categoria, descripcion, transaccion, egreso, observacion, dia, mes, año, idu))
    query = f"INSERT INTO caja (categoria, descripcion, transaccion, egreso, observacion, dia, mes, año, id_user) VALUES {parameters}"
    
    try:
        mant.run_query(query)
    
    except:
        mant.log_error()
        input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
        print()
        return
    
    ult_reg_list = ult_reg()
    print("Se registró: ", ult_reg_list[1], " - ", ult_reg_list[2], " - ","$", ult_reg_list[5], " - ", ult_reg_list[6], " - " "NÚMERO DE REGISTRO: ", f"{ult_reg_list[0]}".rjust(8, '0'))
    
    return


def opcion_menu_edit() -> int:                                                                      # OPCIÓN MENÚ EDITAR
    """Muestra al usuario un menú y luego le solicita ingresar una de las
    opciones mostradas a través del número correspondiente. En caso de no
    ingresar una opción correcta, se le volverá a solicitar.

    :rtype: int
    """
    print("Seleccione una acción")
    print("")
    print("   1. Ver movimientos del día")
    print("   2. Buscar un registro")
    print("   3. Modificar un registro")
    print("   4. Eliminar un registro")
    print("   5. Ver estado de caja actual")
    print("   0. Volver")
    print("")
    accion = -1
    try:
        accion = int(input("Ingrese una opción: "))
        while accion < 0 or accion > 5:
            print("")
            print("Opción incorrecta.")
            print("")
            accion = int(input("Ingrese una opción: "))
    except ValueError: 
        print("Opción incorrecta.")
        accion = -1
    except:
        mant.log_error()
        input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
        print()
        accion = -1
    return accion


def menu_edit(idu: int):                                                                            # MENÚ EDITAR
    """Recibe el ID del usuario. Luego llama a la función donde se muestra las
    opciones y recibe, a través de ella, la opción ingresada por el usuario.
    Luego, según la opción ingresada, llama a la función correspondiente, a la
    cual le transmite el ID del usuario.

    :param idu: ID de usuario
    :type idu: int
    """
    opcion = -1
    while opcion != 0:
        opcion = opcion_menu_edit()
        if opcion == 1:     # Ver registros
            ver_registros()
        elif opcion == 2:   # Buscar registro
            menu_buscar()
        elif opcion == 3:   # Modificar registro
            modif_registro(idu)
        elif opcion == 4:   # Eliminar registro
            eliminar_registro(idu)
        elif opcion == 5:   # Ver estado de caja actual
            ver_estado_caja(idu)
        elif opcion == 0:   # Volver
            return
   

def ver_registros():
    """Permite al usuario ver una tabla con todos los movimientos de caja registrados
    en el día.
    """
    dia = obtener_dia()
    mes = obtener_mes()
    año = obtener_año()
    
    with sql.connect(mant.DATABASE) as conn:
        cursor = conn.cursor()
        instruccion = f"SELECT * FROM caja WHERE dia = '{dia}' AND mes = '{mes}' AND año = '{año}' ORDER BY id"
        cursor.execute(instruccion)
        datos = cursor.fetchall()

    print("---------------------------------------------------------------------------------------------------------------------------------------------------------------")
    print("{:<9} {:<27} {:<27} {:<11} {:<15} {:<15} {:<30} {:<10} {:<6}".format('    ID   ','CATEGORÍA', 'DESCRIPCIÓN', 'TRANSACCIÓN', 'INGRESO', 'EGRESO','OBSERVACIONES', '  FECHA', 'USER'))
    print("---------------------------------------------------------------------------------------------------------------------------------------------------------------")

    for x in datos:
        i_d, cat, des, tra, ing, egr, obs, dia, mes, año, cer, use = x
        idu, nom, ape, tel, dom, user, pas, pri, act = mant.buscar_usuario_por_id(use)
        
        if ing == None:
            ing = ''
        
        if egr == None:
            egr = ''
        
        print("{:<9} {:<27} {:<27} {:<11} {:<15} {:<15} {:<30} {:<10} {:<6}".format(f"{i_d}".rjust(8, '0'), f"{cat[:27]}", f"{des[:27]}", f"{tra}"[:11], f"{ing}", f"{egr}", f"{obs[:30]}", f"{dia}/{mes}/{año}", f"{user}"))

    print("---------------------------------------------------------------------------------------------------------------------------------------------------------------")
    print("")
    input("Presione la tecla enter para continuar... ")


def opcion_menu_buscar() -> int:                                                                    # OPCIÓN MENÚ BUSCAR
    """Muestra al usuario un menú y luego le solicita ingresar una de las
    opciones mostradas a través del número correspondiente. En caso de no
    ingresar una opción correcta, se le volverá a solicitar.

    :rtype: int
    """
    print("")
    print("Seleccione una acción")
    print("")
    print("      1. Buscar por número de registro")
    print("      2. Buscar por categoría")
    print("      3. Buscar por descripción")
    print("      4. Buscar por número de transacción")
    print("      5. Buscar por ingreso")
    print("      6. Buscar por egreso")
    print("      7. Buscar por observación")
    print("      8. Buscar por fecha")
    print("      0. Volver")
    print("")
    opcion = -1
    try:
        opcion = int(input("Ingrese una opción: "))
        while opcion < 0 or opcion > 8:
            print("")
            print("Opción incorrecta.")
            print("")
            accion = int(input("Ingrese una opción: "))
    except ValueError: 
        print("Opción incorrecta.")
        opcion = -1
    except:
        mant.log_error()
        input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
        print()
        opcion = -1
    return opcion


def menu_buscar():                                                                                  # MENÚ BUSCAR
    """Llama a la función donde se muestra las opciones y recibe, a través de
    ella, la opción ingresada por el usuario. Luego, según la opción ingresada,
    permite al usuario buscar movimientos de caja en la base de datos según los
    siguientes parámetros:
    - Buscar por ID de registro
    - Buscar por categoría *
    - Buscar por descripción *
    - Buscar por transacción
    - Buscar por ingreso
    - Buscar por egreso
    - Buscar por observación * 
    - Buscar por fecha (abre un sub-menú)

    *Búsqueda no exacta. Puede utilizarse comodín.
    """
    opcion = -1
    columna = ""
    valor = ""
    
    while opcion != 0:
        opcion = opcion_menu_buscar()
    
        if opcion == 1:     # Buscar por ID
            print("")
            columna = "id"
            
            valor = input("Indique número de registro: ")
            
            buscar_registro(columna, valor)
            print("")
    
        elif opcion == 2:   # Buscar por categoría
            print("")
            columna = "categoria"
            
            inp = input("Indique categoría o parte de ella: ")
            valor = f"%{inp}%"
            
            buscar_registro_like(columna, valor)
            print("")
    
        elif opcion == 3:   # Buscar por descripción
            print("")
            columna = "descripcion"
            
            inp = input("Indique descripción o parte de ella: ")
            valor = f"%{inp}%"

            buscar_registro_like(columna, valor)
            print("")
    
        elif opcion == 4:   # Buscar por transacción
            print("")
            columna = "transaccion"

            valor = input("Indique número de transacción: ")

            buscar_registro_like(columna, valor)
            print("")
    
        elif opcion == 5:   # Buscar por ingreso
            try:
                print("")
                columna = "ingreso"
                
                valor = float(input("Indique monto de ingreso: $ "))
                
                buscar_registro(columna, valor)
                print("")
            
            except ValueError:
                print("")
                print("         ERROR. El monto debe ser numérico.")
            except:
                mant.log_error()
                input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
                print()
    
        elif opcion == 6:   # Buscar por egreso
            try:
                print("")
                columna = "egreso"

                valor = float(input("Indique monto de egreso: $ "))
                
                buscar_registro(columna, valor)
                print("")
            
            except ValueError:
                print("")
                print("         ERROR. El monto debe ser numérico.")
            except:
                mant.log_error()
                input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
                print()
    
        elif opcion == 7:   # Buscar por observación
            print("")
            columna = "observacion"

            inp = input("Indique observación o parte de ella: ")
            valor = f"%{inp}%"
            
            buscar_registro_like(columna, valor)
            print("")
    
        elif opcion == 8:   # Buscar por fecha
            print("")
            menu_buscar_fecha()
    
        elif opcion == 0:   # Volver
            return


def buscar_registro(columna: str, valor: str | int | float | bool):
    """Recupera desde la tabla caja en la base de datos aquellos registros
    que contengan un valor específico en una columna específica y luego
    los muestra al usuario en una tabla impresa en la pantalla.

    :param columna: Columna donde se buscará el valor especificado
    :type columna: str

    :param valor: Valor que se buscará en la columna especificada
    :type valor: str or int or float or bool
    """
    valor = mant.reemplazar_comilla(valor)
    
    try:
        with sql.connect(mant.DATABASE) as conn:
            cursor = conn.cursor()
            instruccion = f"SELECT * FROM caja WHERE {columna} = '{valor}' ORDER BY id"
            cursor.execute(instruccion)
            datos = cursor.fetchall()

    except sql.OperationalError:
        print("         ERROR. Se ha encontrado un caracter no permitido en la busqueda.")
        return

    print("---------------------------------------------------------------------------------------------------------------------------------------------------------------")
    print("{:<9} {:<27} {:<27} {:<11} {:<15} {:<15} {:<30} {:<10} {:<6}".format('    ID   ','CATEGORÍA','DESCRIPCIÓN', 'TRANSACCIÓN', 'INGRESO', 'EGRESO','OBSERVACIONES', '  FECHA', 'USER'))
    print("---------------------------------------------------------------------------------------------------------------------------------------------------------------")

    for x in datos:
        i_d, cat, des, tra, ing, egr, obs, dia, mes, año, cer, use = x
        idu, nom, ape, tel, dom, user, pas, pri, act = mant.buscar_usuario_por_id(use)
        
        if ing == None:
            ing = ''
        
        if egr == None:
            egr = ''
        
        print("{:<9} {:<27} {:<27} {:<11} {:<15} {:<15} {:<30} {:<10} {:<6}".format(f"{i_d}".rjust(8, '0'), cat[:27], des[:27], f"{tra}"[:10], ing, egr, obs[:30], f'{dia}/{mes}/{año}', f'{user}'))

    print("---------------------------------------------------------------------------------------------------------------------------------------------------------------")
    print("")
    input("Presione la tecla enter para continuar... ")


def buscar_registro_like(columna: str, valor: str | int | float | bool):
    """Recupera desde la tabla caja en la base de datos aquellos registros
    que contengan un valor específico, o parte de él, en una columna 
    específica y luego los muestra al usuario en una tabla impresa en la pantalla.

    Esta función, a diferencia de la funcion buscar_registro, permite el uso de 
    comodines (%), realizar búsquedas no exactas y no distingue mayúsculas.

    :param columna: Columna donde se buscará el valor especificado
    :type columna: str

    :param valor: Valor que se buscará en la columna especificada
    :type valor: str or int or float or bool
    """
    valor = mant.reemplazar_comilla(valor)

    try:
        with sql.connect(mant.DATABASE) as conn:
            cursor = conn.cursor()
            instruccion = f"SELECT * FROM caja WHERE {columna} ILIKE '{valor}' ORDER BY id"
            cursor.execute(instruccion)
            datos = cursor.fetchall()

    except sql.OperationalError:
        print("         ERROR. Se ha encontrado un caracter no permitido en la busqueda.")
        return
    
    print("---------------------------------------------------------------------------------------------------------------------------------------------------------------")
    print("{:<9} {:<27} {:<27} {:<11} {:<15} {:<15} {:<30} {:<10} {:<6}".format('    ID   ','CATEGORÍA','DESCRIPCIÓN', 'TRANSACCIÓN', 'INGRESO', 'EGRESO','OBSERVACIONES', '  FECHA', 'USER'))
    print("---------------------------------------------------------------------------------------------------------------------------------------------------------------")
    
    for x in datos:
        i_d, cat, des, tra, ing, egr, obs, dia, mes, año, cer, use = x
        idu, nom, ape, tel, dom, user, pas, pri, act = mant.buscar_usuario_por_id(use)
    
        if ing == None:
            ing = ''
    
        if egr == None:
            egr = ''
    
        print("{:<9} {:<27} {:<27} {:<11} {:<15} {:<15} {:<30} {:<10} {:<6}".format(f"{i_d}".rjust(8, '0'), cat[:27], des[:27], f"{tra}"[:10], ing, egr, obs[:30], f'{dia}/{mes}/{año}', f'{user}'))

    print("---------------------------------------------------------------------------------------------------------------------------------------------------------------")
    print("")
    input("Presione la tecla enter para continuar... ")


def opcion_menu_buscar_fecha() -> int:                                                              # OPCIÓN MENÚ BUSCAR POR FECHA
    """Muestra al usuario un menú y luego le solicita ingresar una de las
    opciones mostradas a través del número correspondiente. En caso de no
    ingresar una opción correcta, se le volverá a solicitar.

    :rtype: int
    """
    print("")
    print("Seleccione una acción")
    print("")
    print("      1. Buscar por fecha exacta")
    print("      2. Buscar por mes")
    print("      3. Buscar por año")
    print("      0. Volver")
    print("")
    accion = -1
    try:
        accion = int(input("Ingrese una opción: "))
        while accion < 0 or accion > 3:
            print("")
            print("Opción incorrecta.")
            print("")
            accion = int(input("Ingrese una opción: "))
    except ValueError: 
        print("Opción incorrecta.")
        accion = -1
    except:
        mant.log_error()
        input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
        print()
        accion = -1
    return accion


def menu_buscar_fecha():                                                                            # MENÚ BUSCAR POR FECHA
    """Llama a la función donde se muestra las opciones de búsqueda por fecha y
    recibe, a través de ella, la opción ingresada por el usuario. Luego, según 
    la opción ingresada, permite al usuario buscar movimientos de caja en la 
    base de datos según los siguientes parámetros:
    - Buscar por fecha exacta
    - Buscar por mes y año
    - Buscar por año
    """
    opcion = -1
    dia = ""
    mes = ""
    año = ""
    
    while opcion != 0:
        opcion = opcion_menu_buscar_fecha()
    
        if opcion == 1:     # Buscar por fecha exacta
            print("")
    
            dia = input("Indique día: ")
            print("")
    
            mes = input("Indique mes: ")
            print("")
    
            año = input("Indique año: ")
            print("")
    
            print(f"Registros del día {dia.rjust(2, '0')}/{mes.rjust(2, '0')}/{año.rjust(3, '0').rjust(4, '2')}")
            print("")
    
            buscar_registro_fecha(dia.rjust(2, '0'), mes.rjust(2, '0'), año.rjust(3, '0').rjust(4, '2'))
    
        elif opcion == 2:   # Buscar por mes y año
            print("")

            mes = input("Indique mes: ")
            print("")

            año = input("Indique año: ")
            print("")

            print(f"Registros del mes {mes} de {año.rjust(3, '0').rjust(4, '2')}")
            print("")

            buscar_registro_mes(mes.rjust(2, '0'), año.rjust(3, '0').rjust(4, '2'))
            print("")

        elif opcion == 3:   # Buscar por año
            print("")

            año = input("Idique el año: ")
            print("")

            print(f"Registros del año {año.rjust(3, '0').rjust(4, '2')}")
            print("")

            buscar_registro_año(año.rjust(3, '0').rjust(4, '2'))

        elif opcion == 0:   # Volver
            return


def buscar_registro_fecha(dia: str, mes: str, año: str):
    """Recupera desde la tabla caja en la base de datos aquellos registros
    que hayan sido realizados en una fecha específica y luego los muestra 
    al usuario en una tabla impresa en la pantalla.

    :param dia: Día, número de dos dígitos en una cadena.
    :type dia: str

    :param mes: Mes, número de dos dígitos en una cadena.
    :type mes: str

    :param año: Año, número de cuatro dígitos en una cadena.
    :type año: str
    """
    with sql.connect(mant.DATABASE) as conn:
        cursor = conn.cursor()
        instruccion = f"SELECT * FROM caja WHERE dia = '{dia}' AND mes = '{mes}' AND año = '{año}' ORDER BY id"
        cursor.execute(instruccion)
        datos = cursor.fetchall()

    print("---------------------------------------------------------------------------------------------------------------------------------------------------------------")
    print("{:<9} {:<27} {:<27} {:<11} {:<15} {:<15} {:<30} {:<10} {:<6}".format('    ID   ','CATEGORÍA','DESCRIPCIÓN', 'TRANSACCIÓN', 'INGRESO', 'EGRESO','OBSERVACIONES', '  FECHA', 'USER'))
    print("---------------------------------------------------------------------------------------------------------------------------------------------------------------")

    for x in datos:
        i_d, cat, des, tra, ing, egr, obs, dia, mes, año, cer, use = x
        idu, nom, ape, tel, dom, user, pas, pri, act = mant.buscar_usuario_por_id(use)

        if ing == None:
            ing = ''

        if egr == None:
            egr = ''

        print("{:<9} {:<27} {:<27} {:<11} {:<15} {:<15} {:<30} {:<10} {:<6}".format(f"{i_d}".rjust(8, '0'), cat[:27], des[:27], f"{tra}"[:10], ing, egr, obs[:30], f'{dia}/{mes}/{año}', f'{user}'))

    print("---------------------------------------------------------------------------------------------------------------------------------------------------------------")
    print("")
    input("Presione la tecla enter para continuar... ")


def buscar_registro_mes(mes: str, año: str):
    """Recupera desde la tabla caja en la base de datos aquellos registros
    que hayan sido realizados en una mes específico y luego los muestra 
    al usuario en una tabla impresa en la pantalla.

    :param mes: Mes, número de dos dígitos en una cadena.
    :type mes: str

    :param año: Año, número de cuatro dígitos en una cadena.
    :type año: str
    """
    with sql.connect(mant.DATABASE) as conn:
        cursor = conn.cursor()
        instruccion = f"SELECT * FROM caja WHERE mes = '{mes}' AND año = '{año}' ORDER BY id"
        cursor.execute(instruccion)
        datos = cursor.fetchall()

    print("---------------------------------------------------------------------------------------------------------------------------------------------------------------")
    print("{:<9} {:<27} {:<27} {:<11} {:<15} {:<15} {:<30} {:<10} {:<6}".format('    ID   ','CATEGORÍA','DESCRIPCIÓN', 'TRANSACCIÓN', 'INGRESO', 'EGRESO','OBSERVACIONES', '  FECHA', 'USER'))
    print("---------------------------------------------------------------------------------------------------------------------------------------------------------------")

    for x in datos:
        i_d, cat, des, tra, ing, egr, obs, dia, mes, año, cer, use = x
        idu, nom, ape, tel, dom, user, pas, pri, act = mant.buscar_usuario_por_id(use)

        if ing == None:
            ing = ''

        if egr == None:
            egr = ''

        print("{:<9} {:<27} {:<27} {:<11} {:<15} {:<15} {:<30} {:<10} {:<6}".format(f"{i_d}".rjust(8, '0'), cat[:27], des[:27], f"{tra}"[:10], ing, egr, obs[:30], f'{dia}/{mes}/{año}', f'{user}'))

    print("---------------------------------------------------------------------------------------------------------------------------------------------------------------")
    print("")
    input("Presione la tecla enter para continuar... ")


def buscar_registro_año(año):
    """Recupera desde la tabla caja en la base de datos aquellos registros
    que hayan sido realizados en una año específico y luego los muestra 
    al usuario en una tabla impresa en la pantalla.

    :param año: Año, número de cuatro dígitos en una cadena.
    :type año: str
    """
    with sql.connect(mant.DATABASE) as conn:
        cursor = conn.cursor()
        instruccion = f"SELECT * FROM caja WHERE año = '{año}' ORDER BY id"
        cursor.execute(instruccion)
        datos = cursor.fetchall()

    print("---------------------------------------------------------------------------------------------------------------------------------------------------------------")
    print("{:<9} {:<27} {:<27} {:<11} {:<15} {:<15} {:<30} {:<10} {:<6}".format('    ID   ','CATEGORÍA','DESCRIPCIÓN', 'TRANSACCIÓN', 'INGRESO', 'EGRESO','OBSERVACIONES', '  FECHA', 'USER'))
    print("---------------------------------------------------------------------------------------------------------------------------------------------------------------")

    for x in datos:
        i_d, cat, des, tra, ing, egr, obs, dia, mes, año, cer, use = x
        idu, nom, ape, tel, dom, user, pas, pri, act = mant.buscar_usuario_por_id(use)

        if ing == None:
            ing = ''

        if egr == None:
            egr = ''

        print("{:<9} {:<27} {:<27} {:<11} {:<15} {:<15} {:<30} {:<10} {:<6}".format(f"{i_d}".rjust(8, '0'), cat[:27], des[:27], f"{tra}"[:10], ing, egr, obs[:30], f'{dia}/{mes}/{año}', f'{user}'))

    print("---------------------------------------------------------------------------------------------------------------------------------------------------------------")
    print("")
    input("Presione la tecla enter para continuar... ")


def opcion_menu_modif_registro() -> int:                                                            # OPCIÓN MENÚ MODIFICAR REGISTRO
    """Muestra al usuario un menú y luego le solicita ingresar una de las
    opciones mostradas a través del número correspondiente. En caso de no
    ingresar una opción correcta, se le volverá a solicitar.

    :rtype: int
    """
    print("")
    print("Seleccione una acción")
    print("")
    print("      1. Modificar descripción")
    print("      2. Modificar número de transacción")
    print("      3. Modificar ingreso")
    print("      4. Modificar egreso")
    print("      5. Modificar observación")
    print("      0. Volver")
    print("")
    print("  *** La categoría no puede modificarse. Se debe eliminar el registro y volver a registrarlo correctamente")
    print("")
    accion = -1
    try:
        accion = int(input("Ingrese una opción: "))
        while accion < 0 or accion > 5:
            print("")
            print("Opción incorrecta.")
            print("")
            accion = int(input("Ingrese una opción: "))
    except ValueError: 
        print("Opción incorrecta.")
        accion = -1
    except:
        mant.log_error()
        input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
        print()
        accion = -1
    return accion


def menu_modif_registro(id: int, idu: int):                                                         # MENÚ MODIFICAR REGISTRO
    """Llama a la función donde se muestra las opciones y recibe, a través de
    ella, la opción ingresada por el usuario. Luego, según la opción ingresada,
    permite al usuario editar un movimiento de caja específico. 
    El usuario puede elegir editar alguno de los siguientes campos:
    - Descripción
    - Transacción
    - Ingreso
    - Egreso
    - Observación

    Una vez que el usuario modifica un registro se agrega, en las observaciones,
    una leyenda que da aviso que el mismo fue modificado, indicando el usuario
    que hizo la modificación y se guarda una copia del registro original en la
    tabla historial_caja.
    En caso que el campo modificado sea la observación, se le agrega a éste unos
    signos al final y al comienzo para que ningún registro pueda modificarse sin
    dejar un aviso.
    """
    opcion = -1
    string = ""
    floating = float(0)
    i_d, nom, ape, tel, dom, use, pas, pri, act = mant.buscar_usuario_por_id(idu)

    while opcion != 0:
        opcion = opcion_menu_modif_registro()

        if opcion == 1:     # Modificar descripción
            print("")
            string = input("Ingrese la nueva descripción: ")
            print("")

            guardar_historial(id, idu)

            edit_registro(id, 'descripcion', string)
            edit_registro(id, 'observacion', f'* Descripción modificada por {use}')

            print("Registro modificado exitosamente: ")
            mostrar_registro(id)
            string = ""

        elif opcion == 2:   # Modificar transacción
            print("")
            string = input("Ingrese el nuevo número de transacción: ")
            print("")
            
            guardar_historial(id, idu)
            
            edit_registro(id, 'transaccion', string)
            edit_registro(id, 'observacion', f'* Transacción modificada por {use}')
            
            print("Registro modificado exitosamente.: ")
            mostrar_registro(id)
            string = ""
        
        elif opcion == 3:   # Modificar ingreso
            try:
                print("")
                floating = float(input("Ingrese el nuevo monto de ingreso: $ "))
                print("")
             
                guardar_historial(id, idu)
             
                edit_registro(id, 'ingreso', floating)
                edit_registro(id, 'observacion', f'* Ingreso modificado por {use}')
             
                print("Registro modificado exitosamente: ")
                mostrar_registro(id)
                floating = float(0)
            
            except ValueError:
                print("")
                print("         ERROR. El monto debe ser numérico.")
            except:
                mant.log_error()
                input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
                print()
        
        elif opcion == 4:   # Modificar egreso
            try:
                print("")
                floating = float(input("Ingrese el nuevo monto de egreso: $ "))
                print("")
        
                guardar_historial(id, idu)
        
                edit_registro(id, 'egreso', floating)
                edit_registro(id, 'observacion', f'* Egreso modificado por {use}')
        
                print("Registro modificado exitosamente: ")
                mostrar_registro(id)
                floating = float(0)
        
            except ValueError:
                print("")
                print("         ERROR. El monto debe ser numérico.")
            except:
                mant.log_error()
                input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
                print()
        
        elif opcion == 5:   # Modificar observación
            print("")
            string = input("Ingrese la nueva observación: ")
            print("")
        
            guardar_historial(id, idu)
        
            edit_registro(id, 'observacion', f'*/ {string} /*')
        
            print("Registro modificado exitosamente: ")
            mostrar_registro(id)
            string = ""
        

def modif_registro(idu: int):
    """Solicita al usuario un ID de registro de caja y, si el mismo no forma parte de una
    caja ya cerrada, muestra los datos del registro y luego un menú donde el usuario puede
    elegir que campo desea modificar. Por el contrario, si el movimiento pertenece a una 
    caja que se encuentra cerrada, no le permite realizar modificaciones.

    :param idu: ID de usuario
    :type idu: int
    """
    id = 0
    print("")
    
    try:
        id = int(input("Indique el número del registro que desea modificar: "))
        cerrada = es_cerrada(id)
    
        if cerrada == 0:
            print("")
            mostrar_registro(id)
    
            print("")
            menu_modif_registro(id, idu)
    
        elif cerrada == 1:
            print("")
            print("         ERROR. No es posible modificar registros de cajas cerradas")
            print("")
    
    except ValueError:
        print("")
        print("         ERROR. El número de registro debe ser numérico.")
    except:
        mant.log_error()
        input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
        print()


def edit_registro(id: int, columna: str, valor: str | int | float | bool):
    """Edita una columna específica de un registro específico de la tabla
    caja en la base de datos.

    :param id: ID del movimiento de caja.
    :type id: int

    :param columna: Columna donde se editará el valor especificado.
    :type columna: str

    :param valor: Valor que se registrará en la columna especificada.
    :type valor: str or int or float or bool
    """
    valor = mant.reemplazar_comilla(valor)

    with sql.connect(mant.DATABASE) as conn:
        cursor = conn.cursor()
        instruccion = f"UPDATE caja SET {columna} = '{valor}' WHERE id = '{id}'"
        cursor.execute(instruccion)


def guardar_historial(id: int, idu: int):
    """Recupera un registro específico de la tabla caja en la base de datos,
    luego lo copia y lo registra en la tabla historial_caja, junto con el ID
    del usuario que recibe la función, la fecha y la hora exacta en que se
    realiza la copia.

    :param id: ID del movimiento de caja
    :type id: int

    :param idu: ID de usuario
    :type idu: int
    """
    fyh = datetime.now().strftime('%d/%m/%Y %H:%M:%S')

    with sql.connect(mant.DATABASE) as conn:
        cursor = conn.cursor()
        instruccion = f"SELECT * FROM caja WHERE id = {id} ORDER BY id"
        cursor.execute(instruccion)
        datos = cursor.fetchone()

    i_d, cat, des, tra, ing, egr, obs, dia, mes, año, cer, use = datos

    des = mant.reemplazar_comilla(des)
    tra = mant.reemplazar_comilla(tra)
    obs = mant.reemplazar_comilla(obs)

    if ing == None and egr != None:
        parameters = str((i_d, cat, des, tra, egr, obs, idu, fyh))
        query = f"INSERT INTO historial_caja (id, categoria, descripcion, transaccion, egreso, observacion, id_user_m, fecha_y_hora_m) VALUES {parameters}"

    elif egr == None and ing != None:
        parameters = str((i_d, cat, des, tra, ing, obs, idu, fyh))
        query = f"INSERT INTO historial_caja (id, categoria, descripcion, transaccion, ingreso, observacion, id_user_m, fecha_y_hora_m) VALUES {parameters}"

    elif ing != None and egr != None:
        parameters = str((i_d, cat, des, tra, ing, egr, obs, idu, fyh))
        query = f"INSERT INTO historial_caja (id, categoria, descripcion, transaccion, ingreso, egreso, observacion, id_user_m, fecha_y_hora_m) VALUES {parameters}"

    mant.run_query(query)


def mostrar_registro(id: int):
    """Recupera un movimiento de caja específico de la base de datos
    y lo muestra en una tabla impresa en la pantalla.

    :param id: ID del movimiento de caja
    :type id: int
    """
    with sql.connect(mant.DATABASE) as conn:
        cursor = conn.cursor()
        instruccion = f"SELECT * FROM caja WHERE id = {id} ORDER BY id"
        cursor.execute(instruccion)
        datos = cursor.fetchall()

    print("--------------------------------------------------------------------------------------------------------------------------------------------------------------")
    print("{:<9} {:<27} {:<27} {:<11} {:<15} {:<15} {:<30} {:<10} {:<6}".format('    ID   ','CATEGORÍA','DESCRIPCIÓN', 'TRANSACCIÓN', 'INGRESO', 'EGRESO','OBSERVACIONES', '  FECHA', 'USER'))
    print("--------------------------------------------------------------------------------------------------------------------------------------------------------------")

    for x in datos:
        i_d, cat, des, tra, ing, egr, obs, dia, mes, año, cer, use = x

        if ing == None:
            ing = ''

        if egr == None:
            egr = ''

        idu, nom, ape, tel, dom, user, pas, pri, act = mant.buscar_usuario_por_id(use)

        print("{:<9} {:<27} {:<27} {:<11} {:<15} {:<15} {:<30} {:<10} {:<6}".format(f"{i_d}".rjust(8, '0'), cat[:27], des[:27], f"{tra}"[:10], ing, egr, obs[:30], f'{dia}/{mes}/{año}', f'{user}'))

    print("--------------------------------------------------------------------------------------------------------------------------------------------------------------")
    print("")


def eliminar_registro(idu: int):
    """Permite al usuario eliminar un movimiento de caja de la base de datos,
    siempre y cuando éste no pertenezca a una caja cerrada.

    Nivel de privilegios mínimo: 4

    :param idu: ID de usuario
    :type idu: int
    """
    id = 0
    msj = " "
    i_d, nom, ape, tel, dom, use, pas, pri, act = mant.buscar_usuario_por_id(idu)
    print("")
    
    if pri >= 4:
        try:
            id = int(input("Indique el número de registro que desea eliminar: "))
            cerrada = es_cerrada(id)
    
            if cerrada == 0: 
                print("")
                mostrar_registro(id)
                msj = ""
    
                while msj != "S" and msj != "N":
                    msj = input("¿Seguro que desea eliminar el registro? (S/N): ")
    
                    if msj == "S" or msj == "s" or msj == "SI" or msj == "si" or msj == "Si" or msj == "sI":
                        msj = "S"
                        guardar_historial(id, idu)
                        conn = sql.connect(mant.DATABASE)
                        cursor = conn.cursor()
                        instruccion = f"UPDATE historial_caja SET observacion = '[REGISTRO ELIMINADO]' WHERE id = '{id}'"
                        cursor.execute(instruccion)
                        conn.commit()
                        conn.close()
                        delete_row("id", id)
                        print("")
                        print("Registro eliminado exitosamente.")
                        print("")
                        return
                    
                    elif msj == "N" or msj == "n" or msj == "NO" or msj == "no" or msj == "No" or msj == "nO":
                        msj = "N"
                        print("")
                        print("No se han realizado cambios en el registro.")
                        print("")
                        return
                    else:
                        print("")
                        print("         ERROR. Debe indicar S para eliminar o N para cancelar.")
                        print("")
            
            elif cerrada == 1:
                print("")
                print("         ERROR. No es posible modificar registros de cajas cerradas")
                print("")
        
        except ValueError:
            print("")
            print("         ERROR. El dato solicitado debe ser de tipo numérico.")
            print("")
        except IndexError:
            print("")
            print("         ERROR. Indique un número de registro válido.")
            print("")
        except:
            mant.log_error()
            input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
            print("")
    
    else:
        print("         ERROR. No posee los privilegios necesarios para realizar esta operación. Comuníquese con un admnistrador.")
        print("")
        print("No se han realizado cambios en el registro.")
        print("")
        getpass("Presione enter para continuar...")
        print("")


def delete_row(columna: str, valor: str | int | float | bool):
    """Elimina un movimiento de caja específico de la base de datos.

    :param columna: Columna donde se buscará el valor especificado.
    :type columna: str

    :param valor: Valor que se buscará en la columna especificada.
    :type valor: str or int or float or bool
    """
    valor = mant.reemplazar_comilla(valor)
    
    with sql.connect(mant.DATABASE) as conn:
        cursor = conn.cursor()
        instruccion = f"DELETE FROM caja WHERE {columna} = '{valor}'"
        cursor.execute(instruccion)


def ver_estado_caja(idu: int):
    """Permite al usuario si en la caja actual hay sobrante o faltante de dinero
    o si se encuentra correcta. Para ello se le solicita el saldo actual de la
    caja y realiza el cálculo teniendo en cuenta el saldo inicial y los movimientos
    realizados desde el último cierre de caja.

    Asimismo, se imprime en pantalla una tabla que contiene todos estos movimientos
    para que el usuario pueda realizar una revisión en caso que la caja no de cero.

    :param idu: ID de usuario
    :type idu: int
    """
    loop = -1
    
    while loop == -1:
        try:
            loop = caja_actual = float(input('Indique el saldo de caja actual: $ '))
    
        except ValueError:
            print('         ERROR! El dato solicitado debe ser de tipo numérico.')
            loop = -1
    
    caja_inicial = obtener_saldo_inicial()
    ingresos = 0
    egresos = 0
    
    print("---------------------------------------------------------------------------------------------------------------------------------------------------------------")
    print("----------------------------------------------------- MOVIMIENTOS DE CAJA ACTUAL ------------------------------------------------------------------------------")
    print("---------------------------------------------------------------------------------------------------------------------------------------------------------------")
    print()
    
    try:
        with sql.connect(mant.DATABASE) as conn:
            cursor = conn.cursor()
            instruccion = f"SELECT * FROM caja WHERE cerrada = 0 ORDER BY id"
            cursor.execute(instruccion)
            datos = cursor.fetchall()
    
    except sql.OperationalError:
        print("         ERROR. Se ha encontrado un caracter no permitido en la busqueda.")
        return
    
    print("---------------------------------------------------------------------------------------------------------------------------------------------------------------")
    print("{:<9} {:<27} {:<27} {:<11} {:<15} {:<15} {:<30} {:<10} {:<6}".format('    ID   ','CATEGORÍA','DESCRIPCIÓN', 'TRANSACCIÓN', 'INGRESO', 'EGRESO','OBSERVACIONES', '  FECHA', 'USER'))
    print("---------------------------------------------------------------------------------------------------------------------------------------------------------------")
    
    for x in datos:
        i_d, cat, des, tra, ing, egr, obs, dia, mes, año, cer, use = x
        idu, nom, ape, tel, dom, user, pas, pri, act = mant.buscar_usuario_por_id(use)
    
        if ing == None:
            ing = ''
            egresos += egr
    
        if egr == None:
            egr = ''
            ingresos += ing
    
        print("{:<9} {:<27} {:<27} {:<11} {:<15} {:<15} {:<30} {:<10} {:<6}".format(f"{i_d}".rjust(8, '0'), cat[:27], des[:27], f"{tra}"[:10], ing, egr, obs[:30], f'{dia}/{mes}/{año}', f'{user}'))

    print("---------------------------------------------------------------------------------------------------------------------------------------------------------------")
    
    total = ingresos + caja_inicial - egresos - caja_actual
    print()
    
    print(f'Inicial:  $ {caja_inicial:.2f}')
    print(f'Ingresos: $ {ingresos:.2f}')
    print(f'Egresos:  $ {egresos:.2f}')
    print(f'Actual:   $ {caja_actual:.2f}')
    print('___________________________')

    if total < 0:
        print(f'Sobrante: $ {abs(total):.2f}')

    elif total == 0:
        print(f'Diferencia: $ {total:.2f}')

    else:
        print(f'Faltante: $ {abs(total):.2f}')
    print()


def opcion_menu_caja_mensual() -> int:                                                              # OPCIÓN MENÚ CAJA MENSUAL
    """Muestra al usuario un menú y luego le solicita ingresar una de las
    opciones mostradas a través del número correspondiente. En caso de no
    ingresar una opción correcta, se le volverá a solicitar.

    :rtype: int
    """
    print("")
    print("********** Acciones disponibles **********")
    print("")
    print("   1. Imprimir caja mensual detallada")
    print("   2. Imprimir caja mensual comprimida")
    print("   3. Imprimir cobros por cobrador")
    print("   0. Volver")
    print("")
    try:
        opcion = int(input("Ingrese una opción: "))
        while opcion < 0 or opcion > 3:
            print("")
            print("Opción incorrecta.")
            print("")
            opcion = int(input("Ingrese una opción: "))
    except ValueError: 
        print("Opción incorrecta.")
        opcion = -1
    except:
        mant.log_error()
        input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
        print()
        opcion = -1
    return opcion


def menu_caja_mensual():                                                                            # MENÚ CAJA MENSUAL
    """Llama a la función donde se muestra las opciones y recibe, a través de
    ella, la opción ingresada por el usuario. Luego, según la opción ingresada,
    permite al usuario realizar las siguientes acciones relacionadas con la 
    caja mensual:
    - Imprimir caja mensual detallada: Genera un reporte en PDF con los movimientos
    detallados de todo un mes específico.
    - Imprimir caja mensual comprimida: Genera un reporte en PDF con los movimientos
    de todo un mes específico sin detallar.
    - Imprimir cobros por cobrador: Genera un reporte en PDF con todos los cobros
    realizados en un mes específico clasificados por cobrador.    
    """
    opcion = -1
    
    while opcion != 0:
        opcion = opcion_menu_caja_mensual()
    
        if opcion == 1:     # Imprimir caja mensual detallada
            mes = 0
            print("")
    
            try:
                while mes < 1 or mes > 12:
                    mes = int(input("Ingrese el mes: "))
    
                    if mes < 1 or mes > 12:
                        print("         ERROR. Mes incorrecto.")
                        print("")
    
                año = int(input("Ingrese el año: "))
    
                print()
                print("Generando reporte... Por favor aguarde...")
                print()
    
                rep.report_caja_mensual_det(mes, año)
    
            except:
                mant.log_error()
                input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
                print()
    
        elif opcion == 2:   # Imprimir caja mensual comprimida
            mes = 0
            print("")
    
            try:
                while mes < 1 or mes > 12:
                    mes = int(input("Ingrese el mes: "))
    
                    if mes < 1 or mes > 12:
                        print("         ERROR. Mes incorrecto.")
                        print("")
    
                año = int(input("Ingrese el año: "))
    
                print()
                print("Generando reporte... Por favor aguarde...")
                print()
    
                rep.report_caja_mensual_comp(mes, año)
    
            except: 
                mant.log_error()
                input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
                print()
    
        elif opcion == 3:   # Imprimir cobros por cobrador
            mes = 0
            print("")
    
            try:
                while mes < 1 or mes > 12:
                    mes = int(input("Ingrese el mes: "))
    
                    if mes < 1 or mes > 12:
                        print("         ERROR. Mes incorrecto.")
                        print("")
    
                año = int(input("Ingrese el año: "))
    
                print()
                print("Generando reporte... Por favor aguarde...")
                print()
    
                rep.report_caja_mensual_por_cob(mes, año)
    
            except: 
                mant.log_error()
                input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
                print()
    
        elif opcion == 0:   # Volver
            return


def reg_cobros_federacion(idu: int):
    """Permite al usuario registrar un cobro de los panteones administrados para
    Federación Gremial del Comercio y la Industria. Los mismos no ingresan en la
    caja física, por lo que el sistema registra, inmediatamente despuúes del
    ingreso, un egreso en concepto de alivio de caja.
    """
    print("********** Registrar cobros de Federación **********")
    print("")
    
    categoria_ing = "Mantenimiento Federación"
    descripcion_ing = "Oficina Córdoba 2915"
    transaccion_ing = "FED"
    ingreso = 0
    
    try:
        while ingreso == 0:
            ingreso = float(input("Monto: $ "))
            print("")
    
    except ValueError:
        print("")
        print("         ERROR. El monto debe ser numérico. No se registró ningún movimiento.")
        print("")
        return
    except:
        mant.log_error()
        input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
        print()
        return
    
    observacion_ing = input("Observaciones: ")
    print("")
    
    dia = obtener_dia()
    mes = obtener_mes()
    año = obtener_año()
    
    parameters_ing = str((categoria_ing, descripcion_ing, transaccion_ing, ingreso, observacion_ing, dia, mes, año, idu))
    query_ing = f"INSERT INTO caja (categoria, descripcion, transaccion, ingreso, observacion, dia, mes, año, id_user) VALUES {parameters_ing}"
    
    mant.run_query(query_ing)
    
    ult_reg_list = ult_reg()
    print("Se registró: ", ult_reg_list[1], " - ", ult_reg_list[2], " - ","$", ult_reg_list[4], " - ", ult_reg_list[6], " - " "NÚMERO DE REGISTRO: ", f"{ult_reg_list[0]}".rjust(8, '0'))
    print("")
    
    categoria_egr = "Alivios de caja"
    descripcion_egr = "Cobros de Federación"
    transaccion_egr = "FED"
    egreso = ingreso
    observacion_egr = ""
    
    parameters_egr = (categoria_egr, descripcion_egr, transaccion_egr, egreso, observacion_egr, dia, mes, año, idu)
    query_egr = f"INSERT INTO caja (categoria, descripcion, transaccion, egreso, observacion, dia, mes, año, id_user) VALUES {parameters_egr}"
    
    mant.run_query(query_egr)
    
    ult_reg_list = ult_reg()
    print("Se registró: ", ult_reg_list[1], " - ", ult_reg_list[2], " - ","$", ult_reg_list[5], " - ", ult_reg_list[6], " - " "NÚMERO DE REGISTRO: ", f"{ult_reg_list[0]}".rjust(8, '0'))
    print("")
    
    return
    

def cierre_caja():
    """Permite al usuario realizar el cierre de caja. Para ello el usuario
    debe ingresar el saldo actual de la caja. 

    Una vez realizado, el sistema generará un reporte en formato PDF de los
    movimientos de caja y marcará cada uno de ellos como pertenecientes a
    una caja cerrada. También guardará en la base de datos el saldo y el 
    número actual de la caja (para que sea utilizado como saldo inicial para
    la próxima caja).

    En caso de producirse algún error que impida realizar el cierre se le
    avisará al usuario, con un cartel impreso en pantalla de color rojo con
    letras amarillas, que no se pudo realizar el cierre.
    """
    saldo_final = 0
    contador = obtener_contador()
    fecha = obtener_fecha()
    fyh = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    
    print("********** Cierre de caja **********")
    print("")
    print(f"Fecha: {fecha}")
    print()
    print(f"Número de cierre: {str(contador).rjust(6, '0')}")
    print("")
    
    loop = -1
    while loop == -1:
        try:
            loop = saldo_final = float(input("Por favor ingrese el saldo de caja: $ "))
            print()
    
        except ValueError:
            print("         ERROR. El dato solicitado debe ser de tipo numérico.")
            loop = -1
            return menu()
    
        except:
            mant.log_error()
            print(Fore.RED+Back.YELLOW+"""
            #################################################
            #################################################
            ##                                             ##
            ##--------------------ERROR--------------------##
            ##                                             ##
            ##       COMUNÍQUESE CON EL ADMINISTRADOR      ##
            ##                                             ##
            ##       NO SE REGISTRÓ EL CIERRE DE CAJA      ##
            ##                                             ##
            #################################################
            #################################################
    """+Back.BLACK+Fore.LIGHTYELLOW_EX)
            print()
            getpass("Presione enter para cerrar el módulo...")
            return
    
    try:
        print("")
        print(" ***** REALIZANDO ACCIONES DE CAJA. POR FAVOR NO CIERRE EL SISTEMA NI APAGUE EL EQUIPO *****")
        print("")

        ##### GENERANDO REPORTE #####
        rep.report_caja_diaria(saldo_final)
        print("Reporte generado [OK]")
        print("")

        ##### CERRANDO REGISTROS ####
        with sql.connect(mant.DATABASE) as conn:
            cursor = conn.cursor()
            instruccion = f"UPDATE caja SET cerrada = '1' WHERE cerrada = '0'"
            cursor.execute(instruccion)
        
        ##### GUARDANDO SALDO DE CAJA #####
        with sql.connect(mant.DATABASE) as conn:
            cursor = conn.cursor()
            parameters = str((saldo_final, fyh))
            instruccion = f"INSERT INTO saldo_caja (saldo, fecha_y_hora_cierre) VALUES {parameters}"
            cursor.execute(instruccion)

        print("Saldo de caja actualizado [OK]")

    except:
        mant.log_error()
        print()
        init()
        print(Fore.RED+Back.YELLOW+"""
#################################################
#################################################
##                                             ##
##--------------------ERROR--------------------##
##                                             ##
##       NO SE REGISTRÓ EL CIERRE DE CAJA      ##
##             VUELVA A INTENTARLO             ##
##                                             ##
#################################################
#################################################
"""+Back.BLACK+Fore.LIGHTYELLOW_EX)
