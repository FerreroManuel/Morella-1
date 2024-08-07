print("\n\nCargando las funciones necesarias para ejectuar el módulo. Por favor aguarde... \n\n")
import os

import funciones_caja as func
import funciones_mantenimiento as mant

os.system(f'TITLE {mant.WINDOW_TITLE}')
os.system('color 0E')   # Colores del módulo (Amarillo sobre negro)

try:
    print(f"Morella v{mant.VERSION} - MF! Soluciones informáticas.")
    print()
    print()
    print("   #############################################")
    print("   #############################################")
    print("   #####                                   #####")
    print("   #####               CAJA                #####")
    print("   #####                                   #####")
    print("   #############################################")
    print("   #############################################")
    print()
    print()

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
            except Exception as e:
                mant.manejar_excepcion_gral(e)

    if idu > 0:
        if pri >= 3:
            ########## OBTENIENDO EL SALDO INICIAL DESDE ARCHIVO ###########
            saldo_inicial = 0

            print()
            print("Obteniendo saldo inicial...")
            print()

            func.iniciar_caja()

            ########## MOSTRANDO EL MENÚ DE USUARIO ###########
            func.menu(idu)

            ########## CERRANDO CONSOLA ########## 
            
            mant.cerrar_consola()
        else:
            print("         ERROR. No posee los privilegios necesarios para realizar esta operación. Comuníquese con un admnistrador.")
            print()
            print("No se han realizado cambios en el registro.")
            print()
            func.getpass("Presione enter para continuar...")
            print()

            ########## CERRANDO CONSOLA ########## 
                
            mant.cerrar_consola()

        os.system('color 0E')   # Colores del módulo (Amarillo sobre negro)
except Exception as e:
    mant.manejar_excepcion_gral(e)
    print()