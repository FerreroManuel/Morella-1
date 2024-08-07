print("\n\nCargando las funciones necesarias para ejectuar el módulo. Por favor aguarde... \n\n")
import os

import funciones_cuentas as func
import funciones_mantenimiento as mant

os.system(f'TITLE {mant.WINDOW_TITLE}')
os.system('color 0d')   # Colores del módulo (Púrpura sobre negro)

try:
    print(f"Morella v{mant.VERSION} - MF! Soluciones informáticas.")
    print()
    print()
    print("   #############################################")
    print("   #############################################")
    print("   #####                                   #####")
    print("   #####         ESTADO DE CUENTAS         #####")
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
        if pri >= 1:
            print()
            print("********* Buscar estado de cuenta *********")
            print()
            salir = 0
            while salir == 0:
                print()
                try:
                    opcion = int(input("Indique el nro. de socio o ingrese 0 si desea abrir el menú de búsqueda: "))
                    if opcion == 0:
                        func.menu_buscar()
                        print()
                        socio = int(input("Indique el nro. de socio: "))
                        func.buscar_estado_cta(socio)
                        msj = ''
                        while msj == '':
                            msj = input("¿Desea buscar otro estado de cuenta? (S/N) ")
                            if msj in mant.AFIRMATIVO:
                                salir = 0
                            elif msj in mant.NEGATIVO:
                                salir = 1
                            else:
                                print()
                                print("Debe ingresar S para confirmar o N para cancelar.")
                                print()
                                msj = ''
                    if opcion != 0 and opcion != -2:
                        func.buscar_estado_cta(opcion)
                        msj = ''
                        while msj == '':
                            msj = input("¿Desea buscar otro estado de cuenta? (S/N) ")
                            if msj in mant.AFIRMATIVO:
                                salir = 0
                            elif msj in mant.NEGATIVO:
                                salir = 1
                            else:
                                print()
                                print("Debe ingresar S para confirmar o N para cancelar.")
                                print()
                                msj = ''
                except ValueError:
                    print()
                    print("         ERROR. Número de socio inválido")
                    print()
                except TypeError:
                    print()
                    print("         ERROR. Número de socio inválido")
                    print()
                except PermissionError:
                    print()
                    print("         ERROR. El archivo se encuentra abierto. Ciérrelo y vuelva a intentarlo")
                    print()
                except Exception as e:
                    mant.manejar_excepcion_gral(e, False)
                    print()
            if salir == 1:
                ########## CERRANDO CONSOLA ########## 
                
                mant.cerrar_consola()

            os.system('color 0d')   # Colores del módulo (Púrpura sobre negro)
        else:
            print("         ERROR. No posee los privilegios necesarios para realizar esta operación. Comuníquese con un admnistrador.")
            print()
            func.getpass("Presione enter para continuar...")
            print()

            ########## CERRANDO CONSOLA ########## 
                
            mant.cerrar_consola()
            os.system('color 0d')   # Colores del módulo (Púrpura sobre negro)
except Exception as e:
    mant.manejar_excepcion_gral(e)
    print()