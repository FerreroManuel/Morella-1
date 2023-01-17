print("\n\nCargando las funciones necesarias para ejectuar el módulo. Por favor aguarde... \n\n")
import os

import funciones_mantenimiento as mant
import funciones_ventas as func

os.system(f'TITLE Morella v{mant.VERSION} - MF! Soluciones informáticas')
os.system('color 0B')   # Colores del módulo (Celeste sobre negro)

try:
    print(f"Morella v{mant.VERSION} - MF! Soluciones informáticas.")
    print()
    print()
    print("   #############################################")
    print("   #############################################")
    print("   #####                                   #####")
    print("   #####               VENTAS              #####")
    print("   #####                                   #####")
    print("   #############################################")
    print("   #############################################")

    ########## INICIO DE SESIÓN ##########
    idu = -1 

    while idu < 0:
        print()
        idu, nom, ape, tel, dom, use, pas, pri, act = mant.iniciar_sesion()

    if idu == 0:
        mantenimiento = func.getpass("Presione enter para salir...")        
        print()
        if mantenimiento == "admin":
            try:
                mant.mant_database()
            except:
                mant.log_error()
                print()
                func.getpass("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
    
    if idu > 0:
        if pri >= 2:
            ########## MOSTRANDO EL MENÚ DE USUARIO ###########
            func.menu(idu)
        
        else:
            print("         ERROR. No posee los privilegios necesarios para realizar esta operación. Comuníquese con un admnistrador.")
            print()
            func.getpass("Presione enter para continuar...")
            print()

    ########## CERRANDO CONSOLA ##########
    mant.cerrar_consola()

    os.system('color 0B')   # Colores del módulo (Celeste sobre negro)
except:
    mant.log_error()
    print()
    input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
    print()