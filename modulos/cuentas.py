print("\n\nCargando las funciones necesarias para ejectuar el módulo. Por favor aguarde... \n\n")
import funciones_cuentas as func
import funciones_mantenimiento as mant
import os

os.system(f'TITLE Morella v{mant.VERSION} - MF! Soluciones informáticas')
os.system('color 0d')   # Colores del módulo (Púrpura sobre negro)

try:
    print(f"Morella v{mant.VERSION} - MF! Soluciones informáticas.")
    print("")
    print("")
    print("   #############################################")
    print("   #############################################")
    print("   #####                                   #####")
    print("   #####         ESTADO DE CUENTAS         #####")
    print("   #####                                   #####")
    print("   #############################################")
    print("   #############################################")
    print("")
    print("")

    ########## INICIO DE SESIÓN ##########
    idu = -1 

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
        if pri >= 1:
            print()
            print("********* Buscar estado de cuenta *********")
            print("")
            salir = 0
            while salir == 0:
                print("")
                try:
                    opcion = int(input("Indique el nro. de socio o ingrese 0 si desea abrir el menú de búsqueda: "))
                    if opcion == 0:
                        func.menu_buscar()
                        print("")
                        socio = int(input("Indique el nro. de socio: "))
                        func.buscar_estado_cta(socio)
                        msj = ''
                        while msj == '':
                            msj = input("¿Desea buscar otro estado de cuenta? (S/N) ")
                            if msj == 'S' or msj == 's' or msj == 'Si' or msj == 'SI' or msj == 'sI' or msj == 'si':
                                salir = 0
                            elif msj == 'N' or msj == 'n' or msj == 'No' or msj == 'NO' or msj == 'nO' or msj == 'no':
                                salir = 1
                            else:
                                print("")
                                print("Debe ingresar S para confirmar o N para cancelar.")
                                print("")
                                msj = ''
                    if opcion != 0 and opcion != -2:
                        func.buscar_estado_cta(opcion)
                        msj = ''
                        while msj == '':
                            msj = input("¿Desea buscar otro estado de cuenta? (S/N) ")
                            if msj == 'S' or msj == 's' or msj == 'Si' or msj == 'SI' or msj == 'sI' or msj == 'si':
                                salir = 0
                            elif msj == 'N' or msj == 'n' or msj == 'No' or msj == 'NO' or msj == 'nO' or msj == 'no':
                                salir = 1
                            else:
                                print("")
                                print("Debe ingresar S para confirmar o N para cancelar.")
                                print("")
                                msj = ''
                except ValueError:
                    print("")
                    print("         ERROR. Número de socio inválido")
                    print("")
                except TypeError:
                    print("")
                    print("         ERROR. Número de socio inválido")
                    print("")
                except PermissionError:
                    print("")
                    print("         ERROR. El archivo se encuentra abierto. Ciérrelo y vuelva a intentarlo")
                    print("")
                except:
                    mant.log_error()
                    print(f"         ERROR. Comuníquese con el administrador del sistema.")
                    print("")
            if salir == 1:
                ########## CERRANDO CONSOLA ########## 
                
                func.cerrar_consola()

            os.system('color 0d')   # Colores del módulo (Púrpura sobre negro)
        else:
            print("         ERROR. No posee los privilegios necesarios para realizar esta operación. Comuníquese con un admnistrador.")
            print("")
            func.getpass("Presione enter para continuar...")
            print("")

            ########## CERRANDO CONSOLA ########## 
                
            func.cerrar_consola()
            os.system('color 0d')   # Colores del módulo (Púrpura sobre negro)
except:
    mant.log_error()
    print("")
    input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
    print()