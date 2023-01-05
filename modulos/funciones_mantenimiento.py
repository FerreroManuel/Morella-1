VERSION = '1.3.5.2212'
SHORT_VERSION = VERSION[:3]
TYPE_VERSION = 'RC'

import funciones_rendiciones as rend
import funciones_cuentas as ctas
from traceback import format_exc
import psycopg2 as sql
import psycopg2.errors
import os
from datetime import datetime
from getpass import getpass

os.system(f'TITLE Morella v{VERSION} - MF! Soluciones informáticas')
os.system('color 0a')   # Colores del módulo (Verde sobre negro)
os.system('mode con: cols=160 lines=9999')


def obtener_database():
    if not os.path.isfile("../databases/database.ini"):
        arch = open("../databases/database.ini", "w")
        arch.close()
    with open("../databases/database.ini", "r") as arch:
        db = arch.readline()
    return db
database = obtener_database()
arch_log_error = "../error.log"
arch_ini = "../databases/database.ini"


def iniciar_sesion():
    i_d = 0
    user = input("Usuario: ").lower()
    try:
        i_d, nom, ape, tel, dom, use, pas, pri, act = buscar_usuario_por_user(user)
        if i_d == 0 and nom == 0 and ape == 0:
            return 0, 0, 0, 0, 0, 0, 0, 0, 0
        if act == 1:
            counter = 0
            pw = getpass("Contraseña: ")
            while pw != pas:
                print("Contraseña incorrecta")
                print()
                counter += 1
                if counter == 3:
                    edit_registro('usuarios', 'activo', 2, i_d)
                    print("Su usuario ha sido bloqueado por repetición de claves incorrectas. Comuníquese con un administrador.")
                    i_d = -1
                    nom, ape, tel, dom, use, pas, pri, act = "", "", "", "", "", "", "", ""
                    return i_d, nom, ape, tel, dom, use, pas, pri, act
                print("")
                print
                pw = getpass("Contraseña: ")
            if pw == pas:
                print()
                print(f"Bienvenido/a {nom}, que tengas un buen día.")
                print()
                while pw == "0000":
                    pw_new = str(getpass("Ingrese la nueva contraseña: "))
                    while len(pw_new) < 4:
                        print("La contraseña debe ser de 4 dígitos o más.")
                        pw_new = str(getpass("Ingrese la nueva contraseña: "))
                        print()
                    while pw_new == "0000":
                        print("La contraseña no puede ser 0000.")
                        pw_new = str(getpass("Ingrese la nueva contraseña: "))
                        print()
                    pw_conf = str(getpass("Repita la nueva contraseña: "))
                    print()
                    if pw_new == pw_conf:
                        edit_registro('usuarios', 'pass', str(pw_new), i_d)
                        print("Contraseña actualizada exitosamente.")
                        print()
                        return i_d, nom, ape, tel, dom, use, pw_new, pri, act
                    else:
                        pw = ""
                return i_d, nom, ape, tel, dom, use, pas, pri, act
        elif act == 2:
            print("")
            print("Su usuario se encuentra bloqueado. Comuníquese con un administrador.")
            i_d = -1
            nom, ape, tel, dom, use, pas, pri, act = "", "", "", "", "", "", "", ""
            return i_d, nom, ape, tel, dom, use, pas, pri, act
        else:
            print("")
            print("Usuario inactivo.")
            i_d = -1
            nom, ape, tel, dom, use, pas, pri, act = "", "", "", "", "", "", "", ""
            return i_d, nom, ape, tel, dom, use, pas, pri, act
    except TypeError:
        print("")
        print("Usuario inexistente.")
        i_d = -1
        nom, ape, tel, dom, use, pas, pri, act = "", "", "", "", "", "", "", ""
        return i_d, nom, ape, tel, dom, use, pas, pri, act
    except sql.OperationalError:
        print("")
        print("Usuario inexistente.")
        i_d = -1
        nom, ape, tel, dom, use, pas, pri, act = "", "", "", "", "", "", "", ""
        return i_d, nom, ape, tel, dom, use, pas, pri, act
    except:
        log_error()
        print("")
        input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
        i_d = -1
        nom, ape, tel, dom, use, pas, pri, act = "", "", "", "", "", "", "", ""
        return i_d, nom, ape, tel, dom, use, pas, pri, act


def barra_progreso(progreso, total, titulo:str=None, solo_titulo=False):
    if total:
        porcentaje = 100 * (progreso / float(total))
    else:
        porcentaje = 100
    if solo_titulo:
        if titulo:
            os.system(f'TITLE {titulo}  -  PROGRESO: {porcentaje:.2f}%')
        else:
            os.system(f'TITLE PROGRESO: {porcentaje:.2f}%')
    else:
        barra = ('#' * int(porcentaje) + '-' * (100 - int(porcentaje)))
        print(f"\r [{barra}] {porcentaje:.2f}%", end='\r')
        if titulo:
            os.system(f'TITLE {titulo}  -  PROGRESO: {porcentaje:.2f}%')
        else:
            os.system(f'TITLE PROGRESO: {porcentaje:.2f}%')


def buscar_usuario_por_user(user):
    try:
        conn = sql.connect(database)
    except sql.OperationalError:
        log_error()
        print()
        print("         ERROR. La base de datos no responde. Asegurese de estar conectado a la red y que el servidor se encuentre encendido.")
        print()
        print("         Si es así y el problema persiste, comuníquese con el administrador del sistema.")
        print()
        return 0, 0, 0, 0, 0, 0, 0, 0, 0
    cursor = conn.cursor()
    instruccion = f"SELECT * FROM usuarios WHERE user_name = '{user}'"
    cursor.execute(instruccion)
    datos = cursor.fetchone()
    conn.commit()
    conn.close()
    i_d, nom, ape, tel, dom, use, pas, pri, act = datos
    return i_d, nom, ape, tel, dom, use, pas, pri, act


def buscar_usuario_por_id(idu):
    conn = sql.connect(database)
    cursor = conn.cursor()
    instruccion = f"SELECT * FROM usuarios WHERE id = '{idu}'"
    cursor.execute(instruccion)
    datos = cursor.fetchone()
    conn.commit()
    conn.close()
    i_d, nom, ape, tel, dom, use, pas, pri, act = datos
    return i_d, nom, ape, tel, dom, use, pas, pri, act


def log_error():
    exc = format_exc()
    log_error = open(arch_log_error, 'a')
    log_error.write(f"{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}: \n")
    log_error.write(exc)
    log_error.write("\n_________________________________________________\n\n")
    log_error.close


def reemplazar_comilla(variable):
    if type(variable) == str and "'" in variable:
        variable = variable.replace("'", "´")
    else:
        variable = variable
    return variable


def run_query(query):
    conn = sql.connect(database)
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()
    conn.close()


def run_query_w_par(query, parameters = ()):
    conn = sql.connect(database)
    cursor = conn.cursor()
    cursor.execute(query, parameters)
    conn.commit()
    conn.close()


def delete_row(tabla, parametro1, parametro2):
    parametro2 = reemplazar_comilla(parametro2)
    conn = sql.connect(database)
    cursor = conn.cursor()
    instruccion = f"DELETE FROM {tabla} WHERE {parametro1} = '{parametro2}'"
    cursor.execute(instruccion)
    conn.commit()
    conn.close()


def ult_reg(tabla):
    conn = sql.connect(database)
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {tabla} ORDER BY id DESC LIMIT 1")
    ult_registro = cursor.fetchall()
    conn.commit()
    conn.close()
    ult_reg_list = list(ult_registro[0])
    return ult_reg_list


def buscar_op_por_nicho(cod_nicho):
    conn = sql.connect(database)
    cursor = conn.cursor()
    instruccion = f"SELECT * FROM operaciones WHERE nicho = '{cod_nicho}'"
    cursor.execute(instruccion)
    datos = cursor.fetchall()
    conn.commit()
    conn.close
    return datos


def truncate(n, decimals = 0): 
    multiplier = 10 ** decimals 
    return int(n * multiplier) / multiplier


def mostrar_precios_venta(ret):
    counter = 0
    conn = sql.connect(database)
    cursor = conn.cursor()
    instruccion = f"SELECT * FROM precios_venta ORDER BY id"
    cursor.execute(instruccion)
    datos = cursor.fetchall()
    conn.commit()
    conn.close()
    print("------------------------------------------------------------------------------------------")
    print("{:<4} {:<40} {:<15} {:<15} {:<15}".format('ID','DESCRIPCIÓN', '   PRECIO', '   ANTICIPO', 'CUOTAS (x10)'))
    print("------------------------------------------------------------------------------------------")
    for i in datos:
        counter += 1
        i_d, nom, pre, ant, cuo = i
        print("{:<4} {:<40} {:<15} {:<15} {:<15}".format(f'{i_d}'.rjust(2, " "), nom, f'{pre:.2f}'.rjust(11, ' '), f'{ant:.2f}'.rjust(11, ' '), f'{cuo:.2f}'.rjust(11, ' ')))
    conn.close()
    print("------------------------------------------------------------------------------------------")
    print("")
    if ret == 0:
        input("Presione la tecla enter para continuar... ")
    elif ret == 1:
        return counter


def mostrar_precios_mant(ret):
    counter = 0
    conn = sql.connect(database)
    cursor = conn.cursor()
    instruccion = f"SELECT * FROM cat_nichos ORDER BY id"
    cursor.execute(instruccion)
    datos = cursor.fetchall()
    conn.commit()
    conn.close()
    print("--------------------------------------------------------------------------")
    print("{:<4} {:<40} {:<15} {:<15}".format('ID','CATEGORÍA', 'PRECIO BICON', '  PRECIO NOB'))
    print("--------------------------------------------------------------------------")
    for i in datos:
        counter += 1
        i_d, cat, val_mant_bic, val_mant_nob = i
        print("{:<4} {:<40} {:<15} {:<15}".format(f'{i_d}'.rjust(2, " "), cat, f'{val_mant_bic:.2f}'.rjust(11, ' '), f'{val_mant_nob:.2f}'.rjust(11, ' ')))
    conn.close()
    print("--------------------------------------------------------------------------")
    print("")
    if ret == 0:
        input("Presione la tecla enter para continuar... ")
    elif ret == 1:
        return counter


def mostrar_cuentas_mail(ret):
    conn = sql.connect(database)
    cursor = conn.cursor()
    instruccion = f"SELECT * FROM mail ORDER BY id"
    cursor.execute(instruccion)
    datos = cursor.fetchall()
    conn.commit()
    conn.close()
    print("------------------------------------------------------------------------------------------------------------------------------------------------")
    print("{:<4} {:<20} {:<40} {:<40} {:<40}".format('ID','ETIQUETA','CUENTA EMAIL','SERVIDOR SMTP','USUARIO SMTP'))
    print("------------------------------------------------------------------------------------------------------------------------------------------------")
    for i in datos:
        i_d, etiq, mail, server, user, pas = i
        print("{:<4} {:<20} {:<40} {:<40} {:<40}".format(f'{i_d}'.rjust(2, " "), etiq, mail, server, user))
    conn.close()
    print("------------------------------------------------------------------------------------------------------------------------------------------------")
    print("")
    if ret == 0:
        input("Presione la tecla enter para continuar... ")


def buscar_mail(id):
    conn = sql.connect(database)
    cursor = conn.cursor()
    instruccion = f"SELECT * FROM mail WHERE id = {id}"
    cursor.execute(instruccion)
    datos = cursor.fetchone()
    conn.commit()
    conn.close()
    i_d, etiq, mail, server, user, pw = datos
    return i_d, etiq, mail, server, user, pw


def cambio_precio_venta_manual(id_precio, nuevo_valor):
    anticipo = nuevo_valor/2
    cuota = (anticipo*1.5)/10
    cuota_r = float(truncate(cuota, -2))
    conn = sql.connect(database)
    cursor = conn.cursor()
    instruccion = f"UPDATE precios_venta SET precio = {nuevo_valor}, anticipo = {anticipo}, cuotas = {cuota_r} WHERE id = {id_precio}"
    cursor.execute(instruccion)
    conn.commit()
    conn.close()


def calcular_precio_venta_manual(precio_de_contado):
    anticipo = precio_de_contado/2
    cuota = (anticipo*1.5)/10
    cuota_r = float(truncate(cuota, -2))
    return anticipo, cuota_r


def cambio_precio_venta_porcentaje(porcentaje):
    pcnt = 1+(porcentaje/100)
    conn = sql.connect(database)
    cursor = conn.cursor()
    instruccion = f"SELECT * FROM precios_venta ORDER BY id"
    cursor.execute(instruccion)
    datos = cursor.fetchall()
    conn.commit()
    conn.close()
    for i in datos:
        i_d, nom, pre, ant, cuo = i
        n_pre = pre*pcnt
        n_pre_r = float(truncate(n_pre, -2))
        n_ant = n_pre_r/2
        n_cuo = (n_ant*1.5)/10
        n_cuo_r = float(truncate(n_cuo, -2))
        conn = sql.connect(database)
        cursor = conn.cursor()
        instruccion = f"UPDATE precios_venta SET precio = {n_pre_r}, anticipo = {n_ant}, cuotas = {n_cuo_r} WHERE id = {i_d}"
        cursor.execute(instruccion)
        conn.commit()
        conn.close()


def cambio_precio_mant_manual(id_cat, nuevo_val_mant_bic, nuevo_val_mant_nob):
    conn = sql.connect(database)
    cursor = conn.cursor()
    instruccion = f"UPDATE cat_nichos SET valor_mant_bicon = {nuevo_val_mant_bic}, valor_mant_nob = {nuevo_val_mant_nob} WHERE id = {id_cat}"
    cursor.execute(instruccion)
    conn.commit()
    conn.close()


def cambio_precio_mant_porcentaje(facturacion: str, porcentaje: int):
    """Recupera desde la BD los precios actuales de mantenimiento correspondientes al tipo
    de facturación indicada y los actualiza aumentándolos, de forma redondeada en valores
    múltiplos de 100, según el porcentaje indicado.

    :param facturacion: Tipo de facturación a aumentar (puede ser 'todas', 'bicon' o 'nob')
    :type facturacion: str

    :param porcentaje: Porcentaje a aumentar
    :type porcentaje: int
    """

    pcnt = 1+(porcentaje/100)

    # Recuperación de precios actuales
    with sql.connect(database) as conn:
        cursor = conn.cursor()
        instruccion = f"SELECT * FROM cat_nichos ORDER BY id"
        cursor.execute(instruccion)
        datos = cursor.fetchall()

    # Actualización de precios
    for i in datos:
        i_d, cat, val_mant_bic, val_mant_nob = i

        # Cálculo precio BICON
        if facturacion == 'todas' or facturacion == 'bicon':
            n_vmb = val_mant_bic * pcnt
            n_vmb_t = float(truncate(n_vmb, -2))

        # Cálculo precio NOB
        if facturacion == 'todas' or facturacion == 'nob':
            n_vmn = val_mant_nob * pcnt
            n_vmn_t = float(truncate(n_vmn, -2))

        # Definición de la consulta SQL según facturación seleccionada
        if facturacion == 'todas':
            instruccion = f"UPDATE cat_nichos SET valor_mant_bicon = {n_vmb_t}, valor_mant_nob = {n_vmn_t} WHERE id = {i_d}"
        elif facturacion == 'bicon':
            instruccion = f"UPDATE cat_nichos SET valor_mant_bicon = {n_vmb_t} WHERE id = {i_d}"
        elif facturacion == 'nob':
            instruccion = f"UPDATE cat_nichos SET valor_mant_nob = {n_vmn_t} WHERE id = {i_d}"

        # Registro de nuevos precios
        with sql.connect(database) as conn:
            cursor = conn.cursor()
            cursor.execute(instruccion)


def edit_registro(tabla, parametro1, parametro2, id):
    parametro2 = reemplazar_comilla(parametro2)
    conn = sql.connect(database)
    cursor = conn.cursor()
    instruccion = f"UPDATE {tabla} SET {parametro1} = '{parametro2}' WHERE id = '{id}'"
    cursor.execute(instruccion)
    conn.commit()
    conn.close()


def set_null_registro(tabla, parametro1, parametro2, id):
    conn = sql.connect(database)
    cursor = conn.cursor()
    instruccion = f"UPDATE {tabla} SET {parametro1} = NULL WHERE {parametro2} = '{id}'"
    cursor.execute(instruccion)
    conn.commit()
    conn.close()


def edit_nicho(parametro1, parametro2, cod_nicho):
    parametro2 = reemplazar_comilla(parametro2)
    conn = sql.connect(database)
    cursor = conn.cursor()
    instruccion = f"UPDATE nichos SET {parametro1} = '{parametro2}' WHERE codigo = '{cod_nicho}'"
    cursor.execute(instruccion)
    conn.commit()
    conn.close()


def obtener_panteones():
    conn = sql.connect(database)
    cursor = conn.cursor()
    instruccion = f"SELECT * FROM panteones ORDER BY id"
    cursor.execute(instruccion)
    datos = cursor.fetchall()
    conn.commit()
    conn.close()
    return datos


def obtener_cat_nichos():
    conn = sql.connect(database)
    cursor = conn.cursor()
    instruccion = f"SELECT * FROM cat_nichos ORDER BY id"
    cursor.execute(instruccion)
    datos = cursor.fetchall()
    conn.commit()
    conn.close()
    return datos


def generar_user(nombre, apellido):
    letras = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'ñ', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    tildes = ['á', 'é', 'í', 'ó', 'ú', 'à', 'è', 'ì', 'ò', 'ù', 'â', 'ê', 'î', 'ô', 'û', 'ä', 'ë', 'ï', 'ö', 'ü']
    nombre = str(nombre).lower()
    apellido = str(apellido).lower()
    nom = ""
    ape = ""
    contador = 0
    for n in nombre:
        if n in tildes:
            n = convertir_car_esp(n)
        if n in letras:
            contador += 1
            nom += str(n)
            if contador == 3:
                break
    contador = 0
    for a in apellido:
        if a in tildes:
            a = convertir_car_esp(a)
        if a in letras:
            contador += 1
            ape += str(a)
            if contador == 3:
                break
    login_usuario = f"{ape}{nom}"
    return login_usuario


def convertir_car_esp(letra):
    a = ['á','à','â','ä']
    e = ['é','è','ê','ë']
    i = ['í','ì','î','ï']
    o = ['ó','ò','ô','ö']
    u = ['ú','ù','û','ü']
    if letra in a:
        letra_n = 'a'
    elif letra in e:
        letra_n = 'e'
    elif letra in i:
        letra_n = 'i'
    elif letra in o:
        letra_n = 'o'
    elif letra in u:
        letra_n = 'u'
    else:
        return letra
    return letra_n


def opcion_menu():                                                                                  # OPCIÓN MENÚ PRINCIPAL
    print("")
    print("********** Acciones disponibles **********")
    print("")
    print("   1. Mantenimiento de usuarios")
    print("   2. Mantenimiento de panteones")
    print("   3. Mantenimiento de nichos")
    print("   4. Mantenimiento de cobradores")
    print("   5. Mantenimiento de centros de egresos")
    print("   6. Mantenimiento de precios")
    print("   7. Mantenimiento de mails")
    print("   0. Salir")
    print("")
    try:
        opcion = int(input("Ingrese una opción: "))
        while opcion < 0 or opcion > 7:
            print("")
            print("Opción incorrecta.")
            print("")
            opcion = int(input("Ingrese una opción: "))
    except ValueError: 
        print("Opción incorrecta.")
        opcion = -1
    except:
        log_error()
        print("")
        input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
        opcion -1
    return opcion
    

def menu(idu):                                                                                      # MENÚ PRINCIPAL
    opcion = -1
    while opcion != 0:
        opcion = opcion_menu()
        if opcion == 1:
            menu_usuarios(idu)
        elif opcion == 2:
            menu_panteones(idu)
        elif opcion == 3:
            menu_nichos(idu)
        elif opcion == 4:
            menu_cobradores(idu)
        elif opcion == 5:
            menu_centros_egresos(idu)
        elif opcion == 6:
            menu_precios(idu)
        elif opcion == 7: 
            menu_mails(idu)
        elif opcion == 0:
            return


def opcion_menu_usuarios():                                                                         # OPCIÓN MENÚ DE USUARIOS
    print("")
    print("********** Acciones disponibles **********")
    print("")
    print("   1. Ver usuarios")
    print("   2. Crear nuevo usuario")
    print("   3. Modificar usuario")
    print("   4. Activar usuario")
    print("   5. Inactivar usuario")
    print("   0. Volver")
    print("")
    try:
        opcion = int(input("Ingrese una opción: "))
        while opcion < 0 or opcion > 5:
            print("")
            print("Opción incorrecta.")
            print("")
            opcion = int(input("Ingrese una opción: "))
    except ValueError: 
        print("Opción incorrecta.")
        opcion = -1
    except:
        log_error()
        print("")
        input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
        opcion -1
    return opcion


def menu_usuarios(idu):                                                                             # MENÚ DE USUARIOS
    opcion = -1
    while opcion != 0:
        opcion = opcion_menu_usuarios()
        if opcion == 1:
            mostrar_usuarios(idu)
        elif opcion == 2:
            crear_usuario(idu)
        elif opcion == 3:
            modificar_usuario(idu)
        elif opcion == 4:
            activar_usuario(idu)
        elif opcion == 5:
            inactivar_usuario(idu)
        elif opcion == 0:
            return


def mostrar_usuarios(idu):
    i_d, nom, ape, tel, dom, use, pas, pri, act = buscar_usuario_por_id(idu)
    if pri < 3:
        print("No posee privilegios para realizar esta acción")
        print()
    elif pri >= 3:
        conn = sql.connect(database)
        cursor = conn.cursor()
        instruccion = f"SELECT * FROM usuarios ORDER BY user"
        cursor.execute(instruccion)
        datos = cursor.fetchall()
        conn.commit()
        conn.close()
        print("-".rjust(113, '-'))
        print("{:<7} {:<30} {:<25} {:<30} {:<6} {:<10}".format('USER', 'NOMBRE', 'TELÉFONO', 'DOMICILIO', 'NIVEL', 'ESTADO'))
        print("-".rjust(113, '-'))
        for i in datos:
            id_us, nom, ape, tel, dom, use, pas, pri, act = i
            if act == 0:
                estado = "INACTIVO"
            elif act == 1:
                estado = "ACTIVO"
            elif act == 2:
                estado = "BLOQUEADO"
            print("{:<7} {:<30} {:<25} {:<30} {:<6} {:<10}".format(use, f"{ape} {nom}"[0:30], f"{tel}"[0:25], dom[0:30], f"  {pri}  ", estado))
        conn.close()
        print("-".rjust(113, '-'))
        print("")


def crear_usuario(idu):
    i_d, nom, ape, tel, dom, use, pas, pri, act = buscar_usuario_por_id(idu)
    if pri < 3:
        print("No posee privilegios para realizar esta acción")
        print()
    elif pri >= 3:
        print("Ingrese los datos del nuevo usuario:")
        print()
        nombre_usuario = input("Nombre: ")
        if len(nombre_usuario) < 3:
            print()
            print("         ERROR. El nombre debe contener al menos 3 caracteres. No se realizaron cambios en el registro.")
            print()
            return
        apellido_usuario = input("Apellido: ")
        if len(apellido_usuario) < 3:
            print()
            print("         ERROR. El apellido debe contener al menos 3 caracteres. No se realizaron cambios en el registro.")
            print()
            return
        telefono_usuario = input("Teléfono: ")
        domicilio_usuario = input("Domicilio: ")
        login_usuario = generar_user(nombre_usuario, apellido_usuario)
        pass_usuario = "0000"
        try:
            privilegios_usuario = int(input("Nivel de privilegios (1-4): "))
        except ValueError:
            print("         ERROR. Debe indicar un valor numérico entre el 1 y el 4")
            print()
            return
        except:
            log_error()
            print("")
            input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
            return 
        while privilegios_usuario > pri:
            print()
            print("     ERROR. Los privilegios del nuevo usuario no pueden exceder los propios.")
            print()
            privilegios_usuario = input("Nivel de privilegios: ")
        activo_usuario = 1
        print()
        nombre_usuario = reemplazar_comilla(nombre_usuario)
        apellido_usuario = reemplazar_comilla(apellido_usuario)
        telefono_usuario = reemplazar_comilla(telefono_usuario)
        domicilio_usuario = reemplazar_comilla(domicilio_usuario)
        parameters = str((nombre_usuario, apellido_usuario, telefono_usuario, domicilio_usuario, login_usuario, pass_usuario, privilegios_usuario, activo_usuario))
        query = f"INSERT INTO usuarios (nombre, apellido, telefono, domicilio, user_name, pass, privilegios, activo) VALUES {parameters}"
        try:
            run_query(query)
        except sql.errors.UniqueViolation:
            print()
            print(f"         ERROR. Ya existe un usuario con el nombre {login_usuario}.")
            print()
            return
        print(f"Usuario {login_usuario} creado exitosamente.")
        print()
        print("ANTENCIÓN: Al realizar su primer ingreso deberá colocar la contraseña 0000 y luego se le solicitará la creación de una contraseña.")
        print()
        getpass("Presione enter para continuar... ")
        print()


def opcion_modificar_usuarios():
    print("")
    print("********** Acciones disponibles **********")
    print("")
    print("   1. Modificar nombre")
    print("   2. Modificar apellido")
    print("   3. Modificar teléfono")
    print("   4. Modificar domicilio")
    print("   5. Modificar contraseña")
    print("   6. Modificar privilegios")
    print("   0. Volver")
    print("")
    try:
        opcion = int(input("Ingrese una opción: "))
        while opcion < 0 or opcion > 6:
            print("")
            print("Opción incorrecta.")
            print("")
            opcion = int(input("Ingrese una opción: "))
    except ValueError: 
        print("Opción incorrecta.")
        opcion = -1
    except:
        log_error()
        print("")
        input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
        opcion -1
    return opcion


def modificar_usuario(idu):
    opcion = -1
    i_d, nom, ape, tel, dom, use, pas, pri, act = buscar_usuario_por_id(idu)
    while opcion != 0:
        opcion = opcion_modificar_usuarios()
        print()
        if opcion == 1:     # Modificar nombre
            usuario = str(input("Indique el usuario que desea modificar: "))
            print()
            try:
                i_d_m, nom_m, ape_m, tel_m, dom_m, use_m, pas_m, pri_m, act_m = buscar_usuario_por_user(usuario)
            except TypeError:
                print("         ERROR. Nombre de usuario inexistente")
                return
            except:
                log_error()
                print("")
                input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
                return
            print()
            while pri <= pri_m and i_d != i_d_m:
                print("         ERROR. Sólo pueden modificarse los datos propios o de usuarios de niveles inferiores.")
                print()
                usuario = str(input("Indique el usuario que desea modificar o presione enter para volver: "))
                print()
                if usuario != "":
                    try:
                        i_d_m, nom_m, ape_m, tel_m, dom_m, use_m, pas_m, pri_m, act_m = buscar_usuario_por_user(usuario)
                    except TypeError:
                        print("         ERROR. Nombre de usuario inexistente")
                        return
                    except:
                        log_error()
                        print("")
                        input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
                        return
                elif usuario == "":
                    return
            nuevo_nombre = str(input("Ingrese el nuevo nombre: "))
            if len(nuevo_nombre) < 3:
                print()
                print("         ERROR. El nombre debe contener al menos 3 caracteres. No se realizaron cambios en el registro.")
                print()
                return
            nuevo_user = generar_user(nuevo_nombre, ape_m)
            try:
                edit_registro('usuarios', 'user_name', nuevo_user, i_d_m)
            except sql.errors.UniqueViolation:
                print()
                print(f"         ERROR. Ya existe un usuario con el nombre {nuevo_user}.")
                print()
                return
            edit_registro('usuarios', 'nombre', nuevo_nombre, i_d_m)
            print()
            print(f"Nombre modificado correctamente. El nuevo nombre de usuario es: {nuevo_user}")
            print()
        elif opcion == 2:   # Modificar apellido
            usuario = str(input("Indique el usuario que desea modificar: "))
            print()
            try:
                i_d_m, nom_m, ape_m, tel_m, dom_m, use_m, pas_m, pri_m, act_m = buscar_usuario_por_user(usuario)
            except TypeError:
                print("         ERROR. Nombre de usuario inexistente")
                return
            except:
                log_error()
                print("")
                input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
                return
            print()
            while pri <= pri_m and i_d != i_d_m:
                print("         ERROR. Sólo pueden modificarse los datos propios o de usuarios de niveles inferiores.")
                print()
                usuario = str(input("Indique el usuario que desea modificar o presione enter para volver: "))
                print()
                if usuario != "":
                    try:
                        i_d_m, nom_m, ape_m, tel_m, dom_m, use_m, pas_m, pri_m, act_m = buscar_usuario_por_user(usuario)
                    except TypeError:
                        print("         ERROR. Nombre de usuario inexistente")
                        return
                    except:
                        log_error()
                        print("")
                        input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
                        return
                elif usuario == "":
                    return
            nuevo_apellido = str(input("Ingrese el nuevo apellido: "))
            if len(nuevo_apellido) < 3:
                print()
                print("         ERROR. El apellido debe contener al menos 3 caracteres. No se realizaron cambios en el registro.")
                print()
                return
            nuevo_user = generar_user(nom_m, nuevo_apellido)
            try:
                edit_registro('usuarios', 'user_name', nuevo_user, i_d_m)
            except sql.errors.UniqueViolation:
                print()
                print(f"         ERROR. Ya existe un usuario con el nombre {nuevo_user}.")
                print()
                return
            edit_registro('usuarios', 'apellido', nuevo_apellido, i_d_m)
            print()
            print(f"Apellido modificado correctamente. El nuevo nombre de usuario es: {nuevo_user}")
            print()
        elif opcion == 3:   # Modificar teléfono
            usuario = str(input("Indique el usuario que desea modificar: "))
            print()
            try:
                i_d_m, nom_m, ape_m, tel_m, dom_m, use_m, pas_m, pri_m, act_m = buscar_usuario_por_user(usuario)
            except TypeError:
                print("         ERROR. Nombre de usuario inexistente")
                return
            except:
                log_error()
                print("")
                input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
                return
            print()
            while pri <= pri_m and i_d != i_d_m:
                print("         ERROR. Sólo pueden modificarse los datos propios o de usuarios de niveles inferiores.")
                print()
                usuario = str(input("Indique el usuario que desea modificar o presione enter para volver: "))
                print()
                if usuario != "":
                    try:
                        i_d_m, nom_m, ape_m, tel_m, dom_m, use_m, pas_m, pri_m, act_m = buscar_usuario_por_user(usuario)
                    except TypeError:
                        print("         ERROR. Nombre de usuario inexistente")
                        return
                    except:
                        log_error()
                        print("")
                        input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
                        return
                elif usuario == "":
                    return
            nuevo_telefono = str(input("Ingrese el nuevo teléfono: "))
            edit_registro('usuarios', 'telefono', nuevo_telefono, i_d_m)
            print()
            print(f"Teléfono modificado correctamente.")
            print()
        elif opcion == 4:   # Modificar domicilio
            usuario = str(input("Indique el usuario que desea modificar: "))
            print()
            try:
                i_d_m, nom_m, ape_m, tel_m, dom_m, use_m, pas_m, pri_m, act_m = buscar_usuario_por_user(usuario)
            except TypeError:
                print("         ERROR. Nombre de usuario inexistente")
                return
            except:
                log_error()
                print("")
                input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
                return
            print()
            while pri <= pri_m and i_d != i_d_m:
                print("         ERROR. Sólo pueden modificarse los datos propios o de usuarios de niveles inferiores.")
                print()
                usuario = str(input("Indique el usuario que desea modificar o presione enter para volver: "))
                print()
                if usuario != "":
                    try:
                        i_d_m, nom_m, ape_m, tel_m, dom_m, use_m, pas_m, pri_m, act_m = buscar_usuario_por_user(usuario)
                    except TypeError:
                        print("         ERROR. Nombre de usuario inexistente")
                        return
                    except:
                        log_error()
                        print("")
                        input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
                        return
                elif usuario == "":
                    return
            nuevo_domicilio = str(input("Ingrese el nuevo domicilio: "))
            edit_registro('usuarios', 'domicilio', nuevo_domicilio, i_d_m)
            print()
            print(f"Domicilio modificado correctamente.")
            print()
        elif opcion == 5:   # Modificar contraseña
            if pri < 4:
                counter = 0
                pw_act = getpass("Ingrese su contraseña actual: ")
                print()
                while pw_act != pas:
                    print("Contraseña incorrecta")
                    print()
                    counter += 1
                    if counter == 3:
                        edit_registro('usuarios', 'activo', 2, i_d)
                        print("Su usuario ha sido bloqueado por repetición de claves incorrectas. Comuníquese con un administrador.")
                        exit()
                    pw_act = getpass("Ingrese su contraseña actual: ")
                    print()
                if pw_act == pas:
                    pw_new = str(getpass("Ingrese la nueva contraseña: "))
                    print()
                    while len(pw_new) < 4:
                        print("La contraseña debe ser de 4 dígitos o más.")
                        pw_new = str(getpass("Ingrese la nueva contraseña: "))
                        print()
                    while pw_new == "0000":
                        print("La contraseña no puede ser 0000.")
                        pw_new = str(getpass("Ingrese la nueva contraseña: "))
                        print()
                    pw_conf = str(getpass("Repita la nueva contraseña: "))
                    print()
                    if pw_new == pw_conf:
                        edit_registro('usuarios', 'pass', str(pw_new), i_d)
                        print("Contraseña actualizada exitosamente.")
                        print()
                    else:
                        print("         ERROR. Las contraseñas no coinciden.")
                        print()
            elif pri >= 4:
                counter = 0
                pw_act = getpass("Ingrese su contraseña actual: ")
                print()
                while pw_act != pas:
                    print("Contraseña incorrecta")
                    print()
                    counter += 1
                    if counter == 3:
                        edit_registro('usuarios', 'activo', 2, i_d)
                        print("Su usuario ha sido bloqueado por repetición de claves incorrectas. Comuníquese con un administrador.")
                        exit()
                    pw_act = getpass("Ingrese su contraseña actual: ")
                    print()
                if pw_act == pas:
                    usuario = str(input("Indique el usuario que desea modificar: "))
                    print()
                    try:
                        i_d_m, nom_m, ape_m, tel_m, dom_m, use_m, pas_m, pri_m, act_m = buscar_usuario_por_user(usuario)
                    except TypeError:
                        print("         ERROR. Nombre de usuario inexistente")
                        return
                    except:
                        log_error()
                        print("")
                        input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
                        return
                    print()
                    pw_new = str(getpass("Ingrese la nueva contraseña: "))
                    print()
                    while len(pw_new) < 4:
                        print("La contraseña debe ser de 4 dígitos o más.")
                        pw_new = str(getpass("Ingrese la nueva contraseña: "))
                        print()
                    while pw_new == "0000" and i_d_m == i_d:
                        print("La contraseña no puede ser 0000.")
                        pw_new = str(getpass("Ingrese la nueva contraseña: "))
                        print()
                    pw_conf = str(getpass("Repita la nueva contraseña: "))
                    print()
                    if pw_new == pw_conf:
                        edit_registro('usuarios', 'pass', str(pw_new), i_d_m)
                        print("Contraseña actualizada exitosamente.")
                        print()
                    else:
                        print("         ERROR. Las contraseñas no coinciden.")
                        print()
        elif opcion == 6:   # Modificar privilegios
            if pri < 4:
                print("         ERROR. Los privilegios sólo pueden ser modificados por usuarios de nivel 4.")
            elif pri >= 4:
                usuario = str(input("Indique el usuario que desea modificar: "))
                print()
                try:
                    i_d_m, nom_m, ape_m, tel_m, dom_m, use_m, pas_m, pri_m, act_m = buscar_usuario_por_user(usuario)
                except TypeError:
                    print("         ERROR. Nombre de usuario inexistente")
                    return
                except:
                    log_error()
                    print("")
                    input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
                    return
                while i_d_m == i_d or pri <= pri_m:
                    if i_d_m == i_d:
                        print("         ERROR. Un usuario no puede modificarse a si mismo sus privilegios.")
                        print()
                    elif pri <= pri_m:
                        print("         ERROR. Sólo pueden modificarse los dato de usuarios de niveles inferiores.")
                        print()
                    usuario = str(input("Indique el usuario que desea modificar o presione enter para volver: "))
                    print()
                    if usuario == "":
                        return
                    try:
                        i_d_m, nom_m, ape_m, tel_m, dom_m, use_m, pas_m, pri_m, act_m = buscar_usuario_por_user(usuario)
                    except TypeError:
                        print("         ERROR. Nombre de usuario inexistente")
                        print()
                        return
                    except:
                        log_error()
                        input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
                        print("")
                        return
                try:
                    nuevo_privilegio = int(input("Ingrese el nuevo nivel de privilegios (1-4): "))
                except ValueError:
                    print("         ERROR. Debe indicar un valor numérico entre el 1 y el 4")
                    print()
                    return
                except:
                    log_error()
                    print("")
                    input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
                    return
                print()
                while nuevo_privilegio < 1 or nuevo_privilegio > 4:
                    print("         ERROR. Debe indicar un valor numérico entre el 1 y el 4")
                    print()
                    try:
                        nuevo_privilegio = int(input("Ingrese el nuevo nivel de privilegios (1-4): "))
                    except ValueError:
                        print("         ERROR. Debe indicar un valor numérico entre el 1 y el 4")
                        print()
                        return
                    except:
                        log_error()
                        print("")
                        input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
                        return
                edit_registro('usuarios', 'privilegios', nuevo_privilegio, i_d_m)
                print()
                print(f"Privilegios modificados correctamente.")
                print()


def activar_usuario(idu):
    i_d, nom, ape, tel, dom, use, pas, pri, act = buscar_usuario_por_id(idu)
    msj = " "
    if pri < 4:
        print("         ERROR. Los usuarios inactivados sólo pueden ser reactivados por usuarios de nivel 4.")
    elif pri >= 4:
        usuario = str(input("Indique el usuario que desea reactivar: "))
        print()
        try:
            i_d_m, nom_m, ape_m, tel_m, dom_m, use_m, pas_m, pri_m, act_m = buscar_usuario_por_user(usuario)
        except TypeError:
            print("         ERROR. Nombre de usuario inexistente")
            return
        except:
            log_error()
            print("")
            input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
            return
        while i_d_m == i_d:
            print("         ERROR. Un usuario no puede reactivarse a si mismo.")
            try:
                usuario = str(input("Indique el usuario que desea reactivar: "))
                print()
                i_d_m, nom_m, ape_m, tel_m, dom_m, use_m, pas_m, pri_m, act_m = buscar_usuario_por_user(usuario)
            except TypeError:
                print("         ERROR. Nombre de usuario inexistente")
                return
            except:
                log_error()
                print("")
                input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
                return
        msj = ""
        while msj != "S" and msj != "N":
            msj = input(f"¿Seguro que quiere reactivar el usuario <{use_m}>, perteneciente a {nom_m} {ape_m}? (S/N): ")
            if msj == "S" or msj == "s" or msj == "SI" or msj == "si" or msj == "Si" or msj == "sI":
                msj = "S"
                edit_registro('usuarios', 'activo', 1, i_d_m)
                print()
                print("Usuario reactivado exitosamente.")
                print()
                return
            elif msj == "N" or msj == "n" or msj == "NO" or msj == "no" or msj == "No" or msj == "nO":
                msj = "N"
                print("")
                print("No se han realizado cambios en el registro.")
                print("")
                return
            else:
                print("")
                print("         ERROR. Debe indicar S para inactivar o N para cancelar.")
                print("")


def inactivar_usuario(idu):
    i_d, nom, ape, tel, dom, use, pas, pri, act = buscar_usuario_por_id(idu)
    msj = " "
    if pri < 4:
        print("         ERROR. Los usuarios sólo pueden ser dados de baja por usuarios de nivel 4.")
    elif pri >= 4:
        usuario = str(input("Indique el usuario que desea inactivar: "))
        print()
        try:
            i_d_m, nom_m, ape_m, tel_m, dom_m, use_m, pas_m, pri_m, act_m = buscar_usuario_por_user(usuario)
        except TypeError:
            print("         ERROR. Nombre de usuario inexistente")
            return
        except:
            log_error()
            print("")
            input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
            return
        while i_d_m == i_d:
            print("         ERROR. Un usuario no puede darse de baja a si mismo.")
            try:
                usuario = str(input("Indique el usuario que desea inactivar: "))
                print()
                i_d_m, nom_m, ape_m, tel_m, dom_m, use_m, pas_m, pri_m, act_m = buscar_usuario_por_user(usuario)
            except TypeError:
                print("         ERROR. Nombre de usuario inexistente")
                return
            except:
                log_error()
                print("")
                input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
                return
        msj = ""
        while msj != "S" and msj != "N":
            msj = input(f"¿Seguro que quiere dar de baja al usuario <{use_m}>, perteneciente a {nom_m} {ape_m}? (S/N): ")
            if msj == "S" or msj == "s" or msj == "SI" or msj == "si" or msj == "Si" or msj == "sI":
                msj = "S"
                edit_registro('usuarios', 'activo', 0, i_d_m)
                print()
                print("Usuario inactivado exitosamente.")
                print()
                return
            elif msj == "N" or msj == "n" or msj == "NO" or msj == "no" or msj == "No" or msj == "nO":
                msj = "N"
                print("")
                print("No se han realizado cambios en el registro.")
                print("")
                return
            else:
                print("")
                print("         ERROR. Debe indicar S para inactivar o N para cancelar.")
                print("")



    opcion = -1
    while opcion != 0:
        opcion = opcion_menu()
        if opcion == 1:
            menu_usuarios(idu)
        elif opcion == 2:
            menu_panteones(idu)
        elif opcion == 3:
            return
            menu_nichos(idu)
        elif opcion == 4:
            return
            menu_cobradores(idu)
        elif opcion == 5:
            return
            menu_precios(idu)
        elif opcion == 6:
            return
            menu_mails(idu)
        elif opcion == 0:
            return    


def opcion_menu_panteones():                                                                        # OPCIÓN MENÚ DE PANTEONES
    print("")
    print("********** Acciones disponibles **********")
    print("")
    print("   1. Agregar nuevo panteón")
    print("   2. Editar un panteón")
    print("   3. Eliminar un panteón")
    print("   0. Volver")
    print("")
    try:
        opcion = int(input("Ingrese una opción: "))
        while opcion < 0 or opcion > 3:
            print("")
            print("Opción incorrecta.")
            print("")
            opcion = int(input("Ingrese una opción: "))
    except ValueError: 
        print("Opción incorrecta.")
        opcion = -1
    except:
        log_error()
        print("")
        input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
        opcion = -1
    return opcion


def menu_panteones(idu):                                                                            # MENÚ DE PANTEONES
    opcion = -1
    while opcion != 0:
        opcion = opcion_menu_panteones()
        if opcion == 1:
            agregar_panteon(idu)
        elif opcion == 2:
            editar_panteon(idu)
        elif opcion == 3:
            eliminar_panteon(idu)


def agregar_panteon(idu):
    i_d, nom, ape, tel, dom, use, pas, pri, act = buscar_usuario_por_id(idu)
    msj = " "
    print()
    if pri < 3:
        print("         ERROR. No posee los privilegios necesarios para realizar esta operación.")
        print()
        return
    elif pri >= 3:
        nuevo_panteon = input("Ingrese el nombre del nuevo panteon: ").title()
        print()
        print()
        msj = ""
        while msj != "S" and msj != "N":
            nuevo_panteon = reemplazar_comilla(nuevo_panteon)
            msj = str(input(f"¿Seguro que quiere dar de alta el panteón <{nuevo_panteon}>? (S/N): "))
            if msj == "S" or msj == "s" or msj == "SI" or msj == "si" or msj == "Si" or msj == "sI":
                msj = "S"
                print()
                print("Agregando panteón. Aguarde un momento.")
                query = f"INSERT INTO panteones (panteon) VALUES ('{nuevo_panteon}')"
                try:
                    run_query(query)
                except sql.errors.UniqueViolation:
                    print()
                    print("         ERROR. Ya existe un panteón con ese nombre. No se realizaron cambios en el registro.")
                    print()
                    return
                except:
                    log_error()
                    print()
                    input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
                    return
                archivo_categ = open('../databases/categ_ing.mf', 'a', encoding='Utf-8')
                archivo_categ.write(f"\nMantenimiento {nuevo_panteon}")
                archivo_categ.close()
                archivo_pant = open("../databases/panteones.mf", 'a', encoding='Utf-8')
                archivo_pant.write(f'\nMantenimiento {nuevo_panteon}')
                archivo_pant.close()
                print()
                print("Panteón agregado exitosamente.")
                print()
                return
            elif msj == "N" or msj == "n" or msj == "NO" or msj == "no" or msj == "No" or msj == "nO":
                msj = "N"
                print("")
                print("No se han realizado cambios en el registro.")
                print("")
                return
            else:
                print("")
                print("         ERROR. Debe indicar S para dar de alta el panteón o N para cancelar.")
                print("")


def editar_panteon(idu):
    i_d, nom, ape, tel, dom, use, pas, pri, act = buscar_usuario_por_id(idu)
    print()
    if pri < 3:
        print("         ERROR. No posee los privilegios necesarios para realizar esta operación.")
        print()
        return
    elif pri >= 3:
        print("Esta opción no se encuentra disponible por el momento. Comuníquese con el administrador.")


def eliminar_panteon(idu):
    i_d, nom, ape, tel, dom, use, pas, pri, act = buscar_usuario_por_id(idu)
    print()
    if pri < 3:
        print("         ERROR. No posee los privilegios necesarios para realizar esta operación.")
        print()
        return
    elif pri >= 3:
        print("Esta opción no se encuentra disponible por el momento. Comuníquese con el administrador.")


def opcion_menu_nichos():                                                                           # OPCIÓN MENÚ DE NICHOS
    print("")
    print("********** Acciones disponibles **********")
    print("")
    print("   1. Agregar un nicho")
    print("   2. Ocupar un nicho")
    print("   3. Cambiar categoría de un nicho")
    print("   4. Eliminar un nicho")
    print("   5. Agregar una categoría")
    print("   6. Eliminar una categoría")
    print("   0. Volver")
    print("")
    try:
        opcion = int(input("Ingrese una opción: "))
        while opcion < 0 or opcion > 6:
            print("")
            print("Opción incorrecta.")
            print("")
            opcion = int(input("Ingrese una opción: "))
    except ValueError: 
        print("Opción incorrecta.")
        opcion = -1
    except:
        log_error()
        print("")
        input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
        opcion = -1
    return opcion


def menu_nichos(idu):                                                                               # MENÚ DE NICHOS
    opcion = -1
    while opcion != 0:
        opcion = opcion_menu_nichos()
        if opcion == 1:
            alta_nicho(idu, 0)
        elif opcion == 2:
            ocupar_nicho(idu)
        elif opcion == 3:
            cambiar_cat_nicho(idu)
        elif opcion == 4:
            eliminar_nicho(idu)
        elif opcion == 5:
            agregar_categoria(idu)
        elif opcion == 6:
            eliminar_categoria(idu)
        elif opcion == 0:
            return


def alta_nicho(idu, ret):
    msj = " "
    i_d, nom, ape, tel, dom, use, pas, pri, act = buscar_usuario_por_id(idu)
    if pri < 2:
        print()
        print("         ERROR. No posee los privilegios necesarios para realizar esta acción.")
        print()
    else:
        print("*** Alta nuevo nicho ***")
        print()
        print("Indique número de panteón: ")
        datos = obtener_panteones()
        counter = 0
        for i in datos:
            counter += 1
            i_d_pan, n_pan = i
            print(f"    * {i_d_pan}. {n_pan}")
        print()
        try:
            panteon = int(input("Panteón: "))
        except ValueError:
            print("         ERROR. Debe ingresar un dato de tipo numérico.")
            print()
            return
        except:
            log_error()
            print("")
            input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
            return
        while panteon < 1 or panteon > counter:
            print("         ERROR. Debe indicar un nro. de panteón válido.")
            print()
            try:
                panteon = int(input("Panteón: "))
            except ValueError:
                print("         ERROR. Debe ingresar un dato de tipo numérico.")
                print()
                return
            except:
                log_error()
                print("")
                input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
                return
        piso = input("Indique el piso: ").upper()
        if len(piso) < 1 or len(piso) > 2:
            print("         ERROR. No debe ocupar más de dos caracteres.")
            print()
            return
        if "'" in piso:
            print("         ERROR. No se puede utilizar comillas simples (').")
            print()
            return
        try:
            fila = int(input("Indique número de fila: "))
            if len(str(fila)) < 1 or len(str(fila)) > 2:
                print("         ERROR. No debe ocupar más de dos caracteres.")
                print()
                return
        except ValueError:
            print("         ERROR. Debe ingresar un dato de tipo numérico.")
            print()
            return
        except:
            log_error()
            print("")
            input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
            return
        try:
            nicho = int(input("Indique número de nicho: "))
            if len(str(nicho)) < 1 or len(str(nicho)) > 4:
                print("         ERROR. No debe ocupar más de cuatro caracteres.")
                print()
                return
        except ValueError:
            print("         ERROR. Debe ingresar un dato de tipo numérico.")
            print()
            return
        except:
            log_error()
            print("")
            input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
            return
        print("Indique categoría del nicho: ")
        datos = obtener_cat_nichos()
        counter = 0
        for i in datos:
            counter += 1
            i_d_cat_nichos, cat_nichos, val_mant_bic, val_mant_nob = i
            print(f"    * {i_d_cat_nichos}. {cat_nichos}")
        print()
        try:
            cat_nicho = int(input("Categoría: "))
        except ValueError:
            print("         ERROR. Debe ingresar un dato de tipo numérico.")
            print()
            return
        except:
            log_error()
            print("")
            input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
            return
        while cat_nicho < 1 or cat_nicho > counter:
            print("         ERROR. Debe indicar una categoría de nicho válida.")
            print()
            try:
                cat_nicho = int(input("Categoría: "))
                print()
            except ValueError:
                print("         ERROR. Debe ingresar un dato de tipo numérico.")
                print()
                return
            except:
                log_error()
                print("")
                input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
                return
        fallecido = input("Si se encuentra ocupado coloque los datos del fallecido de lo contrario presione enter: ")
        if fallecido == "":
            ocupado = 0
            fallecido = 'NULL'
        else:
            fallecido = reemplazar_comilla(fallecido)
            ocupado = 1
        cod_nicho = f"{str(panteon).rjust(2, '0')}{str(piso).rjust(2, '0')}{str(fila).rjust(2, '0')}{str(nicho).rjust(4, '0')}"
        print()
        msj = ""
        while msj != "S" and msj != "N":
            id_c, cat, val_mant_bic, val_mant_nob = rend.obtener_categoria(cat_nicho)
            msj = str(input(f"¿Seguro que quiere dar de alta el nicho {cat} <{cod_nicho}>? (S/N): "))
            if msj == "S" or msj == "s" or msj == "SI" or msj == "si" or msj == "Si" or msj == "sI":
                msj = "S"
                print()
                print("Agregando nicho. Aguarde un momento.")
                parameters = str((cod_nicho, panteon, str(piso).rjust(2, '0'), str(fila).rjust(2, '0'), str(nicho).rjust(4, '0'), cat_nicho, ocupado, fallecido))
                query = f"INSERT INTO nichos VALUES {parameters}"
                try:
                    run_query(query)
                    print()
                    print("Nicho agregado exitosamente.")
                    print()
                    if ret == 1:
                        return cod_nicho
                except sql.errors.UniqueViolation:
                    print()
                    print("         ERROR. El nicho ya se encuentra cargado en el sistema. No se realizaron cambios en el registro.")
                    if ret == 0:
                        return
                    elif ret == 1:
                        return cod_nicho
                except:
                    log_error()
                    print("")
                    input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
                    if ret == 0:
                        return
                    elif ret == 1:
                        return cod_nicho
            elif msj == "N" or msj == "n" or msj == "NO" or msj == "no" or msj == "No" or msj == "nO":
                msj = "N"
                print("")
                print("No se han realizado cambios en el registro.")
                print("")
                return
            else:
                print("")
                print("         ERROR. Debe indicar S para dar de alta el nicho o N para cancelar.")
                print("")


def ocupar_nicho(idu):
    msj = " "
    i_d, nom, ape, tel, dom, use, pas, pri, act = buscar_usuario_por_id(idu)
    if pri < 2:
        print()
        print("         ERROR. No posee los privilegios necesarios para realizar esta acción.")
        print()
    else:
        print()
        print("*** Ocupar nicho ***")
        print()
        cod_nicho = input("Ingrese el código de nicho: ").upper()
        print()
        try:
            cod, pan, pis, fil, num, cat, ocu, fall = rend.obtener_datos_nicho(cod_nicho)
        except UnboundLocalError:
            print("         ERROR. El nicho indicado no se encuentra dado de alta.")
            return
        except:
            log_error()
            print("")
            input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
            return
        if ocu == 1:
            msj = ""
            while msj != "S" and msj != "N":
                msj = str(input(f"El nicho {cod_nicho} ya se encuentra ocupado por {fall} ¿Quiere modificar los datos del fallecido? (S/N): "))
                print()
                if msj == "S" or msj == "s" or msj == "SI" or msj == "si" or msj == "Si" or msj == "sI":
                    msj = "S"
                    fallecido = input("Ingrese los nuevos datos del fallecido: ")
                    edit_nicho('fallecido', fallecido, cod_nicho)
                    print()
                    print("Datos modificados exitosamente.")
                    print()
                    return
                elif msj == "N" or msj == "n" or msj == "NO" or msj == "no" or msj == "No" or msj == "nO":
                    msj = ""
                    while msj != "S" and msj != "N":
                        msj = str(input(f"¿Quiere cambiar el estado a desocupado? (S/N): "))
                        print()
                        if msj == "S" or msj == "s" or msj == "SI" or msj == "si" or msj == "Si" or msj == "sI":
                            msj = "S"
                            edit_nicho('ocupado', 0, cod_nicho)
                            edit_nicho('fallecido', '', cod_nicho)
                            print()
                            print("Datos modificados exitosamente.")
                            print()
                            return
                        elif msj == "N" or msj == "n" or msj == "NO" or msj == "no" or msj == "No" or msj == "nO":
                            msj = "N"
                            print("")
                            print("No se han realizado cambios en el registro.")
                            print("")
                            return
                        else:
                            print("")
                            print("         ERROR. Debe indicar S para desocupar el nicho o N para cancelar.")
                            print("")
                else:
                    print("")
                    print("         ERROR. Debe indicar S para modificar los datos del fallecido o N para cancelar.")
                    print("")
        else:
            fallecido = input("Ingrese los datos del fallecido: ")
            print()
            edit_nicho('ocupado', 1, cod_nicho)
            edit_nicho('fallecido', fallecido, cod_nicho)
            print()
            print("Datos modificados exitosamente.")
            print()
            return

            
def cambiar_cat_nicho(idu):
    msj = " "
    i_d, nom, ape, tel, dom, use, pas, pri, act = buscar_usuario_por_id(idu)
    if pri < 2:
        print()
        print("         ERROR. No posee los privilegios necesarios para realizar esta acción.")
        print()
    else:
        print()
        print("*** Editar la categoría de un nicho ***")
        print()
        cod_nicho = input("Ingrese el código de nicho: ").upper()
        print()
        try:
            cod, pan, pis, fil, num, cat, ocu, fall = rend.obtener_datos_nicho(cod_nicho)
        except UnboundLocalError:
            print("         ERROR. El nicho indicado no se encuentra dado de alta.")
            return
        except:
            log_error()
            print("")
            input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
            return
        i_d_ant, categ_nicho_ant, val_bic_ant, val_nob_ant = rend.obtener_categoria(cat)
        print(f"El nicho {cod_nicho} pertenece a la categoría {categ_nicho_ant}.")
        print("Indique la nueva categoría: ")
        datos = obtener_cat_nichos()
        counter = 0
        for i in datos:
            counter += 1
            i_d_cat_nichos, cat_nichos, val_mant_bic, val_mant_nob = i
            print(f"    * {i_d_cat_nichos}. {cat_nichos}")
        print()
        try:
            cat_nicho = int(input("Categoría: "))
        except ValueError:
            print("         ERROR. Debe ingresar un dato de tipo numérico.")
            print()
            return
        except:
            log_error()
            print("")
            input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
            return
        while cat_nicho < 1 or cat_nicho > counter:
            print("         ERROR. Debe indicar una categoría de nicho válida.")
            print()
            try:
                cat_nicho = int(input("Categoría: "))
                print()
            except ValueError:
                print("         ERROR. Debe ingresar un dato de tipo numérico.")
                print()
                return
            except:
                log_error()
                print("")
                input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
                return
        i_d_ant, nueva_categ_nicho, val_bic_ant, val_nob_ant = rend.obtener_categoria(cat_nicho)
        msj = ""
        while msj != "S" and msj != "N":
            msj = str(input(f"¿Seguro quiere cambiar la categoría del nicho {cod_nicho} de {categ_nicho_ant} a {nueva_categ_nicho}? (S/N): "))
            if msj == "S" or msj == "s" or msj == "SI" or msj == "si" or msj == "Si" or msj == "sI":
                msj = "S"
                edit_nicho('categoria', cat_nicho, cod_nicho)
                print()
                print("Datos modificados exitosamente.")
                print()
                return
            elif msj == "N" or msj == "n" or msj == "NO" or msj == "no" or msj == "No" or msj == "nO":
                msj = "N"
                print("")
                print("No se han realizado cambios en el registro.")
                print("")
                return
            else:
                print("")
                print("         ERROR. Debe indicar S para cambiar la categoría del nicho o N para cancelar.")
                print("")


def eliminar_nicho(idu):
    msj = " "
    i_d, nom, ape, tel, dom, use, pas, pri, act = buscar_usuario_por_id(idu)
    if pri < 2:
        print()
        print("         ERROR. No posee los privilegios necesarios para realizar esta acción.")
        print()
    else:
        print()
        print("*** Eliminar nicho ***")
        print()
        cod_nicho = input("Ingrese el código de nicho: ").upper()
        print()
        try:
            cod, pan, pis, fil, num, cat, ocu, fall = rend.obtener_datos_nicho(cod_nicho)
        except UnboundLocalError:
            print("         ERROR. El nicho indicado no se encuentra dado de alta.")
            return
        except:
            log_error()
            print("")
            input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
            return
        operacion = buscar_op_por_nicho(cod_nicho)
        if ocu == 0 and len(operacion) == 0:
            msj = ""
            while msj != "S" and msj != "N":
                msj = str(input(f"¿Seguro quiere eliminar el nicho {cod_nicho}? (S/N): "))
                if msj == "S" or msj == "s" or msj == "SI" or msj == "si" or msj == "Si" or msj == "sI":
                    msj = "S"
                    delete_row('nichos', 'codigo', cod_nicho)
                    print()
                    print("Datos eliminados exitosamente.")
                    print()
                    return
                elif msj == "N" or msj == "n" or msj == "NO" or msj == "no" or msj == "No" or msj == "nO":
                    msj = "N"
                    print("")
                    print("No se han realizado cambios en el registro.")
                    print("")
                    return
                else:
                    print("")
                    print("         ERROR. Debe indicar S para eliminar el nicho o N para cancelar.")
                    print("")
        elif len(operacion) == 1:
            i_d, soc, nic, fac, cob, tar, rut, ult, u_a, fec, mor, c_f, u_r, paga, op_cob, nom_alt, dom_alt = operacion[0]
            i_d, nom, dni, tel1, tel2, mail, dom, loc, c_p, f_n, f_a, act = ctas.obtener_datos_socio(soc)
            print(f"         ERROR. El nicho {cod_nicho} se encuentra relacionado a la operación nro. {str(i_d).rjust(7, '0')} del asociado {str(soc).rjust(6, '0')} - {nom}")
            print()
            return
        elif ocu == 1:
            print(f"         ERROR. El nicho {cod_nicho} se encuentra ocupado. Cambie el estado antes de eliminarlo.")
            print()
            return


def agregar_categoria(idu):
    msj = " "
    i_d, nom, ape, tel, dom, use, pas, pri, act = buscar_usuario_por_id(idu)
    if pri < 3:
        print()
        print("         ERROR. No posee los privilegios necesarios para realizar esta acción.")
        print()
    else:
        print()
        print("*** Agregar categoría de nicho ***")
        print()
        categoria = input("Ingrese el nombre de la categoría: ").title()
        print()
        while len(categoria) < 3:
            print("El nombre de la categoría debe tener al menos 3 caracteres de largo.")
            categoria = input("Ingrese el nombre de la categoría: ").title()
        try:
            val_mant_bic = int(input("Indique el costo de mantenimiento para operaciones de Bicon: $ "))
        except ValueError:
            print("         ERROR. Se debe indicar un dato de tipo numérico.")
            return
        except:
            log_error()
            print("")
            input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
            return
        print()
        try:
            val_mant_nob = int(input("Indique el costo de mantenimiento para operaciones de NOB: $ "))
        except ValueError:
            print("         ERROR. Se debe indicar un dato de tipo numérico.")
            return
        except:
            log_error()
            print("")
            input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
            return
        print()
        parameters = str((categoria, float(val_mant_bic), float(val_mant_nob)))
        query = f"INSERT INTO cat_nichos (categoria, valor_mant_bicon, valor_mant_nob) VALUES {parameters}"
        try:
            run_query(query)
            print("Categoría agregada exitosamente. Recuerde agregar los precios de compra.")
            print()
        except sql.errors.UniqueViolation:
            print("         ERROR. Ya existe una categoría con ese nombre. No se realizaron cambios en el registro.")
            print()
        except:
            log_error()
            print("")
            input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
            print()
        print()


def eliminar_categoria(idu):
    msj = " "
    i_d, nom, ape, tel, dom, use, pas, pri, act = buscar_usuario_por_id(idu)
    if pri < 3:
        print()
        print("         ERROR. No posee los privilegios necesarios para realizar esta acción.")
        print()
    else:
        print()
        print("*** Eliminar categoría de nicho ***")
        print()
        print("Ingrese el código de categoría: ")
        datos = obtener_cat_nichos()
        counter = 0
        for i in datos:
            counter += 1
            i_d_cat_nichos, cat_nichos, val_mant_bic, val_mant_nob = i
            print(f"    * {i_d_cat_nichos}. {cat_nichos}")
        print()
        try:
            cat_nicho = int(input("Categoría: "))
        except ValueError:
            print("         ERROR. Debe ingresar un dato de tipo numérico.")
            print()
            return
        except:
            log_error()
            print("")
            input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
            return
        while cat_nicho < 1 or cat_nicho > counter:
            print("         ERROR. Debe indicar una categoría de nicho válida.")
            print()
            try:
                cat_nicho = int(input("Categoría: "))
                print()
            except ValueError:
                print("         ERROR. Debe ingresar un dato de tipo numérico.")
                print()
                return
            except:
                log_error()
                print("")
                input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
                return
        i_d, cat, val_mant_bic, val_mant_nob = rend.obtener_categoria(cat_nicho)
        msj = ""
        while msj != "S" and msj != "N":
            msj = str(input(f"¿Seguro quiere eliminar la categoría {cat}? (S/N): "))
            if msj == "S" or msj == "s" or msj == "SI" or msj == "si" or msj == "Si" or msj == "sI":
                msj = "S"
                delete_row('cat_nichos', 'id', cat_nicho)
                print()
                print("Categoría eliminada exitosamente.")
                print()
                return
            elif msj == "N" or msj == "n" or msj == "NO" or msj == "no" or msj == "No" or msj == "nO":
                msj = "N"
                print("")
                print("No se han realizado cambios en el registro.")
                print("")
                return
            else:
                print("")
                print("         ERROR. Debe indicar S para eliminar la categoría o N para cancelar.")
                print("")


def opcion_menu_cobradores():                                                                       # OPCIÓN MENÚ DE COBRADORES
    print("")
    print("********** Acciones disponibles **********")
    print("")
    print("   1. Agregar un cobrador")
    print("   2. Editar un cobrador")
    print("   3. Eliminar un cobrador")
    print("   0. Volver")
    print("")
    try:
        opcion = int(input("Ingrese una opción: "))
        while opcion < 0 or opcion > 3:
            print("")
            print("Opción incorrecta.")
            print("")
            opcion = int(input("Ingrese una opción: "))
    except ValueError: 
        print("Opción incorrecta.")
        opcion = -1
    except:
        log_error()
        print("")
        input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
        opcion = -1
    return opcion


def menu_cobradores(idu):                                                                           # MENÚ DE COBRADORES
    opcion = -1
    while opcion != 0:
        opcion = opcion_menu_cobradores()
        if opcion == 1:
            alta_cobrador(idu)
        elif opcion == 2:
            editar_cobrador(idu)
        elif opcion == 3:
            eliminar_cobrador(idu)
        elif opcion == 0:
            return


def alta_cobrador(idu):
    i_d, nom, ape, tel, dom, use, pas, pri, act = buscar_usuario_por_id(idu)
    msj = " "
    print()
    if pri < 3:
        print("         ERROR. No posee los privilegios necesarios para realizar esta operación.")
        print()
        return
    elif pri >= 3:
        nuevo_cobrador = input("Ingrese el nombre del nuevo cobrador: ").title()
        print()
        print()
        msj = ""
        while msj != "S" and msj != "N":
            nuevo_cobrador = reemplazar_comilla(nuevo_cobrador)
            msj = str(input(f"¿Seguro que quiere dar de alta el cobrador <{nuevo_cobrador}>? (S/N): "))
            if msj == "S" or msj == "s" or msj == "SI" or msj == "si" or msj == "Si" or msj == "sI":
                msj = "S"
                print()
                print("Agregando cobrador. Aguarde un momento.")
                query = f"INSERT INTO cobradores (cobrador) VALUES ('{nuevo_cobrador}')"
                try:
                    run_query(query)
                except sql.errors.UniqueViolation:
                    print()
                    print("         ERROR. Ya existe un cobrador con ese nombre. No se realizaron cambios en el registro.")
                    print()
                    return
                except:
                    log_error()
                    print()
                    input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
                    return
                archivo_cob = open("../databases/cobradores.mf", 'a', encoding='Utf-8')
                archivo_cob.write(f'\n{nuevo_cobrador}')
                archivo_cob.close()
                print()
                print("Cobrador agregado exitosamente.")
                print()
                return
            elif msj == "N" or msj == "n" or msj == "NO" or msj == "no" or msj == "No" or msj == "nO":
                msj = "N"
                print("")
                print("No se han realizado cambios en el registro.")
                print("")
                return
            else:
                print("")
                print("         ERROR. Debe indicar S para dar de alta el cobrador o N para cancelar.")
                print("")


def editar_cobrador(idu):
    i_d, nom, ape, tel, dom, use, pas, pri, act = buscar_usuario_por_id(idu)
    print()
    if pri < 3:
        print("         ERROR. No posee los privilegios necesarios para realizar esta operación.")
        print()
        return
    elif pri >= 3:
        print("Esta opción no se encuentra disponible por el momento. Comuníquese con el administrador.")


def eliminar_cobrador(idu):
    i_d, nom, ape, tel, dom, use, pas, pri, act = buscar_usuario_por_id(idu)
    print()
    if pri < 3:
        print("         ERROR. No posee los privilegios necesarios para realizar esta operación.")
        print()
        return
    elif pri >= 3:
        print("Esta opción no se encuentra disponible por el momento. Comuníquese con el administrador.")


def opcion_menu_centros_egresos():                                                                  # OPCIÓN MENÚ DE CENTRO DE EGRESOS
    print("")
    print("********** Acciones disponibles **********")
    print("")
    print("   1. Agregar centro de egreso")
    print("   2. Modificar centro de egreso")
    print("   2. Eliminar centro de egreso")
    print("   0. Volver")
    print("")
    try:
        opcion = int(input("Ingrese una opción: "))
        while opcion < 0 or opcion > 3:
            print("")
            print("Opción incorrecta.")
            print("")
            opcion = int(input("Ingrese una opción: "))
    except ValueError: 
        print("Opción incorrecta.")
        opcion = -1
    except:
        log_error()
        print("")
        input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
        opcion = -1
    return opcion


def menu_centros_egresos(idu):                                                                      # MENÚ DE CENTRO DE EGRESOS
    opcion = -1
    while opcion != 0:
        opcion = opcion_menu_centros_egresos()
        if opcion == 1:
            alta_centro_egreso(idu)
        elif opcion == 2:
            editar_centro_egreso(idu)
        elif opcion == 3:
            eliminar_centro_egreso(idu)
        elif opcion == 0:
            return


def alta_centro_egreso(idu):
    i_d, nom, ape, tel, dom, use, pas, pri, act = buscar_usuario_por_id(idu)
    print()
    if pri < 3:
        print("         ERROR. No posee los privilegios necesarios para realizar esta operación.")
        print()
        return
    elif pri >= 3:
        print("Esta opción no se encuentra disponible por el momento. Comuníquese con el administrador.")


def editar_centro_egreso(idu):
    i_d, nom, ape, tel, dom, use, pas, pri, act = buscar_usuario_por_id(idu)
    print()
    if pri < 3:
        print("         ERROR. No posee los privilegios necesarios para realizar esta operación.")
        print()
        return
    elif pri >= 3:
        print("Esta opción no se encuentra disponible por el momento. Comuníquese con el administrador.")


def eliminar_centro_egreso(idu):
    i_d, nom, ape, tel, dom, use, pas, pri, act = buscar_usuario_por_id(idu)
    print()
    if pri < 3:
        print("         ERROR. No posee los privilegios necesarios para realizar esta operación.")
        print()
        return
    elif pri >= 3:
        print("Esta opción no se encuentra disponible por el momento. Comuníquese con el administrador.")


def opcion_menu_precios():                                                                          # OPCIÓN MENÚ DE PRECIOS
    print("")
    print("********** Acciones disponibles **********")
    print("")
    print("   1. Precios de venta")
    print("   2. Precios de mantenimiento")
    print("   0. Volver")
    print("")
    try:
        opcion = int(input("Ingrese una opción: "))
        while opcion < 0 or opcion > 2:
            print("")
            print("Opción incorrecta.")
            print("")
            opcion = int(input("Ingrese una opción: "))
    except ValueError: 
        print("Opción incorrecta.")
        opcion = -1
    except:
        log_error()
        print("")
        input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
        opcion = -1
    return opcion


def menu_precios(idu):                                                                              # MENÚ DE PRECIOS
    opcion = -1
    while opcion != 0:
        opcion = opcion_menu_precios()
        if opcion == 1:
            menu_precios_venta(idu)
        elif opcion == 2:
            menu_precios_mant(idu)
        elif opcion == 0:
            return


def opcion_menu_precios_venta():                                                                    # OPCIÓN MENÚ PRECIOS DE VENTA
    print("")
    print("********** Acciones disponibles **********")
    print("")
    print("   1. Ver precios de venta")
    print("   2. Modificar manualmente")
    print("   3. Actualizar por porcentaje")
    print("   0. Volver")
    print("")
    try:
        opcion = int(input("Ingrese una opción: "))
        while opcion < 0 or opcion > 3:
            print("")
            print("Opción incorrecta.")
            print("")
            opcion = int(input("Ingrese una opción: "))
    except ValueError: 
        print("Opción incorrecta.")
        opcion = -1
    except:
        log_error()
        print("")
        input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
        opcio = -1
    return opcion


def menu_precios_venta(idu):                                                                        # MENÚ PRECIOS DE VENTA
    opcion = -1
    while opcion != 0:
        opcion = opcion_menu_precios_venta()
        if opcion == 1:     # Mostrar precios de veneta
            mostrar_precios_venta(0)
        elif opcion == 2:   # Editar precios de venta manualmente
            editar_precios_venta_manual(idu)
        elif opcion == 3:   # Editar precios de venta por porcentaje
            editar_precios_venta_porcent(idu)
        elif opcion == 4:   # INAHABILITADO
            alta_precio(idu)    
        elif opcion == 5:   # INAHABILITADO
            eliminar_precio(idu)
        elif opcion == 0:   # Volver
            return


def editar_precios_venta_manual(idu):
    i_d, nom, ape, tel, dom, use, pas, pri, act = buscar_usuario_por_id(idu)
    print()
    if pri < 2:
        print("         ERROR. No posee los privilegios necesarios para realizar esta operación.")
        print()
        return
    elif pri >= 2:
        print("*** Cambio de precios manual ***")
        print()
        print("Indique el ID de precio que desea modificar: ")
        cant = mostrar_precios_venta(1)
        try:
            id_precio = int(input("ID: "))
            print()
            while id_precio < 1 or id_precio > cant:
                print("         ERROR. Indique un ID válido o presione enter para volver al menú anterior.")
                print()
                id_precio = int(input("ID: "))
                print()
        except ValueError:
            print("         ERROR. El dato solicitado debe ser de tipo numérico.")
            return
        try:
            precio_nuevo = int(input("Indique el nuevo precio de compra en un pago: $ "))
        except ValueError:
            print("         ERROR. El dato solicitado debe ser de tipo numérico.")
            return
        except:
            log_error()
            print("")
            input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
            return
        print()
        print("Actualizado precio...")
        cambio_precio_venta_manual(id_precio, precio_nuevo)
        print()
        print("Precio actualizado exitosamiente")
        return


def editar_precios_venta_porcent(idu):
    i_d, nom, ape, tel, dom, use, pas, pri, act = buscar_usuario_por_id(idu)
    print()
    if pri < 2:
        print("         ERROR. No posee los privilegios necesarios para realizar esta operación.")
        print()
        return
    elif pri >= 2:
        print("*** Actualizar precios por porcentaje ***")
        print()
        try:
            porcentaje = int(input("Indique el porcentaje de aumento a realizar: "))
            print()
        except ValueError:
            print("         ERROR. El dato solicitado debe ser de tipo numérico.")
            print()
            return
        except:
            log_error()
            print("")
            input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
            return
        print("Actualizando precios. No interrumpa el proceso ni apague el sistema...")
        print()
        cambio_precio_venta_porcentaje(porcentaje)
        print("Lista de precios actualizada exitosamente.")
        print()


def alta_precio(idu):       # INAHABILITADO
    i_d, nom, ape, tel, dom, use, pas, pri, act = buscar_usuario_por_id(idu)
    print()
    if pri < 3:
        print("         ERROR. No posee los privilegios necesarios para realizar esta operación.")
        print()
        return
    elif pri >= 3:
        print("*** Alta de precios de venta ***")
        print() 
        nombre = input("Indique el nombre del precio: [ Piso/s - Categoría (fila/s) ] " ).title()
        nombre = reemplazar_comilla(nombre)
        print()
        try:
            precio = int(input("Indique el precio de compra en un pago: $ "))
        except ValueError:
            print("         ERROR. El dato solicitado es de tipo numérico")
            print()
            return
        except:
            log_error()
            print("")
            input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
            return
        print("Registrando nuevo precio...")
        parameters = str((nombre, precio, 1, 1))
        query = f"INSERT INTO precios_venta (nombre, precio, anticipo, cuotas) VALUES {parameters}"
        run_query(query)
        print("Calculando anticipo y cuotas...")
        id_precio, nomb_pr, pr_ft, pr_ant, pr_cuot = ult_reg('precios_venta')
        cambio_precio_venta_manual(id_precio, precio)
        print()
        print("Precio agregado exitosamente.")
        return


def eliminar_precio(idu):   # INAHABILITADO
    i_d, nom, ape, tel, dom, use, pas, pri, act = buscar_usuario_por_id(idu)
    print()
    if pri < 3:
        print("         ERROR. No posee los privilegios necesarios para realizar esta operación.")
        print()
        return
    elif pri >= 3:
        print("*** Eliminar un precio de venta ***")
        print()
        print("Indique el precio que desea eliminar: ")
        mostrar_precios_venta(1)
        try:
            precio = int(input("ID de precio: "))
            print()
        except ValueError:
            print("         ERROR. El dato solicitado debe ser de tipo numérico.")
            print()
            return
        except:
            log_error()
            print("")
            input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
            return
        msj = ""
        while msj != "S" and msj != "N":
            msj = str(input(f"¿Seguro quiere eliminar este precio? (S/N): "))
            if msj == "S" or msj == "s" or msj == "SI" or msj == "si" or msj == "Si" or msj == "sI":
                msj = "S"
                delete_row('precios_venta', 'id', precio)
                print()
                print("Precio eliminado exitosamente.")
                print()
                return
            elif msj == "N" or msj == "n" or msj == "NO" or msj == "no" or msj == "No" or msj == "nO":
                msj = "N"
                print("")
                print("No se han realizado cambios en el registro.")
                print("")
                return
            else:
                print("")
                print("         ERROR. Debe indicar S para eliminar el precio o N para cancelar.")
                print("")


def opcion_menu_precios_mant():                                                                     # OPCIÓN MENÚ PRECIOS DE MANTENIMIENTO
    print("")
    print("********** Acciones disponibles **********")
    print("")
    print("   1. Ver precios de mantenimiento")
    print("   2. Modificar manualmente")
    print("   3. Actualizar por porcentaje")
    print("   0. Volver")
    print("")
    try:
        opcion = int(input("Ingrese una opción: "))
        while opcion < 0 or opcion > 3:
            print("")
            print("Opción incorrecta.")
            print("")
            opcion = int(input("Ingrese una opción: "))
    except ValueError: 
        print("Opción incorrecta.")
        opcion = -1
    except:
        log_error()
        print("")
        input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
        opcion = -1
    return opcion


def menu_precios_mant(idu):                                                                         # MENÚ PRECIOS DE MANTENIMIENTO
    opcion = -1
    while opcion != 0:
        opcion = opcion_menu_precios_mant()
        if opcion == 1:
            mostrar_precios_mant(0)
        elif opcion == 2:
            editar_precios_mant_manual(idu)
        elif opcion == 3:
            editar_precios_mant_porcent(idu)
        elif opcion == 0:
            return


def editar_precios_mant_manual(idu):
    i_d, nom, ape, tel, dom, use, pas, pri, act = buscar_usuario_por_id(idu)
    print()
    if pri < 2:
        print("         ERROR. No posee los privilegios necesarios para realizar esta operación.")
        print()
        return
    elif pri >= 2:
        print("*** Cambio de precios de mantenimiento manual ***")
        print()
        print("Indique el ID de precio que desea modificar: ")
        cant = mostrar_precios_mant(1)
        try:
            id_precio = int(input("ID: "))
            print()
            while id_precio < 1 or id_precio > cant:
                print("         ERROR. Indique un ID válido o presione enter para volver al menú anterior.")
                print()
                id_precio = int(input("ID: "))
                print()
        except ValueError:
            print("         ERROR. El dato solicitado debe ser de tipo numérico.")
            return
        except:
            log_error()
            print("")
            input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
            return
        try:
            precio_bic_nuevo = int(input("Indique el nuevo precio de mantenimiento para BICON: $ "))
        except ValueError:
            print("         ERROR. El dato solicitado debe ser de tipo numérico.")
            return
        except:
            log_error()
            print("")
            input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
            return
        try:
            precio_nob_nuevo = int(input("Indique el nuevo precio de mantenimiento para NOB: $ "))
        except ValueError:
            print("         ERROR. El dato solicitado debe ser de tipo numérico.")
            return
        except:
            log_error()
            print("")
            input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
            return
        print()
        print("Actualizado precios de mantenimiento...")
        cambio_precio_mant_manual(id_precio, precio_bic_nuevo, precio_nob_nuevo)
        print()
        print("Precio actualizado exitosamiente")
        return


def editar_precios_mant_porcent(idu: int):
    """Permite al usuario actualizar los precios de mantenimiento a partir de un porcentaje. El usuario
    puede elegir hacerlo sólo para una distribución de facturación o para todos los precios a la vez.

    Nivel de privilegios mínimo: 2

    :param idu: ID de usuario
    :type idu: int
    """
    i_d, nom, ape, tel, dom, use, pas, pri, act = buscar_usuario_por_id(idu)
    print()
    if pri < 2:
        print("         ERROR. No posee los privilegios necesarios para realizar esta operación.")
        print()
        return
    elif pri >= 2:
        print("*** Actualizar precios de mantenimiento por porcentaje ***")
        print()
        print("")
        print("Elija una distribución:")
        print("")
        print("   1. Bicon")
        print("   2. NOB")
        print("   3. Todas")
        print("   0. Volver")
        print("")
        opcion = -1
        while opcion == -1:
            try:
                opcion = int(input("Ingrese una opción: "))
                if opcion < 0 or opcion > 3:
                    print("")
                    print("Opción incorrecta.")
                    print("")
                    opcion = -1
                elif opcion == 1:
                    facturacion = 'bicon'
                elif opcion == 2:
                    facturacion = 'nob'
                elif opcion == 3:
                    facturacion = 'todas'
                elif opcion == 0:
                    return
            except ValueError: 
                print("Opción incorrecta.")
                opcion = -1
            except:
                log_error()
                print("")
                input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
                print()
                opcion = -1
        try:
            porcentaje = int(input("Indique el porcentaje de aumento a realizar: "))
            print()
        except ValueError:
            print("         ERROR. El dato solicitado debe ser de tipo numérico.")
            print()
            return
        except:
            log_error()
            print("")
            input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
            return
        print("Actualizando precios. No interrumpa el proceso ni apague el sistema...")
        print()
        cambio_precio_mant_porcentaje(facturacion, porcentaje)
        print("Lista de precios actualizada exitosamente.")
        print()
        

def opcion_menu_mails():                                                                            # OPCIÓN MENÚ DE MAILS
    print("")
    print("********** Acciones disponibles **********")
    print("")
    print("   1. Ver cuentas de mail")
    print("   2. Agregar una cuenta de mail")
    print("   3. Editar una cuenta de mail")
    print("   4. Eliminar una cuenta de mail")
    print("   0. Volver")
    print("")
    try:
        opcion = int(input("Ingrese una opción: "))
        while opcion < 0 or opcion > 4:
            print("")
            print("Opción incorrecta.")
            print("")
            opcion = int(input("Ingrese una opción: "))
    except ValueError: 
        print("Opción incorrecta.")
        opcion = -1
    except:
        log_error()
        print("")
        input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
        opcion = -1
    return opcion


def menu_mails(idu):                                                                                # MENÚ DE MAILS
    opcion = -1
    while opcion != 0:
        opcion = opcion_menu_mails()
        if opcion == 1:
            mostrar_cuentas_mail(0)
        elif opcion == 2:
            alta_mail(idu)
        elif opcion == 3:
            editar_mail(idu)
        elif opcion == 4:
            eliminar_mail(idu)
        elif opcion == 0:
            return


def alta_mail(idu):
    i_d, nom, ape, tel, dom, use, pas, pri, act = buscar_usuario_por_id(idu)
    print()
    if pri < 3:
        print("         ERROR. No posee los privilegios necesarios para realizar esta operación.")
        print()
        return
    elif pri >= 3:
        print("*** Agregar una cuenta de mail ***")
        print()
        nueva_etiq = input("Ingrese un nombre para la nueva cuenta de mail: ").lower()
        nueva_etiq = reemplazar_comilla(nueva_etiq)
        print()
        if nueva_etiq == "":
            print("         ERROR. El campo no puede quedar vacío.")
            return
        nuevo_mail = input("Ingrese la cuenta de email: ").lower()
        print()
        if nuevo_mail == "":
            print("         ERROR. El campo no puede quedar vacío.")
            print()
            return
        if type(nuevo_mail) == str and "'" in nuevo_mail:
            print("         ERROR. No se pueden utilizar comillas simples (').")
            print()
            return
        nuevo_server = input("Ingrese el servidor SMTP: ").lower()
        print()
        if nuevo_server == "":
            print("         ERROR. El campo no puede quedar vacío.")
            print()
            return
        if type(nuevo_server) == str and "'" in nuevo_server:
            print("         ERROR. No se pueden utilizar comillas simples (').")
            print()
            return
        nuevo_usuario = input("Ingrese el usuario SMTP: ").lower()
        print()
        if nuevo_usuario == "":
            print("         ERROR. El campo no puede quedar vacío.")
            print()
            return
        if type(nuevo_usuario) == str and "'" in nuevo_usuario:
            print("         ERROR. No se pueden utilizar comillas simples (').")
            print()
            return
        nuevo_pw = getpass("Ingrese la contraseña del email: ")
        print()
        if nuevo_pw == "":
            print("         ERROR. El campo no puede quedar vacío.")
            return
        if type(nuevo_pw) == str and "'" in nuevo_pw:
            print("         ERROR. No se pueden utilizar comillas simples (').")
            print()
            return
        nuevo_pw_conf = getpass("Vuelva a ingresar la contraseña: ")
        print()
        if nuevo_pw == nuevo_pw_conf:
            parameters = str((nueva_etiq, nuevo_mail, nuevo_server, nuevo_usuario, nuevo_pw))
            query = f"INSERT INTO mail (etiqueta, mail, smtp_server, smtp_user, smtp_pass) VALUES {parameters}"
            try:
                run_query(query)
                print("Cuenta de email agregada exitosamente.")
                print()
            except sql.errors.UniqueViolation:
                print("         ERROR. La cuenta que está intentando ingresar ya existe en la base de datos.")
                print()
            except:
                log_error()
                print("")
                input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
                print()
        else:
            print("         ERROR. Las contraseñas no coinciden.")
            print()
            return


def opcion_editar_mail():                                                                           # OPCIÓN MENÚ EDITAR MAIL
    print("")
    print("********** Acciones disponibles **********")
    print("")
    print("   1. Modificar etiqueta")
    print("   2. Modificar cuenta mail")
    print("   3. Modificar servidor SMTP")
    print("   4. Modificar usuario SMTP")
    print("   5. Modificar contraseña")
    print("   0. Volver")
    print("")
    try:
        opcion = int(input("Ingrese una opción: "))
        while opcion < 0 or opcion > 5:
            print("")
            print("Opción incorrecta.")
            print("")
            opcion = int(input("Ingrese una opción: "))
    except ValueError: 
        print("Opción incorrecta.")
        opcion = -1
    except:
        log_error()
        print("")
        input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
        opcion = -1
    return opcion


def editar_mail(idu):                                                                               # MENÚ EDITAR MAIL
    opcion = -1
    i_d, nom, ape, tel, dom, use, pas, pri, act = buscar_usuario_por_id(idu)
    print()
    if pri < 3:
        print("         ERROR. No posee los privilegios necesarios para realizar esta operación.")
        print()
        return
    elif pri >= 3:
        while opcion != 0:
            opcion = opcion_editar_mail()
            print()
            if opcion == 1:     # Editar etiqueta
                mostrar_cuentas_mail(1)
                print()
                try:
                    id_mail = int(input("Indique el ID de la cuenta que desea modificar: "))
                    i_d, etiq, mail, server, user, pw = buscar_mail(id_mail)
                except ValueError:
                    print("         ERROR. El dato solicitado debe ser de tipo numérico.")
                    print()
                    return
                except TypeError:
                    print("         ERROR. ID de mail inexistente")
                    return
                except:
                    log_error()
                    print("")
                    input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
                    return
                print()
                nueva_etiq = str(input("Ingrese la nueva etiqueta: "))
                edit_registro('mail', 'etiqueta', nueva_etiq, id_mail)
                print()
                print(f"Etiqueta modificada correctamente. La nueva etiqueta es: {nueva_etiq}")
                print()
            elif opcion == 2:   # Editar cuenta
                mostrar_cuentas_mail(1)
                print()
                try:
                    id_mail = int(input("Indique el ID de la cuenta que desea modificar: "))
                    i_d, etiq, mail, server, user, pw = buscar_mail(id_mail)
                except ValueError:
                    print("         ERROR. El dato solicitado debe ser de tipo numérico.")
                    print()
                    return
                except TypeError:
                    print("         ERROR. ID de mail inexistente")
                    return
                except:
                    log_error()
                    print("")
                    input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
                    return
                print()
                nueva_cuenta = str(input("Ingrese la nueva cuenta: "))
                edit_registro('mail', 'mail', nueva_cuenta, id_mail)
                print()
                print(f"Cuenta modificada correctamente. La nueva cuenta es: {nueva_cuenta}")
                print()
            elif opcion == 3:   # Editar server
                mostrar_cuentas_mail(1)
                print()
                try:
                    id_mail = int(input("Indique el ID de la cuenta que desea modificar: "))
                    i_d, etiq, mail, server, user, pw = buscar_mail(id_mail)
                except ValueError:
                    print("         ERROR. El dato solicitado debe ser de tipo numérico.")
                    print()
                    return
                except TypeError:
                    print("         ERROR. ID de mail inexistente")
                    return
                except:
                    log_error()
                    print("")
                    input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
                    return
                print()
                nueva_server = str(input("Ingrese el nuevo servidor SMTP: "))
                edit_registro('mail', 'smtp_server', nueva_server, id_mail)
                print()
                print(f"Servidor modificado correctamente. El nuevo servidor es: {nueva_server}")
                print()
            elif opcion == 4:   # Editar user
                mostrar_cuentas_mail(1)
                print()
                try:
                    id_mail = int(input("Indique el ID de la cuenta que desea modificar: "))
                    i_d, etiq, mail, server, user, pw = buscar_mail(id_mail)
                except ValueError:
                    print("         ERROR. El dato solicitado debe ser de tipo numérico.")
                    print()
                    return
                except TypeError:
                    print("         ERROR. ID de mail inexistente")
                    return
                print()
                nuevo_user = str(input("Ingrese el nuevo usuario SMTP: "))
                edit_registro('mail', 'smtp_user', nuevo_user, id_mail)
                print()
                print(f"Usuario modificado correctamente. El nuevo usuario es: {nuevo_user}")
                print()
            elif opcion == 5:   # Editar pass
                if pri < 4:
                    print("         ERROR. No posee los privilegios necesarios para realizar esta operación.")
                    print()
                    return  
                mostrar_cuentas_mail(1)
                print()
                try:
                    id_mail = int(input("Indique el ID de la cuenta que desea modificar: "))
                    i_d, etiq, mail, server, user, pw = buscar_mail(id_mail)
                except ValueError:
                    print("         ERROR. El dato solicitado debe ser de tipo numérico.")
                    print()
                    return
                except TypeError:
                    print("         ERROR. ID de mail inexistente")
                    return
                except:
                    log_error()
                    print("")
                    input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
                    return
                print()
                nuevo_pw = str(getpass("Ingrese la nueva contraseña: "))
                print()
                conf_pw = str(getpass("Ingrese nuevamente la nueva contraseña: "))
                print()
                if nuevo_pw == conf_pw:
                    edit_registro('mail', 'smtp_pass', nuevo_pw, id_mail)
                    print()
                    print(f"Contraseña modificada correctamente.")
                    print()
                else:
                    print("         ERROR. Las contraseñas no coinciden")
                    print()
                    return
            

def eliminar_mail(idu):
    i_d, nom, ape, tel, dom, use, pas, pri, act = buscar_usuario_por_id(idu)
    print()
    if pri < 4:
        print("         ERROR. No posee los privilegios necesarios para realizar esta operación.")
        print()
        return
    else:
        print("*** Eliminar una cuenta de mail ***")
        print()
        print("Indique el ID de la cuenta que desea eliminar: ")
        mostrar_cuentas_mail(1)
        try:
            id_mail = int(input("ID de cuenta: "))
            print()
        except ValueError:
            print("         ERROR. El dato solicitado debe ser de tipo numérico.")
            print()
            return
        except:
            log_error()
            print("")
            input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
            return
        msj = ""
        while msj != "S" and msj != "N":
            msj = str(input(f"¿Seguro quiere eliminar esta cuenta? (S/N): "))
            if msj == "S" or msj == "s" or msj == "SI" or msj == "si" or msj == "Si" or msj == "sI":
                msj = "S"
                delete_row('mail', 'id', id_mail)
                print()
                print("Cuenta eliminada exitosamente.")
                print()
                return
            elif msj == "N" or msj == "n" or msj == "NO" or msj == "no" or msj == "No" or msj == "nO":
                msj = "N"
                print("")
                print("No se han realizado cambios en el registro.")
                print("")
                return
            else:
                print("")
                print("         ERROR. Debe indicar S para eliminar la cuenta o N para cancelar.")
                print("")


def mant_restaurar_admin():
    conn = sql.connect(database)
    telefono = input("Teléfono: ")
    cursor = conn.cursor()
    instruccion = f"UPDATE usuarios SET nombre = 'Manuel', apellido = 'Ferrero', telefono = '{telefono}', domicilio = 'ADMIN', user_name = 'ferman', pass = '155606038', privilegios = 5, activo = 1 WHERE id = 1"
    cursor.execute(instruccion)
    conn.commit()
    conn.close()
    print("Cuenta ADMIN restaurada exitosamente.")
    print()
    getpass("Presione enter para salir...")
    print()


def mant_database():
    loop = -1
    while loop == -1:
        loop = host = input("Host [192.168.100.100]: ").lower()
        print()
        if host == "":
            host = '192.168.100.100'
        host = revisar_host(host)
        if host == 'error':
            print("         ERROR. Ingrese una dirección de host válida.")
            print()
            loop = -1
    dbname = input("Database [bicon]: ")
    if dbname == "":
        dbname = 'bicon'
    print()
    user = input("User [postgres]: ")
    if user == "":
        user = 'postgres'
    print()
    password = ""
    while password == "":
        password = getpass("Password: ")
        print()
        pw_conf = getpass("Repetir password: ")
        print()
        if password != pw_conf:
            print("         ERROR. Las contraseñas no coinciden. Vuelva a intentarlo.")
            print()
            password = ""        
    loop = -1
    while loop == -1:
        try:
            loop = port = input("Port [5432]: ")
            if port == "":
                port = 5432
            else:
                port = int(port)
            print()
        except ValueError:
            print("         ERROR. El dato solicitado debe ser de tipo numérico.")
            print()
            loop= -1
    conexion = f"host={host} dbname={dbname} user={user} password={password} port={port}"
    with open(arch_ini, 'w') as archivo:
        archivo.write(conexion)
    print("Ruta a base de datos actualizada exitosamente.")
    print()
    getpass("Presione enter para salir...")
    print()
    

def revisar_host(host):
    counter = 0
    if type(host) != str:
        return 'error'
    if host == 'localhost':
        return 'localhost'
    for i in host:
        if i == '.':
            counter += 1
    if counter != 3:
        return 'error'
    ip_s1, ip_s2, ip_s3, ip_s4 = host.split(sep='.')
    try:
        if int(ip_s1) < 0 or int(ip_s1) > 255:
            return 'error'
        if int(ip_s2) < 0 or int(ip_s2) > 255:
            return 'error'
        if int(ip_s3) < 0 or int(ip_s3) > 255:
            return 'error'
        if int(ip_s4) < 0 or int(ip_s4) > 255:
            return 'error'
        host = f"{int(ip_s1)}.{int(ip_s2)}.{int(ip_s3)}.{int(ip_s4)}"
    except ValueError:
        return 'error'
    return host


def cerrar_consola():           ################# ¿¿¿¿¿¿¿¿¿¿¿¿????????????
    print("")
    print("")
    print("")
    print("")
    print("")
    print("")
    print("")
    print("")
    print("")
    print("")
    print("")
    print("")
    print("")
    print("")
    print("")
    print("")
    print("")
    print("")
    print("")
    print("")
    print("")
    print("")
    print("")
    print("")
    print("")
    print("")
    print("")
    print("")
    print("")
    print("")
    print("")
    print("")
    print("")
    print("")
    print("")
    print("")
    print("")
    print("")
    print("")
    print(" -----------------------------")
    print("| Ya puede cerrar la consola. |")
    print(" -----------------------------")
    print("")
    print("")
    print("")
    print("")


