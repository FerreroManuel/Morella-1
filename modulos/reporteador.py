print("\n\nCargando las funciones necesarias para ejectuar el módulo. Por favor aguarde... \n\n")
import funciones_mantenimiento as mant
import funciones_ventas as vent
import funciones_rendiciones as rend
import reporter as rep
import psycopg2 as sql
import psycopg2.errors
from getpass import getpass
import os

os.system(f'TITLE Morella v{mant.VERSION} - MF! Soluciones informáticas')
os.system('color 80')   # Colores del módulo (Negro sobre gris)



#######################################################################################################################################################
###################################################################### FUNCIONES ######################################################################
#######################################################################################################################################################


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
    print("   7. Listado de últimos recibos impagos (Excel)")
    print("   0. Salir")
    print("")
    try:
        opcion = int(input("Ingrese una opción: "))
        while opcion < 0 or opcion > 7:
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
        elif opcion == 7:   # Listado de últimos recibos impagos (Excel)
            ultimos_recibos(idu)
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
            i_d, nom, ape, tel, dom, use, pas, pri, act = mant.buscar_usuario_por_id(idu)
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
            i_d, nom, ape, tel, dom, use, pas, pri, act = mant.buscar_usuario_por_id(idu)
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
    i_d, nom, ape, tel, dom, use, pas, pri, act = mant.buscar_usuario_por_id(idu)
    if pri < 1:
        print("No posee privilegios para realizar esta acción")
        print()
    else:
        print("Confeccionando el listado. Por favor aguarde...")
        print()
        rep.report_excel_socios()
        print()


def modif_caja(idu):
    i_d, nom, ape, tel, dom, use, pas, pri, act = mant.buscar_usuario_por_id(idu)
    if pri < 4:
        print("No posee privilegios para realizar esta acción")
        print()
    else:
        print("Confeccionando el listado. Por favor aguarde...")
        print()
        rep.report_excel_modif_caja()
        print()


def deb_aut(idu):
    i_d, nom, ape, tel, dom, use, pas, pri, act = mant.buscar_usuario_por_id(idu)
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
    i_d, nom, ape, tel, dom, use, pas, pri, act = mant.buscar_usuario_por_id(idu)
    if pri < 1:
        print("No posee privilegios para realizar esta acción")
        print()
    else:
        print("Confeccionando el listado. Por favor aguarde...")
        print()
        rep.report_panteones()
        print()


def cobradores(idu):
    i_d, nom, ape, tel, dom, use, pas, pri, act = mant.buscar_usuario_por_id(idu)
    if pri < 1:
        print("No posee privilegios para realizar esta acción")
        print()
    else:
        print("Confeccionando el listado. Por favor aguarde...")
        print()
        rep.report_cobradores()
        print()


def ultimos_recibos(idu):
    i_d, nom, ape, tel, dom, use, pas, pri, act = mant.buscar_usuario_por_id(idu)
    if pri < 1:
        print("No posee privilegios para realizar esta acción")
        print()
    else:
        print("Indique el ID de cobrador: ")
        cobradores = vent.obtener_cobradores()
        counter = 0
        for i in cobradores:
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
        print("********** Elija una facturación **********")
        print("")
        print("   1. Bicon")
        print("   2. NOB")
        print("")
        opcion = -1
        while opcion == -1:
            try:
                opcion = int(input("Ingrese una opción: "))
                if opcion < 1 or opcion > 2:
                    print("")
                    print("Opción incorrecta.")
                    print("")
                    opcion = -1
            except ValueError: 
                print("Opción incorrecta.")
                opcion = -1
            except:
                mant.log_error()
                print("")
                input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
                print()
                return
        if opcion == 1:
            facturacion = 'bicon'
        elif opcion == 2:
            facturacion = 'nob'
        print("Confeccionando el listado. Por favor aguarde...")
        print()
        ###
        print(f'COBRADOR: {rend.obtener_nom_cobrador(cobrador)} - FACTURACIÓN: {facturacion}')
        ###
        rep.report_ult_recibo(cobrador, facturacion)
        print()


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
        idu, nom, ape, tel, dom, use, pas, pri, act = mant.iniciar_sesion()

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
    mant.cerrar_consola()

    os.system('color 80')   # Colores del módulo (Negro sobre gris)
except:
    mant.log_error()
    print("")
    input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
    print()