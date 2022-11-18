print("\n\nCargando las funciones necesarias para ejectuar el módulo. Por favor aguarde... \n\n")
import funciones_mantenimiento as mant
import reporter as rep
import psycopg2 as sql
import psycopg2.errors
from getpass import getpass
import os

os.system(f'TITLE Morella v{mant.VERSION} - MF! Soluciones informáticas')
os.system('color 80')   # Colores del módulo (Negro sobre gris)

def obtener_database():
    arch = open("../databases/database.ini", "r")
    db = arch.readline()
    arch.close()
    return db
database = obtener_database()

#######################################################################################################################################################
###################################################################### FUNCIONES ######################################################################
#######################################################################################################################################################

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


def opcion_menu():                                                                                  # OPCIÓN MENÚ PRINCIPAL
    print("")
    print("********** Acciones disponibles **********")
    print("")
    print("   1. Listado de morosos")
    print("   2. Listado de socios (excel)")
    print("   3. Listado de modificaciones de caja (excel)")
    print("   4. Listado de ingresos por débito automático (excel)")
    print("   5. Listado de panteones")
    print("   6. Listado de cobradores")
    print("   0. Salir")
    print("")
    try:
        opcion = int(input("Ingrese una opción: "))
        while opcion < 0 or opcion > 6:
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
        print()
        opcion = -1
    return opcion


def menu(idu):                                                                                      # MENÚ PRINCIPAL
    opcion = -1
    while opcion != 0:
        opcion = opcion_menu()
        if opcion == 1:     # Listado de morosos
            morosos(idu)
        elif opcion == 2:   # Listado de socios (excel)
            socios(idu)
        elif opcion == 3:   # Listado de modificaciones de caja (excel)
            modif_caja(idu)
        elif opcion == 4:   # Listado de ingresos por débito automático (excel)
            deb_aut(idu)
        elif opcion == 5:   # Listado de panteones
            panteones(idu)
        elif opcion == 6:   # Listado de cobradores
            cobradores(idu)
        elif opcion == 0:   # Salir
            return


def opcion_morosos():                                                                               # OPCIÓN MENÚ MOROSOS
    print("")
    print("********** Acciones disponibles **********")
    print("")
    print("   1. Listado detallado")
    print("   2. Listado comprimido")
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
        print("")
        input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
        print()
        opcion = -1
    return opcion


def morosos(idu):                                                                                   # MENÚ MOROSOS
    opcion = -1
    while opcion != 0:
        opcion = opcion_morosos()
        if opcion == 1:     # Listado detallado
            i_d, nom, ape, tel, dom, use, pas, pri, act = buscar_usuario_por_id(idu)
            if pri < 1:
                print("No posee privilegios para realizar esta acción")
                print()
            else:
                print("Confeccionando el listado. Por favor aguarde...")
                print()
                rep.report_morosos_det()
                print()
                return
        elif opcion == 2:   # Listado comprimido
            i_d, nom, ape, tel, dom, use, pas, pri, act = buscar_usuario_por_id(idu)
            if pri < 1:
                print("No posee privilegios para realizar esta acción")
                print()
            else:
                print("Confeccionando el listado. Por favor aguarde...")
                print()
                rep.report_morosos_comp()
                print()
                return
        elif opcion == 0:   # Volver
            return


def socios(idu):
    i_d, nom, ape, tel, dom, use, pas, pri, act = buscar_usuario_por_id(idu)
    if pri < 1:
        print("No posee privilegios para realizar esta acción")
        print()
    else:
        print("Confeccionando el listado. Por favor aguarde...")
        print()
        rep.report_excel_socios()
        print()


def modif_caja(idu):
    i_d, nom, ape, tel, dom, use, pas, pri, act = buscar_usuario_por_id(idu)
    if pri < 4:
        print("No posee privilegios para realizar esta acción")
        print()
    else:
        print("Confeccionando el listado. Por favor aguarde...")
        print()
        rep.report_excel_modif_caja()
        print()


def deb_aut(idu):
    i_d, nom, ape, tel, dom, use, pas, pri, act = buscar_usuario_por_id(idu)
    if pri < 3:
        print("No posee privilegios para realizar esta acción")
        print()
    else:
        try:
            mes = int(input("Indique el mes: "))
            print()
        except ValueError: 
            print("         ERROR. El dato solicitado debe ser de tipo numérico.")
            print()
        except:
            mant.log_error()
            input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
            print()
        try:
            año = int(input("Indique el año: "))
            print()
        except ValueError: 
            print("         ERROR. El dato solicitado debe ser de tipo numérico.")
            print()
        except:
            mant.log_error()
            input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
            print() 
        print("Confeccionando el listado. Por favor aguarde...")
        print()
        str_mes = str(mes).rjust(2, '0')
        str_año = str(año).rjust(3,'0').rjust(4, '2')
        rep.report_deb_aut(str_mes, str_año)
        print()


def panteones(idu):
    i_d, nom, ape, tel, dom, use, pas, pri, act = buscar_usuario_por_id(idu)
    if pri < 1:
        print("No posee privilegios para realizar esta acción")
        print()
    else:
        print("Confeccionando el listado. Por favor aguarde...")
        print()
        rep.report_panteones()
        print()


def cobradores(idu):
    i_d, nom, ape, tel, dom, use, pas, pri, act = buscar_usuario_por_id(idu)
    if pri < 1:
        print("No posee privilegios para realizar esta acción")
        print()
    else:
        print("Confeccionando el listado. Por favor aguarde...")
        print()
        rep.report_cobradores()
        print()


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

#######################################################################################################################################################
###################################################################### SCRIPT #########################################################################
#######################################################################################################################################################

try:
    print(f"Morella v{mant.VERSION} - MF! Soluciones informáticas.")
    print("")
    print("")
    print("   #############################################")
    print("   #############################################")
    print("   #####                                   #####")
    print("   #####             REPORTEADOR           #####")
    print("   #####                                   #####")
    print("   #############################################")
    print("   #############################################")

    ########## INICIO DE SESIÓN ##########
    idu = -1 

    while idu < 0:
        print("")
        idu, nom, ape, tel, dom, use, pas, pri, act = iniciar_sesion()

    if idu == 0:
        mantenimiento = getpass("Presione enter para salir...")        
        print()
        if mantenimiento == "admin":
            try:
                mant.mant_database()
            except:
                mant.log_error()
                print("")
                getpass("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
    
    if idu > 0:
        if pri >= 1:
            ########## MOSTRANDO EL MENÚ DE USUARIO ###########
            menu(idu)
        
        else:
            print("         ERROR. No posee los privilegios necesarios para realizar esta operación. Comuníquese con un admnistrador.")
            print("")
            getpass("Presione enter para continuar...")
            print("")

    ########## CERRANDO CONSOLA ##########
    cerrar_consola()

    os.system('color 80')   # Colores del módulo (Negro sobre gris)
except:
    mant.log_error()
    print("")
    input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
    print()