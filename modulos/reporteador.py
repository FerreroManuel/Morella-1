print("\n\nCargando las funciones necesarias para ejectuar el módulo. Por favor aguarde... \n\n")
import os
import psycopg2 as sql
import psycopg2.errors

from getpass import getpass

import correo as email
import funciones_caja as caja
import funciones_mantenimiento as mant
import funciones_ventas as vent
import reporter as rep

os.system(f'TITLE {mant.WINDOW_TITLE}')
os.system('color 80')   # Colores del módulo (Negro sobre gris)



#######################################################################################################################################################
###################################################################### FUNCIONES ######################################################################
#######################################################################################################################################################


def opcion_menu() -> int:                                                                           # OPCIÓN MENÚ PRINCIPAL
    """Muestra al usuario un menú y luego le solicita ingresar una de las
    opciones mostradas a través del número correspondiente. En caso de no
    ingresar una opción correcta, se le volverá a solicitar.

    :rtype: int
    """
    print()
    print("********** Acciones disponibles **********")
    print()
    print("   1. Listado de morosos")
    print("   2. Listado de socios (excel)")
    print("   3. Listado de modificaciones de caja (excel)")
    print("   4. Listado de ingresos por débito automático (excel)")
    print("   5. Listado de panteones")
    print("   6. Listado de cobradores")
    print("   7. Listado de últimos recibos impagos (Excel)")
    print("   8. Errores del sistema")
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
    except Exception as e:
        mant.manejar_excepcion_gral(e)
        print()
        opcion = -1
    return opcion


def menu(idu: int):                                                                                 # MENÚ PRINCIPAL
    """Llama a la función donde se muestra las opciones y recibe, a través de
    ella, la opción ingresada por el usuario. Luego, según la opción ingresada,
    llama a la función correspondiente.

    :param idu: ID de usuario
    :type idu: int
    """
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
        elif opcion == 8:   # Errores de sistema
            errores_sistema(idu)
        elif opcion == 0:   # Salir
            return


def opcion_morosos() -> int:                                                                        # OPCIÓN MENÚ MOROSOS
    """Muestra al usuario un menú y luego le solicita ingresar una de las
    opciones mostradas a través del número correspondiente. En caso de no
    ingresar una opción correcta, se le volverá a solicitar.

    :rtype: int
    """
    print()
    print("********** Acciones disponibles **********")
    print()
    print("   1. Listado detallado")
    print("   2. Listado comprimido")
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
    except Exception as e:
        mant.manejar_excepcion_gral(e)
        print()
        opcion = -1
    return opcion


def morosos(idu: int):                                                                              # MENÚ MOROSOS
    """Llama a la función donde se muestra las opciones y recibe, a través de
    ella, la opción ingresada por el usuario. Luego, según la opción ingresada,
    llama a la función correspondiente.

    :param idu: ID de usuario
    :type idu: int
    """
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


def socios(idu: int):
    """Permite al usuario exportar toda la tabla de socios de la base de datos
    en un archivo XLSX (Excel).

    Nivel de privilegios mínimo: 1

    :param idu: ID de usuario
    :type idu: int
    """
    i_d, nom, ape, tel, dom, use, pas, pri, act = mant.buscar_usuario_por_id(idu)
    
    if pri < 1:
        print("No posee privilegios para realizar esta acción")
        print()
    
    else:
        print("Confeccionando el listado. Por favor aguarde...")
        print()
        rep.report_excel_socios()
        print()


def modif_caja(idu: int):
    """Permite al usuario exportar toda la tabla de historial de caja en
    un archivo XLSX (Excel).

    Nivel de privilegios mínimo: 4

    :param idu: ID de usuario
    :type idu: int
    """
    i_d, nom, ape, tel, dom, use, pas, pri, act = mant.buscar_usuario_por_id(idu)
    
    if pri < 4:
        print("No posee privilegios para realizar esta acción")
        print()
    
    else:
        print("Confeccionando el listado. Por favor aguarde...")
        print()
        rep.report_excel_modif_caja()
        print()


def deb_aut(idu: int):
    """Permite al usuario exportar todos los pagos realizados a través de
    débito automático de un mes específico en un archivo XLSX (Excel).

    Nivel de privilegios mínimo: 3

    :param idu: ID de usuario
    :type idu: int
    """
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
        except Exception as e:
            mant.manejar_excepcion_gral(e)
            print()
    
        try:
            año = int(input("Indique el año: "))
            print()
    
        except ValueError: 
            print("         ERROR. El dato solicitado debe ser de tipo numérico.")
            print()
        except Exception as e:
            mant.manejar_excepcion_gral(e)
            print() 
    
        print("Confeccionando el listado. Por favor aguarde...")
        print()
        str_mes = str(mes).rjust(2, '0')
        str_año = str(año).rjust(3,'0').rjust(4, '2')
    
        rep.report_deb_aut(str_mes, str_año)
        print()


def panteones(idu: int):
    """Permite al usuario exportar de la base de datos toda la tabla de
    panteones en un archivo PDF.

    Nivel de privilegios mínimo: 1

    :param idu: ID de usuario
    :type idu: int
    """
    i_d, nom, ape, tel, dom, use, pas, pri, act = mant.buscar_usuario_por_id(idu)

    if pri < 1:
        print("No posee privilegios para realizar esta acción")
        print()

    else:
        print("Confeccionando el listado. Por favor aguarde...")
        print()
        rep.report_panteones()
        print()


def cobradores(idu: int):
    """Permite al usuario exportar de la base de datos toda la tabla de
    cobradores en un archivo PDF.

    Nivel de privilegios mínimo: 1

    :param idu: ID de usuario
    :type idu: int
    """
    i_d, nom, ape, tel, dom, use, pas, pri, act = mant.buscar_usuario_por_id(idu)
    
    if pri < 1:
        print("No posee privilegios para realizar esta acción")
        print()
    
    else:
        print("Confeccionando el listado. Por favor aguarde...")
        print()
        rep.report_cobradores()
        print()


def ultimos_recibos(idu: int):
    """Permite al usuario generar un reporte en Excel que contiene los datos de los últimos
    recibos impagos de cada operación de un cobrador y una facturación específicos.

    Nivel de privilegios mínimo: 1

    :param idu: ID de usuario
    :type idu: int
    """
    i_d, nom, ape, tel, dom, use, pas, pri, act = mant.buscar_usuario_por_id(idu)
    
    if pri < 1:
        print("No posee privilegios para realizar esta acción")
        print()
    
    else:
        cobrador = mant.rend.menu_cobradores()
        
        if cobrador == 0:
            return
    
        print()
        print("********** Elija una facturación **********")
        print()
        print("   1. Bicon")
        print("   2. NOB")
        print()
        
        opcion = -1
        while opcion == -1:
            try:
                opcion = int(input("Ingrese una opción: "))
        
                if opcion < 1 or opcion > 2:
                    print()
                    print("Opción incorrecta.")
                    print()
                    opcion = -1
        
            except ValueError: 
                print("Opción incorrecta.")
                opcion = -1
            except Exception as e:
                mant.manejar_excepcion_gral(e)
                print()
                return
        
        if opcion == 1:
            facturacion = 'bicon'
        
        elif opcion == 2:
            facturacion = 'nob'
        
        print("Confeccionando el listado. Por favor aguarde...")
        print()
        print(f'COBRADOR: {caja.obtener_nom_cobrador(cobrador)} - FACTURACIÓN: {facturacion}')
        
        rep.report_ult_recibo(cobrador, facturacion)
        print()


def opcion_errores_sistema() -> int:
    """Muestra al usuario un menú y luego le solicita ingresar una de las
    opciones mostradas a través del número correspondiente. En caso de no
    ingresar una opción correcta, se le volverá a solicitar.

    :rtype: int
    """
    print()
    print("********** Acciones disponibles **********")
    print()
    print("   1. Ver log de errores")
    print("   2. Enviar log al administrador")
    print("   3. Limpiar log de errores")
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
    except Exception as e:
        mant.manejar_excepcion_gral(e)
        print()
        opcion = -1
    return opcion


def errores_sistema(idu: int):
    """Recibe el ID del usuario. Luego llama a la función donde se muestra las
    opciones y recibe, a través de ella, la opción ingresada por el usuario.
    Luego, según la opción ingresada, llama a la función correspondiente, a la
    cual le transmite el ID del usuario.

    :param idu: ID de usuario
    :type idu: int
    """
    i_d, nom, ape, tel, dom, use, pas, pri, act = mant.buscar_usuario_por_id(idu)
    
    if pri < 1:
        print("No posee privilegios para realizar esta acción")
        print()
    
    else:
        opcion = -1
        while opcion != 0:
            opcion = opcion_errores_sistema()
            if opcion == 1:
                print()
                print('    Abriendo log de errores... Cierre el archivo para continuar...')
                os.system(f'notepad {mant.ARCH_LOG_ERROR}')
            elif opcion == 2:
                print()
                print('    Enviando log de errores...')
                try:
                    email.envio_de_errores()
                    log = open(mant.ARCH_LOG_ERROR, 'w')
                    log.close()
                    print()
                    getpass('Enviado con éxito... Presione enter para continuar...')
                    print()
                except Exception as e:
                    mant.manejar_excepcion_gral(e)
                    print()
            elif opcion == 3:
                print()
                print('    Limpiando log de errores... Aguarde un momento...')
                log = open(mant.ARCH_LOG_ERROR, 'w')
                log.close()
                print()
                getpass('    Hecho... Presione enter para continuar...')
                print()
            elif opcion == 0:
                return


#######################################################################################################################################################
###################################################################### SCRIPT #########################################################################
#######################################################################################################################################################

try:
    print(f"Morella v{mant.VERSION} - MF! Soluciones informáticas.")
    print()
    print()
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
        print()
        idu, nom, ape, tel, dom, use, pas, pri, act = mant.iniciar_sesion()

    if idu == 0:
        mantenimiento = getpass("Presione enter para salir...")        
        print()
        if mantenimiento == "admin":
            try:
                mant.mant_database()
            except Exception as e:
                mant.manejar_excepcion_gral(e)
    
    if idu > 0:
        if pri >= 1:
            ########## MOSTRANDO EL MENÚ DE USUARIO ###########
            menu(idu)
        
        else:
            print("         ERROR. No posee los privilegios necesarios para realizar esta operación. Comuníquese con un admnistrador.")
            print()
            getpass("Presione enter para continuar...")
            print()

    ########## CERRANDO CONSOLA ##########
    mant.cerrar_consola()

    os.system('color 80')   # Colores del módulo (Negro sobre gris)

except Exception as e:
    mant.manejar_excepcion_gral(e)
    print()
    