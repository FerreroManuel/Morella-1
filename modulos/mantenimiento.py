print("\n\nCargando las funciones necesarias para ejectuar el módulo. Por favor aguarde... \n\n")
import funciones_mantenimiento as func
import os

os.system('TITLE Morella v1.1.0.2205- MF! Soluciones informáticas')
os.system('color 0a')   # Colores del módulo (Verde sobre negro)
os.system('mode con: cols=160 lines=9999')

try:
    print("Morella v1.1.0.2205- MF! Soluciones informáticas.")
    print("")
    print("")
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
        print("")
        idu, nom, ape, tel, dom, use, pas, pri, act = func.iniciar_sesion()



    if idu > 0:
        if pri >= 1:
            ########## MOSTRANDO EL MENÚ DE USUARIO ###########
            func.menu(idu)

        else:
            print("         ERROR. No posee los privilegios necesarios para realizar esta operación. Comuníquese con un admnistrador.")
            print("")
            input("Presione enter para continuar...")
            print("")

    ########## CERRANDO CONSOLA ##########
    func.cerrar_consola()

    os.system('color 0E')   # Colores del módulo (Amarillo sobre negro)
except:
    func.log_error()
    print("")
    input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
    print()