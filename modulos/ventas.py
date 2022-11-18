print("\n\nCargando las funciones necesarias para ejectuar el módulo. Por favor aguarde... \n\n")
import funciones_ventas as func
import funciones_mantenimiento as mant
import os

os.system('TITLE Morella v1.1.0.2205 - MF! Soluciones informáticas')
os.system('color 0B')   # Colores del módulo (Celeste sobre negro)

try:
    print("Morella v1.1.0.2205 - MF! Soluciones informáticas.")
    print("")
    print("")
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
        print("")
        idu, nom, ape, tel, dom, use, pas, pri, act = func.iniciar_sesion()



    if idu > 0:
        if pri >= 2:
            ########## MOSTRANDO EL MENÚ DE USUARIO ###########
            func.menu(idu)
        
        else:
            print("         ERROR. No posee los privilegios necesarios para realizar esta operación. Comuníquese con un admnistrador.")
            print("")
            input("Presione enter para continuar...")
            print("")

    ########## CERRANDO CONSOLA ##########
    func.cerrar_consola()

    os.system('color 0B')   # Colores del módulo (Celeste sobre negro)
except:
    mant.log_error()
    print("")
    input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
    print()