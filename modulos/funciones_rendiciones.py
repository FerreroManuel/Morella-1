import funciones_caja as caja
import funciones_mantenimiento as mant
import funciones_ventas as vent
import correo as email
import reporter as rep
import psycopg2 as sql
from getpass import getpass
import os
from datetime import datetime, date
from dateutil.relativedelta import relativedelta as rd
from smtplib import SMTPAuthenticationError
from socket import gaierror
from threading import Thread

os.system(f'TITLE Morella v{mant.VERSION} - MF! Soluciones informáticas')
os.system('color 09')   # Colores del módulo (Azul sobre negro)
os.system('mode con: cols=160 lines=9999')


def obtener_database():
    if not os.path.isfile("../databases/database.ini"):
        arch = open("../databases/database.ini", "w")
        arch.close()
    with open("../databases/database.ini", "r") as arch:
        db = arch.readline()
    return db
database = obtener_database()


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


def opcion_menu():                                                                                  # OPCIÓN MENÚ PRINCIPAL
    print("")
    print("********** Acciones disponibles **********")
    print("")
    print("   1. Registrar cobro")
    print("   2. Emitir recibos")
    print("   3. Ingresar pagos por adelantado")
    print("   4. Registrar débito automático")
    print("   5. Reimprimir recibo (actualiza importe)")
    print("   0. Salir")
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
        mant.log_error()
        print("")
        input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
        print()
        opcion = -1
    return opcion


def menu(idu):                                                                                      # MENÚ PRINCIPAL
    opcion = -1
    while opcion != 0:
        opcion = opcion_menu()
        if opcion == 1:
            ingresar_cobro(idu)
        elif opcion == 2:
            emitir_recibos()
        elif opcion == 3:
            ingresar_adelantos(idu)
        elif opcion == 4:
            registrar_debito_automatico(idu)
        elif opcion == 5:
            reimprimir_recibo()
        elif opcion == 0:
            return


def ingresar_cobro(idu):
    ndr = 0
    msj = ''
    print("")
    loop = -1
    while loop == -1:
        while ndr == 0:
            try:
                ndr = int(input("Indique el nro. de recibo a ingresar: "))
                msj = ''
                print("")    
                nro, ope, per, año, pag = obtener_datos_recibo(ndr)
            except ValueError:
                print("")
                print("         ERROR. El dato solicitado debe ser de tipo numérico.")
                print("")
                ndr = 0
            except TypeError:
                print("")
                print("         ERROR. Número de recibo inválido. No se han realizado cambios en el registro.")
                print("")
                return
            except:
                mant.log_error()
                print("")
                input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
                print()
                return
        id_op, soc, nic, fac, cob, tar, rut, ult, u_a, fec, mor, c_f, u_r, paga, op_cob, nom_alt, dom_alt = obtener_datos_op(ope)
        cod, pan, pis, fil, num, cat, ocu, fall = obtener_datos_nicho(nic)
        id_cat, cat, val_mant_bic, val_mant_nob = obtener_categoria(cat)
        if fac == 'bicon':
            val = val_mant_bic
        elif fac == 'nob':
            val = val_mant_nob
        if per[0:3] == 'Doc':
            val = obtener_valor_doc(ope)
        if pag == 1:
            print("El recibo ya se encuentra ingresado en sistema.")
            msj = ''
            print("")
            while msj == '':
                msj = input(f"¿Desea ingresar otro pago? (S/N) ")
                if msj == 'S' or msj == 's' or msj == 'Si' or msj == 'SI' or msj == 'sI' or msj == 'si':
                    print("")
                    ndr = 0
                    loop = -1
                elif msj == 'N' or msj == 'n' or msj == 'No' or msj == 'NO' or msj == 'nO' or msj == 'no':
                    print("")
                    return
                else:
                    print("")
                    print("Debe ingresar S para confirmar o N para cancelar.")
                    print("")
                    msj = ''
        elif pag == 0:
            if cob == 6:
                print("         ERROR. La operación tiene habilitado el débito automático. Para registrar el pago seleccione la opción correcta en el menú principal.")
                msj = ''
                print("")
                while msj == '':
                    msj = input(f"¿Desea ingresar otro pago? (S/N) ")
                    if msj == 'S' or msj == 's' or msj == 'Si' or msj == 'SI' or msj == 'sI' or msj == 'si':
                        print("")
                        ndr = 0
                        loop = -1
                    elif msj == 'N' or msj == 'n' or msj == 'No' or msj == 'NO' or msj == 'nO' or msj == 'no':
                        print("")
                        return
                    else:
                        print("")
                        print("Debe ingresar S para confirmar o N para cancelar.")
                        print("")
                        msj = ''
            else:
                if c_f < 0:
                    print()
                    print("         ERROR. La operación debe cuotas previas a la implementación de Morella. Debe saldar la cuenta antes de abonar un nuevo recibo.")
                    print()
                    return
                else:
                    try:
                        rendicion = int(input("Indique el número de rendición: "))
                    except ValueError:
                        print("")
                        print("Número de rendición inválido. No se han realizado cambios en el registro.")
                        print("")
                        return
                    except:
                        mant.log_error()
                        print("")
                        input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
                        print()
                        return
                    while msj == '':
                        msj = input(f"¿Seguro que quiere ingresar el pago por el recibo nro. {f'{ndr}'.rjust(7, '0')} en la rendición nro. {rendicion}? (S/N) ")
                        if msj == 'S' or msj == 's' or msj == 'Si' or msj == 'SI' or msj == 'sI' or msj == 'si':
                            set_pago(ndr)
                            act_periodo(per, ope, año)
                            if per[0:3] == 'Doc':
                                registrar_comision_doc(cob, rendicion, ndr, val)
                            else:
                                registrar_comision_mant(cob, rendicion, ndr, val) 
                            print("")
                            cod, pan, pis, fil, num, cat, ocu, fall = obtener_datos_nicho(nic)
                            categoria = f"Mantenimiento {obtener_panteon(pan)}"
                            descripcion = f"{obtener_nom_cobrador(cob)}"
                            observacion = f"Recibo nro. {f'{ndr}'.rjust(7, '0')}"
                            dia = caja.obtener_dia()
                            mes = caja.obtener_mes()
                            año = caja.obtener_año()
                            parameters = str((categoria, descripcion, rendicion, val, observacion, dia, mes, año, idu))
                            query = f"INSERT INTO caja (categoria, descripcion, transaccion, ingreso, observacion, dia, mes, año, id_user) VALUES {parameters}"
                            run_query(query)
                            if mor == 1:
                                id_op, soc, nic, fac, cob, tar, rut, ult, u_a, fup, mor, c_f, u_r, paga, op_cob, nom_alt, dom_alt = obtener_datos_op(ope)
                                fec_hoy = datetime.now().date()
                                fup_sep = str(fup).split("/")
                                fup_date = date(year = int(fup_sep[1]), month = int(fup_sep[0]), day = 1)
                                cuenta = int(days_between(fup_date, fec_hoy)/730)
                                if cuenta <= 0:
                                    print()
                                    print("         ATENCIÓN: A partir del pago ralizado el asociado deja de ser MOROSO, indique cobrador y ruta para la operación.")
                                    print()
                                    datos = vent.obtener_cobradores()
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
                                    while deb_aut == 1:
                                        try:
                                            tarjeta = int(input("Ingrese los 16 dígitos de la tarjeta de crédito (Sin espacios): "))
                                            if len(str(tarjeta)) < 16 or len(str(tarjeta)) > 16:
                                                print("         ERROR. Indique un número de tarjeta válido")
                                                print()
                                                deb_aut = 1
                                            else:
                                                mant.edit_registro('operaciones', 'tarjeta', tarjeta, ope)
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
                                    mant.edit_registro('operaciones', 'moroso', 0, ope)
                                    mant.edit_registro('operaciones', 'cobrador', cobrador, ope)
                                    mant.edit_registro('operaciones', 'ruta', ruta, ope)
                            print("Pago ingresado exitosamente")
                        elif msj == 'N' or msj == 'n' or msj == 'No' or msj == 'NO' or msj == 'nO' or msj == 'no':
                            print("")
                            print("No se han hecho cambios en el registro.")
                        else:
                            print("")
                            print("Debe ingresar S para confirmar o N para cancelar.")
                            print("")
                            msj = ''
                    msj = ''
                    print("")
                    while msj == '':
                        msj = input(f"¿Desea ingresar otro pago? (S/N) ")
                        if msj == 'S' or msj == 's' or msj == 'Si' or msj == 'SI' or msj == 'sI' or msj == 'si':
                            print("")
                            ndr = 0
                            loop = -1
                        elif msj == 'N' or msj == 'n' or msj == 'No' or msj == 'NO' or msj == 'nO' or msj == 'no':
                            print("")
                            return
                        else:
                            print("")
                            print("Debe ingresar S para confirmar o N para cancelar.")
                            print("")
                            msj = ''


def ingresar_cobro_auto(per, ope, año, fecha, c_f):
    conn = sql.connect(database)
    cursor = conn.cursor()
    instruccion = f"UPDATE operaciones SET ult_pago = '{per}', ult_año = '{año}', fecha_ult_pago = '{fecha}', cuotas_favor = '{c_f}' WHERE id = '{ope}'"
    cursor.execute(instruccion)
    conn.commit()
    conn.close()


def obtener_datos_op(ope):
    conn = sql.connect(database)
    cursor = conn.cursor()
    instruccion = f"SELECT * FROM operaciones WHERE id = {ope}"
    cursor.execute(instruccion)
    datos = cursor.fetchone()
    conn.commit()
    conn.close()
    i_d, soc, nic, fac, cob, tar, rut, ult, u_a, fec, mor, c_f, u_r, paga, op_cob, nom_alt, dom_alt = datos
    return i_d, soc, nic, fac, cob, tar, rut, ult, u_a, fec, mor, c_f, u_r, paga, op_cob, nom_alt, dom_alt


def obtener_str_mes(mes):
    if mes == '01':
        mes = 'Enero'
    elif mes == '02':
        mes = 'Febrero'
    elif mes == '03':
        mes = 'Marzo'
    elif mes == '04':
        mes = 'Abril'
    elif mes == '05':
        mes = 'Mayo'
    elif mes == '06':
        mes = 'Junio'
    elif mes == '07':
        mes = 'Julio'
    elif mes == '08':
        mes = 'Agosto'
    elif mes == '09':
        mes = 'Septiembre'
    elif mes == '10':
        mes = 'Octubre'
    elif mes == '11':
        mes = 'Noviembre'
    elif mes == '12':
        mes = 'Diciembre'
    return mes


def obtener_mes_siguiente(mes):
    if mes == '01':
        str_mes = 'Febrero'
        int_mes = '02'
    elif mes == '02':
        str_mes = 'Marzo'
        int_mes = '03'
    elif mes == '03':
        str_mes = 'Abril'
        int_mes = '04'
    elif mes == '04':
        str_mes = 'Mayo'
        int_mes = '05'
    elif mes == '05':
        str_mes = 'Junio'
        int_mes = '06'
    elif mes == '06':
        str_mes = 'Julio'
        int_mes = '07'
    elif mes == '07':
        str_mes = 'Agosto'
        int_mes = '08'
    elif mes == '08':
        str_mes = 'Septiembre'
        int_mes = '09'
    elif mes == '09':
        str_mes = 'Octubre'
        int_mes = '10'
    elif mes == '10':
        str_mes = 'Noviembre'
        int_mes = '11'
    elif mes == '11':
        str_mes = 'Diciembre'
        int_mes = '12'
    elif mes == '12':
       str_mes = 'Enero'
       int_mes = '01'
    return str_mes, int_mes


def days_between(d1, d2):
    return (d2-d1).days


def set_pago(ndr):
    conn = sql.connect(database)
    cursor = conn.cursor()
    instruccion = f"UPDATE recibos SET pago = '1' WHERE nro_recibo = '{ndr}'"
    cursor.execute(instruccion)
    conn.commit()
    conn.close()    


def act_periodo(per, ope, año):
    mes = calcular_mes(per, 'str')
    fecha = f"{mes}/{año}"
    conn = sql.connect(database)
    cursor = conn.cursor()
    instruccion = f"UPDATE operaciones SET ult_pago = '{per}', ult_año = '{año}', fecha_ult_pago = '{fecha}' WHERE id = '{ope}'"
    cursor.execute(instruccion)
    conn.commit()
    conn.close()


def obtener_datos_recibo(ndr):
    conn = sql.connect(database)
    cursor = conn.cursor()
    instruccion = f"SELECT * FROM recibos WHERE nro_recibo = '{ndr}'"
    cursor.execute(instruccion)
    datos = cursor.fetchone()
    nro, ope, per, año, pag = datos
    conn.commit()
    conn.close()
    return nro, ope, per, año, pag


def run_query(query):
    conn = sql.connect(database)
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()
    conn.close()


def emitir_recibos():
    facturacion = menu_facturacion()
    if facturacion == "ERROR":
        print("")
        print("         ERROR. El período de facturación no corresponde con el mes.")
    elif facturacion == "VOLVER":
        print()
        return
    elif facturacion == "documentos":
        mes = datetime.now().strftime('%m')
        str_mes_siguiente, int_mes_siguiente = obtener_mes_siguiente(mes)
        print("")
        msj = ""
        while msj != "S" and msj != "N":
            msj = input(f"¿Emitir recibos de documentos de {str_mes_siguiente}? (S/N) ")
            if msj == "S" or msj == "s" or msj == "SI" or msj == "si" or msj == "Si" or msj == "sI":
                msj = "S"
                print("")
                print("POR FAVOR, NO CIERRE LA APLICACIÓN NI APAGUE EL SISTEMA MIENTRAS SE REALIZAN LAS ACCIONES SOLICITADAS")
                print("")
                print("Emitiendo recibos...")
                lista_recibos = rep.recibos_documentos()
                print()
                print("Confeccionando listados...")
                rep.listado_recibos_documentos(lista_recibos)
                print()
                return
            elif msj == "N" or msj == "n" or msj == "NO" or msj == "no" or msj == "No" or msj == "nO":
                msj = "N"
                print("")
                print("No se han emitido recibos.")
                print("")
                return
            else:
                print("")
                print("         ERROR. Debe indicar S para emitir o N para cancelar.")
                print("")
    else:
        cobrador = menu_cobradores()
        if cobrador == 0:
            return
        ncobrador = obtener_nom_cobrador(cobrador)
        periodo = obtener_periodo()
        print("")
        msj = input(f"¿Emitir recibos de {periodo}, de {facturacion.upper()} - {ncobrador}? (S/N) ")
        while msj != "S" and msj != "N":
            if msj == "S" or msj == "s" or msj == "SI" or msj == "si" or msj == "Si" or msj == "sI":
                msj = "S"
                print("")
                print("POR FAVOR, NO CIERRE LA APLICACIÓN NI APAGUE EL SISTEMA MIENTRAS SE REALIZAN LAS ACCIONES SOLICITADAS")
                print("")
                print("Emitiendo recibos...")
                recibos = buscar_operaciones(facturacion, cobrador)
                if cobrador != 6:
                    thread1 = Thread(target=rep.recibos, args=(facturacion, cobrador, recibos))
                    thread2 = Thread(target=rep.listado_recibos, args=(facturacion, cobrador, recibos))
                    thread1.start()
                    thread2.start()
                    thread1.join()
                    thread2.join()
                    print("")
                    return
                elif cobrador == 6:
                    thread1 = Thread(target=rep.recibos_deb_aut, args=(facturacion, recibos))
                    thread2 = Thread(target=rep.listado_recibos_deb_aut, args=(facturacion, recibos))
                    thread1.start()
                    thread2.start()
                    thread1.join()
                    thread2.join()
                    print("")
                    return
            elif msj == "N" or msj == "n" or msj == "NO" or msj == "no" or msj == "No" or msj == "nO":
                msj = "N"
                print("")
                print("No se han emitido recibos.")
                print("")
                return
            else:
                print("")
                print("         ERROR. Debe indicar S para emitir o N para cancelar.")
                print("")
                msj = input(f"¿Imprimir recibos de {periodo}, de {facturacion} - {ncobrador}? (S/N) ")
                print("")
            

def ingresar_adelantos(idu):
    print("")
    try:
        oper = int(input("Indique el número de operación: "))
    except ValueError:
        print("         ERROR. El dato solicitado debe ser de tipo numérico")
        return
    except:
        mant.log_error()
        print("")
        input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
        print()
        return
    print("")
    try:
        i_d, soc, nic, fac, cob, tar, rut, ult, u_a, fec, mor, c_f, u_r, paga, op_cob, nom_alt, dom_alt = obtener_datos_op(oper)
    except TypeError:
        print("         ERROR. Número de operación inexistente.")
        return
    except:
        mant.log_error()
        print("")
        input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
        print()
        return
    cod, pan, pis, fil, num, cat, ocu, fall = obtener_datos_nicho(nic)
    i_d, cat, val_mant_bic, val_mant_nob = obtener_categoria(cat)
    rec_impagos = obtener_recibos_impagos_op(oper)
    docs_imp = 0
    mant_imp = []
    q_mant_imp = 0
    if rec_impagos != []:
        for i in rec_impagos:
            nro_rec_imp, ope_imp, per_imp, año_imp, pag_imp = i
            if per_imp[0:3] == 'Doc':
                docs_imp += 1
            else:
                q_mant_imp += 1
                mant_imp.append(i)
    if docs_imp > 0:
        print("         ERROR. La operación adeuda documentos. Debe abonar los documentos impagos antes de realizar el pago de cuotas.")
        print()
        return
    if q_mant_imp > 0 or c_f < 0:
        print()
        input(f"    *** ATENCIÓN! La operación adeuda cuotas. Éstas serán descontadas de las que adelante en esta transacción. *** ")
        print()
        print()
    try:
        cant = int(input("Indique la cantidad de cuotas a adelantar: "))
    except ValueError:
        print("         ERROR. El dato solicitado debe ser de tipo numérico")
        return
    except:
        mant.log_error()
        print("")
        input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
        print()
        return
    if fac == 'bicon':
        valor_total = val_mant_bic * cant
    elif fac == 'nob':
        valor_total = val_mant_nob * cant
    print("")
    try:
        rendicion = int(input("Indique el número de rendición: "))
    except ValueError:
        print("         ERROR. El dato solicitado debe ser de tipo numérico")
        return
    except:
        mant.log_error()
        print("")
        input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
        print()
        return
    print("")
    operacion = str(oper).rjust(7, "0")
    print(f"Se registrará el ingreso de $ {valor_total:.2f} correspondiente al pago de {cant} cuotas de la operación {operacion}")
    print("")
    msj = ""
    while msj != "S" and msj != "N":
        msj = input("¿Está seguro de realizar el registro? (S/N): ")
        if msj == "S" or msj == "s" or msj == "SI" or msj == "si" or msj == "Si" or msj == "sI":
            msj = "S"
            mes_pago = calcular_mes(ult, 'str')
            ult_pago = datetime.strptime(f'{mes_pago}/{u_a}', '%m/%Y')
            pago_hasta = datetime.strftime(ult_pago + rd(months = cant*2), '%m/%Y')
            mes_hasta = pago_hasta[0:2]
            año_hasta = pago_hasta[3:7]
            periodo_hasta = calcular_periodo(mes_hasta)
            if q_mant_imp > 0:
                cant_deud = cant - q_mant_imp
                if c_f >= 0 and cant_deud < 0:
                    cant_deud = 0
                elif c_f < 0:
                    cant_deud = cant
                mant.edit_registro('operaciones', 'cuotas_favor', int(c_f)+cant_deud, oper)
                observacion = f"Pago de {cant} cuotas"
            else:
                mant.edit_registro('operaciones', 'cuotas_favor', int(c_f)+cant, oper)
                observacion = f"Adelanto de {cant} cuotas"
            mant.edit_registro('operaciones', 'ult_pago', periodo_hasta, oper)
            mant.edit_registro('operaciones', 'ult_año', año_hasta, oper)
            mant.edit_registro('operaciones', 'fecha_ult_pago', f"{mes_hasta}/{año_hasta}", oper)
            mant.edit_registro('operaciones', 'ult_rec', f"{mes_hasta}-{año_hasta[2:4]}", oper)
            fec_hoy = datetime.now().date()
            fup_date = date(year = int(año_hasta), month = int(mes_hasta), day = 1)
            cuenta = int(days_between(fup_date, fec_hoy)/730)
            if mor == 1 and cuenta <= 0:
                print()
                print("         ATENCIÓN: A partir del pago ralizado el asociado deja de ser MOROSO, indique cobrador y ruta para la operación.")
                print()
                datos = vent.obtener_cobradores()
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
                while deb_aut == 1:
                    try:
                        tarjeta = int(input("Ingrese los 16 dígitos de la tarjeta de crédito (Sin espacios): "))
                        if len(str(tarjeta)) < 16 or len(str(tarjeta)) > 16:
                            print("         ERROR. Indique un número de tarjeta válido")
                            print()
                            deb_aut = 1
                        else:
                            mant.edit_registro('operaciones', 'tarjeta', tarjeta, oper)
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
                mant.edit_registro('operaciones', 'moroso', 0, oper)
                mant.edit_registro('operaciones', 'cobrador', cobrador, oper)
                mant.edit_registro('operaciones', 'ruta', ruta, oper)
            categoria = f"Mantenimiento {obtener_panteon(pan)}"
            descripcion = f"{obtener_nom_cobrador(cob)}"
            dia = caja.obtener_dia()
            mes = caja.obtener_mes()
            año = caja.obtener_año()
            parameters = str((categoria, descripcion, rendicion, valor_total, observacion, dia, mes, año, idu))
            query = f"INSERT INTO caja (categoria, descripcion, transaccion, ingreso, observacion, dia, mes, año, id_user) VALUES {parameters}"
            run_query(query)
            print("")
            print("Adelanto de cuotas registrado exitosamente. Generando recibo, por favor aguarde...")
            parameters = str((oper, periodo_hasta, año_hasta, 1))
            query = f"INSERT INTO recibos (operacion, periodo, año, pago) VALUES {parameters}"
            run_query(query)
            ndr = obtener_nro_recibo()
            registrar_comision_mant(cob, rendicion, ndr, valor_total)
            rep.recibo_adelanto(ndr, cob, periodo_hasta, año_hasta, valor_total)
            if q_mant_imp > 0 and c_f >= 0:
                counter = 0
                for i in mant_imp:
                    counter += 1
                    nro_imp, ope_imp, per_imp, año_imp, pag_imp = i
                    set_pago(nro_imp)
                    if counter == cant:
                        break
            if q_mant_imp > 0 and c_f < 0:
                if cant > abs(c_f):
                    counter = 0
                    for i in mant_imp:
                        counter += 1
                        nro_imp, ope_imp, per_imp, año_imp, pag_imp = i
                        set_pago(nro_imp)
                        if counter == cant - abs(c_f):
                            break
                    mant.edit_registro('operaciones', 'cuotas_favor', int(c_f)+cant_deud-counter, oper)
            print("")
            return
        elif msj == "N" or msj == "n" or msj == "NO" or msj == "no" or msj == "No" or msj == "nO":
            msj = "N"
            print("")
            print("No se han realizado cambios en el registro.")
            print("")
            return
        else:
            print("")
            print("         ERROR. Debe indicar S para eliminar o N para cancelar.")
            print("")


def registrar_debito_automatico(idu):
    ndr = 0
    msj = ''
    month = datetime.now().strftime('%m')
    year = datetime.now().strftime('%Y')
    fecha = f"{month}/{year}"
    print("")
    while ndr == 0:
        try:
            ndr = int(input("Indique el número de recibo a ingresar: "))
        except ValueError:
            print("         ERROR. El dato solicitado debe ser de tipo numérico")
            return
        except:
            mant.log_error()
            print("")
            input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
            print()
            return
        msj = ''
        print("")
        try:
            nro_rec, ope, per, año, pag = obtener_datos_recibo(ndr)
        except TypeError:
            print("         ERROR. Número de recibo inexistente.")
            print()
            return
        except:
            mant.log_error()
            print("")
            input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
            print()
            return
        id_op, soc, nic, fac, cob, tar, rut, ult, u_a, fec, mor, c_f, u_r, paga, op_cob, nom_alt, dom_alt = obtener_datos_op(ope)
        cod, pan, pis, fil, num, cat, ocu, fall = obtener_datos_nicho(nic)
        id_cat, cat, val_mant_bic, val_mant_nob = obtener_categoria(cat)
        if fac == 'bicon':
            val = val_mant_bic
        elif fac == 'nob':
            val = val_mant_nob
        if per[0:3] == 'Doc':
            val = obtener_valor_doc(ope)
        nro_nicho = str(nic).rjust(10, '0')
        t01, t02, t03, t04 = split_nro_tarjeta(tar)
        cobrador = obtener_nom_cobrador(cob)
        if pag == 1:
            print("El recibo ya se encuentra ingresado en sistema.")
            msj = ''
            print("")
            while msj == '':
                msj = input(f"¿Desea ingresar otro pago? (S/N) ")
                if msj == 'S' or msj == 's' or msj == 'Si' or msj == 'SI' or msj == 'sI' or msj == 'si':
                    print("")
                    ndr = 0      
                elif msj == 'N' or msj == 'n' or msj == 'No' or msj == 'NO' or msj == 'nO' or msj == 'no':
                    print("")
                    return
                else:
                    print("")
                    print("Debe ingresar S para confirmar o N para cancelar.")
                    print("")
                    msj = ''
        elif pag == 0:
            if cob != 6:
                print("         ERROR. La operación no tiene habilitado el débito automático. Para registrar el pago seleccione la opción correcta en el menú principal.")
                msj = ''
                print("")
                while msj == '':
                    msj = input(f"¿Desea ingresar otro pago? (S/N) ")
                    if msj == 'S' or msj == 's' or msj == 'Si' or msj == 'SI' or msj == 'sI' or msj == 'si':
                        print("")
                        ndr = 0      
                    elif msj == 'N' or msj == 'n' or msj == 'No' or msj == 'NO' or msj == 'nO' or msj == 'no':
                        print("")
                        return
                    else:
                        print("")
                        print("Debe ingresar S para confirmar o N para cancelar.")
                        print("")
                        msj = ''
            elif cob == 6:
                operacion = f"{ope}".rjust(7, '0')
                while msj == '':
                    msj = input(f"¿Seguro que quiere ingresar el pago por el recibo nro. {f'{ndr}'.rjust(7, '0')} de la operación {operacion}? (S/N) ")
                    if msj == 'S' or msj == 's' or msj == 'Si' or msj == 'SI' or msj == 'sI' or msj == 'si':
                        set_pago(ndr)
                        act_periodo(per, ope, año)
                        print("")
                        cod, pan, pis, fil, num, cat, ocu, fall = obtener_datos_nicho(nic)
                        categoria = f"Mantenimiento {obtener_panteon(pan)}"
                        socio = f"{soc}".rjust(6, '0')
                        observacion = f"Recibo nro. {f'{ndr}'.rjust(7, '0')} Deb.Aut. {t04}"
                        dia = caja.obtener_dia()
                        mes = caja.obtener_mes()
                        año = caja.obtener_año()
                        parameters = str((categoria, socio, operacion, val, observacion, dia, mes, año, idu))
                        query = f"INSERT INTO debitos_automaticos (categoria, socio, operacion, igreso, observacion, dia, mes, año, id_user) VALUES {parameters}"
                        run_query(query)
                        print("Pago ingresado exitosamente")
                        print("")
                        msj = ''
                        while msj == '':
                            msj = input("Enviar recibo por email? (S/N) ")
                            print("")
                            if msj == 'S' or msj == 's' or msj == 'Si' or msj == 'SI' or msj == 'sI' or msj == 'si':
                                try:
                                    print("Enviando email. Por favor aguarde...")
                                    print("")
                                    email.envio_de_recibo(soc, id_op, per, nro_nicho, pan, t04, cobrador, nro_rec)
                                    print("Email enviado exitosamente")
                                    print("")
                                except FileNotFoundError:
                                    print("ERROR: No es posible encontrar el recibo.")
                                    print("")
                                    getpass("Presione enter para continuar...")
                                except SMTPAuthenticationError:
                                    print("ERROR: Los datos de acceso al servidor son incorrectos. El recibo no ha sido enviado.")
                                    print("")
                                    getpass("Presione enter para continuar...")
                                except gaierror:
                                    print("ERROR: No fue posible conectarse a internet. El recibo no ha sido enviado.")
                                    print("")
                                    getpass("Presione enter para continuar...")
                                except:
                                    mant.log_error()
                                    print("         ERROR. El recibo no ha sido enviado. Póngase en contacto con el administrador.")
                                    print("")
                                    getpass("Presione enter para continuar...")
                            elif msj == 'N' or msj == 'n' or msj == 'No' or msj == 'NO' or msj == 'nO' or msj == 'no':
                                print("")
                                print("El recibo no ha sido enviado.")
                    elif msj == 'N' or msj == 'n' or msj == 'No' or msj == 'NO' or msj == 'nO' or msj == 'no':
                        print("")
                        print("No se han hecho cambios en el registro.")
                    else:
                        print("")
                        print("Debe ingresar S para confirmar o N para cancelar.")
                        print("")
                        msj = ''
                msj = ''
                print("")
                while msj == '':
                    msj = input(f"¿Desea ingresar otro pago? (S/N) ")
                    if msj == 'S' or msj == 's' or msj == 'Si' or msj == 'SI' or msj == 'sI' or msj == 'si':
                        print("")
                        ndr = 0      
                    elif msj == 'N' or msj == 'n' or msj == 'No' or msj == 'NO' or msj == 'nO' or msj == 'no':
                        print("")
                        return
                    else:
                        print("")
                        print("Debe ingresar S para confirmar o N para cancelar.")
                        print("")
                        msj = ''


def reimprimir_recibo():
    ndr = 0
    while ndr == 0:
        try:
            print()
            ndr = int(input("Indique el número de recibo a reimprimir: "))
        except ValueError:
            print("         ERROR. El dato solicitado debe ser de tipo numérico")
            print()
            ndr = 0
        except:
            mant.log_error()
            print("")
            input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
            print()
            return
    try:
        nro, ope, per, año, pag = obtener_datos_recibo(ndr)
        if pag == 1:
            print("         ERROR. No se puede reimprimir un recibo que ya ha sido abonado.")
            print()
            return
        else:
            print("Confeccionando recibo. Por favor aguarde...")
            print()
            rep.reimpresion_recibo(ndr)
        print()
    except TypeError:
        print("")
        print("         ERROR. Número de recibo inválido.")
        print("")
    except:
        mant.log_error()
        print("")
        input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
        print()
    

def registrar_comision_mant(cobrador, rendicion, recibo, cobro):
    rendicion = mant.reemplazar_comilla(rendicion)
    cobradores = [6, 7, 9, 13, 15]
    if cobrador not in cobradores:
        comision = float(cobro)*0.15
        conn = sql.connect(database)
        cursor = conn.cursor()
        instruccion = f"INSERT INTO comisiones VALUES ('{cobrador}', '{rendicion}', '{recibo}', '{cobro}', '{comision}')"
        cursor.execute(instruccion)
        conn.commit()
        conn.close()


def registrar_comision_doc(cobrador, rendicion, recibo, cobro):
    rendicion = mant.reemplazar_comilla(rendicion)
    cobradores = [6, 7, 9, 13, 15]
    if cobrador not in cobradores:
        comision = float(cobro)*0.075
        conn = sql.connect(database)
        cursor = conn.cursor()
        instruccion = f"INSERT INTO comisiones VALUES ('{cobrador}', '{rendicion}', '{recibo}', '{cobro}', '{comision}')"
        cursor.execute(instruccion)
        conn.commit()
        conn.close()


def split_nro_tarjeta(tar):
    tar = str(tar)
    t1 = tar[:len(tar)//2]
    t2 = tar[len(tar)//2:]
    t01 = t1[:len(t1)//2]
    t02 = t1[len(t1)//2:]
    t03 = t2[:len(t2)//2]
    t04 = t2[len(t2)//2:]
    return t01, t02, t03, t04


def opcion_menu_facturacion():
    print("")
    print("********** Elija una distribución **********")
    print("")
    print("   1. Bicon")
    print("   2. NOB")
    print("   3. Documentos")
    print("   0. Volver")
    print("")
    opcion = -1
    while opcion -1:
        try:
            opcion = int(input("Ingrese una opción: "))
            if opcion < 0 or opcion > 3:
                print("")
                print("Opción incorrecta.")
                print("")
                opcion = -1
            else:
                return opcion
        except ValueError: 
            print("Opción incorrecta.")
            opcion = -1
        except:
            mant.log_error()
            print("")
            input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
            print()
            opcion = -1


def menu_facturacion():
    mes = int(datetime.now().strftime("%m"))
    opcion = opcion_menu_facturacion()
    if opcion == 3:
        facturacion = "documentos"
        return facturacion
    elif opcion == 0:
        return "VOLVER"
    else: 
        while opcion != 0 and mes % 2 == 0:
            if opcion == 1:
                facturacion = 'bicon'
                return 'ERROR'
            elif opcion == 2:
                facturacion = 'nob'
                return facturacion
        while opcion != 0 and mes % 2 != 0:
            if opcion == 1:
                facturacion = 'bicon'
                return facturacion
            elif opcion == 2:
                facturacion = 'nob'
                return "ERROR"


def menu_cobradores():
    print("Indique el ID de cobrador: ")
    datos = vent.obtener_cobradores()
    counter = 0
    for i in datos:
        counter += 1
        id_cob, n_cob = i
        print(f"    * {id_cob}. {n_cob}")
    print(f"    * 0. Volver")
    print()
    loop = -1
    while loop == -1:
        try:
            loop = cobrador = int(input("Cobrador: "))
            print()
            while cobrador < 0 or cobrador > counter:
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
    return cobrador


def buscar_operaciones(facturacion, id_cobrador):
    conn = sql.connect(database)
    cursor = conn.cursor()
    instruccion = f"SELECT * FROM operaciones WHERE facturacion = '{facturacion}' AND cobrador = '{id_cobrador}' ORDER BY ruta"
    cursor.execute(instruccion)
    recibos = cursor.fetchall()
    conn.commit()
    conn.close()
    return recibos


def obtener_ult_rec_de_op(id_op):
    conn = sql.connect(database)
    cursor = conn.cursor()
    cursor.execute(f"SELECT nro_recibo FROM recibos WHERE operacion = {id_op} ORDER BY nro_recibo DESC LIMIT 1")
    ult_rec = cursor.fetchone()
    conn.commit()
    conn.close()
    return ult_rec[0]


def calcular_mes(periodo, tipo):
    if periodo == "Enero - Febrero":
        mes = 1
    elif periodo == "Febrero - Marzo":
        mes = 2
    elif periodo == "Marzo - Abril":
        mes = 3
    elif periodo == "Abril - Mayo":
        mes = 4
    elif periodo == "Mayo - Junio":
        mes =5
    elif periodo == "Junio - Julio":
        mes = 6
    elif periodo == "Julio - Agosto":
        mes = 7
    elif periodo == "Agosto - Septiembre":
        mes = 8
    elif periodo == "Septiembre - Octubre":
        mes = 9
    elif periodo == "Octubre - Noviembre":
        mes = 10
    elif periodo == "Noviembre - Diciembre":
        mes = 11
    elif periodo == "Diciembre - Enero":
        mes = 12
    if tipo == 'str':
        return str(mes).rjust(2, '0')
    if tipo == 'int':
        return mes


def calcular_periodo(mes):
    try:
        mes = int(mes)
    except ValueError:
        print('ERROR. El dato solicitado debe ser de tipo numérico.')
        print()
        return
    if mes == 1:
        periodo = "Enero - Febrero"
    elif mes == 2:
        periodo = "Febrero - Marzo"
    elif mes == 3:
        periodo = "Marzo - Abril"
    elif mes == 4:
        periodo = "Abril - Mayo"
    elif mes == 5:
        periodo = "Mayo - Junio"
    elif mes == 6:
        periodo = "Junio - Julio"
    elif mes == 7:
        periodo = "Julio - Agosto"
    elif mes == 8:
        periodo = "Agosto - Septiembre"
    elif mes == 9:
        periodo = "Septiembre - Octubre"
    elif mes == 10:
        periodo = "Octubre - Noviembre"
    elif mes == 11:
        periodo = "Noviembre - Diciembre"
    elif mes == 12:
        periodo = "Diciembre - Enero"
    return periodo


def obtener_periodo():
    mes = int(datetime.now().strftime('%m'))
    if mes == 1:
        periodo_actual = "Febrero - Marzo"
        return periodo_actual
    elif mes == 2:
        periodo_actual = "Marzo - Abril"
        return periodo_actual
    elif mes == 3:
        periodo_actual = "Abril - Mayo"
        return periodo_actual
    elif mes == 4:
        periodo_actual = "Mayo - Junio"
        return periodo_actual
    elif mes == 5:
        periodo_actual = "Junio - Julio"
        return periodo_actual
    elif mes == 6:
        periodo_actual = "Julio - Agosto"
        return periodo_actual
    elif mes == 7:
        periodo_actual = "Agosto - Septiembre"
        return periodo_actual
    elif mes == 8:
        periodo_actual = "Septiembre - Octubre"
        return periodo_actual
    elif mes == 9:
        periodo_actual = "Octubre - Noviembre"
        return periodo_actual
    elif mes == 10:
        periodo_actual = "Noviembre - Diciembre"
        return periodo_actual
    elif mes == 11:
        periodo_actual = "Diciembre - Enero"
        return periodo_actual
    elif mes == 12:
        periodo_actual = "Enero - Febrero"
        return periodo_actual


def obtener_periodo_anterior(periodo_actual):
    if periodo_actual == "Enero - Febrero":
        periodo_anterior = "Noviembre - Diciembre"
        return periodo_anterior
    elif periodo_actual == "Febrero - Marzo":
        periodo_anterior = "Diciembre - Enero"
        return periodo_anterior
    elif periodo_actual == "Marzo - Abril":
        periodo_anterior = "Enero - Febrero"
        return periodo_anterior
    elif periodo_actual == "Abril - Mayo":
        periodo_anterior = "Febrero - Marzo"
        return periodo_anterior
    elif periodo_actual == "Mayo - Junio":
        periodo_anterior = "Marzo - Abril"
        return periodo_anterior
    elif periodo_actual == "Junio - Julio":
        periodo_anterior = "Abril - Mayo"
        return periodo_anterior
    elif periodo_actual == "Julio - Agosto":
        periodo_anterior = "Mayo - Junio"
        return periodo_anterior
    elif periodo_actual == "Agosto - Septiembre":
        periodo_anterior = "Junio - Julio"
        return periodo_anterior
    elif periodo_actual == "Septiembre - Octubre":
        periodo_anterior = "Julio - Agosto"
        return periodo_anterior
    elif periodo_actual == "Octubre - Noviembre":
        periodo_anterior = "Agosto - Septiembre"
        return periodo_anterior
    elif periodo_actual == "Noviembre - Diciembre":
        periodo_anterior = "Septiembre - Octubre"
        return periodo_anterior
    elif periodo_actual == "Diciembre - Enero":
        periodo_anterior = "Octubre - Noviembre"
        return periodo_anterior


def obtener_periodo_siguiente(periodo_actual):
    if periodo_actual == "Enero - Febrero":
        periodo_siguiente = "Marzo - Abril"
        return periodo_siguiente
    elif periodo_actual == "Febrero - Marzo":
        periodo_siguiente = "Abril - Mayo"
        return periodo_siguiente
    elif periodo_actual == "Marzo - Abril":
        periodo_siguiente = "Mayo - Junio"
        return periodo_siguiente
    elif periodo_actual == "Abril - Mayo":
        periodo_siguiente = "Junio - Julio"
        return periodo_siguiente
    elif periodo_actual == "Mayo - Junio":
        periodo_siguiente = "Julio - Agosto"
        return periodo_siguiente
    elif periodo_actual == "Junio - Julio":
        periodo_siguiente = "Agosto - Septiembre"
        return periodo_siguiente
    elif periodo_actual == "Julio - Agosto":
        periodo_siguiente = "Septiembre - Octubre"
        return periodo_siguiente
    elif periodo_actual == "Agosto - Septiembre":
        periodo_siguiente = "Octubre - Noviembre"
        return periodo_siguiente
    elif periodo_actual == "Septiembre - Octubre":
        periodo_siguiente = "Noviembre - Diciembre"
        return periodo_siguiente
    elif periodo_actual == "Octubre - Noviembre":
        periodo_siguiente = "Diciembre - Enero"
        return periodo_siguiente
    elif periodo_actual == "Noviembre - Diciembre":
        periodo_siguiente = "Enero - Febrero"
        return periodo_siguiente
    elif periodo_actual == "Diciembre - Enero":
        periodo_siguiente = "Febrero - Marzo"
        return periodo_siguiente


def obtener_datos_nicho(cod_nicho):
    conn = sql.connect(database)
    cursor = conn.cursor()
    instruccion = f"SELECT * FROM nichos WHERE codigo = '{cod_nicho}'"
    cursor.execute(instruccion)
    datos = cursor.fetchall()
    conn.commit()
    conn.close()
    for x in datos:
        cod, pan, pis, fil, num, cat, ocu, fall = x
    return cod, pan, pis, fil, num, cat, ocu, fall


def obtener_datos_socio(nro_socio):
    conn = sql.connect(database)
    cursor = conn.cursor()
    instruccion = f"SELECT * FROM socios WHERE nro_socio = {nro_socio}"
    cursor.execute(instruccion)
    datos = cursor.fetchall()
    conn.commit()
    conn.close()
    for x in datos:
        nro, nom, dni, te_1, te_2, mail, dom, loc, c_p, f_n, f_a, act = x
    return nro, nom, dni, te_1, te_2, mail, dom, loc, c_p, f_n, f_a, act


def obtener_nom_cobrador(id_cobrador):
    conn = sql.connect(database)
    cursor = conn.cursor()
    instruccion = f"SELECT * FROM cobradores WHERE id = '{id_cobrador}'"
    cursor.execute(instruccion)
    datos = cursor.fetchall()
    conn.commit()
    conn.close()
    for x in datos:
        nco, cob= x
    return cob


def obtener_categoria(id_cat):
    conn = sql.connect(database)
    cursor = conn.cursor()
    instruccion = f"SELECT * FROM cat_nichos WHERE id = {id_cat}"
    cursor.execute(instruccion)
    datos = cursor.fetchone()
    conn.commit()
    conn.close()
    i_d, cat, val_mant_bic, val_mant_nob = datos
    return i_d, cat, val_mant_bic, val_mant_nob


def obtener_panteon(id_pant):
    conn = sql.connect(database)
    cursor = conn.cursor()
    instruccion = f"SELECT * FROM panteones WHERE id = {id_pant}"
    cursor.execute(instruccion)
    datos = cursor.fetchone()
    conn.commit()
    conn.close()
    i_d, pant = datos
    return pant


def obtener_nro_recibo():
    conn = sql.connect(database)
    cursor = conn.cursor()
    instruccion = f"SELECT * FROM recibos ORDER BY nro_recibo DESC LIMIT 1"
    cursor.execute(instruccion)
    datos = cursor.fetchone()
    conn.commit()
    conn.close()
    nro, ope, per, año, pag  = datos
    return nro


def evitar_duplicado(mes, año2c, id_op):
    conn = sql.connect(database)
    cursor = conn.cursor()
    instruccion = f"UPDATE operaciones SET ult_rec = '{mes}-{año2c}' WHERE id = '{id_op}'"
    cursor.execute(instruccion)
    conn.commit()
    conn.close()


def obtener_recibos_impagos_op(id_op):
    conn = sql.connect(database)
    cursor = conn.cursor()
    instruccion = f"SELECT * FROM recibos WHERE operacion = {id_op} AND pago = 0 ORDER BY nro_recibo ASC"
    cursor.execute(instruccion)
    datos = cursor.fetchall()
    conn.commit()
    conn.close()
    return datos


def set_moroso(id_op):
    conn = sql.connect(database)
    cursor = conn.cursor()
    instruccion = f"UPDATE operaciones SET moroso = '{1}', cobrador = '{5}' WHERE id = {id_op}"
    cursor.execute(instruccion)
    conn.commit()
    conn.close()


def obtener_valor_doc(id_op):
    conn = sql.connect(database)
    cursor = conn.cursor()
    instruccion = f"SELECT * FROM documentos WHERE id = {id_op}"
    cursor.execute(instruccion)
    documento = cursor.fetchone()
    conn.commit()
    conn.close()
    id_op, cant_cuotas, val_cuota, ult_rec = documento
    return val_cuota


def cerrar_consola():
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


