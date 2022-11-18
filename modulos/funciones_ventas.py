import funciones_rendiciones as rend
import funciones_mantenimiento as mant
import funciones_cuentas as ctas
import psycopg2 as sql
import psycopg2.errors
import os
from getpass import getpass
from datetime import datetime


os.system(f'TITLE Morella v{mant.VERSION} - MF! Soluciones informáticas')
os.system('color 0B')   # Colores del módulo (Celeste sobre negro)
os.system('mode con: cols=160 lines=9999')


def obtener_database():
    if not os.path.isfile("../databases/database.ini"):
        arch = open("../databases/database.ini", "w")
        arch.close()
    with open("../databases/database.ini", "r") as arch:
        db = arch.readline()
    return db
database = obtener_database()
dia = datetime.now().strftime('%d')
mes = datetime.now().strftime('%m')
año = datetime.now().strftime('%Y')


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
                    mant.edit_registro('usuarios', 'activo', 2, i_d)
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
                        mant.edit_registro('usuarios', 'pass', str(pw_new), i_d)
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
        mant.log_error()
        print("")
        input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
        i_d = -1
        nom, ape, tel, dom, use, pas, pri, act = "", "", "", "", "", "", "", ""
        return i_d, nom, ape, tel, dom, use, pas, pri, act


def buscar_usuario_por_user(user):
    try:
        conn = sql.connect(database)
    except sql.OperationalError:
        mant.log_error()
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


def obtener_precio_venta(id_cat, pis, fil):
    planta_baja = ["00", "0A", "0B", "0C", "0D", "0E", "0G", "0H", "0I", "0M", "0N", "0P", "0Q", "0S", "0U", "0X", "0Y", "0Z", "PB"]
    if id_cat == 1:                                                             # Simple
        if pis in planta_baja:                                                      # Planta baja
            if fil == "02" or fil == "03":                                              # Filas 2 y 3
                id_p_vent = 3
            elif fil == "04":                                                           # Fila 4
                id_p_vent = 4
            elif fil == "05":                                                           # Fila 5
                id_p_vent = 5
            else:
                id_p_vent = 999
        elif pis == "01" or pis[0] == "1" or pis == "02" or pis[0] == "2":          # 1er y 2do piso
            if fil == "01":                                                             # Fila 1
                id_p_vent = 11
            elif fil == "02" or fil == "03":                                            # Filas 2 y 3
                id_p_vent = 12
            elif fil == "04":                                                           # Fila 4
                id_p_vent = 13
            elif fil == "05":                                                           # Fila 5
                id_p_vent = 14
            else:
                id_p_vent = 999
        else:
            id_p_vent = 999
    elif id_cat == 2:                                                           # Simple especial
        if pis in planta_baja:                                                      # Planta baja
            id_p_vent = 1
        elif pis == "01" or pis[0] == "1" or pis == "02" or pis[0] == "2":          # 1er y 2do piso
            id_p_vent = 9
        else:
            id_p_vent = 999
    elif id_cat == 3:                                                           # Doble
        if pis in planta_baja:                                                      # Planta baja
            if fil == "02" or fil == "03":                                              # Filas 2 y 3
                id_p_vent = 6
            elif fil == "04":                                                           # Fila 4
                id_p_vent = 7
            elif fil == "05":                                                           # Fila 5
                id_p_vent = 8
            else:
                id_p_vent = 999
        elif pis == "01" or pis[0] == "1" or pis == "02" or pis[0] == "2":          # 1er y 2do piso
            if fil == "01":                                                             # Fila 1
                id_p_vent = 15
            elif fil == "02" or fil == "03":                                            # Filas 2 y 3
                id_p_vent = 16
            elif fil == "04":                                                           # Fila 4
                id_p_vent = 17
            elif fil == "05":                                                           # Fila 5
                id_p_vent = 18
            else:
                id_p_vent = 999
        else:
            id_p_vent = 999
    elif id_cat == 4:                                                           # Doble especial
        if pis in planta_baja:                                                      # Planta baja
            id_p_vent = 2
        elif pis == "01" or pis[0] == "1" or pis == "02" or pis[0] == "2":          # 1er y 2do piso
            id_p_vent = 10
        else:
            id_p_vent = 999
    elif id_cat == 5:                                                           # Doble vertical
        if pis in planta_baja:                                                      # Planta baja
            if fil == "02" or fil == "03":                                          # Filas 2 y 3
                id_p_vent = 6
            elif fil == "04":                                              # Fila 4
                id_p_vent = 7
            elif fil == "05":                                              # Fila 5
                id_p_vent = 8
            else:
                id_p_vent = 999
        elif pis == "01" or pis[0] == "1" or pis == "02" or pis[0] == "2":          # 1er y 2do piso
            if fil == "01":                                                # Fila 1
                id_p_vent = 15
            elif fil == "02" or fil == "03":                                  # Filas 2 y 3
                id_p_vent = 16
            elif fil == "04":                                              # Fila 4
                id_p_vent = 17
            elif fil == "05":                                              # Fila 5
                id_p_vent = 18
            else:
                id_p_vent = 999
        else:
            id_p_vent = 999
    else:
        id_p_vent = 999
    if id_p_vent == 999:
        print("No fue posible encontar el precio de venta.")
        print()
        loop = -1
        while loop == -1:
            try:
                loop = nuevo_precio = float(input("Ingrese precio de venta de contado: "))
                anticipo, cuota = mant.calcular_precio_venta_manual(nuevo_precio)
                print()
                print(f"Anticipo: $ {anticipo} - Cuotas: 10x $ {cuota}")
                print()
                return 999, 'Precio manual', nuevo_precio, anticipo, cuota
            except ValueError:
                print()
                print("")
                print()
                loop = -1
            except:
                mant.log_error()
                print("")
                input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
                loop = -1
    conn = sql.connect(database)
    cursor = conn.cursor()
    instruccion = f"SELECT * FROM precios_venta WHERE id = '{id_p_vent}'"
    cursor.execute(instruccion)
    datos = cursor.fetchone()
    conn.commit()
    conn.close()
    i_d, nom, pre, ant, cuo = datos
    return i_d, nom, pre, ant, cuo

    
def agregar_datos_comp(id_op):
    print()
    datos_comp = str(input(f"Ingrese los datos complementarios que quiera incluir en la operación nro. {str(id_op).rjust(7, '0')}: "))
    datos_comp = mant.reemplazar_comilla(datos_comp)
    parameters = str((id_op, datos_comp))
    query = f"INSERT INTO datos_complementarios VALUES {parameters}"
    mant.run_query(query)
    print()
    print("Datos agregados exitosamente.")
    print()
    

def buscar_socio_dni(dni):
    conn = sql.connect(database)
    cursor = conn.cursor()
    instruccion = f"SELECT * FROM socios WHERE dni = '{dni}'"
    cursor.execute(instruccion)
    datos = cursor.fetchall()
    conn.commit()
    conn.close()
    return datos[0]


def obtener_localidad(c_p):
    conn = sql.connect(database)
    cursor = conn.cursor()
    instruccion = f"SELECT localidad FROM cod_post WHERE cp = {c_p}"
    cursor.execute(instruccion)
    datos = cursor.fetchone()
    conn.commit()
    conn.close()
    return datos[0]


def obtener_cobradores():
    conn = sql.connect(database)
    cursor = conn.cursor()
    instruccion = f"SELECT * FROM cobradores ORDER BY id"
    cursor.execute(instruccion)
    datos = cursor.fetchall()
    conn.commit()
    conn.close()
    return datos


def obtener_datos_complementarios(id_op):
    conn = sql.connect(database)
    cursor = conn.cursor()
    instruccion = f"SELECT * FROM datos_complementarios WHERE id_op = {id_op}"
    cursor.execute(instruccion)
    datos = cursor.fetchone()
    conn.commit()
    conn.close()
    id_op, dat_comp = datos
    return dat_comp


def ult_reg(tabla, columna):
    conn = sql.connect(database)
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {tabla} ORDER BY {columna} DESC LIMIT 1")
    ult_registro = cursor.fetchall()
    conn.commit()
    conn.close()
    ult_reg_list = list(ult_registro[0])
    return ult_reg_list


def edit_registro_socio(parametro1, parametro2, id):
    parametro2 = mant.reemplazar_comilla(parametro2)
    conn = sql.connect(database)
    cursor = conn.cursor()
    instruccion = f"UPDATE socios SET {parametro1} = '{parametro2}' WHERE nro_socio = '{id}'"
    cursor.execute(instruccion)
    conn.commit()
    conn.close()


def opcion_menu():                                                                                  # OPC. MENÚ PRINCIPAL
    print("")
    print("********** Acciones disponibles **********")
    print("")
    print("   1. Venta de nicho")
    print("   2. Ingresar nuevo socio")
    print("   3. Modificar datos de socio")
    print("   4. Ingresar nueva operación")
    print("   5. Ver datos de operación")
    print("   6. Modificar datos de operación")
    print("   0. Salir")
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
        mant.log_error()
        print("")
        input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
        print()
        return
    return opcion


def menu(idu):                                                                                      # MENÚ PRINCIPAL
    opcion = -1
    while opcion != 0:
        opcion = opcion_menu()
        if opcion == 1:
            venta_nicho(idu)
        elif opcion == 2:
            crear_socio(idu, 0)
        elif opcion == 3:
            menu_editar_socio(idu)
        elif opcion == 4:
            crear_op(idu, 0, 0)
        elif opcion == 5:
            ver_operacion()
        elif opcion == 6:
            menu_editar_op(idu)
        elif opcion == 0:
            return


def venta_nicho(idu):
    i_d, nom, ape, tel, dom, use, pas, pri, act = buscar_usuario_por_id(idu)
    if pri < 2:
        print()
        print("         ERROR. No posee los privilegios necesarios para realizar esta acción.")
        print()
    else:
        print()
        print("***** Venta de nicho *****")
        print()
        print("   1. Crear un nuevo socio")
        print("   2. Utilizar un socio existente")
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
            mant.log_error()
            print("")
            input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
            print()
            return
        if opcion == 1:
            id_socio, opcion = crear_socio(idu, 1)
        if opcion == 2:
            loop = -1
            while loop == -1:
                try:
                    loop = id_socio = int(input("Indique el nro. de socio o ingrese 0 para buscar: "))
                    if id_socio == 0:
                        ctas.menu_buscar()
                        print()
                        id_socio = int(input("Indique el nro. de socio: "))
                    n_so, nom_socio, dni, te_1, te_2, mail, dom, loc, c_p, f_n, f_a, act = ctas.obtener_datos_socio(id_socio)
                    loop = 1
                except TypeError:
                    print()
                    print("         ERROR. Indique un nro de socio válido.")
                    print()
                    loop = -1    
                except ValueError:
                    print()
                    print("         ERROR. El dato solicitado debe ser de tipo numérico.")
                    print()
                    loop = -1
                except:
                    mant.log_error()
                    print("")
                    input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
                    print()
                    return
        if opcion == 0:
            print()
            return
        id_op = crear_op(idu, id_socio, 1)
        if id_op == -1:
            return
        print()
        id_op, soc, nic, fac, cob, tar, rut, ult, u_a, fec, mor, c_f, u_r, paga, op_cob, nom_alt, dom_alt = rend.obtener_datos_op(id_op)
        n_so, nom_socio, dni, te_1, te_2, mail, dom, loc, c_p, f_n, f_a, act = ctas.obtener_datos_socio(id_socio)
        cod_nic, pan, pis, fil, num, cat, ocu, fall = rend.obtener_datos_nicho(nic)
        i_d, nom_precio, pre, ant, cuo = obtener_precio_venta(cat, pis, fil)
        # msj = ""
        # while msj != "S" and msj != "N":
        #     msj = input(f"¿Quiere agregar datos complementarios a la operación? (S/N)): ")
        #     print()
        #     if msj == "S" or msj == "s" or msj == "SI" or msj == "si" or msj == "Si" or msj == "sI":
        #         agregar_datos_comp(id_op)
        #         msj = "S"
        #         pass
        #     elif msj == "N" or msj == "n" or msj == "NO" or msj == "no" or msj == "No" or msj == "nO":
        #         msj = "N"
        #         pass
        #     else:
        #         print()
        #         print("         ERROR. Debe indicar S para agregar datos o N para cancelar.")
        #         print()
        loop = -1
        while loop == -1:
            try:
                loop = cuotas = int(input("Indique la cantidad de cuotas (1 o 10): "))
                print()
                while cuotas != 1 and cuotas != 10:
                    print("         ERROR. Debe elegir entre un pago o diez.")
                    print()
                    cuotas = int(input("Indique la cantidad de cuotas (1 o 10): "))
                    print()
            except ValueError:
                print("         ERROR. El dato solicitado debe ser de tipo numérico.")
                print()
                loop = -1
            except:
                mant.log_error()
                print("")
                input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
                print()
                return
        if cuotas == 1:
            print(f"El/la socio/a nro. {str(id_socio).rjust(6, '0')}, {nom_socio} abona la compra del nicho {str(nic).rjust(10, '0')} en un pago de $ {float(pre):.2f}")
            print()
            trans = input("Indique el nro de rendición: ")
            print()
            print("Impactando el pago en caja. Por favor no interrumpa el proceso ni apague la computadora...", end="")
            print()
            ingreso = pre
            observ = f"Operación nro. {str(id_op).rjust(7, '0')}"
            parameters = str(('Compra de nicho', f'Nicho {str(nic).rjust(10, "0")}', trans, ingreso, observ, dia, mes, año, 0, idu))
            query = f"INSERT INTO caja (categoria, descripcion, transaccion, ingreso, observacion, dia, mes, año, cerrada, id_user) VALUES {parameters}"
            mant.run_query(query)
            print("[OK!]")
            print()
            print("Proceso finalizado exitosamente.")
            print()
        elif cuotas == 10:
            print(f"El/la socio/a nro. {str(id_socio).rjust(6, '0')}, {nom_socio} abona la compra del nicho {str(nic).rjust(10, '0')} realizando un anticipo de $ {float(ant):.2f} y el resto en 10 cuotas de $ {float(cuo):.2f} c/u.")
            print()
            trans = input("Indique el nro de rendición: ")
            print()
            print("Impactando el pago en caja. Por favor no interrumpa el proceso ni apague la computadora...", end=" ")
            ingreso = ant
            observ = f"Operación nro. {str(id_op).rjust(7, '0')}"
            ult_rec = datetime.now().strftime('%m-&y')
            param_caja = str(('Compra de nicho', f'Nicho {str(nic).rjust(10, "0")}', trans, ingreso, observ, dia, mes, año, 0, idu))
            query_caja = f"INSERT INTO caja (categoria, descripcion, transaccion, ingreso, observacion, dia, mes, año, cerrada, id_user) VALUES {param_caja}"
            mant.run_query(query_caja)
            print("[OK!]")
            print()
            print("Registrando deuda en la base de datos. Por favor no interrumpa el proceso ni apague la computadora...", end=" ")
            param_cuot = str((id_op, cuotas, cuo, ult_rec))
            query_cuot = f"INSERT INTO documentos VALUES {param_cuot}"
            mant.run_query(query_cuot)
            print("[OK!]")
            print()
            print("Proceso finalizado exitosamente.")
            print()


def crear_socio(idu, ret):
    i_d, nom, ape, tel, dom, use, pas, pri, act = buscar_usuario_por_id(idu)
    if pri < 2:
        print()
        print("         ERROR. No posee los privilegios necesarios para realizar esta acción.")
        print()
    else:
        print()
        print("***** Alta de nuevo socio *****")
        print()
        loop = -1
        while loop == -1:
            try:
                loop = documento = int(input("Ingrese nro. de documento (sin puntos) o 0 para volver: "))
                print()
                if documento == 0:
                    return 0, 0
                while documento < 1000000 or documento > 99999999:
                    print("         ERROR. Ingrese un nro de documento válido")
                    print()
                    documento = int(input("Ingrese nro. de documento (sin puntos): "))
                    print()
            except ValueError:
                print("         ERROR. El dato solicitado debe ser de tipo numérico.")
                print()
                loop = -1
            except:
                mant.log_error()
                print("")
                input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
                print()
                return
        try:
            nro_soc, nomb, dni, tel1, tel2, mail, dom, loc, cod_pos, f_nac, f_alt, act = buscar_socio_dni(documento)
            print(f"         ERROR. El documento ya se encuentra ingresado en la base de datos. Nro. de socio: {str(nro_soc).rjust(6, '0')} - {nomb}.")
            return 0, 2
        except UnboundLocalError:
            pass
        except IndexError:
            pass
        loop = -1
        while loop == -1:
            loop = nombre = input("Ingrese apellido y nombre: ").title()
            nombre = mant.reemplazar_comilla(nombre)
            if len(nombre) < 3:
                print()
                print("         ERROR. El campo debe tener al menos 3 caracteres")
                print()
                loop = -1
        loop = -1
        while loop == -1:
            print()
            loop = telefono_1 = input("Ingrese un nro. de teléfono (preferentemente fijo): ").title()
            telefono_1 = mant.reemplazar_comilla(telefono_1)
            print()
            loop = telefono_2 = input("Ingrese un nro. de teléfono (preferentemente celular): ").title()
            telefono_2 = mant.reemplazar_comilla(telefono_2)
            print()
            if len(telefono_1) < 7 and len(telefono_2) < 7:
                print()
                print("         ERROR. Debe indicar al menos un teléfono válido")
                print()
                loop = -1
            if telefono_1 == "":
                telefono_1 = None
            if telefono_2 == "":
                telefono_2 = None
        email = input("Ingrese un email: ").lower()
        if email == "":
            email = None
        print()
        loop = -1
        while loop == -1:
            loop = domicilio = input("Ingrese domicilio : ").title()
            domicilio = mant.reemplazar_comilla(domicilio)
            if len(domicilio) < 3:
                print()
                print("         ERROR. El campo debe tener al menos 3 caracteres")
                print()
                loop = -1
        print()
        loop = -1
        while loop == -1:
            try:
                loop = cod_postal = int(input("Ingrese código postal: "))
                print()
                while cod_postal < 1000 or cod_postal > 9999:
                    print("         ERROR. Ingrese un código postal válido")
                    print()
                    cod_postal = int(input("Ingrese código postal: "))
                    print()
            except ValueError:
                print("         ERROR. El dato solicitado debe ser de tipo numérico.")
                print()
                loop = -1
            except:
                mant.log_error()
                print("")
                input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
                print()
                return
        try:
            localidad = obtener_localidad(cod_postal)
            print(f"Localidad: {localidad}")
            print()
        except TypeError:
            localidad = input("Ingrese localidad: ").title()
            localidad = mant.reemplazar_comilla(localidad)
            print()
            parameters = str((cod_postal, localidad))
            query = f"INSERT INTO cod_post VALUES {parameters}"
            mant.run_query(query)
        f_nacimiento = input("Ingrese fecha de nacimiento (DD/MM/AAAA): ")
        while len(f_nacimiento) != 10 or f_nacimiento[2] != '/' or f_nacimiento[5] != '/':
            print("         ERROR. Ingrese una fecha válida. Recuerde que debe ingresarse con el siguiente formato: (DD/MM/AAAA)")
            print()
            f_nacimiento = input("Ingrese fecha de nacimiento (DD/MM/AAAA): ")        
        print()
        f_alta = datetime.now().strftime('%d/%m/%Y')
        print("Ingresando socio a la base de datos. No interrumpa el proceso ni apague la computadora.")
        parameters = (nombre, documento, telefono_1, telefono_2, email, domicilio, localidad, cod_postal, f_nacimiento, f_alta, 1)
        query = "INSERT INTO socios (nombre, dni, telefono_1, telefono_2, mail, domicilio, localidad, cod_postal, fecha_nacimiento, fecha_alta, activo) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        mant.run_query_w_par(query, parameters)
        print("[OK!]")
        print()
        print("Proceso finalizado exitosamente.")
        print()
        i_d, nom, dni, tel1, tel2, mail, dom, loc, cod_pos, f_nac, f_alt, act = ult_reg("socios", "nro_socio")
        print(f"Se registró con el nro {str(i_d).rjust(6, '0')} y documento {dni} al asociado/a {nom}")
        if ret == 1:
            return i_d, 1
        
            
def opcion_menu_editar_socio():                                                                     # OPC. MENU EDITAR SOCIOS
    print("")
    print("********** Acciones disponibles **********")
    print("")
    print("   1. Editar nombre")
    print("   2. Editar documento")
    print("   3. Editar telefonos")
    print("   4. Editar email")
    print("   5. Editar domicilio")
    print("   6. Editar localidad")
    print("   7. Editar fecha de nacimiento")
    print("   8. Cambiar estado de socio")
    print("   0. Volver")
    print("")
    try:
        opcion = int(input("Ingrese una opción: "))
        while opcion < 0 or opcion > 8:
            print("")
            print("Opción incorrecta.")
            print("")
            opcion = int(input("Ingrese una opción: "))
    except ValueError: 
        print("Opción incorrecta.")
        opcion = -1
    except:
        mant.log_error()
        print("")
        input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
        print()
        return
    return opcion


def menu_editar_socio(idu):                                                                         # MENU EDITAR SOCIOS
    loop = -1
    print("")
    print("********** Modificar datos de socio **********")
    print("")
    while loop == -1:
        try:
            loop = id_socio = int(input("Indique nro. de socio o ingrese 0 para buscar: "))
            print()
            if id_socio == 0:
                ctas.menu_buscar()
                id_socio = int(input("Indique nro. de socio: "))
                print()
        except ValueError:
            print("         ERROR. El dato solicitado debe ser de tipo numérico.")
            print()
            loop = -1
        except UnboundLocalError:
            print("         ERROR. No existe nro. de socio.")
            print()
            loop = -1
        except:
            mant.log_error()
            print("")
            input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
            print()
            return
    opcion = -1
    while opcion != 0:
        try:
            id_soc, nom, dni, te_1, te_2, mail, dom, loc, c_p, f_n, f_a, act = ctas.obtener_datos_socio(id_socio)
        except TypeError:
            print("         ERROR. No existe nro. de socio.")
            print()
            return
        except:
            mant.log_error()
            print("")
            input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
            print()
            return
        if act == 1:
            str_act = 'ACTIVO'
        elif act == 0:
            str_act = 'INACTIVO'
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
        print(f"Socio: {str(id_soc).rjust(6, '0')} - {nom}. DNI: {dni}.")
        print(f"Telefono/s: {tel}. eMail: {mail}. Domicilio: {dom}, {loc} - {c_p}.")
        print(f"Nacimiento: {f_n}. Estado: {str_act}")
        print()
        opcion = opcion_menu_editar_socio()
        if opcion == 1:
            edit_nombre(idu, id_soc)
        elif opcion == 2:
            edit_dni(idu, id_soc)
        elif opcion == 3:
            edit_tel(idu, id_soc)
        elif opcion == 4:
            edit_mail(idu, id_soc)
        elif opcion == 5:
            edit_dom(idu, id_soc)
        elif opcion == 6:
            edit_loc(idu, id_soc)
        elif opcion == 7:
            edit_fec_nac(idu, id_soc)
        elif opcion == 8:
            edit_act(idu, id_soc, act)
        elif opcion == 0:
            return


def edit_nombre(idu, id_soc):
    i_d, nom, ape, tel, dom, use, pas, pri, act = buscar_usuario_por_id(idu)
    if pri < 2:
        print()
        print("         ERROR. No posee los privilegios necesarios para realizar esta acción.")
        print()
    else:
        print("***** Editar nombre de socio *****")
        print()
        nombre_nuevo = input("Ingrese apellido y nombres nuevos: ").title()
        if len(nombre_nuevo) < 3:
            print()
            print("         ERROR. El campo debe tener al menos 3 caracteres")
            print()
            return
        print()
        edit_registro_socio('nombre', nombre_nuevo, id_soc)
        print("Nombre modificado exitosamente.")
        print()


def edit_dni(idu, id_soc):
    i_d, nom, ape, tel, dom, use, pas, pri, act = buscar_usuario_por_id(idu)
    if pri < 2:
        print()
        print("         ERROR. No posee los privilegios necesarios para realizar esta acción.")
        print()
    else:
        print("***** Editar documento de socio *****")
        print()
        loop = -1
        while loop == -1:
            try:
                loop = dni_nuevo = int(input("Ingrese documento nuevo (Sin puntos): "))
                print()
                if dni_nuevo < 1000000 or dni_nuevo > 99999999:
                    print("         ERROR. Ingrese un nro. de documento válido.")
                    print()
                    loop = -1
            except ValueError:
                print("         ERROR. El dato solicitado debe ser de tipo numérico.")
                print()
                loop = -1
            except:
                mant.log_error()
                print("")
                input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
                print()
                return
        try:
            edit_registro_socio('dni', dni_nuevo, id_soc)
            print()
        except sql.errors.UniqueViolation:
            nro_soc, nomb, dni, tel1, tel2, mail, dom, loc, cod_pos, f_nac, f_alt, act = buscar_socio_dni(dni_nuevo)
            print(f"         ERROR. El número de documento ingresado pertenece al socio nro. {str(nro_soc).rjust(6, '0')} - {nomb}.")
            print()
            return
        print("Documento modificado exitosamente.")
        print()


def edit_tel(idu, id_soc):
    i_d, nom, ape, tel, dom, use, pas, pri, act = buscar_usuario_por_id(idu)
    if pri < 2:
        print()
        print("         ERROR. No posee los privilegios necesarios para realizar esta acción.")
        print()
    else:
        loop = -1
        while loop == -1:
            try:
                loop = pos_tel = int(input("¿Qué teléfono desea modificar? (1 o 2) "))
                print()
                if pos_tel < 1 or pos_tel > 2:
                    print("         ERROR. Debe elegir entre 1 o 2.")
                    print()
                    loop = -1
            except ValueError:
                print("         ERROR. El dato solicitado debe ser de tipo numérico.")
                print()
                loop = -1
            except:
                mant.log_error()
                print("")
                input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
                print()
                return
        tel_nuevo = input("Ingrese teléfono nuevo o presione enter para eliminar el teléfono actual: ").title()
        if tel_nuevo == "":
            if pos_tel == 1:
                mant.set_null_registro('socios', 'telefono_1', 'nro_socio', id_soc)
            elif pos_tel == 2:
                mant.set_null_registro('socios', 'telefono_2', 'nro_socio', id_soc)
            print()
            print("Teléfono eliminado exitosamente.")
            print()
            return
        elif len(tel_nuevo) < 7:
            print()
            print("         ERROR. Indique un número de teléfono válido")
            print()
            return
        print()
        if pos_tel == 1:
            edit_registro_socio('telefono_1', tel_nuevo, id_soc)
        elif pos_tel == 2:
            edit_registro_socio('telefono_2', tel_nuevo, id_soc)
        print("Teléfono modificado exitosamente.")
        print()


def edit_mail(idu, id_soc):
    i_d, nom, ape, tel, dom, use, pas, pri, act = buscar_usuario_por_id(idu)
    if pri < 2:
        print()
        print("         ERROR. No posee los privilegios necesarios para realizar esta acción.")
        print()
    else:
        print()
        mail_nuevo = input("Ingrese email nuevo o presione enter para eliminar el actual: ").lower()
        print()
        if mail_nuevo == "":
            mant.set_null_registro('socios', 'mail', 'nro_socio', id_soc)
        else:
            edit_registro_socio('mail', mail_nuevo, id_soc)
        print("Email modificado exitosamente.")
        print()


def edit_dom(idu, id_soc):
    i_d, nom, ape, tel, dom, use, pas, pri, act = buscar_usuario_por_id(idu)
    if pri < 2:
        print()
        print("         ERROR. No posee los privilegios necesarios para realizar esta acción.")
        print()
    else:
        print()
        domicilio_nuevo = input("Ingrese domicilio nuevo: ").title()
        if len(domicilio_nuevo) < 3:
            print()
            print("         ERROR. El campo debe tener al menos 3 caracteres")
            print()
            return
        print()
        edit_registro_socio('domicilio', domicilio_nuevo, id_soc)
        print("Domicilio modificado exitosamente.")
        print()


def edit_loc(idu, id_soc):
    i_d, nom, ape, tel, dom, use, pas, pri, act = buscar_usuario_por_id(idu)
    if pri < 2:
        print()
        print("         ERROR. No posee los privilegios necesarios para realizar esta acción.")
        print()
    else:
        loop = -1
        while loop == -1:
            try:
                loop = cod_postal = int(input("Ingrese código postal: "))
                print()
                while cod_postal < 1000 or cod_postal > 9999:
                    print("         ERROR. Ingrese un código postal válido")
                    print()
                    cod_postal = int(input("Ingrese código postal: "))
                    print()
            except ValueError:
                print("         ERROR. El dato solicitado debe ser de tipo numérico.")
                print()
                loop = -1
            except:
                mant.log_error()
                print("")
                input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
                print()
                return
            try:
                localidad = obtener_localidad(cod_postal)
                print()
                edit_registro_socio('cod_postal', cod_postal, id_soc)
                edit_registro_socio('localidad', localidad, id_soc)
                print("Localidad modificada exitosamente.")
                print()
            except TypeError:
                localidad = input("Ingrese localidad: ").title()
                localidad = mant.reemplazar_comilla(localidad)
                print()
                parameters = str((cod_postal, localidad))
                query = f"INSERT INTO cod_post VALUES {parameters}"
                mant.run_query(query)
                edit_registro_socio('cod_postal', cod_postal, id_soc)
                edit_registro_socio('localidad', localidad, id_soc)
                print("Localidad modificada exitosamente.")
                print()


def edit_fec_nac(idu, id_soc):
    i_d, nom, ape, tel, dom, use, pas, pri, act = buscar_usuario_por_id(idu)
    if pri < 2:
        print()
        print("         ERROR. No posee los privilegios necesarios para realizar esta acción.")
        print()
    else:
        print()
        nacimiento_nuevo = input("Ingrese fecha de nacimiento nueva (DD/MM/AAAA): ")
        while len(nacimiento_nuevo) != 10 or nacimiento_nuevo[2] != '/' or nacimiento_nuevo[5] != '/':
            print("         ERROR. Ingrese una fecha válida. Recuerde que debe ingresarse con el siguiente formato: (DD/MM/AAAA)")
            print()
            nacimiento_nuevo = input("Ingrese fecha de nacimiento (DD/MM/AAAA): ")        
        print()
        edit_registro_socio('fecha_nacimiento', nacimiento_nuevo, id_soc)
        print("Fecha de nacimiento modificada exitosamente.")


def edit_act(idu, id_soc, estado):
    i_d, nom, ape, tel, dom, use, pas, pri, act = buscar_usuario_por_id(idu)
    if pri < 2:
        print()
        print("         ERROR. No posee los privilegios necesarios para realizar esta acción.")
        print()
    else:
        msj = ""
        while msj != "S" and msj != "N":
            msj = input(f"¿Seguro que quiere cambiar el estado del socio? (S/N): ")
            if msj == "S" or msj == "s" or msj == "SI" or msj == "si" or msj == "Si" or msj == "sI":
                msj = "S"
                if estado == 1:
                    edit_registro_socio('activo', 0, id_soc)
                    print()
                    print("Usuario inactivado exitosamente.")
                elif estado == 0:
                    edit_registro_socio('activo', 1, id_soc)
                    print()
                    print("Usuario activado exitosamente.")
                print()
            elif msj == "N" or msj == "n" or msj == "NO" or msj == "no" or msj == "No" or msj == "nO":
                msj = "N"
                print("No se han hecho cambios en el registro.")
                print()
            else:
                print()
                print("         ERROR. Debe indicar S para cambiar el estado o N para cancelar.")
                print()
                msj = input(f"¿Seguro que quiere cambiar el estado del socio? (S/N): ")
                print()
            
    
def crear_op(idu, id_socio, ret):
    i_d, nom, ape, tel, dom, use, pas, pri, act = buscar_usuario_por_id(idu)
    if pri < 2:
        print()
        print("         ERROR. No posee los privilegios necesarios para realizar esta acción.")
        print()
    else:
        if ret == 0:
            print()
            print("            **************")
            print("            * ¡ATENCIÓN! *")
            print("            **************")
            print()
            print("Esta acción NO genera impacto en la caja ni deuda por compra al asociado.")
            print("Si el asociado está realizando la compra de un nicho debe indicar la opción 1 (Venta de nicho) en el menú anterior.")
            print()
            msj = getpass("Presione enter para continuar o ingrese cualquier letra para volver: ")
            if msj != "":
                return
        print()
        print("***** Alta de nueva operación *****")
        print()
        exist = input("Si desea asociar la operación a un nicho existente ingrese el código de nicho, de lo contrario presione enter para crear un nicho: ").upper()
        print()
        if exist != "":
            try:
                cod_nicho, pan, pis, fil, num, cat, ocu, fall = rend.obtener_datos_nicho(exist)
                try:
                    id_operacion, soc, nic, fac, cob, tar, rut, ult, u_a, fec, mor, c_f, u_r, paga, op_cob, nom_alt, dom_alt = ctas.buscar_op_cod_nicho(str(cod_nicho), 1)
                    print(f"         ERROR. El nicho indicado ya se encuentra asociado a la operación {str(id_operacion).rjust(7, '0')}")
                    print()
                    print()
                    print()
                    print()
                    print()
                    return -1
                except UnboundLocalError:
                    pass
                except TypeError:
                    pass
                except IndexError:
                    pass
            except UnboundLocalError:
                print("         ERROR. El nicho indicado no existe. Proceda a crearlo")
                print()
                exist = ""
            except:
                mant.log_error()
                print("")
                input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
                print()
                return -1
        if exist == "":
            cod_nicho = mant.alta_nicho(idu, 1)
            try:
                id_operacion, soc, nic, fac, cob, tar, rut, ult, u_a, fec, mor, c_f, u_r, paga, op_cob, nom_alt, dom_alt = ctas.buscar_op_cod_nicho(str(cod_nicho), 1)
                print()
                print()
                print(f"         ERROR. El nicho indicado ya se encuentra asociado a la operación {str(id_operacion).rjust(7, '0')}")
                print()
                print()
                print()
                print()
                print()
                return -1
            except UnboundLocalError:
                pass
            except TypeError:
                pass
            except IndexError:
                pass
            try:
                cod, pan, pis, fil, num, cat, ocu, fall = rend.obtener_datos_nicho(cod_nicho)
            except UnboundLocalError:
                return -1
            except:
                mant.log_error()
                print("")
                input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
                print()
                return -1
            print()
        if ret == 0:
            exist = input("Si desea asociar la operación a un socio existente ingrese el nro. de socio, de lo contrario presione enter para dar de alta un socio nuevo: ")
            print()
            if exist != "":
                loop = -1
                while loop == -1:
                    try:
                        loop = id_socio = int(exist)
                        n_so, nom_soc, dni, te_1, te_2, mail, dom, loc, c_p, f_n, f_a, act = ctas.obtener_datos_socio(id_socio)
                        print()
                        print(f'            Socio {str(n_so).rjust(6, "0")} - {nom_soc}. Domicilio: {dom}')
                        print()
                    except ValueError:
                        print("         ERROR. El dato solicitado debe ser de tipo numérico")
                        print()
                        exist = input("Si desea asociar la operación a un socio existente ingrese el nro. de socio, de lo contrario presione enter para dar de alta un socio nuevo: ")
                        loop = -1
                    except UnboundLocalError:
                        print("         ERROR. El nro. de socio indicado no existe. Proceda a crearlo")
                        exist = ""
                        print()
                    except TypeError:
                        print("         ERROR. El nro. de socio indicado no existe. Proceda a crearlo")
                        exist = ""
                        print()
                    except:
                        mant.log_error()
                        print("")
                        input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
                        print()
                        return -1
            if exist == "":
                id_socio, opcion = crear_socio(idu, 1)
                n_so, nom_soc, dni, te_1, te_2, mail, dom, loc, c_p, f_n, f_a, act = ctas.obtener_datos_socio(id_socio)
                print()
        n_so, nom_soc, dni, te_1, te_2, mail, dom, loc, c_p, f_n, f_a, act = ctas.obtener_datos_socio(id_socio)
        cod_nich, pan, pis, fil, num, cat, ocu, fall = rend.obtener_datos_nicho(cod_nicho)
        if pan == 6 or pan == 7:
            facturacion = 'nob'
        else:
            facturacion = 'bicon'
        print("Indique el ID de cobrador: ")
        datos = obtener_cobradores()
        counter = 0
        for i in datos:
            counter += 1
            id_cob, n_cob = i
            print(f"    * {id_cob}. {n_cob}")
        print()
        loop = -1
        while loop == -1:
            try:
                loop = cobrador = int(input("Cobrador: "))
                print()
                while cobrador < 1 or cobrador > counter:
                    print("         ERROR. Debe indicar un ID de cobrador válido.")
                    print()
                    cobrador = int(input("Cobrador: "))
            except ValueError:
                print("         ERROR. Debe ingresar un dato de tipo numérico.")
                print()
                loop = -1
            except:
                mant.log_error()
                print("")
                input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
                print()
                return
        if cobrador == 6:
            deb_aut = 1
            ruta = 0
        else:
            loop = -1
            while loop == -1:
                try:
                    loop = ruta = int(input("Indique nro. de ruta: "))
                    print()
                except ValueError:
                    print("         ERROR. El dato solicitado debe ser de tipo numérico")
                    print()
                    loop = -1
                except:
                    mant.log_error()
                    print("")
                    input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
                    print()
                    return
            deb_aut = 0
            msj = ""
            while msj != "S" and msj != "N":
                msj = input(f"¿Desea asociar una tarjeta de crédito? (S/N): ")
                if msj == "S" or msj == "s" or msj == "SI" or msj == "si" or msj == "Si" or msj == "sI":
                    msj = "S"
                    deb_aut = 1
                    print("")
                    pass
                elif msj == "N" or msj == "n" or msj == "NO" or msj == "no" or msj == "No" or msj == "nO":
                    msj = "N"
                    tarjeta = None
                    deb_aut = 0
                    print("")
                    pass
                else:
                    print()
                    print("         ERROR. Debe indicar S para cambiar el estado o N para cancelar.")
                    print()
        while deb_aut == 1:
            try:
                tarjeta = int(input("Ingrese los 16 dígitos de la tarjeta de crédito (Sin espacios): "))
                if len(str(tarjeta)) < 16 or len(str(tarjeta)) > 16:
                    print("         ERROR. Indique un número de tarjeta válido")
                    print()
                    deb_aut = 1
                else:
                    deb_aut = 0
                print()
            except ValueError:
                print("         ERROR. El dato solicitado debe ser de tipo numérico.")
                print()
                deb_aut = 1
            except:
                mant.log_error()
                print("")
                input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
                print()
                return
        ult_pago = rend.obtener_periodo()
        ult_año = datetime.now().strftime('%Y')
        fecha_ult_pago = datetime.now().strftime('%m/%Y')
        moroso = 0
        cuotas_favor = 0
        ult_rec = datetime.now().strftime('%m-%y')
        paga = 1
        msj = ""
        while msj != "S" and msj != "N":
            msj = input(f"¿Desea indicar un número de operación de Cobol para la operación? (S/N): ")
            print()
            if msj == "S" or msj == "s" or msj == "SI" or msj == "si" or msj == "Si" or msj == "sI":
                msj = "S"
                op_cobol = input("Número de operación de Cobol: ")
                if op_cobol == "":
                    op_cobol = None
                else:
                    try:
                        op_cobol = int(op_cobol)
                    except ValueError:
                        print("         ERROR. El dato solicitado debe ser de tipo numérico.")
                        print()
                        return
                    except:
                        mant.log_error()
                        print("")
                        input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
                        print()
                        return
                print()
                pass
            elif msj == "N" or msj == "n" or msj == "NO" or msj == "no" or msj == "No" or msj == "nO":
                msj = "N"
                op_cobol = None
                pass
            else:
                print()
                print("         ERROR. Debe indicar S para indicar un nombre alternativo o N para cancelar.")
                print()
        msj = ""
        while msj != "S" and msj != "N":
            msj = input(f"¿Desea indicar un nombre alternativo para la operación? (S/N): ")
            print()
            if msj == "S" or msj == "s" or msj == "SI" or msj == "si" or msj == "Si" or msj == "sI":
                msj = "S"
                nombre_alt = input("Nombre alternativo: ").title()
                nombre_alt = mant.reemplazar_comilla(nombre_alt)
                if nombre_alt == "":
                    nombre_alt = None
                print()
                pass
            elif msj == "N" or msj == "n" or msj == "NO" or msj == "no" or msj == "No" or msj == "nO":
                msj = "N"
                nombre_alt = None
                pass
            else:
                print()
                print("         ERROR. Debe indicar S para indicar un nombre alternativo o N para cancelar.")
                print()
        msj = ""
        while msj != "S" and msj != "N":
            msj = input(f"¿Desea indicar un domicilio alternativo para la operación? (S/N): ")
            print()
            if msj == "S" or msj == "s" or msj == "SI" or msj == "si" or msj == "Si" or msj == "sI":
                msj = "S"
                domicilio_alt = input("Domicilio alternativo: ").title()
                domicilio_alt = mant.reemplazar_comilla(domicilio_alt)
                if domicilio_alt == "":
                    domicilio_alt = None
                print()
                pass
            elif msj == "N" or msj == "n" or msj == "NO" or msj == "no" or msj == "No" or msj == "nO":
                msj = "N"
                domicilio_alt = None
                pass
            else:
                print()
                print("         ERROR. Debe indicar S para indicar un domicilio alternativo o N para cancelar.")
                print()
        print("Ingresando socio a la base de datos. No interrumpa el proceso ni apague la computadora.", end="  ")
        parameters = (id_socio, cod_nicho, facturacion, cobrador, tarjeta, ruta, ult_pago, ult_año, fecha_ult_pago, moroso, cuotas_favor, ult_rec, paga, op_cobol, nombre_alt, domicilio_alt)
        query = f"INSERT INTO operaciones (socio, nicho, facturacion, cobrador, tarjeta, ruta, ult_pago, ult_año, fecha_ult_pago, moroso, cuotas_favor, ult_rec, paga, op_cobol, nombre_alt, domicilio_alt) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        mant.run_query_w_par(query, parameters)
        print("[OK!]")
        print()
        print("Proceso finalizado exitosamente.")
        print()
        id_ope, socio, nicho, fact, cobr, tarj, rut, ult_pago, ult_año, fup, moroso, c_f, ult_rec, paga, op_cob, nom_a, dom_a = mant.ult_reg("operaciones")
        print(f"Se registró la operación nro. {str(id_ope).rjust(7, '0')}, relacionando al asociado {str(socio).rjust(6, '0')} - {nom_soc} con el nicho {nicho}")
        if ret == 1:
            return id_ope


def opcion_menu_buscar_op():                                                                        # OPC. MENÚ BUSCAR OPERACIONES
    print("")
    print("********** Acciones disponibles **********")
    print("")
    print("   1. Buscar por nro. de socio")
    print("   2. Buscar por nombre de socio")
    print("   3. Buscar por documento")
    print("   4. Buscar por domicilio")
    print("   5. Buscar por nombre alternativo")
    print("   6. Buscar por domicilio alternativo")
    print("   7. Buscar por nro. de operación de Cobol")
    print("   0. Volver")
    print("")
    try:
        opcion = int(input("Ingrese una opción: "))
        print()
        while opcion < 0 or opcion > 7:
            print("")
            print("Opción incorrecta.")
            print("")
            opcion = int(input("Ingrese una opción: "))
            print()
    except ValueError: 
        print("Opción incorrecta.")
        print()
        opcion = -1
    except:
        mant.log_error()
        print("")
        input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
        print()
        return
    return opcion


def menu_buscar_op():                                                                               # MENÚ BUSCAR OPERACIONES
    opcion = -1
    while opcion != 0:
        opcion = opcion_menu_buscar_op()
        if opcion == 1:
            try:
                print("   *** Buscar por nro. de socio ***")
                print()
                nro_socio = int(input("Indique nro. de socio: "))
                ctas.buscar_op_nro_socio(nro_socio)
                print()
                return
            except ValueError:
                print("El dato solicitado debe ser de tipo numérico.")
                print()
                return
            except:
                mant.log_error()
                print("")
                input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
                print()
                return
        elif opcion == 2:
            print("   *** Buscar por nombre de socio ***")
            print()
            nombre = input("Indique nombre de socio: ")
            ctas.buscar_op_nombre_socio(nombre)
            print()
            return
        elif opcion == 3:
            try:
                print("   *** Buscar por nro. de documento ***")
                print()
                dni = int(input("Indique nro. de documento (Sin puntos): "))
                ctas.buscar_op_dni(dni)
                print()
                return
            except ValueError:
                print("El dato solicitado debe ser de tipo numérico.")
                print()
                return
            except:
                mant.log_error()
                print("")
                input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
                print()
                return
        elif opcion == 4:
            print("   *** Buscar por domicilio ***")
            print()
            domicilio = input("Indique domicilio: ")
            ctas.buscar_op_domicilio(domicilio)
            print()
            return
        elif opcion == 5:
            print("   *** Buscar por nombre alternativo ***")
            print()
            nom_alt = input("Indique nombre alternativo: ")
            ctas.buscar_op_nom_alt(nom_alt)
            print()
            return
        elif opcion == 6:
            print("   *** Buscar por domicilio alternativo ***")
            print()
            dom_alt = input("Indique domicilio alternativo: ")
            ctas.buscar_op_nom_alt(dom_alt)
            print()
            return
        elif opcion == 7:
            try:
                print("   *** Buscar por nro. de operación de Cobol ***")
                print()
                op_cob = int(input("Indique nro. de operación de Cobol: "))
                ctas.buscar_op_cobol(op_cob)
                print()
                return
            except ValueError:
                print("El dato solicitado debe ser de tipo numérico.")
                print()
                return
            except:
                mant.log_error()
                print("")
                input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
                print()
                return
        elif opcion == 0:
            print()
            return


def ver_operacion():
    loop = -1
    print("")
    print("********** Ver datos de operación **********")
    print("")
    while loop == -1:
        try:
            loop = id_op = int(input("Indique nro. de operación o ingrese 0 para buscar: "))
            print()
            if id_op == 0:
                menu_buscar_op()
                loop = -1
                print()
        except ValueError:
            print("         ERROR. El dato solicitado debe ser de tipo numérico.")
            print()
            loop = -1
        except UnboundLocalError:
            print("         ERROR. No existe nro. de operación.")
            print()
            loop = -1
        except:
            mant.log_error()
            print("")
            input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
            print()
            return
    try:
        id_op, nro_soc, cod_nic, fac, cob, tar, rut, ult, u_a, fec, mor, c_f, u_r, paga, op_cob, nom_alt, dom_alt = rend.obtener_datos_op(id_op)
    except TypeError:
        print("         ERROR. No existe nro. de operación.")
        print()
        return
    except:
        mant.log_error()
        print("")
        input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
        print()
        return
    cobrador = rend.obtener_nom_cobrador(cob)
    # try:
    #     dat_comp = obtener_datos_complementarios(id_op)
    # except UnboundLocalError:
    #     dat_comp = None
    # except TypeError:
    #     dat_comp = None
    # except:
    #     mant.log_error()
    #     print("")
    #     input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
    #     print()
    #     return
    id_soc, nom, dni, te_1, te_2, mail, dom, loc, c_p, f_n, f_a, act = ctas.obtener_datos_socio(nro_soc)
    cod_nicho, pan, pis, fil, num, cat, ocu, fall = rend.obtener_datos_nicho(cod_nic)
    panteon = rend.obtener_panteon(pan)
    if paga == 1:
        pag = ''
    elif paga == 0:
        pag = 'NO'
    if tar == None:
        tarjeta = 'N/D'
    else:
        t01, t02, t03, t04 = rend.split_nro_tarjeta(tar)
        tarjeta = f"XXXX XXXX XXXX {t04}"
    if act == 1:
        activo = 'ACTIVO'
    elif act == 0:
        activo = 'INACTIVO'
    print()
    print(f"-".rjust(150, '-'))
    if mor == 0:
        print(f"------------------------------ VER DATOS DE LA OPERACIÓN N° {str(id_op).rjust(7, '0')} {str('').rjust(82, '-')}")
    elif mor == 1:
        print(f"------------------------------ VER DATOS DE LA OPERACIÓN N° {str(id_op).rjust(7, '0')} (MOROSO) {str('').rjust(73, '-')}")
    print()
    print(f"    SOCIO: {str(nro_soc).rjust(6, '0')} - {nom}       DNI: {dni}   ({activo})")
    print()
    print(f"    DOMICILIO: {dom}")
    print()
    print(f"    LOCALIDAD: {c_p}  {loc}")
    print()
    if te_1 != None and te_2 == None:
        if mail == None:
            print(f"    TELÉFONO: {te_1}       EMAIL: N/D")
            print()
        elif mail != None:
            print(f"    TELÉFONO: {te_1}       EMAIL: {mail}")
            print()
    elif te_1 == None and te_2 != None:
        if mail == None:
            print(f"    TELÉFONO: {te_2}       EMAIL: N/D")
            print()
        elif mail != None:
            print(f"    TELÉFONO: {te_2}       EMAIL: {mail}")
            print()
    elif te_1 != None and te_2 != None:
        if mail == None:
            print(f"    TELÉFONOS: {te_1} / {te_2}       EMAIL: N/D")
            print()
        elif mail != None:
            print(f"    TELÉFONOS: {te_1} / {te_2}       EMAIL: {mail}")
            print()
    elif te_1 == None and te_2 == None:
        if mail == None:
            print(f"    TELÉFONO: N/D       EMAIL: N/D")
            print()
        elif mail != None:
            print(f"    TELÉFONO: N/D       EMAIL: {mail}")
            print()
    if op_cob != None:
        print(f"    N° DE OPERACIÓN DE COBOL: {op_cob}")
        print()
    if nom_alt != None:
        print(f"    NOMBRE ALTERNATIVO: {nom_alt}")
        print()
    if dom_alt != None:
        print(f"    DOMICILIO ALTERNATIVO: {dom_alt}")
        print()
    print()
    print()
    print(f"    NICHO: {cod_nic}    PANTEÓN: {panteon}  PISO: {str(pis).rjust(2, '0')}  FILA: {str(fil).rjust(2, '0')}  NICHO: {str(num).rjust(4, '0')}")
    print()    
    print(f"    COBRADOR: {cobrador}    -   RUTA: {rut}")
    print()
    # if dat_comp != None:
    #     print(f"    DATOS COMPLEMENTARIOS: {dat_comp}")
    #     print()
    print(f"-".rjust(150, '-'))


def opcion_menu_editar_op():                                                                        # OPC. MENU EDITAR OPERACIONES
    print("")
    print("********** Acciones disponibles **********")
    print("")
    print("   1. Transferir operación a otro asociado")
    print("   2. Cambiar nicho")
    print("   3. Cambiar cobrador")
    print("   4. Editar ruta")
    print("   5. Editar tarjeta de crédito")
    print("   6. Editar número de operación de Cobol")
    print("   7. Editar nombre alternativo")
    print("   8. Editar domicilio alternativo")
    print("   9. Cambiar estado de cobro")
    print("   0. Volver")
    print("")
    try:
        opcion = int(input("Ingrese una opción: "))
        while opcion < 0 or opcion > 9:
            print("")
            print("Opción incorrecta.")
            print("")
            opcion = int(input("Ingrese una opción: "))
    except ValueError: 
        print("Opción incorrecta.")
        opcion = -1
    except:
        mant.log_error()
        print("")
        input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
        print()
        return
    return opcion


def menu_editar_op(idu):                                                                            # MENU EDITAR OPERACIONES
    loop = -1
    print("")
    print("********** Modificar datos de operación **********")
    print("")
    while loop == -1:
        try:
            loop = id_op = int(input("Indique nro. de operación o ingrese 0 para buscar: "))
            print()
            if id_op == 0:
                menu_buscar_op()
                loop = -1
                print()
        except ValueError:
            print("         ERROR. El dato solicitado debe ser de tipo numérico.")
            print()
            loop = -1
        except UnboundLocalError:
            print("         ERROR. No existe nro. de operación.")
            print()
            loop = -1
        except:
            mant.log_error()
            print("")
            input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
            print()
            return
    opcion = -1
    while opcion != 0:
        try:
            id_op, nro_soc, cod_nic, fac, cob, tar, rut, ult, u_a, fec, mor, c_f, u_r, paga, op_cob, nom_alt, dom_alt = rend.obtener_datos_op(id_op)
        except TypeError:
            print("         ERROR. No existe nro. de operación.")
            print()
            return
        except:
            mant.log_error()
            print("")
            input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
            print()
            return
        cobrador = rend.obtener_nom_cobrador(cob)
        id_soc, nom, dni, te_1, te_2, mail, dom, loc, c_p, f_n, f_a, act = ctas.obtener_datos_socio(nro_soc)
        if paga == 1:
            pag = 'SI'
        elif paga == 0:
            pag = 'NO'
        if tar == None:
            tarjeta = 'N/D'
        else:
            t01, t02, t03, t04 = rend.split_nro_tarjeta(tar)
            tarjeta = f"XXXX XXXX XXXX {t04}"
        if cod_nic == None:
            cod_nic = "Ninguno asociado"
        print(f"Operación: {str(id_op).rjust(7, '0')}. Nicho: {cod_nic}")
        print(f"Socio: {str(id_soc).rjust(6, '0')} - {nom}.")
        if op_cob != None:
            print(f"N° de operación de COBOL: {op_cob}")
        if nom_alt != None:
            print(f"Nombre alternativo: {nom_alt}")
        if dom_alt != None:
            print(f"Domicilio alternativo: {dom_alt}")
        print(f"Cobrador: {cobrador}. Ruta: {rut}. Tarjeta: {tarjeta}")
        print(f"¿Paga?: {pag}")
        opcion = opcion_menu_editar_op()
        if opcion == 1:
            opcion = transferir_op(idu, id_op)
        elif opcion == 2:
            cambiar_nicho(idu, id_op)
        elif opcion == 3:
            cambiar_cobrador(idu, id_op, tar)
        elif opcion == 4:
            editar_ruta(idu, id_op)
        elif opcion == 5:
            editar_tarjeta(idu, id_op)
        elif opcion == 6:
            editar_op_cobol(idu, id_op)
        elif opcion == 7:
            editar_nom_alt(idu, id_op)
        elif opcion == 8:
            editar_dom_alt(idu, id_op)
        elif opcion == 9:
            cambiar_estado_cobro(idu, id_op, paga)
        elif opcion == 0:
            return


def transferir_op(idu, id_op):
    i_d, nom, ape, tel, dom, use, pas, pri, act = buscar_usuario_por_id(idu)
    if pri < 2:
        print()
        print("         ERROR. No posee los privilegios necesarios para realizar esta acción.")
        print()
    else:
        print("***** Transferir operación a otro socio *****")
        print()
        print("   1. Crear un nuevo socio")
        print("   2. Utilizar un socio existente")
        print("   0. Volver")
        print("")
        loop = -1
        while loop == -1:
            try:
                loop = opcion = int(input("Ingrese una opción: "))
                if opcion < 0 or opcion > 2:
                    print("")
                    print("Opción incorrecta.")
                    print("")
                    loop = -1
            except ValueError: 
                print("Opción incorrecta.")
                print("")
                opcion = -1
                loop = -1
            except:
                mant.log_error()
                print("")
                input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
                print()
                return
        if opcion == 0:
            print()
            return
        if opcion == 1:
            id_socio, opcion = crear_socio(idu, 1)
            if id_socio == 0:
                print()
                return
            else:
                n_so_n, nom_n, dni_n, te_1_n, te_2_n, mail_n, dom_n, loc_n, c_p_n, f_n_n, f_a_n, act_n = ctas.obtener_datos_socio(id_socio)
        if opcion == 2:
            loop = -1
            while loop == -1:
                try:
                    loop = id_socio = int(input("Indique el nro. de socio o ingrese 0 para buscar: "))
                    print()
                    if id_socio == 0:
                        ctas.menu_buscar()
                        print()
                        id_socio = int(input("Indique el nro. de socio: "))
                    n_so_n, nom_n, dni_n, te_1_n, te_2_n, mail_n, dom_n, loc_n, c_p_n, f_n_n, f_a_n, act_n = ctas.obtener_datos_socio(id_socio)
                    loop = 1
                except UnboundLocalError:
                    print()
                    print("         ERROR. Indique un nro de socio válido.")
                    print()
                    loop = -1
                except TypeError:
                    print()
                    print("         ERROR. Indique un nro de socio válido.")
                    print()
                    loop = -1    
                except ValueError:
                    print()
                    print("         ERROR. El dato solicitado debe ser de tipo numérico.")
                    print()
                    loop = -1
                except:
                    mant.log_error()
                    print("")
                    input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
                    print()
                    return
        try:
            id_op, nro_soc, cod_nic, fac, cob, tar, rut, ult, u_a, fec, mor, c_f, u_r, paga, op_cob, nom_alt, dom_alt = rend.obtener_datos_op(id_op)
        except TypeError:
            print("         ERROR. No existe nro. de operación.")
            print()
            return
        except:
            mant.log_error()
            print("")
            input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
            print()
            return
        try:
            n_so_v, nom_v, dni_v, te_1_v, te_2_v, mail_v, dom_v, loc_v, c_p_v, f_n_v, f_a_v, act_v = ctas.obtener_datos_socio(nro_soc)
        except TypeError:
            print("         ERROR. No existe nro. de socio.")
            print()
            return
        except:
            mant.log_error()
            print("")
            input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
            print()
            return
        msj = ""
        while msj != "S" and msj != "N":
            msj = input(f"¿Transferir la operación nro. {str(id_op).rjust(7, '0')} del socio {str(n_so_v).rjust(6, '0')} - {nom_v} al socio {str(n_so_n).rjust(6, '0')} - {nom_n}? (S/N): ")
            print()
            if msj == "S" or msj == "s" or msj == "SI" or msj == "si" or msj == "Si" or msj == "sI":
                msj = "S"
                mant.edit_registro('operaciones', 'socio', id_socio, id_op)                
                print("Operación transferida exitosamente.")
                print()
                editar_nom_alt(idu, id_op)
                editar_dom_alt(idu, id_op)
                pass
            elif msj == "N" or msj == "n" or msj == "NO" or msj == "no" or msj == "No" or msj == "nO":
                msj = "N"
                print("No se han realizado cambios en el registro")
                print("")
            else:
                print()
                print("         ERROR. Debe indicar S para transferir o N para cancelar.")
                print()
                msj = input(f"¿Transferir la operación nro. {str(id_op).rjust(7, '0')} del socio {str(n_so_v).rjust(6, '0')} - {nom_v} al socio {str(n_so_n).rjust(6, '0')} - {nom_n}? (S/N): ")
                print()


def cambiar_nicho(idu, id_op):
    i_d, nom, ape, tel, dom, use, pas, pri, act = buscar_usuario_por_id(idu)
    if pri < 2:
        print()
        print("         ERROR. No posee los privilegios necesarios para realizar esta acción.")
        print()
    else:
        print("***** Cambiar nicho *****")
        print()
        exist = input("Si desea asociar la operación a un nicho existente ingrese el código de nicho, de lo contrario presione enter: ").upper()
        print()
        if exist == "":
            opcion = -1
        if exist != "":
            try:
                cod_nicho, pan, pis, fil, num, cat, ocu, fall = rend.obtener_datos_nicho(exist)
                try:
                    id_operacion, soc, nic, fac, cob, tar, rut, ult, u_a, fec, mor, c_f, u_r, paga, op_cob, nom_alt, dom_alt = ctas.buscar_op_cod_nicho(str(cod_nicho), 1)
                    print(f"         ERROR. El nicho indicado ya se encuentra asociado a la operación {str(id_operacion).rjust(7, '0')}")
                    print()
                    return
                except UnboundLocalError:
                    pass
                except TypeError:
                    pass
                except IndexError:
                    pass
            except UnboundLocalError:
                print("         ERROR. El nicho indicado no existe. Proceda a crearlo")
                print()
                exist = ""
                opcion = 1
        if exist == "":
            if opcion == -1:
                print("   1. Crear un nuevo nicho")
                print("   2. Desasociar el nicho actual")
                print("   0. Volver")
                print("")
                loop = -1
                while loop == -1:
                    try:
                        loop = opcion = int(input("Ingrese una opción: "))
                        if opcion < 0 or opcion > 2:
                            print("")
                            print("Opción incorrecta.")
                            print("")
                            loop = -1
                    except ValueError: 
                        print("Opción incorrecta.")
                        print("")
                        opcion = -1
                        loop = -1
                    except:
                        mant.log_error()
                        print("")
                        input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
                        print()
                        return
            if opcion == 1:
                cod_nicho = mant.alta_nicho(idu, 1)
                try:
                    cod, pan, pis, fil, num, cat, ocu, fall = rend.obtener_datos_nicho(cod_nicho)
                except UnboundLocalError:
                    return
                except:
                    mant.log_error()
                    print("")
                    input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
                    print()
                    return
                print()
            elif opcion == 2:
                id_op, nro_soc, cod_nic, fac, cob, tar, rut, ult, u_a, fec, mor, c_f, u_r, paga, op_cob, nom_alt, dom_alt = rend.obtener_datos_op(id_op)
                if cod_nic == None:
                    print()
                    print("         ERROR. La operación seleccionada no tiene ningún nicho asociado")
                    print()
                    return
                msj = " "
                while msj != "S" and msj != "N":
                    msj = input(f"¿Desasociar el nicho {cod_nic} de la operación {str(id_op).rjust(7, '0')}? (S/N): ")
                    print()
                    if msj == "S" or msj == "s" or msj == "SI" or msj == "si" or msj == "Si" or msj == "sI":
                        msj = "S"
                        mant.set_null_registro('operaciones', 'nicho', 'id', id_op)
                        mant.edit_nicho('ocupado', 0, cod_nic)                        
                        print("Nicho desasociado exitosamente.")
                        print()
                        return
                    elif msj == "N" or msj == "n" or msj == "NO" or msj == "no" or msj == "No" or msj == "nO":
                        msj = "N"
                        print("No se han realizado cambios en el registro")
                        print("")
                        return
                    else:
                        print()
                        print("         ERROR. Debe indicar S para desasociar el nicho o N para cancelar.")
                        print()
            else:
                print()
                return
        try:
            id_op, nro_soc, cod_nic, fac, cob, tar, rut, ult, u_a, fec, mor, c_f, u_r, paga, op_cob, nom_alt, dom_alt = rend.obtener_datos_op(id_op)
        except TypeError:
            print("         ERROR. No existe nro. de operación.")
            print()
            return
        except:
            mant.log_error()
            print("")
            input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
            print()
            return
        msj = " "
        while msj != "S" and msj != "N":
            if cod_nic == None:
                msj = input(f"¿Asociar el nicho {cod_nicho} a la operación {str(id_op).rjust(7, '0')}? (S/N): ")
            else:
                msj = input(f"¿Cambiar el nicho {cod_nic} por el nicho {cod_nicho} en la operación {str(id_op).rjust(7, '0')}? (S/N): ")
            print()
            if msj == "S" or msj == "s" or msj == "SI" or msj == "si" or msj == "Si" or msj == "sI":
                msj = "S"
                mant.edit_registro('operaciones', 'nicho', cod_nicho, id_op)
                print("Nicho modificado exitosamente.")
                print()
                pass
            elif msj == "N" or msj == "n" or msj == "NO" or msj == "no" or msj == "No" or msj == "nO":
                msj = "N"
                print("No se han realizado cambios en el registro")
                print("")
            else:
                print()
                print("         ERROR. Debe indicar S para cambiar el nicho o N para cancelar.")
                print()
                msj = input(f"¿Cambiar el nicho {cod_nic} por el nicho {cod_nicho} en la operación {str(id_op).rjust(7, '0')}? (S/N): ")
                print()


def cambiar_cobrador(idu, id_op, tarjeta):
    i_d, nom, ape, tel, dom, use, pas, pri, act = buscar_usuario_por_id(idu)
    if pri < 2:
        print()
        print("         ERROR. No posee los privilegios necesarios para realizar esta acción.")
        print()
    else:
        print("***** Editar tarjeta de crédito *****")
        print()
        print("Indique el ID de cobrador: ")
        datos = obtener_cobradores()
        counter = 0
        for i in datos:
            counter += 1
            id_cob, n_cob = i
            print(f"    * {id_cob}. {n_cob}")
        print()
        loop = -1
        while loop == -1:
            try:
                loop = cobrador = int(input("Cobrador: "))
                print()
                while cobrador < 1 or cobrador > counter:
                    print("         ERROR. Debe indicar un ID de cobrador válido.")
                    print()
                    cobrador = int(input("Cobrador: "))
            except ValueError:
                print("         ERROR. Debe ingresar un dato de tipo numérico.")
                print()
                loop = -1
            except:
                mant.log_error()
                print("")
                input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
                print()
                return
        mant.edit_registro('operaciones', 'cobrador', cobrador, id_op)
        print("Cobrador modificado exitosamente.")
        print()
        if cobrador == 6:
            mant.edit_registro('operaciones', 'ruta', 0, id_op)
            print("Ruta modificada exitosamente.")
            print()
            if tarjeta == None:
                editar_tarjeta(idu, id_op)
                

def editar_ruta(idu, id_op):
    i_d, nom, ape, tel, dom, use, pas, pri, act = buscar_usuario_por_id(idu)
    if pri < 2:
        print()
        print("         ERROR. No posee los privilegios necesarios para realizar esta acción.")
        print()
    else:
        print("***** Editar ruta *****")
        print()
        try:
            ruta_nueva = int(input("Ingrese la ruta nueva: "))
        except ValueError:
            print("         ERROR. El dato solicitado debe ser de tipo numérico.")
            print()
            return
        except:
            mant.log_error()
            print("")
            input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
            print()
            return
        print()
        mant.edit_registro('operaciones', 'ruta', ruta_nueva, id_op)
        print("Ruta modificada exitosamente.")
        print()


def editar_tarjeta(idu, id_op):
    i_d, nom, ape, tel, dom, use, pas, pri, act = buscar_usuario_por_id(idu)
    if pri < 2:
        print()
        print("         ERROR. No posee los privilegios necesarios para realizar esta acción.")
        print()
    else:
        print("***** Editar tarjeta de crédito *****")
        print()
        try:
            tarjeta_nueva = int(input("Ingrese los 16 dígitos de la tarjeta (Sin espacios): "))
        except ValueError:
            print("         ERROR. El dato solicitado debe ser de tipo numérico.")
            print()
            return
        except:
            mant.log_error()
            print("")
            input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
            print()
            return
        print()
        mant.edit_registro('operaciones', 'tarjeta', tarjeta_nueva, id_op)
        print("Tarjeta modificada exitosamente.")
        print()


def editar_op_cobol(idu, id_op):
    i_d, nom, ape, tel, dom, use, pas, pri, act = buscar_usuario_por_id(idu)
    if pri < 2:
        print()
        print("         ERROR. No posee los privilegios necesarios para realizar esta acción.")
        print()
    else:
        print("***** Editar nro. de operación de Cobol *****")
        print()
        op_cobol_nuevo = input("Ingrese número de operación de Cobol nuevo o presione enter para eliminarlo: ")
        if op_cobol_nuevo == "":
            conn = sql.connect(database)
            cursor = conn.cursor()
            instruccion = f"UPDATE operaciones SET op_cobol = NULL WHERE id = '{id_op}'"
            cursor.execute(instruccion)
            conn.commit()
            conn.close()
        else:
            try:
                mant.edit_registro('operaciones', 'op_cobol', int(op_cobol_nuevo), id_op)
            except ValueError:
                print("         ERROR. El dato solicitado debe ser de tipo numérico.")
                print()
                return
            except:
                mant.log_error()
                print("")
                input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
                print()
                return
        print()
        print("Número de operación de Cobol modificado exitosamente.")
        print()


def editar_nom_alt(idu, id_op):
    i_d, nom, ape, tel, dom, use, pas, pri, act = buscar_usuario_por_id(idu)
    if pri < 2:
        print()
        print("         ERROR. No posee los privilegios necesarios para realizar esta acción.")
        print()
    else:
        print("***** Editar nombre alternativo *****")
        print()
        nombre_nuevo = input("Ingrese apellido y nombres alternativos nuevos o presione enter para eliminarlos: ").title()
        print()
        if nombre_nuevo == "":
            conn = sql.connect(database)
            cursor = conn.cursor()
            instruccion = f"UPDATE operaciones SET nombre_alt = NULL WHERE id = '{id_op}'"
            cursor.execute(instruccion)
            conn.commit()
            conn.close()
        else:
            mant.edit_registro('operaciones', 'nombre_alt', nombre_nuevo, id_op)
        print("Nombre alternativo modificado exitosamente.")
        print()


def editar_dom_alt(idu, id_op):
    i_d, nom, ape, tel, dom, use, pas, pri, act = buscar_usuario_por_id(idu)
    if pri < 2:
        print()
        print("         ERROR. No posee los privilegios necesarios para realizar esta acción.")
        print()
    else:
        print("***** Editar domicilio alternativo *****")
        print()
        domicilio_nuevo = input("Ingrese domicilio alternativo nuevo o presione enter para eliminarlo: ").title()
        print()
        if domicilio_nuevo == "":
            conn = sql.connect(database)
            cursor = conn.cursor()
            instruccion = f"UPDATE operaciones SET domicilio_alt = NULL WHERE id = '{id_op}'"
            cursor.execute(instruccion)
            conn.commit()
            conn.close()
        else:
            mant.edit_registro('operaciones', 'domicilio_alt', domicilio_nuevo, id_op)
        print("Domicilio alternativo modificado exitosamente.")
        print()


def cambiar_estado_cobro(idu, id_op, paga):
    i_d, nom, ape, tel, dom, use, pas, pri, act = buscar_usuario_por_id(idu)
    if pri < 4:
        print()
        print("         ERROR. No posee los privilegios necesarios para realizar esta acción.")
        print()
    else:
        msj = ""
        while msj != "S" and msj != "N":
            msj = input(f"¿Seguro que quiere cambiar el estado de cobro de la operación? (S/N): ")
            if msj == "S" or msj == "s" or msj == "SI" or msj == "si" or msj == "Si" or msj == "sI":
                msj = "S"
                if paga == 1:
                    mant.edit_registro('operaciones', 'paga', 0, id_op)
                    print()
                    print("Cobranza inactivada exitosamente.")
                elif paga == 0:
                    mant.edit_registro('operaciones', 'paga', 1, id_op)
                    print()
                    print("Cobranza activada exitosamente.")
                print()
            elif msj == "N" or msj == "n" or msj == "NO" or msj == "no" or msj == "No" or msj == "nO":
                msj = "N"
                print("No se han hecho cambios en el registro.")
                print()
            else:
                print()
                print("         ERROR. Debe indicar S para cambiar el estado o N para cancelar.")
                print()
                msj = input(f"¿Seguro que quiere cambiar el estado del socio? (S/N): ")
                print()


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


