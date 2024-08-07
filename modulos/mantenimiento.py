print("\n\nCargando las funciones necesarias para ejectuar el módulo. Por favor aguarde... \n\n")
import os

import funciones_mantenimiento as func

os.system(f'TITLE {func.WINDOW_TITLE}')
os.system('color 0a')   # Colores del módulo (Verde sobre negro)
os.system('mode con: cols=160 lines=9999')

try:
    print(f"Morella v{func.VERSION} - MF! Soluciones informáticas.")
    print()
    print()
    print("   #############################################")
    print("   #############################################")
    print("   #####                                   #####")
    print("   #####      MANTENIMIENTO DE TABLAS      #####")
    print("   #####                                   #####")
    print("   #############################################")
    print("   #############################################")

    ########## INICIO DE SESIÓN ##########
    idu = -1 

    while idu < 0:
        print()
        try:
            idu, nom, ape, tel, dom, use, pas, pri, act = func.iniciar_sesion()
        except KeyboardInterrupt:
            mantenimiento = func.getpass("\n\nPresione enter para volver... ")
            print()
            if mantenimiento == "admin":
                print()
                print()
                print()
                print()
                print("                         +++++++++++++++++++++++++++++++++++++++++++++++++")
                print("                         +++++++++++++++++++++++++++++++++++++++++++++++++")
                print("                         ++++++++++                             ++++++++++")
                print("                         ++++++++++    MENÚ DE ADMINISTRADOR    ++++++++++")
                print("                         ++++++++++                             ++++++++++")
                print("                         +++++++++++++++++++++++++++++++++++++++++++++++++")
                print("                         +++++++++++++++++++++++++++++++++++++++++++++++++")
                print()
                print("   _________________________________________________________________________________________________________")
                print("  |                                                                                                         |")
                print("  |  ATENCION! Este menú es de uso exclusivo del administrador de sistemas.                                 |")
                print("  |  Cualquier modificación que realice desde este menú puede corromper el sistema dejándolo inutilizable.  |")
                print("  |  Toda acción realizada a partir de aquí queda bajo su responsabilidad total y absoluta.                 |")
                print("  |  El administrador no se hace responsable por los daños que pueda ocasionar.                             |")
                print("  |_________________________________________________________________________________________________________|")
                print()
                print()
                print()
                print("********** Acciones disponibles **********")
                print()
                print("   1. Restaurar cuenta ADMIN")
                print("   2. Mantenimiento de ruta a base de datos")
                print("   0. Salir")
                print()
                loop = -1
                cerrar = 0
                while loop == -1:
                    try:
                        loop = opcion = int(input("Ingrese una opción: "))
                        print()
                        while opcion < 0 or opcion > 2:
                            print("Opción incorrecta.")
                            print()
                            loop = opcion = int(input("Ingrese una opción: "))
                            print()
                    except ValueError:
                        print("Opción incorrecta.")
                        print()
                        loop = opcion = int(input("Ingrese una opción: "))
                        print()
                    except:
                        func.log_error()
                        print()
                        func.getpass("         ERROR. Información al respecto en el log de errores...  Presione enter para continuar con el inicio de sesión...")
                        print()
                if opcion == 1:
                    func.mant_restaurar_admin()
                elif opcion == 2:
                    try:
                        func.mant_database()
                        print()
                    except:
                        func.log_error()
                        print()
                        func.getpass("         ERROR. Información al respecto en el log de errores...  Presione enter para continuar con el inicio de sesión...")
                        print()
                    cerrar = 1
                else:
                    cerrar = 1
                if cerrar == 1:
                    os._exit(1)


    if idu == 0:
        mantenimiento = func.getpass("Presione enter para salir...")        
        print()
        if mantenimiento == "admin":
            try:
                func.mant_database()
            except Exception as e:
                func.manejar_excepcion_gral(e)

    if idu > 0:
        if pri >= 1:
            ########## MOSTRANDO EL MENÚ DE USUARIO ###########
            func.menu(idu)

        else:
            print("         ERROR. No posee los privilegios necesarios para realizar esta operación. Comuníquese con un admnistrador.")
            print()
            func.getpass("Presione enter para continuar...")
            print()

    ########## CERRANDO CONSOLA ##########
    func.cerrar_consola()

    os.system('color 0E')   # Colores del módulo (Amarillo sobre negro)
except Exception as e:
    func.manejar_excepcion_gral(e)
    print()
