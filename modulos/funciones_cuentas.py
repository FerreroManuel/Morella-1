import os
import psycopg2 as sql
import psycopg2.errors

from getpass import getpass

import funciones_caja as caja
import funciones_mantenimiento as mant
import funciones_rendiciones as rend
import funciones_ventas as vent
import reporter as rep

os.system(f'TITLE Morella v{mant.VERSION} - MF! Soluciones informáticas')
os.system('color 0d')   # Colores del módulo (Púrpura sobre negro)
os.system('mode con: cols=160 lines=9999')


def opcion_menu_buscar() -> int:                                                                    # OPCIÓN MENÚ BUSCAR
    """Muestra al usuario un menú y luego le solicita ingresar una de las
    opciones mostradas a través del número correspondiente. En caso de no
    ingresar una opción correcta, se le volverá a solicitar.

    :rtype: int
    """
    print()
    print("********** Acciones disponibles **********")
    print()
    print("   1. Buscar por nro. de operación")
    print("   2. Buscar por apellido y nombre")
    print("   3. Buscar por DNI")
    print("   4. Buscar por domicilio")
    print("   5. Buscar por código de nicho")
    print("   6. Buscar por cobrador")
    print("   7. Buscar morosos")
    print("   8. Buscar por datos COBOL")
    print("   0. Volver")
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
    except:
        mant.log_error()
        print()
        input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
    return opcion


def menu_buscar():                                                                                  # MENÚ BUSCAR
    """Llama a la función donde se muestra las opciones y recibe, a través de
    ella, la opción ingresada por el usuario. Luego, según la opción ingresada,
    llama a la función correspondiente.

    :param idu: ID de usuario
    :type idu: int
    """
    opcion = -1
    while opcion != 0:
        opcion = opcion_menu_buscar()
        
        if opcion == 1:     # Buscar por nro. op
            try:
                print()
                nro_operacion = int(input("Indique nro. de operación: "))
                buscar_op_nro_operacion(nro_operacion)
        
            except ValueError:
                print()
                print("         ERROR. Nro de operación inválido")
                print()
            except:
                mant.log_error()
                print()
                input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
                print()
        
        elif opcion == 2:   # Buscar por nombre
            try:
                nombre = input("Ingrese apellido y nombre del asociado o parte de él: ")
                buscar_op_nombre_socio(nombre)
        
            except:
                mant.log_error()
                print()
                input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
                print()
        
        elif opcion == 3:   # Buscar por DNI
            try:
                dni = int(input("Ingrese DNI (sin puntos): "))
                buscar_op_dni(dni)
        
            except ValueError:
                print()
                print("         ERROR. DNI inválido. Recuerde que debe ingresarlo sin puntos.")
                print()
            except:
                mant.log_error()
                print()
                input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
                print()
        
        elif opcion == 4:   # Buscar por domicilio
            try:
                domicilio = input("Ingrese domicilio o parte de él: ")
                buscar_op_domicilio(domicilio)
        
            except:
                mant.log_error()
                print()
                input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
                print()
        
        elif opcion == 5:   # Buscar por código de nicho
            try:
                cod_nicho = input("Ingrese el código de nicho: ")
                buscar_op_cod_nicho(cod_nicho)
        
            except:
                mant.log_error()
                print()
                input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
                print()
        
        elif opcion == 6:   # Buscar por ID de cobrador
            cobrador = rend.menu_cobradores()
            buscar_op_cob(cobrador)
        
        elif opcion == 7:   # Buscar morosos
            buscar_op_morosos()
        
        elif opcion == 8:   # Buscar por datos Cobol
            buscar_datos_cobol()
        
        elif opcion == 0:   # Volver
            return


def buscar_datos_cobol():
    """Muestra al usuario un menú y luego le solicita ingresar una de las
    opciones mostradas a través del número correspondiente. En caso de no
    ingresar una opción correcta, se le volverá a solicitar.

    Dependiendo la opción ingresada le permite a buscar una operación, a
    través de información extraida del sistema antiguo. Las posibles 
    opciones de búsqueda son:
    - Por número de operación de Cobol.
    - Por apellido y nombre de Cobol (o nombre alternativo).
    - Por domicilio de Cobol (o domiclio alternativo).

    Permite búsquedas inexactas y el uso de comodín (%).
    """
    opcion = -1
    while opcion != 0:
        print()
        print("********** Acciones disponibles **********")
        print()
        print("   1. Buscar por nro. de operación de COBOL")
        print("   2. Buscar por apellido y nombre de COBOL (o alternativo)")
        print("   3. Buscar por domicilio de COBOL (o alternativo)")
        print("   0. Volver")
        print()
    
        try:
            opcion = int(input("Ingrese una opción: "))
            print()
    
            while opcion < 0 or opcion > 3:
                print()
                print("Opción incorrecta.")
                print()
                opcion = int(input("Ingrese una opción: "))
                print()
    
        except ValueError: 
            print("Opción incorrecta.")
            print()
            opcion = -1
        except:
            mant.log_error()
            print()
            input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
            print()
    
        if opcion == 1:         # Buscar por nro. op. Cobol
            try:
                op_cobol = int(input("Indique el número de operación de COBOL: "))
                print()
                buscar_op_cobol(op_cobol)
                print()
    
            except ValueError:
                print()
                print("         ERROR. El dato solicitado debe ser de tipo numérico.")
                print()
            except:
                mant.log_error()
                print()
                input("         ERROR. Comuníquese con el administrador... Presione enter para continuar...")
                print()
    
        elif opcion == 2:       # Buscar por nombre alternativo
            nom_alt = input("Indique nombre alternativo o parte de él: ")
            print()
            buscar_op_nom_alt(nom_alt)
            print()
        
        elif opcion == 3:       # Buscar por domicilio alternativo
            dom_alt = input("Indique domicilio alternativo o parte de él: ")
            print()
            buscar_op_dom_alt(dom_alt)
            print()


def buscar_op_nro_operacion(id_operacion: int, ret: bool = False) -> tuple | None:
    """Recupera de la base de datos la información de una operación específica
    a partir del ID de operación.

    En caso de solicitarlo, retorna una tupla conteniendo dicha información, de
    lo contrario, la imprime en una tabla en la pantalla.

    :param id_operacion: ID de operación a buscar.
    :type id_operacion: int

    :param ret: Solicitar retorno de información (por defecto False).
    :type ret: bool

    :rtype: tuple or None
    """
    with sql.connect(mant.DATABASE) as conn:
        cursor = conn.cursor()
        instruccion = f"SELECT * FROM operaciones WHERE id = '{id_operacion}'"
        cursor.execute(instruccion)
        datos = cursor.fetchall()

    if ret:
        return datos[0]

    print()
    print("-".rjust(155, '-'))
    print("{:<10} {:<12} {:<37} {:<37} {:<35} {:<10} {:<10}".format('N° SOCIO', 'COD.NICHO','APELLIDO Y NOMBRE', 'DOMICILIO', 'TELÉFONOS', 'COBRADOR','¿MOROSO?'))
    print("-".rjust(155, '-'))
    
    for x in datos:
        i_d, soc, nic, fac, cob, tar, rut, ult, u_a, fec, mor, c_f, u_r, paga, op_cob, nom_alt, dom_alt = x
        nro, nom, dni, te_1, te_2, mail, dom, loc, c_p, f_n, f_a, act = rend.obtener_datos_socio(soc)
        cob = caja.obtener_nom_cobrador(cob)
    
        if nom_alt != None:
            nom = f"[{nom_alt}]"
    
        if dom_alt != None:
            dom = f"[{dom_alt}]"
    
        if te_1 != None and te_2 != None:
            tel = f"{te_1} / {te_2}"
    
        elif te_1 != None and te_2 == None:
            tel = str(te_1)
    
        elif te_1 == None and te_2 != None:
            tel = str(te_2)
    
        elif te_1 == None and te_2 == None:
            tel = "N/D"
    
        if mor == 1:
            mor = 'SI'
    
        elif mor == 0:
            mor = 'NO'

        print("{:<10} {:<12} {:<37} {:<37} {:<35} {:<10} {:<10}".format(f'{soc}'.rjust(6, '0'), f'{nic}'.rjust(10, '0'), nom[0:37], dom[0:37], tel[0:35], cob,f'   {mor}'))
    print("-".rjust(155, '-'))
    print()


def buscar_op_nro_socio(nro_socio: int):
    """Recupera de la base de datos la información de una o más operaciones a
    partir del ID de asociado, luego la imprime en una tabla en la pantalla

    :param nro_socio: ID de asociado a buscar.
    :type nro_socio: int
    """
    try:
        nro, nom, dni, te_1, te_2, mail, dom, loc, c_p, f_n, f_a, act = rend.obtener_datos_socio(nro_socio)
        
        with sql.connect(mant.DATABASE) as conn:
            cursor = conn.cursor()
            instruccion = f"SELECT * FROM operaciones WHERE socio = '{nro_socio}'"
            cursor.execute(instruccion)
            datos = cursor.fetchall()

        print()
        if te_1 != None and te_2 != None:
            tel = f"{te_1} / {te_2}"

        elif te_1 != None and te_2 == None:
            tel = str(te_1)

        elif te_1 == None and te_2 != None:
            tel = str(te_2)

        elif te_1 == None and te_2 == None:
            tel = "N/D"

        if mail == None:
            mail = "N/D"

        print(f"ASOCIADO: {f'{nro_socio}'.rjust(6, '0')} - {nom}. DNI: {dni}. DOMICILIO: {dom} - TELÉFONOS: {tel} - EMAIL: {mail}")
        print()
        print("OPERACIONES:")
        print("-----------------------------------------------------------------------------------------------------------------------------------------------------------")
        print("{:<20} {:<20} {:<20} {:<10} {:<35} {:<35} {:<8}".format('N° OPERACIÓN', 'COD.NICHO', 'COBRADOR', '¿MOROSO?', 'NOMBRE ALTERNATIVO', 'DOMICILIO ALTERNATIVO', 'OP.COBOL'))
        print("-----------------------------------------------------------------------------------------------------------------------------------------------------------")
        
        for x in datos:
            i_d, soc, nic, fac, cob, tar, rut, ult, u_a, fec, mor, c_f, u_r, paga, op_cob, nom_alt, dom_alt = x
            cob = caja.obtener_nom_cobrador(cob)
        
            if mor == 1:
                mor = 'SI'
        
            elif mor == 0:
                mor = 'NO'
        
            if nom_alt == None:
                nom_alt = " "
        
            if dom_alt == None:
                dom_alt = " "
        
            if op_cob == None or op_cob == 0:
                op_cob = " "
        
            print("{:<20} {:<20} {:<20} {:<10} {:<35} {:<35} {:<8}".format(f'{i_d}'.rjust(7, '0'), f'{nic}'.rjust(10, '0'), cob, f'   {mor}', nom_alt, dom_alt, str(op_cob).rjust(8, ' ')))
        print("-----------------------------------------------------------------------------------------------------------------------------------------------------------")
        print()
    
    except ValueError:
        print("         ERROR. Número de socio inválido")
        print()
    except TypeError:
        print("         ERROR. No existe un asociado con ese número.")
        print()
    except:
        mant.log_error()
        print()
        input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
        print()


def buscar_op_nombre_socio(nombre: str):
    """Recupera de la base de datos la información de uno o más asociados a
    partir del apellido y nombre o parte de ellos, luego la imprime en una
    tabla en la pantalla.

    Permite la búsqueda inexacta y el uso de comodín (%).

    :param nombre: Apellido y nombre (o parte de ellos) del asociado a buscar.
    :type nombre: str
    """
    nombre = mant.reemplazar_comilla(nombre)
    
    if nombre == "":
        return
    
    try:
        with sql.connect(mant.DATABASE) as conn:
            cursor = conn.cursor()
            instruccion = f"SELECT * FROM socios WHERE nombre ilike '%{nombre}%'"
            cursor.execute(instruccion)
            datos = cursor.fetchall()

        print()
        print("***********************************************************************************************************************************************************")

        for i in datos:
            nro, nom, dni, te_1, te_2, mail, dom, loc, c_p, f_n, f_a, act = i
            buscar_op_nro_socio(nro)
            print("****************************************************************************************************************************************************************")
        input("Presione la tecla enter para continuar... ")

    except sql.errors.SyntaxError:
        print()
        print("         ERROR. Nombre inválido. No se pueden utilizar comillas simples (') en las busquedas")
        print()
        return
    except:
        mant.log_error()
        print()
        input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
        print()
        return


def buscar_op_dni(dni: int):
    """Recupera de la base de datos la información de uno o más asociados a
    partir de su documento, luego la imprime en una tabla en la pantalla.

    :param dni: Documento de identidad del asociado a buscar (sin puntos).
    :type dni: int
    """
    with sql.connect(mant.DATABASE) as conn:
        cursor = conn.cursor()
        instruccion = f"SELECT * FROM socios WHERE dni = '{dni}'"
        cursor.execute(instruccion)
        datos = cursor.fetchall()

    print()
    print("***********************************************************************************************************************************************************")

    for i in datos:
        nro, nom, dni, te_1, te_2, mail, dom, loc, c_p, f_n, f_a, act = i
        buscar_op_nro_socio(nro)
        print("***********************************************************************************************************************************************************")
    print()


def buscar_op_domicilio(domicilio: str):
    """Recupera de la base de datos la información de uno o más asociados a
    partir del domicilio o parte de él, luego la imprime en una tabla en la
    pantalla.

    Permite la búsqueda inexacta y el uso de comodín (%).

    :param domicilio: Domicilio (o parte de él) del asociado a buscar.
    :type domicilio: str
    """
    domicilio = mant.reemplazar_comilla(domicilio)
    if domicilio == "":
        return
    
    try:
        with sql.connect(mant.DATABASE) as conn:
            cursor = conn.cursor()
            instruccion = f"SELECT * FROM socios WHERE domicilio ilike '%{domicilio}%'"
            cursor.execute(instruccion)
            datos = cursor.fetchall()

        print()
        print("***********************************************************************************************************************************************************")

        for i in datos:
            nro, nom, dni, te_1, te_2, mail, dom, loc, c_p, f_n, f_a, act = i
            buscar_op_nro_socio(nro)
            print("***********************************************************************************************************************************************************")
        input("Presione la tecla enter para continuar... ")

    except sql.errors.SyntaxError:
        print()
        print("         ERROR. Domicilio inválido. Recuerde que no se pueden utilizar comillas simples (') en las busquedas")
        print()
        return
    except:
        mant.log_error()
        print()
        input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
        print()
        return


def buscar_op_cod_nicho(cod_nicho: str, ret: bool = False) -> tuple | None:
    """Recupera de la base de datos la información de una operación específica
    a partir del código de nicho.

    En caso de solicitarlo, retorna una tupla conteniendo dicha información, de
    lo contrario, la imprime en una tabla en la pantalla.

    :param cod_nicho: Código de nicho a buscar.
    :type cod_nicho: str

    :param ret: Solicitar retorno de información (por defecto False).
    :type ret: bool

    :rtype: tuple or None
    """
    cod_nicho = str(cod_nicho).upper()
    
    try:
        cod, pan, pis, fil, num, cat, ocu, fall = rend.obtener_datos_nicho(cod_nicho)
    
    except UnboundLocalError:
        print("         ERROR. Código de nicho inválido")
        print()
        return
    except sql.errors.SyntaxError:
        print("         ERROR. Código de nicho inválido")
        print()
        return
    except:
        mant.log_error()
        print()
        input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
        print()
        return
    
    panteon = rend.obtener_panteon(pan)
    id_nic, categ, val_mant_bic, val_mant_nob = rend.obtener_categoria(cat)
    
    with sql.connect(mant.DATABASE) as conn:
        cursor = conn.cursor()
        instruccion = f"SELECT * FROM operaciones WHERE nicho = '{cod_nicho}'"
        cursor.execute(instruccion)
        datos = cursor.fetchall()

    if ret:
        return datos[0]

    print()
    print(f"CÓDIGO DE NICHO: {f'{cod_nicho}'.rjust(10, '0')}. PANTEÓN: {panteon}. PISO: {pis}. FILA: {fil}. NICHO: {num}. CATEGORÍA: {categ}")
    print()
    print(f"OPERACION: {str(datos[0][0]).rjust(7, '0')}")
    print("-".rjust(154, '-'))
    print("{:<10} {:<38} {:<38} {:<35} {:<20} {:<10}".format('N° SOCIO', 'APELLIDO Y NOMBRE', 'DOMICILIO', 'TELÉFONOS', 'COBRADOR', '¿MOROSO?'))
    print("-".rjust(154, '-'))

    for x in datos:
        i_d, soc, nic, fac, cob, tar, rut, ult, u_a, fec, mor, c_f, u_r, paga, op_cob, nom_alt, dom_alt = x
        cob = caja.obtener_nom_cobrador(cob)
        nro, nom, dni, te_1, te_2, mail, dom, loc, c_p, f_n, f_a, act = rend.obtener_datos_socio(soc)

        if nom_alt != None:
            nom = f"[{nom_alt}]"

        if dom_alt != None:
            dom = f"[{dom_alt}]"

        if te_1 != None and te_2 != None:
            tel = f"{te_1} / {te_2}"

        elif te_1 != None and te_2 == None:
            tel = str(te_1)

        elif te_1 == None and te_2 != None:
            tel = str(te_2)

        elif te_1 == None and te_2 == None:
            tel = "N/D"

        if mor == 1:
            mor = 'SI'

        elif mor == 0:
            mor = 'NO'

        print("{:<10} {:<38} {:<38} {:<35} {:<20} {:<10}".format(f'{soc}'.rjust(6, '0'), nom[0:38], dom[0:38], tel[0:35], cob, f'   {mor}'))
    print("-".rjust(154, '-'))
    print()


def buscar_op_cob(id_cobrador: int):
    """Recupera de la base de datos la información de una o más operaciones a
    partir del ID de cobrador, luego la imprime en una tabla en la pantalla

    :param id_cobrador: ID del cobrador a buscar.
    :type id_cobrador: int
    """
    with  sql.connect(mant.DATABASE) as conn:
        cursor = conn.cursor()
        instruccion = f"SELECT * FROM operaciones WHERE cobrador = '{id_cobrador}'"
        cursor.execute(instruccion)
        datos = cursor.fetchall()

    cobrador = caja.obtener_nom_cobrador(id_cobrador)
    
    print()
    print(f"COBRADOR: {id_cobrador} - {cobrador}")
    print()
    print("OPERACIONES:")
    print("-".rjust(155, '-'))
    print("{:<10} {:<10} {:<12} {:<42} {:<42} {:<25} {:<10}".format('N° SOCIO', 'N° OPER.', 'COD.NICHO','APELLIDO Y NOMBRE', 'DOMICILIO', 'TELÉFONOS', '¿MOROSO?'))
    print("-".rjust(155, '-'))
    
    for x in datos:
        id_op, soc, nic, fac, cob, tar, rut, ult, u_a, fec, mor, c_f, u_r, paga, op_cob, nom_alt, dom_alt = x
        nro, nom, dni, te_1, te_2, mail, dom, loc, c_p, f_n, f_a, act = rend.obtener_datos_socio(soc)
    
        if nom_alt != None:
            nom = f"[{nom_alt}]"
    
        if dom_alt != None:
            dom = f"[{dom_alt}]"
    
        if nom_alt != None:
            nom = f"[{nom_alt}]"
    
        if dom_alt != None:
            dom = f"[{dom_alt}]"
    
        if te_1 != None and te_2 != None:
            tel = f"{te_1} / {te_2}"
    
        elif te_1 != None and te_2 == None:
            tel = str(te_1)
    
        elif te_1 == None and te_2 != None:
            tel = str(te_2)
    
        elif te_1 == None and te_2 == None:
            tel = "N/D"
    
        if mor == 1:
            mor = 'SI'
    
        elif mor == 0:
            mor = 'NO'
    
        print("{:<10} {:<10} {:<12} {:<42} {:<42} {:<25} {:<10}".format(f'{soc}'.rjust(6, '0'), f'{id_op}'.rjust(7, '0'), f'{nic}'.rjust(10, '0'), nom[0:42], dom[0:42], tel[0:25], f'   {mor}'))
    print("-".rjust(155, '-'))
    print()


def buscar_op_nom_alt(nom_alt: str):
    """Recupera de la base de datos la información de una o más operaciones a
    partir del nombre alternativo, luego la imprime en una tabla en la pantalla.

    Permite búsqueda inexacta y el uso de comodín (%).

    :param nom_alt: Nombre alternativo (o parte de él) a buscar.
    :type nom_alt: str
    """
    try:
        with sql.connect(mant.DATABASE) as conn:
            cursor = conn.cursor()
            instruccion = f"SELECT * FROM operaciones WHERE nombre_alt ilike '%{nom_alt}%'"
            cursor.execute(instruccion)
            datos = cursor.fetchall()

        print()
        print("***********************************************************************************************************************************************************")

        for x in datos:
            i_d, soc, nic, fac, cob, tar, rut, ult, u_a, fec, mor, c_f, u_r, paga, op_cob, nom_alt, dom_alt = x
            buscar_op_nro_socio(soc)

            print("***********************************************************************************************************************************************************")
        print()
        input("Presione la tecla enter para continuar... ")

    except sql.errors.SyntaxError:
        print()
        print("         ERROR. Nombre inválido. No se pueden utilizar comillas simples (') en las busquedas")
        print()
        return
    except:
        mant.log_error()
        print()
        input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
        print()
        return


def buscar_op_dom_alt(dom_alt: str):
    """Recupera de la base de datos la información de una o más operaciones a partir
    del domicilio alternativo, luego la imprime en una tabla en la pantalla.

    Permite búsqueda inexacta y el uso de comodín (%).

    :param nom_alt: Domicilio alternativo (o parte de él) a buscar.
    :type nom_alt: str
    """
    try:
        with sql.connect(mant.DATABASE) as conn:
            cursor = conn.cursor()
            instruccion = f"SELECT * FROM operaciones WHERE domicilio_alt ilike '%{dom_alt}%'"
            cursor.execute(instruccion)
            datos = cursor.fetchall()

        print()
        print("***********************************************************************************************************************************************************")

        for x in datos:
            i_d, soc, nic, fac, cob, tar, rut, ult, u_a, fec, mor, c_f, u_r, paga, op_cob, nom_alt, dom_alt = x
            buscar_op_nro_socio(soc)
            print("***********************************************************************************************************************************************************")
        print()        
        input("Presione la tecla enter para continuar... ")

    except sql.errors.SyntaxError:
        print()
        print("         ERROR. Nombre inválido. No se pueden utilizar comillas simples (') en las busquedas")
        print()
        return
    except:
        mant.log_error()
        print()
        input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
        print()
        return


def buscar_op_cobol(op_cobol: int):
    """Recupera de la base de datos la información de una o más operaciones a
    partir del número de operación utilizado en el sistema antiguo, luego la
    imprime en una tabla en la pantalla.

    :param op_cobol: Número de operación de Cobol a buscar.
    :type op_cobol: int
    """
    with sql.connect(mant.DATABASE) as conn:
        cursor = conn.cursor()
        instruccion = f"SELECT * FROM operaciones WHERE op_cobol = {op_cobol}"
        cursor.execute(instruccion)
        datos = cursor.fetchall()

    print()
    print("***********************************************************************************************************************************************************")
    for x in datos:
        i_d, soc, nic, fac, cob, tar, rut, ult, u_a, fec, mor, c_f, u_r, paga, op_cob, nom_alt, dom_alt = x
        buscar_op_nro_socio(soc)
        print("***********************************************************************************************************************************************************")
    print()        
    print()


def obtener_op_morosos() -> list:
    """Recupera de la base de datos todas las operaciónes marcadas
    como morosas y las retorna en una lista.

    :rtype: list
    """
    with sql.connect(mant.DATABASE) as conn:
        cursor = conn.cursor()
        instruccion = f"SELECT * FROM operaciones WHERE moroso = '{1}'"
        cursor.execute(instruccion)
    datos = cursor.fetchall()
    return datos


def buscar_op_morosos():
    """Recupera de la base de datos la información de todas las operaciones
    marcadas como morosas, luego la imprime en una tabla en la pantalla.
    """
    datos = obtener_op_morosos()

    print("OPERACIONES MOROSAS:")
    print("-".rjust(157, '-'))
    print("{:<8} {:<8} {:<10} {:<42} {:<42} {:<30} {:<12}".format('N° SOCIO', 'N° OPER.', 'COD.NICHO','APELLIDO Y NOMBRE', 'DOMICILIO', 'TELÉFONOS', 'ÚLTIMO PAGO'))
    print("-".rjust(157, '-'))

    for x in datos:
        id_op, soc, nic, fac, cob, tar, rut, ult, u_a, fec_u_p, mor, c_f, u_r, paga, op_cob, nom_alt, dom_alt = x
        nro, nom, dni, te_1, te_2, mail, dom, loc, c_p, f_n, f_a, act = rend.obtener_datos_socio(soc)

        if nom_alt != None:
            nom = f"[{nom_alt}]"

        if dom_alt != None:
            dom = f"[{dom_alt}]"

        if nom_alt != None:
            nom = f"[{nom_alt}]"

        if dom_alt != None:
            dom = f"[{dom_alt}]"

        if te_1 != None and te_2 != None:
            tel = f"{te_1} / {te_2}"

        elif te_1 != None and te_2 == None:
            tel = str(te_1)

        elif te_1 == None and te_2 != None:
            tel = str(te_2)

        elif te_1 == None and te_2 == None:
            tel = "N/D"

        if mor == 1:
            mor = 'SI'

        elif mor == 0:
            mor = 'NO'

        print("{:<8} {:<8} {:<10} {:<42} {:<42} {:<30} {:<12}".format(f'{soc}'.rjust(6, '0'), f'{id_op}'.rjust(7, '0'), f'{nic}'.rjust(10, '0'), nom[0:42], dom[0:42], tel[0:30], f'    {fec_u_p}'))
    print("-".rjust(157, '-'))
    print()
   

def buscar_estado_cta(nro_socio: int):
    """Imprime en pantalla una tabla con la información y el
    estado de cuenta de un asociado, luego permite al usuario
    generar un reporte del mismo en formato PDF.

    :param nro_socio: ID de asociado.
    :type nro_socio: int
    """
    nro, nom, dni, te_1, te_2, mail, dom, loc, c_p, f_n, f_a, act = rend.obtener_datos_socio(nro_socio)
    deuda = 0
    deuda_total = 0
    msj = ''
    operaciones = obtener_datos_op_por_nro_socio(nro_socio)
    #solicitudes = buscar_sol_por_nro_socio(nro_socio)
    solicitudes = [] # <- BORRAR CUANDO ESTÉ FUNCIONANDO LA BUSQUEDA ^
    print()
    
    if te_1 != None and te_2 != None:
        tel = f"{te_1} / {te_2}"
    
    elif te_1 != None and te_2 == None:
        tel = str(te_1)
    
    elif te_1 == None and te_2 != None:
        tel = str(te_2)
    
    elif te_1 == None and te_2 == None:
        tel = "N/D"
    
    if mail == None:
        mail = "N/D"
    
    print(f"ASOCIADO: {f'{nro_socio}'.rjust(6, '0')} - {nom}. DNI: {dni}. DOMICILIO: {dom} - TELÉFONOS: {tel} - EMAIL: {mail}")
    print()
    
    if len(operaciones) != 0:   # Operaciones
        print("-----------------------------------------------------------------------------------------------------------------------------------------------------------")
        print("OPERACIONES:")
        print("-----------------------------------------------------------------------------------------------------------------------------------------------------------")
        print("{:<13} {:<11} {:<20} {:<20} {:<10} {:<33} {:<33} {:<8}".format('N° OPERACIÓN', 'COD.NICHO', 'DEUDA', 'COBRADOR', '¿MOROSO?', 'NOMBRE ALT.', 'DOMICILIO ALT.', 'OP.COBOL'))
        print("-----------------------------------------------------------------------------------------------------------------------------------------------------------")
        
        for x in operaciones:
            i_d, soc, nic, fac, cob, tar, rut, ult, u_a, fec, mor, c_f, u_r, paga, op_cob, nom_alt, dom_alt = x
            deuda = float(deuda_por_op(i_d))
            cob = caja.obtener_nom_cobrador(cob)
        
            if mor:
                mor = 'SI'
        
            else:
                mor = 'NO'
        
            if not nom_alt:
                nom_alt = " "
        
            if not dom_alt:
                dom_alt = " "
        
            if not op_cob:
                op_cob = " "
        
            if nic == None:
                nic = '----------'
        
            print("{:<13} {:<11} {:<20} {:<20} {:<10} {:<33} {:<33} {:<8}".format(f'{i_d}'.rjust(7, '0'), f'{nic}'.rjust(10, '0'), f'$ {deuda:.2f}', cob, f'   {mor}', nom_alt[0:33], dom_alt[0:33], str(op_cob).rjust(8, ' ')))
    
    if len(solicitudes) != 0:   # Solicitudes
        print("-----------------------------------------------------------------------------------------------------------------------------------------------------------")
        print("SOLICITUDES PREVENIR:")
        print("-----------------------------------------------------------------------------------------------------------------------------------------------------------")
        print("{:<20} {:<20} {:<20} {:<10} {:<35} {:<35} {:<8}".format('N° SOLICITUD', 'DEUDA', 'COBRADOR', '¿MOROSO?', 'NOMBRE ALT.', 'DOMICILIO ALT.', 'OP.COBOL'))
        print("-----------------------------------------------------------------------------------------------------------------------------------------------------------")
    
    if len(operaciones) != 0 or len(solicitudes) != 0:
        deuda_total = deuda_por_socio(soc)
        print("-----------------------------------------------------------------------------------------------------------------------------------------------------------")
        print(f"TOTAL DEUDA ASOCIADO: $ {deuda_total:.2f}-----".rjust(155, '-'))
        print()
    
    if len(operaciones) == 0 and len(solicitudes) == 0:
        print()
        print("EL ASOCIADO NO POSEE OPERACIONES O SOLICITUDES A SU NOMBRE...")
        print()
    
    else:
        while msj == '':
            msj = input("¿Desea generar un reporte? (S/N) ")
    
            if msj == 'S' or msj == 's' or msj == 'Si' or msj == 'SI' or msj == 'sI' or msj == 'si':
                print()
                print("Generando reporte...")
                print()
                rep.report_estado_cta(nro_socio, nom, dni, fac, dom, te_1, te_2, mail, c_p, loc, act)   # Cuando se active prevenir, tener en cuenta los argumentos
    
            elif msj == 'N' or msj == 'n' or msj == 'No' or msj == 'NO' or msj == 'nO' or msj == 'no':
                print()
            else:
                print()
                print("Debe ingresar S para confirmar o N para cancelar.")
                print()
                msj = ''


def deuda_por_op(id_operacion: int) -> float | int:
    """Recupera de la base de datos la deuda total de una operación
    y la retorna. Si la misma posee deuda previa a la implementación
    de Morella, se suma al total y luego lo retorna.

    :param id_operacion: ID de operación.
    :type id_operacion: int

    :rtype: float or int
    """
    deuda = 0
    
    with sql.connect(mant.DATABASE) as conn:
        cursor = conn.cursor()
        instruccion = f"SELECT * FROM recibos WHERE operacion = '{id_operacion}' AND pago = '0'"
        cursor.execute(instruccion)
        datos = cursor.fetchall()

    for d in datos:
        nro, ope, per, año, pag = d
        i_d, soc, nic, fac, cob, tar, rut, ult, u_a, fec, mor, c_f, u_r, paga, op_cob, nom_alt, dom_alt = rend.obtener_datos_op(ope)
        
        try:
            cod, pan, pis, fil, num, cat, ocu, fall = rend.obtener_datos_nicho(nic)
        
        except UnboundLocalError:
            return deuda + deuda_vieja_por_op(id_operacion)
        except:
            mant.log_error()
            print()
            input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
            print()
            return
        
        i_d, cat, val_mant_bic, val_mant_nob = rend.obtener_categoria(cat)
        
        if fac == 'bicon':
            val = val_mant_bic
        
        elif fac == 'nob':
            val = val_mant_nob
        
        if per[0:3] == 'Doc':
            val = rend.obtener_valor_doc(ope)
        
        deuda += val

    return deuda + deuda_vieja_por_op(id_operacion)


def deuda_vieja_por_op(id_operacion: int) -> float | int:
    """Calcula la deuda, anterior a la implementación de Morella,
    de una operación y la retorna.

    :param id_operacion: ID de operación.
    :type id_operacion: int

    :rtype: float or int
    """
    i_d, soc, nic, fac, cob, tar, rut, ult, u_a, fec, mor, c_f, u_r, paga, op_cob, nom_alt, dom_alt = rend.obtener_datos_op(id_operacion)
    
    try:
        cod, pan, pis, fil, num, cat, ocu, fall = rend.obtener_datos_nicho(nic)
    
    except UnboundLocalError:
        return 0
    except:
        mant.log_error()
        print()
        input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
        print()
        return
    
    i_d, cat, val_mant_bic, val_mant_nob = rend.obtener_categoria(cat)
    
    if fac == 'bicon':
        val = val_mant_bic
    
    elif fac == 'nob':
        val = val_mant_nob
    
    if c_f < 0:
        return abs(c_f) * val
    
    else:
        return 0
    

def buscar_recibos_por_op(id_operacion: int) -> list:
    """Recupera de la base de datos la información de los recibos
    impagos de una operación y los retonra en una lista.

    :param id_operacion: ID de operación.
    :type id_operacion: int

    :rtype: list
    """
    with sql.connect(mant.DATABASE) as conn:
        cursor = conn.cursor()
        instruccion = f"SELECT * FROM recibos WHERE operacion = '{id_operacion}' AND pago = '0'"
        cursor.execute(instruccion)
        datos = cursor.fetchall()
    return datos


def deuda_por_socio(nro_socio: int) -> float | int:
    """Recupera de la base de datos la deuda total de un asociado
    y la retorna.
    
    ### ATENCIÓN:
    Por el momento sólo tiene en cuenta las operaciones, teniendo
    que modificarse en el momento que se active PREVENIR.

    :param nro_socio: ID de asociado.
    :type nro_socio: int

    :rtype: float or int
    """
    deuda = 0
    
    with sql.connect(mant.DATABASE) as conn:
        cursor = conn.cursor()
        instruccion = f"SELECT * FROM operaciones WHERE socio = '{nro_socio}'"
        cursor.execute(instruccion)
        datos = cursor.fetchall()
    
    for d in datos:
            i_d, soc, nic, fac, cob, tar, rut, ult, u_a, fec, mor, c_f, u_r, paga, op_cob, nom_alt, dom_alt = d
            deuda += float(deuda_por_op(i_d))
    
    return deuda


def obtener_datos_op_por_nro_socio(nro_socio: int) -> list:
    """Recupera de la base de datos toda la información de una o más
    operaciones específica a partir de un ID de asociado y la retorna
    en una lista.

    :param nro_socio: ID de asociado.
    :type nro_socio: int

    :rtype: list
    """
    with sql.connect(mant.DATABASE) as conn:
        cursor = conn.cursor()
        instruccion = f"SELECT * FROM operaciones WHERE socio = '{nro_socio}'"
        cursor.execute(instruccion)
        datos = cursor.fetchall()
    return datos


def buscar_nicho_por_op(id_operacion: int) -> str:
    """Recupera de la base de datos el código de nicho correspondiente
    a una operación específica a partir del ID de operación y lo
    retorna.

    :param id_operacion: ID de operación.
    :type id_operacion: int

    :rtype: str
    """
    with sql.connect(mant.DATABASE) as conn:
        cursor = conn.cursor()
        instruccion = f"SELECT nicho FROM operaciones WHERE id = '{id_operacion}'"
        cursor.execute(instruccion)
        datos = cursor.fetchone()
    nicho = datos[0]
    return nicho
