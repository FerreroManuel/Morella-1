import funciones_caja as caja
import funciones_rendiciones as rend
import funciones_mantenimiento as mant
import funciones_ventas as vent
import reporter as rep
import psycopg2 as sql
import psycopg2.errors
import os
from getpass import getpass

os.system(f'TITLE Morella v{mant.VERSION} - MF! Soluciones informáticas')
os.system('color 0d')   # Colores del módulo (Púrpura sobre negro)
os.system('mode con: cols=160 lines=9999')

def obtener_database():
    if not os.path.isfile("../databases/database.ini"):
        arch = open("../databases/database.ini", "w")
        arch.close()
    with open("../databases/database.ini", "r") as arch:
        db = arch.readline()
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


def opcion_menu_buscar():                                                                           # OPCIÓN MENÚ BUSCAR
    print("")
    print("********** Acciones disponibles **********")
    print("")
    print("   1. Buscar por nro. de operación")
    print("   2. Buscar por apellido y nombre")
    print("   3. Buscar por DNI")
    print("   4. Buscar por domicilio")
    print("   5. Buscar por código de nicho")
    print("   6. Buscar por cobrador")
    print("   7. Buscar morosos")
    print("   8. Buscar por datos COBOL")
    print("   0. Volver")
    print("")
    try:
        opcion = int(input("Ingrese una opción: "))
        while opcion < 0 or opcion > 8:
            print("")
            print("Opción incorrecta.")
            print("")
            opcion = int(input("Ingrese una opción: "))
    except ValueError: 
        print("Opción incorrecta.")
        opcion = -1
    except:
        mant.log_error()
        print("")
        input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
    return opcion


def menu_buscar():                                                                                  # MENÚ BUSCAR
    opcion = -1
    while opcion != 0:
        opcion = opcion_menu_buscar()
        if opcion == 1:     # Buscar por nro. op
            try:
                print("")
                nro_operacion = int(input("Indique nro. de operación: "))
                buscar_op_nro_operacion(nro_operacion, 0)
            except ValueError:
                print("")
                print("         ERROR. Nro de operación inválido")
                print("")
            except:
                mant.log_error()
                print("")
                input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
                print()
        elif opcion == 2:   # Buscar por nombre
            try:
                nombre = input("Ingrese apellido y nombre del asociado o parte de él: ")
                buscar_op_nombre_socio(nombre)
            except:
                mant.log_error()
                print("")
                input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
                print()
        elif opcion == 3:   # Buscar por DNI
            try:
                dni = int(input("Ingrese DNI (sin puntos): "))
                buscar_op_dni(dni)
            except ValueError:
                print("")
                print("         ERROR. DNI inválido. Recuerde que debe ingresarlo sin puntos.")
                print("")
            except:
                mant.log_error()
                print("")
                input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
                print()
        elif opcion == 4:   # Buscar por domicilio
            try:
                domicilio = input("Ingrese domicilio o parte de él: ")
                buscar_op_domicilio(domicilio)
            except:
                mant.log_error()
                print("")
                input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
                print()
        elif opcion == 5:   # Buscar por código de nicho
            try:
                cod_nicho = input("Ingrese el código de nicho: ")
                buscar_op_cod_nicho(cod_nicho, 0)
            except:
                mant.log_error()
                print("")
                input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
                print()
        elif opcion == 6:   # Buscar por ID de cobrador
            print("Indique el ID de cobrador: ")
            datos = vent.obtener_cobradores()
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
                        print("         ERROR. Debe indicar un nro. de panteón válido.")
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
                    loop = -1
            buscar_op_cob(cobrador)
        elif opcion == 7:   # Buscar morosos
            buscar_op_morosos()
        elif opcion == 8:   # Buscar por datos Cobol
            buscar_datos_cobol()
        elif opcion == 0:   # Volver
            return


def buscar_datos_cobol():
    opcion = -1
    while opcion != 0:
        print()
        print("********** Acciones disponibles **********")
        print("")
        print("   1. Buscar por nro. de operación de COBOL")
        print("   2. Buscar por apellido y nombre de COBOL (o alternativo)")
        print("   3. Buscar por domicilio de COBOL (o alternativo)")
        print("   0. Volver")
        print("")
        try:
            opcion = int(input("Ingrese una opción: "))
            print()
            while opcion < 0 or opcion > 3:
                print("")
                print("Opción incorrecta.")
                print("")
                opcion = int(input("Ingrese una opción: "))
                print()
        except ValueError: 
            print("Opción incorrecta.")
            print()
            opcion = -1
        except:
            mant.log_error()
            print("")
            input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
            print()
        if opcion == 1:
            try:
                op_cobol = int(input("Indique el número de operación de COBOL: "))
                print()
                buscar_op_cobol(op_cobol)
                print()
            except ValueError:
                print()
                print("         ERROR. El dato solicitado debe ser de tipo numérico.")
                print()
            except:
                mant.log_error()
                print()
                input("         ERROR. Comuníquese con el administrador... Presione enter para continuar...")
                print()
        elif opcion == 2:
            nom_alt = input("Indique nombre alternativo o parte de él: ")
            print()
            buscar_op_nom_alt(nom_alt)
            print()
        elif opcion == 3:
            dom_alt = input("Indique domicilio alternativo o parte de él: ")
            print()
            buscar_op_dom_alt(dom_alt)
            print()


def buscar_op_nro_operacion(nro_operacion, ret):
    conn = sql.connect(database)
    cursor = conn.cursor()
    instruccion = f"SELECT * FROM operaciones WHERE id = '{nro_operacion}'"
    cursor.execute(instruccion)
    datos = cursor.fetchall()
    conn.commit()
    conn.close
    if ret == 1:
        return datos[0]
    elif ret == 0:
        print("")
        print("-".rjust(155, '-'))
        print("{:<10} {:<12} {:<37} {:<37} {:<35} {:<10} {:<10}".format('N° SOCIO', 'COD.NICHO','APELLIDO Y NOMBRE', 'DOMICILIO', 'TELÉFONOS', 'COBRADOR','¿MOROSO?'))
        print("-".rjust(155, '-'))
        for x in datos:
            i_d, soc, nic, fac, cob, tar, rut, ult, u_a, fec, mor, c_f, u_r, paga, op_cob, nom_alt, dom_alt = x
            nro, nom, dni, te_1, te_2, mail, dom, loc, c_p, f_n, f_a, act = rend.obtener_datos_socio(soc)
            cob = caja.obtener_nom_cobrador(cob)
            if nom_alt != None:
                nom = f"[{nom_alt}]"
            if dom_alt != None:
                dom = f"[{dom_alt}]"
            if te_1 != None and te_2 != None:
                tel = f"{te_1} / {te_2}"
            elif te_1 != None and te_2 == None:
                tel = str(te_1)
            elif te_1 == None and te_2 != None:
                tel = str(te_2)
            elif te_1 == None and te_2 == None:
                tel = "N/D"
            if mor == 1:
                mor = 'SI'
            elif mor == 0:
                mor = 'NO'
            print("{:<10} {:<12} {:<37} {:<37} {:<35} {:<10} {:<10}".format(f'{soc}'.rjust(6, '0'), f'{nic}'.rjust(10, '0'), nom[0:37], dom[0:37], tel[0:35], cob,f'   {mor}'))
        print("-".rjust(155, '-'))
        print("")


def buscar_op_nro_socio(nro_socio):
    try:
        nro, nom, dni, te_1, te_2, mail, dom, loc, c_p, f_n, f_a, act = obtener_datos_socio(nro_socio)
        conn = sql.connect(database)
        cursor = conn.cursor()
        instruccion = f"SELECT * FROM operaciones WHERE socio = '{nro_socio}'"
        cursor.execute(instruccion)
        datos = cursor.fetchall()
        conn.commit()
        conn.close()
        print("")
        if te_1 != None and te_2 != None:
            tel = f"{te_1} / {te_2}"
        elif te_1 != None and te_2 == None:
            tel = str(te_1)
        elif te_1 == None and te_2 != None:
            tel = str(te_2)
        elif te_1 == None and te_2 == None:
            tel = "N/D"
        if mail == None:
            mail = "N/D"
        print(f"ASOCIADO: {f'{nro_socio}'.rjust(6, '0')} - {nom}. DNI: {dni}. DOMICILIO: {dom} - TELÉFONOS: {tel} - EMAIL: {mail}")
        print("")
        print("OPERACIONES:")
        print("-----------------------------------------------------------------------------------------------------------------------------------------------------------")
        print("{:<20} {:<20} {:<20} {:<10} {:<35} {:<35} {:<8}".format('N° OPERACIÓN', 'COD.NICHO', 'COBRADOR', '¿MOROSO?', 'NOMBRE ALTERNATIVO', 'DOMICILIO ALTERNATIVO', 'OP.COBOL'))
        print("-----------------------------------------------------------------------------------------------------------------------------------------------------------")
        for x in datos:
            i_d, soc, nic, fac, cob, tar, rut, ult, u_a, fec, mor, c_f, u_r, paga, op_cob, nom_alt, dom_alt = x
            cob = rend.obtener_nom_cobrador(cob)
            if mor == 1:
                mor = 'SI'
            elif mor == 0:
                mor = 'NO'
            if nom_alt == None:
                nom_alt = " "
            if dom_alt == None:
                dom_alt = " "
            if op_cob == None or op_cob == 0:
                op_cob = " "
            print("{:<20} {:<20} {:<20} {:<10} {:<35} {:<35} {:<8}".format(f'{i_d}'.rjust(7, '0'), f'{nic}'.rjust(10, '0'), cob, f'   {mor}', nom_alt, dom_alt, str(op_cob).rjust(8, ' ')))
        print("-----------------------------------------------------------------------------------------------------------------------------------------------------------")
        print("")
    except ValueError:
        print("         ERROR. Número de socio inválido")
        print()
    except TypeError:
        print("         ERROR. No existe un asociado con ese número.")
        print()
    except:
        mant.log_error()
        print("")
        input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
        print()


def buscar_op_nombre_socio(nombre):
    nombre = mant.reemplazar_comilla(nombre)
    if nombre == "":
        return
    try:
        conn = sql.connect(database)
        cursor = conn.cursor()
        instruccion = f"SELECT * FROM socios WHERE nombre ilike '%{nombre}%'"
        cursor.execute(instruccion)
        datos = cursor.fetchall()
        conn.commit()
        print("")
        print("***********************************************************************************************************************************************************")
        for i in datos:
            nro, nom, dni, te_1, te_2, mail, dom, loc, c_p, f_n, f_a, act = i
            buscar_op_nro_socio(nro)
            print("****************************************************************************************************************************************************************")
        input("Presione la tecla enter para continuar... ")
        conn.close()
    except sql.errors.SyntaxError:
        print("")
        print("         ERROR. Nombre inválido. No se pueden utilizar comillas simples (') en las busquedas")
        print()
        return
    except:
        mant.log_error()
        print("")
        input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
        print()
        return


def buscar_op_dni(dni):
    conn = sql.connect(database)
    cursor = conn.cursor()
    instruccion = f"SELECT * FROM socios WHERE dni = '{dni}'"
    cursor.execute(instruccion)
    datos = cursor.fetchall()
    conn.commit()
    conn.close()
    print("")
    print("***********************************************************************************************************************************************************")
    for i in datos:
        nro, nom, dni, te_1, te_2, mail, dom, loc, c_p, f_n, f_a, act = i
        buscar_op_nro_socio(nro)
        print("***********************************************************************************************************************************************************")
    print()


def buscar_op_domicilio(domicilio):
    domicilio = mant.reemplazar_comilla(domicilio)
    if domicilio == "":
        return
    try:
        conn = sql.connect(database)
        cursor = conn.cursor()
        instruccion = f"SELECT * FROM socios WHERE domicilio ilike '%{domicilio}%'"
        cursor.execute(instruccion)
        datos = cursor.fetchall()
        conn.commit()
        print("")
        print("***********************************************************************************************************************************************************")
        for i in datos:
            nro, nom, dni, te_1, te_2, mail, dom, loc, c_p, f_n, f_a, act = i
            buscar_op_nro_socio(nro)
            print("***********************************************************************************************************************************************************")
        input("Presione la tecla enter para continuar... ")
        conn.close()
    except sql.errors.SyntaxError:
        print("")
        print("         ERROR. Domicilio inválido. Recuerde que no se pueden utilizar comillas simples (') en las busquedas")
        print("")
        return
    except:
        mant.log_error()
        print("")
        input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
        print()
        return


def buscar_op_cod_nicho(cod_nicho, ret):
    cod_nicho = str(cod_nicho).upper()
    try:
        cod, pan, pis, fil, num, cat, ocu, fall = rend.obtener_datos_nicho(cod_nicho)
    except UnboundLocalError:
        print("         ERROR. Código de nicho inválido")
        print()
        return
    except sql.errors.SyntaxError:
        print("         ERROR. Código de nicho inválido")
        print()
        return
    except:
        mant.log_error()
        print("")
        input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
        print()
        return
    panteon = rend.obtener_panteon(pan)
    id_nic, categ, val_mant_bic, val_mant_nob = rend.obtener_categoria(cat)
    conn = sql.connect(database)
    cursor = conn.cursor()
    instruccion = f"SELECT * FROM operaciones WHERE nicho = '{cod_nicho}'"
    cursor.execute(instruccion)
    datos = cursor.fetchall()
    conn.commit()
    conn.close
    if ret == 1:
        return datos[0]
    print("")
    print(f"CÓDIGO DE NICHO: {f'{cod_nicho}'.rjust(10, '0')}. PANTEÓN: {panteon}. PISO: {pis}. FILA: {fil}. NICHO: {num}. CATEGORÍA: {categ}")
    print("")
    print(f"OPERACION: {str(datos[0][0]).rjust(7, '0')}")
    print("-".rjust(154, '-'))
    print("{:<10} {:<38} {:<38} {:<35} {:<20} {:<10}".format('N° SOCIO', 'APELLIDO Y NOMBRE', 'DOMICILIO', 'TELÉFONOS', 'COBRADOR', '¿MOROSO?'))
    print("-".rjust(154, '-'))
    for x in datos:
        i_d, soc, nic, fac, cob, tar, rut, ult, u_a, fec, mor, c_f, u_r, paga, op_cob, nom_alt, dom_alt = x
        cob = rend.obtener_nom_cobrador(cob)
        nro, nom, dni, te_1, te_2, mail, dom, loc, c_p, f_n, f_a, act = rend.obtener_datos_socio(soc)
        if nom_alt != None:
            nom = f"[{nom_alt}]"
        if dom_alt != None:
            dom = f"[{dom_alt}]"
        if te_1 != None and te_2 != None:
            tel = f"{te_1} / {te_2}"
        elif te_1 != None and te_2 == None:
            tel = str(te_1)
        elif te_1 == None and te_2 != None:
            tel = str(te_2)
        elif te_1 == None and te_2 == None:
            tel = "N/D"
        if mor == 1:
            mor = 'SI'
        elif mor == 0:
            mor = 'NO'
        print("{:<10} {:<38} {:<38} {:<35} {:<20} {:<10}".format(f'{soc}'.rjust(6, '0'), nom[0:38], dom[0:38], tel[0:35], cob, f'   {mor}'))
    print("-".rjust(154, '-'))
    print("")


def buscar_op_cob(cod_cobrador):
    cobrador = rend.obtener_nom_cobrador(cod_cobrador)
    conn = sql.connect(database)
    cursor = conn.cursor()
    instruccion = f"SELECT * FROM operaciones WHERE cobrador = '{cod_cobrador}'"
    cursor.execute(instruccion)
    datos = cursor.fetchall()
    conn.commit()
    conn.close
    print("")
    print(f"COBRADOR: {cod_cobrador} - {cobrador}")
    print("")
    print("OPERACIONES:")
    print("-".rjust(155, '-'))
    print("{:<10} {:<10} {:<12} {:<42} {:<42} {:<25} {:<10}".format('N° SOCIO', 'N° OPER.', 'COD.NICHO','APELLIDO Y NOMBRE', 'DOMICILIO', 'TELÉFONOS', '¿MOROSO?'))
    print("-".rjust(155, '-'))
    for x in datos:
        id_op, soc, nic, fac, cob, tar, rut, ult, u_a, fec, mor, c_f, u_r, paga, op_cob, nom_alt, dom_alt = x
        nro, nom, dni, te_1, te_2, mail, dom, loc, c_p, f_n, f_a, act = rend.obtener_datos_socio(soc)
        if nom_alt != None:
            nom = f"[{nom_alt}]"
        if dom_alt != None:
            dom = f"[{dom_alt}]"
        if nom_alt != None:
            nom = f"[{nom_alt}]"
        if dom_alt != None:
            dom = f"[{dom_alt}]"
        if te_1 != None and te_2 != None:
            tel = f"{te_1} / {te_2}"
        elif te_1 != None and te_2 == None:
            tel = str(te_1)
        elif te_1 == None and te_2 != None:
            tel = str(te_2)
        elif te_1 == None and te_2 == None:
            tel = "N/D"
        if mor == 1:
            mor = 'SI'
        elif mor == 0:
            mor = 'NO'
        print("{:<10} {:<10} {:<12} {:<42} {:<42} {:<25} {:<10}".format(f'{soc}'.rjust(6, '0'), f'{id_op}'.rjust(7, '0'), f'{nic}'.rjust(10, '0'), nom[0:42], dom[0:42], tel[0:25], f'   {mor}'))
    print("-".rjust(155, '-'))
    print("")


def buscar_op_nom_alt(nom_alt):
    try:
        conn = sql.connect(database)
        cursor = conn.cursor()
        instruccion = f"SELECT * FROM operaciones WHERE nombre_alt ilike '%{nom_alt}%'"
        cursor.execute(instruccion)
        datos = cursor.fetchall()
        conn.commit()
        conn.close()
        print("")
        print("***********************************************************************************************************************************************************")
        for x in datos:
            i_d, soc, nic, fac, cob, tar, rut, ult, u_a, fec, mor, c_f, u_r, paga, op_cob, nom_alt, dom_alt = x
            buscar_op_nro_socio(soc)
            print("***********************************************************************************************************************************************************")
        print()
        input("Presione la tecla enter para continuar... ")
    except sql.errors.SyntaxError:
        print("")
        print("         ERROR. Nombre inválido. No se pueden utilizar comillas simples (') en las busquedas")
        print()
        return
    except:
        mant.log_error()
        print("")
        input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
        print()
        return


def buscar_op_dom_alt(dom_alt):
    try:
        conn = sql.connect(database)
        cursor = conn.cursor()
        instruccion = f"SELECT * FROM operaciones WHERE domicilio_alt ilike '%{dom_alt}%'"
        cursor.execute(instruccion)
        datos = cursor.fetchall()
        conn.commit()
        conn.close()
        print("")
        print("***********************************************************************************************************************************************************")
        for x in datos:
            i_d, soc, nic, fac, cob, tar, rut, ult, u_a, fec, mor, c_f, u_r, paga, op_cob, nom_alt, dom_alt = x
            buscar_op_nro_socio(soc)
            print("***********************************************************************************************************************************************************")
        print()        
        input("Presione la tecla enter para continuar... ")
    except sql.errors.SyntaxError:
        print("")
        print("         ERROR. Nombre inválido. No se pueden utilizar comillas simples (') en las busquedas")
        print()
        return
    except:
        mant.log_error()
        print("")
        input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
        print()
        return


def buscar_op_cobol(op_cobol):
    conn = sql.connect(database)
    cursor = conn.cursor()
    instruccion = f"SELECT * FROM operaciones WHERE op_cobol = {op_cobol}"
    cursor.execute(instruccion)
    datos = cursor.fetchall()
    conn.commit()
    conn.close()
    print("")
    print("***********************************************************************************************************************************************************")
    for x in datos:
        i_d, soc, nic, fac, cob, tar, rut, ult, u_a, fec, mor, c_f, u_r, paga, op_cob, nom_alt, dom_alt = x
        buscar_op_nro_socio(soc)
        print("***********************************************************************************************************************************************************")
    print()        
    print()


def obtener_op_morosos():
    conn = sql.connect(database)
    cursor = conn.cursor()
    instruccion = f"SELECT * FROM operaciones WHERE moroso = '{1}'"
    cursor.execute(instruccion)
    datos = cursor.fetchall()
    conn.commit()
    conn.close
    return datos


def buscar_op_morosos():                    
    datos = obtener_op_morosos()
    print("OPERACIONES MOROSAS:")
    print("-".rjust(157, '-'))
    print("{:<8} {:<8} {:<10} {:<42} {:<42} {:<30} {:<12}".format('N° SOCIO', 'N° OPER.', 'COD.NICHO','APELLIDO Y NOMBRE', 'DOMICILIO', 'TELÉFONOS', 'ÚLTIMO PAGO'))
    print("-".rjust(157, '-'))
    for x in datos:
        id_op, soc, nic, fac, cob, tar, rut, ult, u_a, fec_u_p, mor, c_f, u_r, paga, op_cob, nom_alt, dom_alt = x
        nro, nom, dni, te_1, te_2, mail, dom, loc, c_p, f_n, f_a, act = rend.obtener_datos_socio(soc)
        if nom_alt != None:
            nom = f"[{nom_alt}]"
        if dom_alt != None:
            dom = f"[{dom_alt}]"
        if nom_alt != None:
            nom = f"[{nom_alt}]"
        if dom_alt != None:
            dom = f"[{dom_alt}]"
        if te_1 != None and te_2 != None:
            tel = f"{te_1} / {te_2}"
        elif te_1 != None and te_2 == None:
            tel = str(te_1)
        elif te_1 == None and te_2 != None:
            tel = str(te_2)
        elif te_1 == None and te_2 == None:
            tel = "N/D"
        if mor == 1:
            mor = 'SI'
        elif mor == 0:
            mor = 'NO'
        print("{:<8} {:<8} {:<10} {:<42} {:<42} {:<30} {:<12}".format(f'{soc}'.rjust(6, '0'), f'{id_op}'.rjust(7, '0'), f'{nic}'.rjust(10, '0'), nom[0:42], dom[0:42], tel[0:30], f'    {fec_u_p}'))
    print("-".rjust(157, '-'))
    print("")
   

def buscar_estado_cta(nro_socio):
    nro, nom, dni, te_1, te_2, mail, dom, loc, c_p, f_n, f_a, act = obtener_datos_socio(nro_socio)
    deuda = 0
    deuda_total = 0
    msj = ''
    operaciones = buscar_op_por_nro_socio(nro_socio)
    #solicitudes = buscar_sol_por_nro_socio(nro_socio)
    solicitudes = [] # <- BORRAR CUANDO ESTÉ FUNCIONANDO LA BUSQUEDA ^
    print("")
    if te_1 != None and te_2 != None:
        tel = f"{te_1} / {te_2}"
    elif te_1 != None and te_2 == None:
        tel = str(te_1)
    elif te_1 == None and te_2 != None:
        tel = str(te_2)
    elif te_1 == None and te_2 == None:
        tel = "N/D"
    if mail == None:
        mail = "N/D"
    print(f"ASOCIADO: {f'{nro_socio}'.rjust(6, '0')} - {nom}. DNI: {dni}. DOMICILIO: {dom} - TELÉFONOS: {tel} - EMAIL: {mail}")
    print("")
    if len(operaciones) != 0:
        print("-----------------------------------------------------------------------------------------------------------------------------------------------------------")
        print("OPERACIONES:")
        print("-----------------------------------------------------------------------------------------------------------------------------------------------------------")
        print("{:<13} {:<11} {:<20} {:<20} {:<10} {:<33} {:<33} {:<8}".format('N° OPERACIÓN', 'COD.NICHO', 'DEUDA', 'COBRADOR', '¿MOROSO?', 'NOMBRE ALT.', 'DOMICILIO ALT.', 'OP.COBOL'))
        print("-----------------------------------------------------------------------------------------------------------------------------------------------------------")
        for x in operaciones:
            i_d, soc, nic, fac, cob, tar, rut, ult, u_a, fec, mor, c_f, u_r, paga, op_cob, nom_alt, dom_alt = x
            deuda = float(deuda_por_op(i_d))
            cob = rend.obtener_nom_cobrador(cob)
            if mor:
                mor = 'SI'
            else:
                mor = 'NO'
            if not nom_alt:
                nom_alt = " "
            if not dom_alt:
                dom_alt = " "
            if not op_cob:
                op_cob = " "
            print("{:<13} {:<11} {:<20} {:<20} {:<10} {:<33} {:<33} {:<8}".format(f'{i_d}'.rjust(7, '0'), f'{nic}'.rjust(10, '0'), f'$ {deuda:.2f}', cob, f'   {mor}', nom_alt[0:33], dom_alt[0:33], str(op_cob).rjust(8, ' ')))
        print("")
    if len(solicitudes) != 0:
        print("-----------------------------------------------------------------------------------------------------------------------------------------------------------")
        print("SOLICITUDES PREVENIR:")
        print("-----------------------------------------------------------------------------------------------------------------------------------------------------------")
        print("{:<20} {:<20} {:<20} {:<10} {:<35} {:<35} {:<8}".format('N° SOLICITUD', 'DEUDA', 'COBRADOR', '¿MOROSO?', 'NOMBRE ALT.', 'DOMICILIO ALT.', 'OP.COBOL'))
        print("-----------------------------------------------------------------------------------------------------------------------------------------------------------")
    if len(operaciones) != 0 or len(solicitudes) != 0:
        deuda_total = deuda_por_socio(soc)
        print("-----------------------------------------------------------------------------------------------------------------------------------------------------------")
        print(f"TOTAL DEUDA ASOCIADO: $ {deuda_total:.2f}-----".rjust(155, '-'))
        print("")
    
    while msj == '':
        msj = input("¿Desea generar un reporte? (S/N) ")
        if msj == 'S' or msj == 's' or msj == 'Si' or msj == 'SI' or msj == 'sI' or msj == 'si':
            print("")
            print("Generando reporte...")
            print("")
            rep.report_estado_cta(nro_socio, nom, dni, fac, dom, te_1, te_2, mail, c_p, loc, act)
        elif msj == 'N' or msj == 'n' or msj == 'No' or msj == 'NO' or msj == 'nO' or msj == 'no':
            print("")
        else:
            print("")
            print("Debe ingresar S para confirmar o N para cancelar.")
            print("")
            msj = ''


def obtener_datos_socio(nro_socio):
    conn = sql.connect(database)
    cursor = conn.cursor()
    instruccion = f"SELECT * FROM socios WHERE nro_socio = '{nro_socio}'"
    cursor.execute(instruccion)
    datos = cursor.fetchone()
    conn.commit()
    conn.close
    return datos


def deuda_por_op(id_operacion):
    conn = sql.connect(database)
    cursor = conn.cursor()
    instruccion = f"SELECT * FROM recibos WHERE operacion = '{id_operacion}' AND pago = '0'"
    cursor.execute(instruccion)
    datos = cursor.fetchall()
    conn.commit()
    conn.close
    deuda = 0
    for d in datos:
        nro, ope, per, año, pag = d
        i_d, soc, nic, fac, cob, tar, rut, ult, u_a, fec, mor, c_f, u_r, paga, op_cob, nom_alt, dom_alt = rend.obtener_datos_op(ope)
        cod, pan, pis, fil, num, cat, ocu, fall = rend.obtener_datos_nicho(nic)
        i_d, cat, val_mant_bic, val_mant_nob = rend.obtener_categoria(cat)
        if fac == 'bicon':
            val = val_mant_bic
        elif fac == 'nob':
            val = val_mant_nob
        if per[0:3] == 'Doc':
            val = rend.obtener_valor_doc(ope)
        deuda += val
    return deuda + deuda_vieja_por_op(id_operacion)


def deuda_vieja_por_op(id_operacion):
    i_d, soc, nic, fac, cob, tar, rut, ult, u_a, fec, mor, c_f, u_r, paga, op_cob, nom_alt, dom_alt = rend.obtener_datos_op(id_operacion)
    cod, pan, pis, fil, num, cat, ocu, fall = rend.obtener_datos_nicho(nic)
    i_d, cat, val_mant_bic, val_mant_nob = rend.obtener_categoria(cat)
    if fac == 'bicon':
        val = val_mant_bic
    elif fac == 'nob':
        val = val_mant_nob
    if c_f < 0:
        return abs(c_f) * val
    else:
        return 0
    

def buscar_recibos_por_op(id_operacion):
        conn = sql.connect(database)
        cursor = conn.cursor()
        instruccion = f"SELECT * FROM recibos WHERE operacion = '{id_operacion}' AND pago = '0'"
        cursor.execute(instruccion)
        datos = cursor.fetchall()
        conn.commit()
        conn.close
        return datos


def deuda_por_socio(nro_socio):
    with sql.connect(database) as conn:
        cursor = conn.cursor()
        instruccion = f"SELECT * FROM operaciones WHERE socio = '{nro_socio}'"
        cursor.execute(instruccion)
        datos = cursor.fetchall()
    deuda = 0
    for d in datos:
            i_d, soc, nic, fac, cob, tar, rut, ult, u_a, fec, mor, c_f, u_r, paga, op_cob, nom_alt, dom_alt = d
            deuda += float(deuda_por_op(i_d))
    return deuda


def buscar_op_por_nro_socio(nro_socio):
    conn = sql.connect(database)
    cursor = conn.cursor()
    instruccion = f"SELECT * FROM operaciones WHERE socio = '{nro_socio}'"
    cursor.execute(instruccion)
    datos = cursor.fetchall()
    conn.commit()
    conn.close()
    return datos


def buscar_nicho_por_op(id_operacion):
    conn = sql.connect(database)
    cursor = conn.cursor()
    instruccion = f"SELECT * FROM operaciones WHERE id = '{id_operacion}'"
    cursor.execute(instruccion)
    datos = cursor.fetchone()
    conn.commit()
    conn.close()
    i_d, soc, nic, fac, cob, tar, rut, ult, año, fec, mor, c_f, u_r, paga, op_cob, nom_alt, dom_alt = datos
    return nic
    

def obtener_datos_op_por_nro_socio(nro_socio):
    conn = sql.connect(database)
    cursor = conn.cursor()
    instruccion = f"SELECT * FROM operaciones WHERE socio = '{nro_socio}'"
    cursor.execute(instruccion)
    datos = cursor.fetchall()
    conn.commit()
    conn.close()
    return datos


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


