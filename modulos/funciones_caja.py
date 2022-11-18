import funciones_mantenimiento as mant
import reporter as rep
import psycopg2 as sql
import os
from colorama import init, Fore, Back
from datetime import datetime
from getpass import getpass

os.system('TITLE Morella v1.2.0.2205 - MF! Soluciones informáticas')
os.system('color 0E')   # Colores del módulo (Amarillo sobre negro)
os.system('mode con: cols=160 lines=9999')

def obtener_database():
    arch = open("../databases/database.ini", "r")
    db = arch.readline()
    arch.close()
    return db
database = obtener_database()


def iniciar_sesion():
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
                    mant.edit_registro('usuarios', 'activo', 2, i_d)
                    print("Su usuario ha sido bloqueado por repetición de claves incorrectas. Comuníquese con un administrador.")
                    i_d = -1
                    nom, ape, tel, dom, use, pas, pri, act = "", "", "", "", "", "", "", ""
                    return i_d, nom, ape, tel, dom, use, pas, pri, act
                print("")
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
                        mant.edit_registro('usuarios', 'pass', str(pw_new), i_d)
                        print("Contraseña actualizada exitosamente.")
                        print()
                        return i_d, nom, ape, tel, dom, use, pw_new, pri, act
                    else:
                        pw = ""
                return i_d, nom, ape, tel, dom, use, pas, pri, act
        elif act == 2:
            print("")
            print("Su usuario se encuentra bloqueado. Comuníquese con un administrador.")
            i_d = -1
            nom, ape, tel, dom, use, pas, pri, act = "", "", "", "", "", "", "", ""
            return i_d, nom, ape, tel, dom, use, pas, pri, act
        else:
            print("")
            print("Usuario inactivo.")
            i_d = -1
            nom, ape, tel, dom, use, pas, pri, act = "", "", "", "", "", "", "", ""
            return i_d, nom, ape, tel, dom, use, pas, pri, act
    except TypeError:
        print("")
        print("Usuario inexistente.")
        i_d = -1
        nom, ape, tel, dom, use, pas, pri, act = "", "", "", "", "", "", "", ""
        return i_d, nom, ape, tel, dom, use, pas, pri, act
    except sql.OperationalError:
        print("")
        print("Usuario inexistente.")
        i_d = -1
        nom, ape, tel, dom, use, pas, pri, act = "", "", "", "", "", "", "", ""
        return i_d, nom, ape, tel, dom, use, pas, pri, act
    except:
        mant.log_error()
        print("")
        input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
        i_d = -1
        nom, ape, tel, dom, use, pas, pri, act = "", "", "", "", "", "", "", ""
        return i_d, nom, ape, tel, dom, use, pas, pri, act


def buscar_usuario_por_user(user):
    try:
        conn = sql.connect(database)
    except sql.OperationalError:
        mant.log_error()
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


def buscar_usuario_por_id(idu):
    conn = sql.connect(database)
    cursor = conn.cursor()
    instruccion = f"SELECT * FROM usuarios WHERE id = '{idu}'"
    cursor.execute(instruccion)
    datos = cursor.fetchone()
    conn.commit()
    conn.close()
    i_d, nom, ape, tel, dom, use, pas, pri, act = datos
    return i_d, nom, ape, tel, dom, use, pas, pri, act


def obtener_saldo_inicial():
    conn = sql.connect(database)
    cursor = conn.cursor()
    instruccion = f"SELECT saldo FROM saldo_caja ORDER BY nro_caja DESC LIMIT 1"
    cursor.execute(instruccion)
    datos = cursor.fetchone()
    conn.commit()
    conn.close()
    return datos[0]


def obtener_contador():
    conn = sql.connect(database)
    cursor = conn.cursor()
    instruccion = f"SELECT nro_caja FROM saldo_caja ORDER BY nro_caja DESC LIMIT 1"
    cursor.execute(instruccion)
    datos = cursor.fetchone()
    conn.commit()
    conn.close()
    return datos[0]+1


def obtener_cobradores():
    conn = sql.connect(database)
    cursor = conn.cursor()
    instruccion = f"SELECT * FROM cobradores ORDER BY id"
    cursor.execute(instruccion)
    datos = cursor.fetchall()
    conn.commit()
    conn.close()
    return datos


def iniciar_caja():
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
                conn = sql.connect(database)
                cursor = conn.cursor()
                instruccion = f"UPDATE saldo_caja SET saldo = {saldo_inicial} WHERE saldo = -1"
                cursor.execute(instruccion)
                conn.commit()
                conn.close()
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


def obtener_dia():
    dia = datetime.now().strftime('%d')
    return dia


def obtener_mes():
    mes = datetime.now().strftime('%m')
    return mes


def obtener_año():
    año = datetime.now().strftime('%Y')
    return año


def obtener_fecha():
    dia = obtener_dia()
    mes = obtener_mes()
    año = obtener_año()
    fecha = f"{dia}/{mes}/{año}"
    return fecha


def obtener_categ_ing():
    archivo = open("../databases/categ_ing.mf", 'r', encoding='Utf-8')
    categ_ing = []
    for i in archivo.readlines():
        categ_ing.append(i.rstrip())
    archivo.close()
    return categ_ing


# def obtener_categ_ing():
#     conn = sql.connect(database)
#     cursor = conn.cursor()
#     instruccion = f"SELECT categoria FROM categorias_ingresos ORDER BY id"
#     cursor.execute(instruccion)
#     datos = cursor.fetchall()
#     conn.commit()
#     conn.close()
#     return datos


def obtener_categ_egr():
    archivo = open("../databases/categ_egr.mf", 'r', encoding='Utf-8')
    categ_egr = []
    for i in archivo.readlines():
        categ_egr.append(i.rstrip())
    archivo.close()
    return categ_egr


# def obtener_categ_egr():
#     conn = sql.connect(database)
#     cursor = conn.cursor()
#     instruccion = f"SELECT categoria FROM categorias_egresos ORDER BY id"
#     cursor.execute(instruccion)
#     datos = cursor.fetchall()
#     conn.commit()
#     conn.close()
#     return datos


def obtener_cobrador():
    archivo = open("../databases/cobradores.mf", 'r', encoding='Utf-8')
    cobradores = []
    for i in archivo.readlines():
        cobradores.append(i.rstrip())
    archivo.close()
    return cobradores


def obtener_nom_cobrador(id_cobrador):
    conn = sql.connect(database)
    cursor = conn.cursor()
    instruccion = f"SELECT * FROM cobradores WHERE id = '{id_cobrador}'"
    cursor.execute(instruccion)
    datos = cursor.fetchall()
    conn.commit()
    conn.close()
    for x in datos:
        nco, cob= x
    return cob


def obtener_panteon():
    archivo = open("../databases/panteones.mf", 'r', encoding='Utf-8')
    panteones = []
    for i in archivo.readlines():
        panteones.append(i.rstrip())
    archivo.close()
    return panteones


def obtener_fecha_reg(id):
    conn = sql.connect(database)
    cursor = conn.cursor()
    instruccion = f"SELECT * FROM caja WHERE id = '{id}'"
    cursor.execute(instruccion)
    datos = cursor.fetchall()
    i_d, cat, des, tra, ing, egr, obs, dia, mes, año, cer, use = datos[0]
    conn.commit()
    conn.close()
    return dia, mes, año


def obtener_comisiones(rendicion):
    conn = sql.connect(database)
    cursor = conn.cursor()
    instrucción = f"SELECT * FROM comisiones WHERE rendicion = '{rendicion}'"
    cursor.execute(instrucción)
    datos = cursor.fetchall()
    conn.commit()
    conn.close()
    return datos


def eliminar_comisiones(rendicion):
    conn = sql.connect(database)
    cursor = conn.cursor()
    instrucción = f"DELETE FROM comisiones WHERE rendicion = '{rendicion}'"
    cursor.execute(instrucción)
    conn.commit()
    conn.close()


def es_cerrada(id):
    conn = sql.connect(database)
    cursor = conn.cursor()
    instruccion = f"SELECT * FROM caja WHERE id = '{id}'"
    cursor.execute(instruccion)
    datos = cursor.fetchall()
    i_d, cat, des, tra, ing, egr, obs, dia, mes, año, cer, use = datos[0]
    conn.commit()
    conn.close()
    return cer


def añadir_categ_ing(nueva_cat_ing):
    archivo = open("../databases/categ_ing.mf", 'a', encoding='Utf-8')
    archivo.write(f'\n{nueva_cat_ing}')
    archivo.close()


def añadir_categ_egr(nueva_cat_egr):
    archivo = open("../databases/categ_egr.mf", 'a', encoding='Utf-8')
    archivo.write(f'\n{nueva_cat_egr}')
    archivo.close()


def añadir_cobrador(nuevo_cobrador):
    archivo = open("../databases/cobradores.mf", 'a', encoding='Utf-8')
    archivo.write(f'\n{nuevo_cobrador}')
    archivo.close()


def añadir_panteon(nuevo_panteon):
    archivo = open("../databases/panteones.mf", 'a', encoding='Utf-8')
    archivo.write(f'\nMantenimiento {nuevo_panteon}')
    archivo.close()
    añadir_categ_ing(f'Mantenimiento {nuevo_panteon}')


def run_query(query):
    conn = sql.connect(database)
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()
    conn.close()


def id_ult_reg():
    conn = sql.connect(database)
    cursor = conn.cursor()
    cursor.execute(f"SELECT id FROM caja ORDER BY id DESC LIMIT 1")
    numreg = cursor.fetchall()
    conn.commit()
    conn.close()
    ultimo_reg = numreg
    return ultimo_reg


def ult_reg():
    conn = sql.connect(database)
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM caja ORDER BY id DESC LIMIT 1")
    ult_registro = cursor.fetchall()
    conn.commit()
    conn.close()
    ult_reg_list = list(ult_registro[0])
    return ult_reg_list


def total_ing_por_cob(cobrador, mes, año):
    categ = obtener_panteon()
    total = 0
    for i in categ:
        conn = sql.connect(database)
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM caja WHERE descripcion = '{cobrador}' AND categoria = '{i}' AND mes='{mes}' AND año='{año}' ORDER BY id")
        datos = cursor.fetchall()
        conn.close()
        subtotal = 0
        for x in datos:
            i_d, cat, des, tra, ing, egr, obs, dia, mes, año, cer, use = x
            if type(ing) == float:
                subtotal = subtotal + ing
        total = total + subtotal
    return total


def total_egr_por_cob(cobrador, mes, año):
    total = 0
    conn = sql.connect(database)
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM caja WHERE descripcion = '{cobrador}' AND categoria = 'A rendir' AND mes='{mes}' AND año='{año}' ORDER BY id")
    datos = cursor.fetchall()
    conn.close()
    total = 0
    for x in datos:
        i_d, cat, des, tra, ing, egr, obs, dia, mes, año, cer, use = x
        if type(egr) == float:
            total = total + egr
    return total


def opcion_menu():                                                                                  # OPCIÓN MENÚ PRINCIPAL
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


def menu(idu):                                                                                      # MENÚ PRINCIPAL
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


def menu_oficinas():                                                                                # MENÚ OFICINAS
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


def reg_gastos_of(idu):
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
            if "'" in descripcion:
                descripcion = descripcion.replace("'", "´")
            if "'" in transaccion:
                transaccion = transaccion.replace("'", "´")
            if "'" in observacion:
                observacion = observacion.replace("'", "´")
            parameters = str((categoria, descripcion, transaccion, egreso, observacion, dia, mes, año, idu))
            query = f"INSERT INTO caja (categoria, descripcion, transaccion, egreso, observacion, dia, mes, año, id_user) VALUES {parameters}"
            try:
                run_query(query)
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
            if "'" in descripcion:
                descripcion = descripcion.replace("'", "´")
            if "'" in transaccion:
                transaccion = transaccion.replace("'", "´")
            if "'" in observacion:
                observacion = observacion.replace("'", "´")
            parameters = str((categoria, descripcion, transaccion, egreso, observacion, dia, mes, año, idu))
            query = f"INSERT INTO caja (categoria, descripcion, transaccion, egreso, observacion, dia, mes, año, id_user) VALUES {parameters}"
            try:
                run_query(query)
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
            if "'" in descripcion:
                descripcion = descripcion.replace("'", "´")
            if "'" in transaccion:
                transaccion = transaccion.replace("'", "´")
            if "'" in observacion:
                observacion = observacion.replace("'", "´")
            parameters = str((categoria, descripcion, transaccion, egreso, observacion, dia, mes, año, idu))
            query = f"INSERT INTO caja (categoria, descripcion, transaccion, egreso, observacion, dia, mes, año, id_user) VALUES {parameters}"
            try:
                run_query(query)
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
            if "'" in descripcion:
                descripcion = descripcion.replace("'", "´")
            if "'" in transaccion:
                transaccion = transaccion.replace("'", "´")
            if "'" in observacion:
                observacion = observacion.replace("'", "´")
            parameters = str((categoria, descripcion, transaccion, egreso, observacion, dia, mes, año, idu))
            query = f"INSERT INTO caja (categoria, descripcion, transaccion, egreso, observacion, dia, mes, año, id_user) VALUES {parameters}"
            try:
                run_query(query)
            except:
                mant.log_error()
                input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
                print()
                return
            ult_reg_list = ult_reg()
            print("Se registró: ", ult_reg_list[1], " - ", ult_reg_list[2], " - ","$", ult_reg_list[5], " - ", ult_reg_list[6], " - " "NÚMERO DE REGISTRO: ", f"{ult_reg_list[0]}".rjust(8, '0'))
            return
    

def reg_pago_alquiler(idu):
    print("********** Registrar pago de alquiler **********")
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
    if "'" in descripcion:
        descripcion = descripcion.replace("'", "´")
    if "'" in transaccion:
        transaccion = transaccion.replace("'", "´")
    if "'" in observacion:
        observacion = observacion.replace("'", "´")
    parameters = str((categoria, descripcion, transaccion, egreso, observacion, dia, mes, año, idu))
    query = f"INSERT INTO caja (categoria, descripcion, transaccion, egreso, observacion, dia, mes, año, id_user) VALUES {parameters}"
    try:
        run_query(query)
    except:
        mant.log_error()
        input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
        print()
        return
    ult_reg_list = ult_reg()
    print("Se registró: ", ult_reg_list[1], " - ", ult_reg_list[2], " - ","$", ult_reg_list[5], " - ", ult_reg_list[6], " - " "NÚMERO DE REGISTRO: ", f"{ult_reg_list[0]}".rjust(8, '0'))
    return


def reg_pago_sueldo(idu):
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
    if "'" in descripcion:
        descripcion = descripcion.replace("'", "´")
    if "'" in transaccion:
        transaccion = transaccion.replace("'", "´")
    if "'" in observacion:
        observacion = observacion.replace("'", "´")
    parameters = str((categoria, descripcion, transaccion, egreso, observacion, dia, mes, año, idu))
    query = f"INSERT INTO caja (categoria, descripcion, transaccion, egreso, observacion, dia, mes, año, id_user) VALUES {parameters}"
    try:
        run_query(query)
    except:
        mant.log_error()
        input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
        print()
        return
    ult_reg_list = ult_reg()
    print("Se registró: ", ult_reg_list[1], " - ", ult_reg_list[2], " - ","$", ult_reg_list[5], " - ", ult_reg_list[6], " - " "NÚMERO DE REGISTRO: ", f"{ult_reg_list[0]}".rjust(8, '0'))
    return


def reg_pago_comision(idu):
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
        for i in datos:
            cob, ren, rec, imp, com = i
            total_com = total_com + com
        categoria = "Pago de comisiones"
        cobrador = obtener_nom_cobrador(cob)
        observacion = input("Observaciones: ")
        print("")
        dia = obtener_dia()
        mes = obtener_mes()
        año = obtener_año()
        if "'" in observacion:
            observacion = observacion.replace("'", "´")
        parameters = str((categoria, cobrador, rendicion, total_com, observacion, dia, mes, año, idu))
        query = f"INSERT INTO caja (categoria, descripcion, transaccion, egreso, observacion, dia, mes, año, id_user) VALUES {parameters}"
        run_query(query)
        ult_reg_list = ult_reg()
        print("Se registró: ", ult_reg_list[1], " - ", ult_reg_list[2], " - ","$", ult_reg_list[5], " - ", ult_reg_list[6], " - " "NÚMERO DE REGISTRO: ", f"{ult_reg_list[0]}".rjust(8, '0'))
        print("")
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


def reg_alivio(idu):
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
        des1 = input("Quien realiza el alvio: ")
        print("")
        des2 = input("A quien se lo entrega: ")
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
    if "'" in descripcion:
        descripcion = descripcion.replace("'", "´")
    if "'" in transaccion:
        transaccion = transaccion.replace("'", "´")
    if "'" in observacion:
        observacion = observacion.replace("'", "´")
    parameters = str((categoria, descripcion, transaccion, egreso, observacion, dia, mes, año, idu))
    query = f"INSERT INTO caja (categoria, descripcion, transaccion, egreso, observacion, dia, mes, año, id_user) VALUES {parameters}"
    run_query(query)
    ult_reg_list = ult_reg()
    print("Se registró: ", ult_reg_list[1], " - ", ult_reg_list[2], " - ","$", ult_reg_list[5], " - ", ult_reg_list[6], " - " "NÚMERO DE REGISTRO: ", f"{ult_reg_list[0]}".rjust(8, '0'))
    return


def reg_ingreso_extraordinario(idu):
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
    if "'" in descripcion:
        descripcion = descripcion.replace("'", "´")
    if "'" in transaccion:
        transaccion = transaccion.replace("'", "´")
    if "'" in observacion:
        observacion = observacion.replace("'", "´")
    parameters = str((categoria, descripcion, transaccion, ingreso, observacion, dia, mes, año, idu))
    query = f"INSERT INTO caja (categoria, descripcion, transaccion, ingreso, observacion, dia, mes, año, id_user) VALUES {parameters}"
    run_query(query)
    ult_reg_list = ult_reg()
    print("Se registró: ", ult_reg_list[1], " - ", ult_reg_list[2], " - ","$", ult_reg_list[4], " - ", ult_reg_list[6], " - " "NÚMERO DE REGISTRO: ", f"{ult_reg_list[0]}".rjust(8, '0'))
    return


def opcion_menu_rendiciones():                                                                      # OPCIÓN MENÚ RENDICIONES
    print("")
    print("********** Acciones disponibles **********")
    print("")
    print("   1. Registrar un monto a rendir")
    print("   2. Registrar pago de rendición adeudada")
    print("   0. Volver")
    print("")
    try:
        opcion = int(input("Ingrese una opción: "))
        while opcion < 0 or opcion > 2:
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


def menu_rendiciones(idu):                                                                          # MENÚ RENDICIONES
    opcion = -1
    while opcion != 0:
        opcion = opcion_menu_rendiciones()
        if opcion == 1:
            a_rendir(idu)
        elif opcion == 2:
            rend_adeudada(idu)


def a_rendir(idu):
    print("********** Registrar monto a rendir **********")
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
    if "'" in descripcion:
        descripcion = descripcion.replace("'", "´")
    if "'" in transaccion:
        transaccion = transaccion.replace("'", "´")
    if "'" in observacion:
        observacion = observacion.replace("'", "´")
    parameters = str((categoria, descripcion, transaccion, egreso, observacion, dia, mes, año, idu))
    query = f"INSERT INTO caja (categoria, descripcion, transaccion, egreso, observacion, dia, mes, año, id_user) VALUES {parameters}"
    try:
        run_query(query)
    except:
        mant.log_error()
        input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
        print()
        return
    ult_reg_list = ult_reg()
    print("Se registró: ", ult_reg_list[1], " - ", ult_reg_list[2], " - ","$", ult_reg_list[5], " - ", ult_reg_list[6], " - " "NÚMERO DE REGISTRO: ", f"{ult_reg_list[0]}".rjust(8, '0'))
    return


def rend_adeudada(idu):
    print("********** Registrar pago de rendición adeudada **********")
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
    if "'" in descripcion:
        descripcion = descripcion.replace("'", "´")
    if "'" in transaccion:
        transaccion = transaccion.replace("'", "´")
    if "'" in observacion:
        observacion = observacion.replace("'", "´")
    parameters = str((categoria, descripcion, transaccion, ingreso, observacion, dia, mes, año, idu))
    query = f"INSERT INTO caja (categoria, descripcion, transaccion, ingreso, observacion, dia, mes, año, id_user) VALUES {parameters}"
    try:
        run_query(query)
    except:
        mant.log_error()
        input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
        print()
        return
    ult_reg_list = ult_reg()
    print("Se registró: ", ult_reg_list[1], " - ", ult_reg_list[2], " - ","$", ult_reg_list[4], " - ", ult_reg_list[6], " - " "NÚMERO DE REGISTRO: ", f"{ult_reg_list[0]}".rjust(8, '0'))
    return


def opcion_menu_edit():                                                                             # OPCIÓN MENÚ EDITAR
    print("Seleccione una acción")
    print("")
    print("   1. Ver movimientos del día")
    print("   2. Buscar un registro")
    print("   3. Modificar un registro")
    print("   4. Eliminar un registro")
    print("   0. Volver")
    print("")
    accion = -1
    try:
        accion = int(input("Ingrese una opción: "))
        while accion < 0 or accion > 4:
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


def menu_edit(idu):                                                                                 # MENÚ EDITAR
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
        elif opcion == 0:   # Volver
            return
   

def ver_registros():
    dia = obtener_dia()
    mes = obtener_mes()
    año = obtener_año()
    conn = sql.connect(database)
    cursor = conn.cursor()
    instruccion = f"SELECT * FROM caja WHERE dia = '{dia}' AND mes = '{mes}' AND año = '{año}' ORDER BY id"
    cursor.execute(instruccion)
    datos = cursor.fetchall()
    conn.commit()
    print("---------------------------------------------------------------------------------------------------------------------------------------------------------------")
    print("{:<9} {:<27} {:<27} {:<11} {:<15} {:<15} {:<30} {:<10} {:<6}".format('    ID   ','CATEGORÍA', 'DESCRIPCIÓN', 'TRANSACCIÓN', 'INGRESO', 'EGRESO','OBSERVACIONES', '  FECHA', 'USER'))
    print("---------------------------------------------------------------------------------------------------------------------------------------------------------------")
    for x in datos:
        i_d, cat, des, tra, ing, egr, obs, dia, mes, año, cer, use = x
        idu, nom, ape, tel, dom, user, pas, pri, act = buscar_usuario_por_id(use)
        if ing == None:
            ing = ''
        if egr == None:
            egr = ''
        print("{:<9} {:<27} {:<27} {:<11} {:<15} {:<15} {:<30} {:<10} {:<6}".format(f"{i_d}".rjust(8, '0'), f"{cat[:27]}", f"{des[:27]}", f"{tra}"[:11], f"{ing}", f"{egr}", f"{obs[:30]}", f"{dia}/{mes}/{año}", f"{user}"))
    conn.close()
    print("---------------------------------------------------------------------------------------------------------------------------------------------------------------")
    print("")
    input("Presione la tecla enter para continuar... ")


def opcion_menu_buscar():                                                                           # OPCIÓN MENÚ BUSCAR
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
    opcion = -1
    par1 = ""
    par2 = ""
    while opcion != 0:
        opcion = opcion_menu_buscar()
        if opcion == 1:     # Buscar por ID
            print("")
            par1 = "id"
            par2= input("Indique número de registro: ")
            buscar_registro(par1, par2)
            print("")
        elif opcion == 2:   # Buscar por categoría
            print("")
            par1 = "categoria"
            inp = input("Indique categoría o parte de ella: ")
            par2 = f"%{inp}%"
            buscar_registro_like(par1, par2)
            print("")
        elif opcion == 3:   # Buscar por descripción
            print("")
            par1 = "descripcion"
            inp = input("Indique descripción o parte de ella: ")
            par2 = f"%{inp}%"
            print("")
            buscar_registro_like(par1, par2)
        elif opcion == 4:   # Buscar por transacción
            print("")
            par1 = "transaccion"
            par2 = input("Indique número de transacción: ")
            print("")
            buscar_registro_like(par1, par2)
        elif opcion == 5:   # Buscar por ingreso
            try:
                print("")
                par1 = "ingreso"
                par2 = float(input("Indique monto de ingreso: $ "))
                print("")
                buscar_registro(par1, par2)
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
                par1 = "egreso"
                par2 = float(input("Indique monto de egreso: $ "))
                print("")
                buscar_registro(par1, par2)
            except ValueError:
                print("")
                print("         ERROR. El monto debe ser numérico.")
            except:
                mant.log_error()
                input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
                print()
        elif opcion == 7:   # Buscar por observación
            print("")
            par1 = "observacion"
            inp = input("Indique observación o parte de ella: ")
            par2 = f"%{inp}%"
            print("")
            buscar_registro_like(par1, par2)
        elif opcion == 8:   # Buscar por fecha
            print("")
            menu_buscar_fecha()
        elif opcion == 0:   # Volver
            return


def buscar_registro(par1, par2):
    if type(par2) == str and "'" in par2:
        par2 = par2.replace("'", "´")
    try:
        conn = sql.connect(database)
        cursor = conn.cursor()
        instruccion = f"SELECT * FROM caja WHERE {par1} = '{par2}' ORDER BY id"
        cursor.execute(instruccion)
        datos = cursor.fetchall()
        conn.commit()
    except sql.OperationalError:
        print("         ERROR. Se ha encontrado un caracter no permitido en la busqueda.")
        return
    print("---------------------------------------------------------------------------------------------------------------------------------------------------------------")
    print("{:<9} {:<27} {:<27} {:<11} {:<15} {:<15} {:<30} {:<10} {:<6}".format('    ID   ','CATEGORÍA','DESCRIPCIÓN', 'TRANSACCIÓN', 'INGRESO', 'EGRESO','OBSERVACIONES', '  FECHA', 'USER'))
    print("---------------------------------------------------------------------------------------------------------------------------------------------------------------")
    for x in datos:
        i_d, cat, des, tra, ing, egr, obs, dia, mes, año, cer, use = x
        idu, nom, ape, tel, dom, user, pas, pri, act = buscar_usuario_por_id(use)
        if ing == None:
            ing = ''
        if egr == None:
            egr = ''
        print("{:<9} {:<27} {:<27} {:<11} {:<15} {:<15} {:<30} {:<10} {:<6}".format(f"{i_d}".rjust(8, '0'), cat[:27], des[:27], f"{tra}"[:10], ing, egr, obs[:30], f'{dia}/{mes}/{año}', f'{user}'))
    conn.close()
    print("---------------------------------------------------------------------------------------------------------------------------------------------------------------")
    print("")
    input("Presione la tecla enter para continuar... ")


def buscar_registro_like(par1, par2):
    if type(par2) == str and "'" in par2:
        par2 = par2.replace("'", "´")
    try:
        conn = sql.connect(database)
        cursor = conn.cursor()
        instruccion = f"SELECT * FROM caja WHERE {par1} ILIKE '{par2}' ORDER BY id"
        cursor.execute(instruccion)
        datos = cursor.fetchall()
        conn.commit()
    except sql.OperationalError:
        print("         ERROR. Se ha encontrado un caracter no permitido en la busqueda.")
        return
    print("---------------------------------------------------------------------------------------------------------------------------------------------------------------")
    print("{:<9} {:<27} {:<27} {:<11} {:<15} {:<15} {:<30} {:<10} {:<6}".format('    ID   ','CATEGORÍA','DESCRIPCIÓN', 'TRANSACCIÓN', 'INGRESO', 'EGRESO','OBSERVACIONES', '  FECHA', 'USER'))
    print("---------------------------------------------------------------------------------------------------------------------------------------------------------------")
    for x in datos:
        i_d, cat, des, tra, ing, egr, obs, dia, mes, año, cer, use = x
        idu, nom, ape, tel, dom, user, pas, pri, act = buscar_usuario_por_id(use)
        if ing == None:
            ing = ''
        if egr == None:
            egr = ''
        print("{:<9} {:<27} {:<27} {:<11} {:<15} {:<15} {:<30} {:<10} {:<6}".format(f"{i_d}".rjust(8, '0'), cat[:27], des[:27], f"{tra}"[:10], ing, egr, obs[:30], f'{dia}/{mes}/{año}', f'{user}'))
    conn.close()
    print("---------------------------------------------------------------------------------------------------------------------------------------------------------------")
    print("")
    input("Presione la tecla enter para continuar... ")


def opcion_menu_buscar_fecha():                                                                     # OPCIÓN MENÚ BUSCAR POR FECHA
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


def buscar_registro_fecha(dia, mes, año):
    conn = sql.connect(database)
    cursor = conn.cursor()
    instruccion = f"SELECT * FROM caja WHERE dia = '{dia}' AND mes = '{mes}' AND año = '{año}' ORDER BY id"
    cursor.execute(instruccion)
    datos = cursor.fetchall()
    conn.commit()
    print("---------------------------------------------------------------------------------------------------------------------------------------------------------------")
    print("{:<9} {:<27} {:<27} {:<11} {:<15} {:<15} {:<30} {:<10} {:<6}".format('    ID   ','CATEGORÍA','DESCRIPCIÓN', 'TRANSACCIÓN', 'INGRESO', 'EGRESO','OBSERVACIONES', '  FECHA', 'USER'))
    print("---------------------------------------------------------------------------------------------------------------------------------------------------------------")
    for x in datos:
        i_d, cat, des, tra, ing, egr, obs, dia, mes, año, cer, use = x
        idu, nom, ape, tel, dom, user, pas, pri, act = buscar_usuario_por_id(use)
        if ing == None:
            ing = ''
        if egr == None:
            egr = ''
        print("{:<9} {:<27} {:<27} {:<11} {:<15} {:<15} {:<30} {:<10} {:<6}".format(f"{i_d}".rjust(8, '0'), cat[:27], des[:27], f"{tra}"[:10], ing, egr, obs[:30], f'{dia}/{mes}/{año}', f'{user}'))
    conn.close()
    print("---------------------------------------------------------------------------------------------------------------------------------------------------------------")
    print("")
    input("Presione la tecla enter para continuar... ")


def buscar_registro_mes(mes, año):
    conn = sql.connect(database)
    cursor = conn.cursor()
    instruccion = f"SELECT * FROM caja WHERE mes = '{mes}' AND año = '{año}' ORDER BY id"
    cursor.execute(instruccion)
    datos = cursor.fetchall()
    conn.commit()
    print("---------------------------------------------------------------------------------------------------------------------------------------------------------------")
    print("{:<9} {:<27} {:<27} {:<11} {:<15} {:<15} {:<30} {:<10} {:<6}".format('    ID   ','CATEGORÍA','DESCRIPCIÓN', 'TRANSACCIÓN', 'INGRESO', 'EGRESO','OBSERVACIONES', '  FECHA', 'USER'))
    print("---------------------------------------------------------------------------------------------------------------------------------------------------------------")
    for x in datos:
        i_d, cat, des, tra, ing, egr, obs, dia, mes, año, cer, use = x
        idu, nom, ape, tel, dom, user, pas, pri, act = buscar_usuario_por_id(use)
        if ing == None:
            ing = ''
        if egr == None:
            egr = ''
        print("{:<9} {:<27} {:<27} {:<11} {:<15} {:<15} {:<30} {:<10} {:<6}".format(f"{i_d}".rjust(8, '0'), cat[:27], des[:27], f"{tra}"[:10], ing, egr, obs[:30], f'{dia}/{mes}/{año}', f'{user}'))
    conn.close()
    print("---------------------------------------------------------------------------------------------------------------------------------------------------------------")
    print("")
    input("Presione la tecla enter para continuar... ")


def buscar_registro_año(año):
    conn = sql.connect(database)
    cursor = conn.cursor()
    instruccion = f"SELECT * FROM caja WHERE año = '{año}' ORDER BY id"
    cursor.execute(instruccion)
    datos = cursor.fetchall()
    conn.commit()
    print("---------------------------------------------------------------------------------------------------------------------------------------------------------------")
    print("{:<9} {:<27} {:<27} {:<11} {:<15} {:<15} {:<30} {:<10} {:<6}".format('    ID   ','CATEGORÍA','DESCRIPCIÓN', 'TRANSACCIÓN', 'INGRESO', 'EGRESO','OBSERVACIONES', '  FECHA', 'USER'))
    print("---------------------------------------------------------------------------------------------------------------------------------------------------------------")
    for x in datos:
        i_d, cat, des, tra, ing, egr, obs, dia, mes, año, cer, use = x
        idu, nom, ape, tel, dom, user, pas, pri, act = buscar_usuario_por_id(use)
        if ing == None:
            ing = ''
        if egr == None:
            egr = ''
        print("{:<9} {:<27} {:<27} {:<11} {:<15} {:<15} {:<30} {:<10} {:<6}".format(f"{i_d}".rjust(8, '0'), cat[:27], des[:27], f"{tra}"[:10], ing, egr, obs[:30], f'{dia}/{mes}/{año}', f'{user}'))
    conn.close()
    print("---------------------------------------------------------------------------------------------------------------------------------------------------------------")
    print("")
    input("Presione la tecla enter para continuar... ")


def opcion_menu_modif_registro():                                                                   # OPCIÓN MENÚ MODIFICAR REGISTRO
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


def menu_modif_registro(id, idu):                                                                   # MENÚ MODIFICAR REGISTRO
    opcion = -1
    id = id
    string = ""
    floating = float(0)
    i_d, nom, ape, tel, dom, use, pas, pri, act = buscar_usuario_por_id(idu)
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
        

def modif_registro(idu):
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


def edit_registro(id, parametro1, parametro2):
    if type(parametro2) == str and "'" in parametro2:
        parametro2 = parametro2.replace("'", "´")
    conn = sql.connect(database)
    cursor = conn.cursor()
    instruccion = f"UPDATE caja SET {parametro1} = '{parametro2}' WHERE id = '{id}'"
    cursor.execute(instruccion)
    conn.commit()
    conn.close()


def guardar_historial(id, idu):
    conn = sql.connect(database)
    cursor = conn.cursor()
    instruccion = f"SELECT * FROM caja WHERE id = {id} ORDER BY id"
    cursor.execute(instruccion)
    datos = cursor.fetchone()
    conn.commit()
    conn.close()
    i_d, cat, des, tra, ing, egr, obs, dia, mes, año, cer, use = datos
    fyh = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    if "'" in des:
        des = des.replace("'", "´")
    if "'" in tra:
        tra = tra.replace("'", "´")
    if "'" in obs:
        obs = obs.replace("'", "´")
    if ing == None and egr != None:
        parameters = str((i_d, cat, des, tra, egr, obs, idu, fyh))
        query = f"INSERT INTO historial_caja (id, categoria, descripcion, transaccion, egreso, observacion, id_user_m, fecha_y_hora_m) VALUES {parameters}"
    elif egr == None and ing != None:
        parameters = str((i_d, cat, des, tra, ing, obs, idu, fyh))
        query = f"INSERT INTO historial_caja (id, categoria, descripcion, transaccion, ingreso, observacion, id_user_m, fecha_y_hora_m) VALUES {parameters}"
    elif ing != None and egr != None:
        parameters = str((i_d, cat, des, tra, ing, egr, obs, idu, fyh))
        query = f"INSERT INTO historial_caja (id, categoria, descripcion, transaccion, ingreso, egreso, observacion, id_user_m, fecha_y_hora_m) VALUES {parameters}"
    run_query(query)


def mostrar_registro(id):
    conn = sql.connect(database)
    cursor = conn.cursor()
    instruccion = f"SELECT * FROM caja WHERE id = {id} ORDER BY id"
    cursor.execute(instruccion)
    datos = cursor.fetchall()
    conn.commit()
    print("--------------------------------------------------------------------------------------------------------------------------------------------------------------")
    print("{:<9} {:<27} {:<27} {:<11} {:<15} {:<15} {:<30} {:<10} {:<6}".format('    ID   ','CATEGORÍA','DESCRIPCIÓN', 'TRANSACCIÓN', 'INGRESO', 'EGRESO','OBSERVACIONES', '  FECHA', 'USER'))
    print("--------------------------------------------------------------------------------------------------------------------------------------------------------------")
    for x in datos:
        i_d, cat, des, tra, ing, egr, obs, dia, mes, año, cer, use = x
        if ing == None:
            ing = ''
        if egr == None:
            egr = ''
        idu, nom, ape, tel, dom, user, pas, pri, act = buscar_usuario_por_id(use)
        print("{:<9} {:<27} {:<27} {:<11} {:<15} {:<15} {:<30} {:<10} {:<6}".format(f"{i_d}".rjust(8, '0'), cat[:27], des[:27], f"{tra}"[:10], ing, egr, obs[:30], f'{dia}/{mes}/{año}', f'{user}'))
    conn.close()
    print("--------------------------------------------------------------------------------------------------------------------------------------------------------------")
    print("")


def eliminar_registro(idu):
    id = 0
    msj = " "
    i_d, nom, ape, tel, dom, use, pas, pri, act = buscar_usuario_por_id(idu)
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
                        conn = sql.connect(database)
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


def delete_row(parametro1, parametro2):
    if type(parametro2) == str and "'" in parametro2:
        parametro2 = parametro2.replace("'", "´")
    conn = sql.connect(database)
    cursor = conn.cursor()
    instruccion = f"DELETE FROM caja WHERE {parametro1} = '{parametro2}'"
    cursor.execute(instruccion)
    conn.commit()
    conn.close()


def opcion_menu_caja_mensual():                                                                     # OPCIÓN MENÚ CAJA MENSUAL
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


def reg_cobros_federacion(idu):
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
    run_query(query_ing)
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
    run_query(query_egr)
    ult_reg_list = ult_reg()
    print("Se registró: ", ult_reg_list[1], " - ", ult_reg_list[2], " - ","$", ult_reg_list[5], " - ", ult_reg_list[6], " - " "NÚMERO DE REGISTRO: ", f"{ult_reg_list[0]}".rjust(8, '0'))
    print("")
    return
    

def cierre_caja():
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
        conn = sql.connect(database)
        cursor = conn.cursor()
        instruccion = f"UPDATE caja SET cerrada = '1' WHERE cerrada = '0'"
        cursor.execute(instruccion)
        conn.commit()
        conn.close()
        
        ##### GUARDANDO SALDO DE CAJA #####
        conn = sql.connect(database)
        cursor = conn.cursor()
        parameters = str((saldo_final, fyh))
        instruccion = f"INSERT INTO saldo_caja (saldo, fecha_y_hora_cierre) VALUES {parameters}"
        cursor.execute(instruccion)
        conn.commit()
        conn.close()

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
        opcion = -1
        return menu()


def cerrar_consola():           ################# ¿¿¿¿¿¿¿¿¿¿¿¿????????????
    print("")
    print("")
    print("")
    print("")
    print("")
    print("")
    print("")
    print("")
    print("")
    print("")
    print("")
    print("")
    print("")
    print("")
    print("")
    print("")
    print("")
    print("")
    print("")
    print("")
    print("")
    print("")
    print("")
    print("")
    print("")
    print("")
    print("")
    print("")
    print("")
    print("")
    print("")
    print("")
    print("")
    print("")
    print("")
    print("")
    print("")
    print("")
    print("")
    print(" -----------------------------")
    print("| Ya puede cerrar la consola. |")
    print(" -----------------------------")
    print("")
    print("")
    print("")
    print("")

