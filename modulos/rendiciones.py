print("\n\nCargando las funciones necesarias para ejectuar el módulo. Por favor aguarde... \n\n")
import funciones_rendiciones as func
import funciones_mantenimiento as mant
import os

os.system('TITLE Morella v1.2.0.2205 - MF! Soluciones informáticas')
os.system('color 09')   # Colores del módulo (Azul sobre negro)

try:
    print("Morella v1.2.0.2205 - MF! Soluciones informáticas.")
    print("")
    print("")
    print("   #############################################")
    print("   #############################################")
    print("   #####                                   #####")
    print("   #####            RENDICIONES            #####")
    print("   #####                                   #####")
    print("   #############################################")
    print("   #############################################")
    print("")
    print("")

    ########## INICIO DE SESIÓN ##########
    idu = -1

    idu, nom, ape, tel, dom, use, pas, pri, act = func.iniciar_sesion()

    while idu < 0:
        print("")
        idu, nom, ape, tel, dom, use, pas, pri, act = func.iniciar_sesion()

    if idu == 0:
        mantenimiento = func.getpass("Presione enter para salir...")        
        print()
        if mantenimiento == "admin":
            try:
                mant.mant_database()
            except:
                mant.log_error()
                print("")
                func.getpass("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
    
    if idu > 0:
        if pri >= 2:
            func.menu(idu)

            ########## CERRANDO CONSOLA ##########
            func.cerrar_consola()
        else:
            print("         ERROR. No posee los privilegios necesarios para realizar esta operación. Comuníquese con un admnistrador.")
            print("")
            func.getpass("Presione enter para continuar...")
            print("")

            ########## CERRANDO CONSOLA ##########
            func.cerrar_consola()
            
    os.system('color 09')   # Colores del módulo (Azul sobre negro)
            
except:
    mant.log_error()
    print("")
    input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
    print()