import os
import psycopg2 as sql
import psycopg2.errors

from datetime import datetime, date
from dateutil.relativedelta import relativedelta as rd
from getpass import getpass
from smtplib import SMTPAuthenticationError
from socket import gaierror
from threading import Thread

import correo as email
import funciones_caja as caja
import funciones_mantenimiento as mant
import funciones_ventas as vent
import reporter as rep

os.system(f'TITLE Morella v{mant.VERSION} - MF! Soluciones informáticas')
os.system('color 09')   # Colores del módulo (Azul sobre negro)
os.system('mode con: cols=160 lines=9999')




def opcion_menu() -> int:                                                                           # OPCIÓN MENÚ PRINCIPAL
    """Muestra al usuario un menú y luego le solicita ingresar una de las
    opciones mostradas a través del número correspondiente. En caso de no
    ingresar una opción correcta, se le volverá a solicitar.

    :rtype: int
    """
    print()
    print("********** Acciones disponibles **********")
    print()
    print("   1. Registrar cobro")
    print("   2. Emitir recibos")
    print("   3. Ingresar pagos por adelantado")
    print("   4. Registrar débito automático")
    print("   5. Reimprimir recibo (actualiza importe)")
    print("   0. Salir")
    print()
    try:
        opcion = int(input("Ingrese una opción: "))
        while opcion < 0 or opcion > 5:
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
        print()
        opcion = -1
    return opcion


def menu(idu: int):                                                                                 # MENÚ PRINCIPAL
    """Llama a la función donde se muestra las opciones y recibe, a través de
    ella, la opción ingresada por el usuario. Luego, según la opción ingresada,
    llama a la función correspondiente.

    :param idu: ID de usuario
    :type idu: int
    """
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


def ingresar_cobro(idu: int):
    """Permite al usuario ingresar el cobro de un recibo específico.
    
    El recibo se marca como pago, se registra el movimiento en la caja y se
    registra la comisión en la tabla de comisiones.

    Si el recibo ingresado ya se encuentra pago se da aviso al usuario y se 
    finaliza la acción sin realizar cambios.

    En caso que la operación sea morosa y, a partir del pago, deje de serlo se
    le quita la condición de operación morosa y se le solicita al usuario que
    indique un cobrador nuevo.

    En caso que la operación tenga habilitado el débito automático (cobrador 6),
    se da aviso al usuario que debe hacerlo desde la opción correspondiente y se
    finaliza la acción sin realizar cambios.

    En caso que la operación tenga deuda previa a la implementación de Morella
    o recibos anteriores al que se desea ingresar, se da aviso al usuario que 
    debe realizar el pago de los mismos antes de poder realizar el pago y se 
    finaliza la acción sin realizar cambios.

    :param idu: ID de usuario
    :type idu: int
    """
    ndr = 0
    msj = ''
    print()
    
    loop = -1
    while loop == -1:
       
        while ndr == 0:
            try:
                ndr = int(input("Indique el nro. de recibo a ingresar: "))
                msj = ''
                print()    
                nro, ope, per, año, pag = obtener_datos_recibo(ndr)
    
            except ValueError:
                print()
                print("         ERROR. El dato solicitado debe ser de tipo numérico.")
                print()
                ndr = 0
            except TypeError:
                print()
                print("         ERROR. Número de recibo inválido. No se han realizado cambios en el registro.")
                print()
                return
            except:
                mant.log_error()
                print()
                input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
                print()
                return
        
        id_op, soc, nic, fac, cob, tar, rut, ult, u_a, fec, mor, c_f, u_r, paga, op_cob, nom_alt, dom_alt = obtener_datos_op(ope)
        
        try:
            cod, pan, pis, fil, num, cat, ocu, fall = obtener_datos_nicho(nic)
        
        except TypeError:
            print("         ERROR. La operación no tiene nicho asociado.")
            print()
            return
        except sql.errors.SyntaxError:
            print("         ERROR. La operación no tiene nicho asociado.")
            print()
            return
        except:
            mant.log_error()
            print()
            input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
            print()
            return
        
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
            print()
            while msj == '':
                msj = input(f"¿Desea ingresar otro pago? (S/N) ")
        
                if msj in mant.AFIRMATIVO:
                    print()
                    ndr = 0
                    loop = -1
        
                elif msj in mant.NEGATIVO:
                    print()
                    return
                else:
                    print()
                    print("Debe ingresar S para confirmar o N para cancelar.")
                    print()
                    msj = ''
        
        elif pag == 0:
       
            if cob == 6:
                print("         ERROR. La operación tiene habilitado el débito automático. Para registrar el pago seleccione la opción correcta en el menú principal.")
                msj = ''
                print()
                
                while msj == '':
                    msj = input(f"¿Desea ingresar otro pago? (S/N) ")
                    if msj in mant.AFIRMATIVO:
                        print()
                        ndr = 0
                        loop = -1
                    elif msj in mant.NEGATIVO:
                        print()
                        return
                    else:
                        print()
                        print("Debe ingresar S para confirmar o N para cancelar.")
                        print()
                        msj = ''
            
            else:
                if c_f < 0:
                    print()
                    print("         ERROR. La operación debe cuotas previas a la implementación de Morella. Debe saldar la cuenta antes de abonar un nuevo recibo.")
                    print()
                    return

                recibos_impagos = buscar_recibos_impagos(ope)

                if len(recibos_impagos) > 1:
                    if ndr == recibos_impagos[0][0]:
                        pass
                    else:
                        print()
                        print(f"         ERROR. La operación debe recibos anteriores al que está intentando ingresar.")
                        print()
                        return

                try:
                    rendicion = int(input("Indique el número de rendición: "))
        
                except ValueError:
                    print()
                    print("Número de rendición inválido. No se han realizado cambios en el registro.")
                    print()
                    return
                except:
                    mant.log_error()
                    print()
                    input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
                    print()
                    return
        
                while msj == '':
                    msj = input(f"¿Seguro que quiere ingresar el pago por el recibo nro. {f'{ndr}'.rjust(7, '0')}, perteneciente a la operación {str(ope).rjust(7, '0')} en la rendición nro. {rendicion}? (S/N) ")
        
                    if msj in mant.AFIRMATIVO:
                        set_pago(ndr)
        
                        if per[0:3] == 'Doc':
                            registrar_comision_doc(cob, rendicion, ndr, val)
        
                        else:
                            act_periodo(per, ope, año)
                            registrar_comision_mant(cob, rendicion, ndr, val) 
        
                        print()
                        cod, pan, pis, fil, num, cat, ocu, fall = obtener_datos_nicho(nic)
                        categoria = f"Mantenimiento {obtener_panteon(pan)}"
                        descripcion = f"{caja.obtener_nom_cobrador(cob)}"
                        observacion = f"Rec: {f'{ndr}'.rjust(7, '0')} - Op: {str(ope).rjust(7, '0')}"
                        dia = caja.obtener_dia()
                        mes = caja.obtener_mes()
                        año = caja.obtener_año()
        
                        parameters = str((categoria, descripcion, rendicion, val, observacion, dia, mes, año, idu))
                        query = f"INSERT INTO caja (categoria, descripcion, transaccion, ingreso, observacion, dia, mes, año, id_user) VALUES {parameters}"
        
                        mant.run_query(query)
        
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
        
                                cobrador = menu_cobradores()
        
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
                                            print()
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
                                        print()
                                        input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
                                        print()
                                        return
        
                                mant.edit_registro('operaciones', 'moroso', 0, ope)
                                mant.edit_registro('operaciones', 'cobrador', cobrador, ope)
                                mant.edit_registro('operaciones', 'ruta', ruta, ope)
                        print("Pago ingresado exitosamente")
        
                    elif msj in mant.NEGATIVO:
                        print()
                        print("No se han hecho cambios en el registro.")
                    else:
                        print()
                        print("Debe ingresar S para confirmar o N para cancelar.")
                        print()
                        msj = ''
        
                msj = ''
                print()
                while msj == '':
                    msj = input(f"¿Desea ingresar otro pago? (S/N) ")
        
                    if msj in mant.AFIRMATIVO:
                        print()
                        ndr = 0
                        loop = -1
        
                    elif msj in mant.NEGATIVO:
                        print()
                        return
                    else:
                        print()
                        print("Debe ingresar S para confirmar o N para cancelar.")
                        print()
                        msj = ''


def ingresar_cobro_auto(ope: int, c_f: int, u_r: str):
    """Modifica en la base de datos las cuotas a favor y el último
    recibo de una operación específica a partir de su ID.

    :param ope: ID de operación.
    :type ope: int

    :param c_f: Nueva cantidad de cuotas a favor.
    :type c_f: int

    :param u_r: Nuevo último recibo
    :type u_r: str
    """
    with sql.connect(mant.DATABASE) as conn:
        cursor = conn.cursor()
        instruccion = f"UPDATE operaciones SET cuotas_favor = '{c_f}', ult_rec = '{u_r}' WHERE id = '{ope}'"
        cursor.execute(instruccion)


def obtener_datos_op(ope: int) -> tuple:
    """Recupera de la base de datos toda la información de una operación
    específica y la retorna en una tupla.

    :param ope: ID de operación.
    :type ope: int

    :rtype: tuple
    """
    with sql.connect(mant.DATABASE) as conn:
        cursor = conn.cursor()
        instruccion = f"SELECT * FROM operaciones WHERE id = {ope}"
        cursor.execute(instruccion)
        datos = cursor.fetchone()
    
    i_d, soc, nic, fac, cob, tar, rut, ult, u_a, fec, mor, c_f, u_r, paga, op_cob, nom_alt, dom_alt = datos
    return i_d, soc, nic, fac, cob, tar, rut, ult, u_a, fec, mor, c_f, u_r, paga, op_cob, nom_alt, dom_alt


def obtener_str_mes(mes: str) -> str:
    """Recibe una cadena con un número de dos dígitos del uno al doce
    y retorna una cadena con el nombre del mes correspondiente.

    :param mes: Mes en número de dos dígitos.
    :type mes: str

    :rtype: str
    """
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


def obtener_mes_siguiente(mes: str) -> tuple:
    """Recibe una cadena con un número de dos dígitos del uno al doce
    y retorna una tupla que contiene dos cadenas, una con el nombre
    correspondiente al mes siguiente y otra con el número de
    dos dígitos correspondiente al mes siguiente.

    :param mes: Mes en número de dos dígitos.
    :type mes: str

    :rtype: tuple
    """
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


def days_between(d1: date, d2: date) -> int:
    """Recibe dos fechas y retorna la diferencia absoluta en días entre ellas.

    :param d1: Fecha 1
    :type d1: datetime.date

    :param d2: Fecha 2
    :type d2: datetime.date

    :rtype: int
    """
    return (d2-d1).days


def set_pago(ndr: int):
    """Cambia el estado de un recibo impago específico a pago.

    :param ndr: Número de recibo
    :type ndr: int
    """
    with sql.connect(mant.DATABASE) as conn:
        cursor = conn.cursor()
        instruccion = f"UPDATE recibos SET pago = '1' WHERE nro_recibo = '{ndr}'"
        cursor.execute(instruccion)


def act_periodo(per: str, ope: int, año: str):
    """Modifica el último pago, último año y fecha del último pago de una
    operación específica a partir de su ID.

    :param per: Período que paga.
    :type per: str

    :param ope: ID de operación.
    :type ope: int

    :param año: Año del período que paga.
    :type año: str
    """
    mes = calcular_mes(per, 'str')
    fecha = f"{mes}/{año}"
    
    with sql.connect(mant.DATABASE) as conn:
        cursor = conn.cursor()
        instruccion = f"UPDATE operaciones SET ult_pago = '{per}', ult_año = '{año}', fecha_ult_pago = '{fecha}' WHERE id = '{ope}'"
        cursor.execute(instruccion)


def obtener_datos_recibo(ndr: int) -> tuple:
    """Recupera de la base de datos toda la información de un recibo
    a partir del número de recibo (ID) y la retorna en una tupla.

    :param ndr: Número de recibo
    :type ndr: int
    """
    with sql.connect(mant.DATABASE) as conn:
        cursor = conn.cursor()
        instruccion = f"SELECT * FROM recibos WHERE nro_recibo = '{ndr}'"
        cursor.execute(instruccion)
        datos = cursor.fetchone()
    
    nro, ope, per, año, pag = datos
    return nro, ope, per, año, pag


def emitir_recibos():
    """Muestra al usuario un menú y luego le solicita ingresar una de las
    opciones mostradas a través del número correspondiente. Luego permite
    al usuario realizar la emisión de recibos de una facturación y
    cobrador específicos.
    """
    facturacion = menu_facturacion()
    
    if facturacion == "ERROR":
        print()
        print("         ERROR. El período de facturación no corresponde con el mes.")
    
    elif facturacion == "VOLVER":
        print()
        return
    
    elif facturacion == "documentos":
        mes = datetime.now().strftime('%m')
        str_mes_siguiente, int_mes_siguiente = obtener_mes_siguiente(mes)
        print()
        msj = ""
    
        while msj != "S" and msj != "N":
            msj = input(f"¿Emitir recibos de documentos de {str_mes_siguiente}? (S/N) ")
    
            if msj in mant.AFIRMATIVO:
                msj = "S"
                print()
                print("POR FAVOR, NO CIERRE LA APLICACIÓN NI APAGUE EL SISTEMA MIENTRAS SE REALIZAN LAS ACCIONES SOLICITADAS")
                print()
                print("Emitiendo recibos...")
                lista_recibos = rep.recibos_documentos()
                print()
                print("Confeccionando listado...")
                rep.listado_recibos_documentos(lista_recibos)
                print()
                return
            
            elif msj in mant.NEGATIVO:
                msj = "N"
                print()
                print("No se han emitido recibos.")
                print()
                return
            else:
                print()
                print("         ERROR. Debe indicar S para emitir o N para cancelar.")
                print()
    
    else:
        cobrador = menu_cobradores()
    
        if cobrador == 0:
            return
    
        ncobrador = caja.obtener_nom_cobrador(cobrador)
        periodo = obtener_periodo()
        print()
    
        msj = input(f"¿Emitir recibos de {periodo}, de {facturacion.upper()} - {ncobrador}? (S/N) ")
        while msj != "S" and msj != "N":
    
            if msj in mant.AFIRMATIVO:
                msj = "S"
                print()
                print("POR FAVOR, NO CIERRE LA APLICACIÓN NI APAGUE EL SISTEMA MIENTRAS SE REALIZAN LAS ACCIONES SOLICITADAS")
                print()
                print("Emitiendo recibos...")
                recibos = buscar_recibos(facturacion, cobrador)

                # NO débito automático
                if cobrador != 6:
                    thread1 = Thread(target=rep.recibos, args=(facturacion, recibos))
                    thread2 = Thread(target=rep.listado_recibos, args=(cobrador, recibos))
                    thread1.start()
                    thread2.start()
                    thread1.join()
                    thread2.join()
                    print()
                    return

                # Débito automático
                elif cobrador == 6:
                    thread1 = Thread(target=rep.recibos_deb_aut, args=(recibos))
                    thread2 = Thread(target=rep.listado_recibos_deb_aut, args=(recibos))
                    thread1.start()
                    thread2.start()
                    thread1.join()
                    thread2.join()
                    print()
                    return
    
            elif msj in mant.NEGATIVO:
                msj = "N"
                print()
                print("No se han emitido recibos.")
                print()
                return
            else:
                print()
                print("         ERROR. Debe indicar S para emitir o N para cancelar.")
                print()
                msj = input(f"¿Imprimir recibos de {periodo}, de {facturacion} - {ncobrador}? (S/N) ")
                print()
            

def ingresar_adelantos(idu: int):
    """Permite al usuario ingresar el cobro de una o más cuotas sin 
    tener que especificar un número de recibo. Si la operación no
    tiene recibos pendientes o deuda previa a la implementación de
    Morella, se registra un adelanto de cuotas, de lo contrario se
    realiza el pago de la cantidad de cuotas que sean indicadas y,
    en caso de indicar una cantidad mayor de cuotas que las que la
    operación debe, se registra un adelanto por el restante.

    Al finalizar se genera un recibo en PDF por el monto total,
    especificando el período hasta el cual se realizó el pago.

    En caso que la operación tenga documentos sin abonar se dará
    aviso al usuario y se terminará la acción sin registrar cambios.

    :param idu: ID de usuario.
    :type idu: int
    """
    print()
    try:
        oper = int(input("Indique el número de operación: "))
    
    except ValueError:
        print("         ERROR. El dato solicitado debe ser de tipo numérico")
        return
    except:
        mant.log_error()
        print()
        input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
        print()
        return
    print()
    
    try:
        i_d, soc, nic, fac, cob, tar, rut, ult, u_a, fec, mor, c_f, u_r, paga, op_cob, nom_alt, dom_alt = obtener_datos_op(oper)
        soc, nom, dni, te_1, te_2, mail, dom, loc, c_p, f_n, f_a, act = obtener_datos_socio(soc)
    
        if nom_alt:
            nom = nom_alt
    
        if dom_alt:
            dom = dom_alt
    
        if ult == 'Diciembre - Enero':
            ultimo_pago = f'{ult} {u_a}/{int(str(u_a)[-2:])+1}'
    
        else:
            ultimo_pago = f'{ult} {u_a}'
        print(f'Operación: {str(i_d).rjust(7, "0")} - {nom}. Domicilio: {dom}. Último pago: {ultimo_pago}')
    
    except TypeError:
        print("         ERROR. Número de operación inexistente.")
        return
    except:
        mant.log_error()
        print()
        input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
        print()
        return
    
    try:
        cod, pan, pis, fil, num, cat, ocu, fall = obtener_datos_nicho(nic)
    
    except TypeError:
        print("         ERROR. La operación no tiene nicho asociado.")
        print()
        return
    except sql.errors.SyntaxError:
        print("         ERROR. La operación no tiene nicho asociado.")
        print()
        return
    except:
        mant.log_error()
        print()
        input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
        print()
        return
    
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
        print()
        input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
        print()
        return
    
    if fac == 'bicon':
        valor_total = val_mant_bic * cant
    
    elif fac == 'nob':
        valor_total = val_mant_nob * cant
    print()
    
    try:
        rendicion = int(input("Indique el número de rendición: "))
    
    except ValueError:
        print("         ERROR. El dato solicitado debe ser de tipo numérico")
        return
    except:
        mant.log_error()
        print()
        input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
        print()
        return
    print()
    
    operacion = str(oper).rjust(7, "0")
    print(f"Se registrará el ingreso de $ {valor_total:.2f} correspondiente al pago de {cant} cuotas de la operación {operacion}")
    print()
    
    msj = ""
    while msj != "S" and msj != "N":
        msj = input("¿Está seguro de realizar el registro? (S/N): ")
    
        if msj in mant.AFIRMATIVO:
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
                observacion = f"Pago {cant} cuotas. Op: {operacion}"
    
            else:
                mant.edit_registro('operaciones', 'cuotas_favor', int(c_f)+cant, oper)
                observacion = f"Adel. {cant} cuotas. Op: {operacion}"
    
            mant.edit_registro('operaciones', 'ult_pago', periodo_hasta, oper)
            mant.edit_registro('operaciones', 'ult_año', año_hasta, oper)
            mant.edit_registro('operaciones', 'fecha_ult_pago', f"{mes_hasta}/{año_hasta}", oper)
    
            fec_hoy = datetime.now().date()
            fup_date = date(year = int(año_hasta), month = int(mes_hasta), day = 1)
            cuenta = int(days_between(fup_date, fec_hoy)/730)
    
            if mor == 1 and cuenta <= 0:
                print()
                print("         ATENCIÓN: A partir del pago ralizado el asociado deja de ser MOROSO, indique cobrador y ruta para la operación.")
                print()
                
                cobrador = menu_cobradores()
    
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
                            print()
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
                        print()
                        input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
                        print()
                        return

                mant.edit_registro('operaciones', 'moroso', 0, oper)
                mant.edit_registro('operaciones', 'cobrador', cobrador, oper)
                mant.edit_registro('operaciones', 'ruta', ruta, oper)

            categoria = f"Mantenimiento {obtener_panteon(pan)}"
            descripcion = f"{caja.obtener_nom_cobrador(cob)}"
            dia = caja.obtener_dia()
            mes = caja.obtener_mes()
            año = caja.obtener_año()

            parameters = str((categoria, descripcion, rendicion, valor_total, observacion, dia, mes, año, idu))
            query = f"INSERT INTO caja (categoria, descripcion, transaccion, ingreso, observacion, dia, mes, año, id_user) VALUES {parameters}"

            mant.run_query(query)

            print()
            print("Adelanto de cuotas registrado exitosamente. Generando recibo, por favor aguarde...")

            parameters = str((oper, periodo_hasta, año_hasta, 1))
            query = f"INSERT INTO recibos (operacion, periodo, año, pago) VALUES {parameters}"

            mant.run_query(query)

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

            print()
            return

        elif msj in mant.NEGATIVO:
            msj = "N"
            print()
            print("No se han realizado cambios en el registro.")
            print()
            return
        else:
            print()
            print("         ERROR. Debe indicar S para eliminar o N para cancelar.")
            print()


def registrar_debito_automatico(idu: int):
    """Permite al usuario ingresar el cobro de un recibo de débito automático
    específico.
    
    El recibo se marca como pago y se registra el movimiento en la tabla de
    débitos automáticos, luego se genera un reporte en PDF del mismo y se le
    ofrece al usuario realizar el envío por mail al asociodo correspondiente.

    Si el recibo ingresado ya se encuentra pago se da aviso al usuario y se 
    finaliza la acción sin realizar cambios.

    :param idu: ID de usuario
    :type idu: int
    """
    ndr = 0
    msj = ''
    month = datetime.now().strftime('%m')
    year = datetime.now().strftime('%Y')
    print()
    
    while ndr == 0:
        try:
            ndr = int(input("Indique el número de recibo a ingresar: "))
    
        except ValueError:
            print("         ERROR. El dato solicitado debe ser de tipo numérico")
            return
        except:
            mant.log_error()
            print()
            input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
            print()
            return
    
        msj = ''
        print()
        try:
            nro_rec, ope, per, año, pag = obtener_datos_recibo(ndr)
    
        except TypeError:
            print("         ERROR. Número de recibo inexistente.")
            print()
            return
        except:
            mant.log_error()
            print()
            input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
            print()
            return
    
        id_op, soc, nic, fac, cob, tar, rut, ult, u_a, fec, mor, c_f, u_r, paga, op_cob, nom_alt, dom_alt = obtener_datos_op(ope)
    
        try:
            cod, pan, pis, fil, num, cat, ocu, fall = obtener_datos_nicho(nic)
    
        except TypeError:
            print("         ERROR. La operación no tiene nicho asociado.")
            print()
            return
        except sql.errors.SyntaxError:
            print("         ERROR. La operación no tiene nicho asociado.")
            print()
            return
        except:
            mant.log_error()
            print()
            input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
            print()
            return
    
        id_cat, cat, val_mant_bic, val_mant_nob = obtener_categoria(cat)
    
        if fac == 'bicon':
            val = val_mant_bic
    
        elif fac == 'nob':
            val = val_mant_nob
    
        if per[0:3] == 'Doc':
            val = obtener_valor_doc(ope)
    
        nro_nicho = str(nic).rjust(10, '0')
        t01, t02, t03, t04 = split_nro_tarjeta(tar)
        cobrador = caja.obtener_nom_cobrador(cob)
    
        if pag == 1:
            print("El recibo ya se encuentra ingresado en sistema.")
            msj = ''
            print()
            while msj == '':
                msj = input(f"¿Desea ingresar otro pago? (S/N) ")
    
                if msj in mant.AFIRMATIVO:
                    print()
                    ndr = 0      
    
                elif msj in mant.NEGATIVO:
                    print()
                    return
                else:
                    print()
                    print("Debe ingresar S para confirmar o N para cancelar.")
                    print()
                    msj = ''
    
        elif pag == 0:
            if cob != 6:
                print("         ERROR. La operación no tiene habilitado el débito automático. Para registrar el pago seleccione la opción correcta en el menú principal.")
                msj = ''
                print()
    
                while msj == '':
                    msj = input(f"¿Desea ingresar otro pago? (S/N) ")
    
                    if msj in mant.AFIRMATIVO:
                        print()
                        ndr = 0      
    
                    elif msj in mant.NEGATIVO:
                        print()
                        return
                    else:
                        print()
                        print("Debe ingresar S para confirmar o N para cancelar.")
                        print()
                        msj = ''
    
            elif cob == 6:
                operacion = f"{ope}".rjust(7, '0')
    
                while msj == '':
                    msj = input(f"¿Seguro que quiere ingresar el pago por el recibo nro. {f'{ndr}'.rjust(7, '0')} de la operación {operacion}? (S/N) ")
                    if msj in mant.AFIRMATIVO:
                        set_pago(ndr)
                        act_periodo(per, ope, año)
                        print()
                        cod, pan, pis, fil, num, cat, ocu, fall = obtener_datos_nicho(nic)
                        categoria = f"Mantenimiento {obtener_panteon(pan)}"
                        socio = f"{soc}".rjust(6, '0')
                        observacion = f"Recibo nro. {f'{ndr}'.rjust(7, '0')} Deb.Aut. {t04}"
                        dia = caja.obtener_dia()
                        mes = caja.obtener_mes()
                        año = caja.obtener_año()
    
                        parameters = str((categoria, socio, operacion, val, observacion, dia, mes, año, idu))
                        query = f"INSERT INTO debitos_automaticos (categoria, socio, operacion, igreso, observacion, dia, mes, año, id_user) VALUES {parameters}"
    
                        mant.run_query(query)
    
                        print("Pago ingresado exitosamente")
                        print()
                        msj = ''
    
                        while msj == '':
                            msj = input("Enviar recibo por email? (S/N) ")
                            print()
    
                            if msj in mant.AFIRMATIVO:
                                try:
                                    print("Enviando email. Por favor aguarde...")
                                    print()
                                    email.envio_de_recibo(soc, id_op, per, nro_nicho, pan, t04, cobrador, nro_rec)
                                    print("Email enviado exitosamente")
                                    print()
    
                                except FileNotFoundError:
                                    print("ERROR: No es posible encontrar el recibo.")
                                    print()
                                    getpass("Presione enter para continuar...")
                                except SMTPAuthenticationError:
                                    print("ERROR: Los datos de acceso al servidor son incorrectos. El recibo no ha sido enviado.")
                                    print()
                                    getpass("Presione enter para continuar...")
                                except gaierror:
                                    print("ERROR: No fue posible conectarse a internet. El recibo no ha sido enviado.")
                                    print()
                                    getpass("Presione enter para continuar...")
                                except:
                                    mant.log_error()
                                    print("         ERROR. El recibo no ha sido enviado. Póngase en contacto con el administrador.")
                                    print()
                                    getpass("Presione enter para continuar...")
    
                            elif msj in mant.NEGATIVO:
                                print()
                                print("El recibo no ha sido enviado.")
    
                    elif msj in mant.NEGATIVO:
                        print()
                        print("No se han hecho cambios en el registro.")
                    else:
                        print()
                        print("Debe ingresar S para confirmar o N para cancelar.")
                        print()
                        msj = ''
    
                msj = ''
                print()
                while msj == '':
                    msj = input(f"¿Desea ingresar otro pago? (S/N) ")
    
                    if msj in mant.AFIRMATIVO:
                        print()
                        ndr = 0      
    
                    elif msj in mant.NEGATIVO:
                        print()
                        return
                    else:
                        print()
                        print("Debe ingresar S para confirmar o N para cancelar.")
                        print()
                        msj = ''


def reimprimir_recibo():
    """Permite al usuario reimprimir un recibo que se encuentre impago con el importe
    actualizado al precio de la fecha.
    """
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
            print()
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
        print()
        print("         ERROR. Número de recibo inválido.")
        print()
    except:
        mant.log_error()
        print()
        input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
        print()
    

def registrar_comision_mant(cobrador: int, rendicion: int, recibo: int, cobro: float | int):
    """Si se indica un ID de cobrador que comisione, se calcula la comisión
    correspondiente al cobro de una cuota de mantenimiento y se registra en
    la base de datos junto con el resto de la información solicitada.

    :param cobrador: ID de cobrador
    :type cobrador: int

    :param rendicion: Número de rendición
    :type rendicion: int

    :param recibo: Número de recibo
    :type recibo: int

    :param cobro: Monto total cobrado
    :type cobro: float or int
    """
    rendicion = mant.reemplazar_comilla(rendicion)
    cobradores = [6]
    
    if cobrador not in cobradores:
        comision = float(cobro)*0.15
    
        with sql.connect(mant.DATABASE) as conn:
            cursor = conn.cursor()
            instruccion = f"INSERT INTO comisiones VALUES ('{cobrador}', '{rendicion}', '{recibo}', '{cobro}', '{comision}')"
            cursor.execute(instruccion)


def registrar_comision_doc(cobrador: int, rendicion: int, recibo: int, cobro: float | int):
    """Si se indica un ID de cobrador que comisione, se calcula la comisión
    correspondiente al cobro de una cuota de un documento y se registra en
    la base de datos junto con el resto de la información solicitada.

    :param cobrador: ID de cobrador
    :type cobrador: int

    :param rendicion: Número de rendición
    :type rendicion: int

    :param recibo: Número de recibo
    :type recibo: int

    :param cobro: Monto total cobrado
    :type cobro: float or int
    """
    rendicion = mant.reemplazar_comilla(rendicion)
    cobradores = [6, 7, 9, 13, 15]
    if cobrador not in cobradores:
        comision = float(cobro)*0.075
        conn = sql.connect(mant.DATABASE)
        cursor = conn.cursor()
        instruccion = f"INSERT INTO comisiones VALUES ('{cobrador}', '{rendicion}', '{recibo}', '{cobro}', '{comision}')"
        cursor.execute(instruccion)
        conn.commit()
        conn.close()


def split_nro_tarjeta(tar: int) -> tuple:
    """Recibe los dieciseis dígitos de una tarjeta de crédito y lo
    retorna una tupla conteniendo cuatro bloques de cuatro números.

    :param tar: Dieciseis dígitos de la tarjeta (sin espacios)
    :type tar: int

    :rtype: tuple
    """
    tar = str(tar)

    t1 = tar[:len(tar)//2]
    t2 = tar[len(tar)//2:]
    
    t01 = t1[:len(t1)//2]
    t02 = t1[len(t1)//2:]
    
    t03 = t2[:len(t2)//2]
    t04 = t2[len(t2)//2:]

    return t01, t02, t03, t04


def opcion_menu_facturacion() -> int:
    """Muestra al usuario un menú y luego le solicita ingresar una de las
    opciones mostradas a través del número correspondiente. En caso de no
    ingresar una opción correcta, se le volverá a solicitar.

    :rtype: int
    """
    print()
    print("********** Elija una distribución **********")
    print()
    print("   1. Bicon")
    print("   2. NOB")
    print("   3. Documentos")
    print("   0. Volver")
    print()
    opcion = -1
    while opcion -1:
        try:
            opcion = int(input("Ingrese una opción: "))
            if opcion < 0 or opcion > 3:
                print()
                print("Opción incorrecta.")
                print()
                opcion = -1
            else:
                return opcion
        except ValueError: 
            print("Opción incorrecta.")
            opcion = -1
        except:
            mant.log_error()
            print()
            input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
            print()
            opcion = -1


def menu_facturacion() -> str:
    """Llama a la función donde se muestra las opciones y recibe, a través de
    ella, la opción ingresada por el usuario. Luego, según la opción ingresada,
    retorna una cadena donde indica si la opción ingresada se encuentra en un
    mes válido para dicha opción:

    - Bicon: Meses impares.
    - NOB: Meses pares.
    - Documentos: Todos los meses.

    En caso de seleccionar una opción en un inválido se retorna ERROR y, si se
    indica la opción cero, se retorna VOLVER.

    :param idu: ID de usuario
    :type idu: int
    """
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


def menu_cobradores() -> int:
    """Desplega un menú con los cobradores y permite al usuario elegir uno
    a partir de su ID, el cual es retornado.
    """
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
            print()
            input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
            print()
            return
    
    return cobrador


def buscar_recibos(facturacion: str, id_cobrador: int) -> list:
    """Recupera de la base de datos todas las operaciones que tengan el pago
    habilitado, pertenecientes a un cobrador y una facturación específica,
    ordernados por ruta y los retorna en una lista.

    :param facturacion: Tipo de facturación (bicon o nob)
    :type facturacion: str

    :param id_cobrador: ID del cobrador
    :type id_cobrador: int

    :rtype: list
    """
    with sql.connect(mant.DATABASE) as conn:
        cursor = conn.cursor()
        instruccion = f"SELECT * FROM operaciones WHERE facturacion = '{facturacion}' AND cobrador = '{id_cobrador}' AND paga = 1 ORDER BY ruta"
        cursor.execute(instruccion)
        recibos = cursor.fetchall()
    return recibos


def obtener_ult_rec_de_op(id_op: int) -> int:
    """Recupera de la base de datos el número del último recibo
    perteneciente a una operación específica y lo retorna.

    :param id_op: ID de operación
    :type id_op: int

    :rtype: int
    """
    with sql.connect(mant.DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute(f"SELECT nro_recibo FROM recibos WHERE operacion = {id_op} ORDER BY nro_recibo DESC LIMIT 1")
        ult_rec = cursor.fetchone()
    return ult_rec[0]


def calcular_mes(periodo: str, tipo: str) -> str | int:
    """Recibe una cadena de un período bimestral y retorna el
    primer mes correspondiente. Permite al usuario elegir entre 
    retornarlo como un entero o como una cadena de dos dígitos.

    :param periodo: Período bimestral
    :type periodo: str

    :param tipo: Tipo de retorno (str o int)
    :type tipo: str

    :rtype: str or int
    """
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


def calcular_periodo(mes: int) -> str:
    """Recibe el mes como un entero y retorna una cadena
    con su bimestre correspondiente.

    :param mes: Mes (número)
    :type mes: int

    :rtype: str
    """
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


def obtener_periodo() -> str:
    """Obtiene el mes actual y retorna una cadena con el período
    correspondiente al siguiente mes.

    :rtype: str
    """
    mes = int(datetime.now().strftime('%m'))
    
    if mes == 1:
        periodo_siguiente = "Febrero - Marzo"
    elif mes == 2:
        periodo_siguiente = "Marzo - Abril"
    elif mes == 3:
        periodo_siguiente = "Abril - Mayo"
    elif mes == 4:
        periodo_siguiente = "Mayo - Junio"
    elif mes == 5:
        periodo_siguiente = "Junio - Julio"
    elif mes == 6:
        periodo_siguiente = "Julio - Agosto"
    elif mes == 7:
        periodo_siguiente = "Agosto - Septiembre"
    elif mes == 8:
        periodo_siguiente = "Septiembre - Octubre"
    elif mes == 9:
        periodo_siguiente = "Octubre - Noviembre"
    elif mes == 10:
        periodo_siguiente = "Noviembre - Diciembre"
    elif mes == 11:
        periodo_siguiente = "Diciembre - Enero"
    elif mes == 12:
        periodo_siguiente = "Enero - Febrero"
    
    return periodo_siguiente


def obtener_periodo_anterior(periodo_actual: str) -> str:
    """Recibe una cadena con el período actual y retorna otra con el período anterior.

    :param periodo_actual: Período actual
    :type periodo_actual: str

    :rtype: str
    """
    if periodo_actual == "Enero - Febrero":
        periodo_anterior = "Noviembre - Diciembre"
        
    elif periodo_actual == "Febrero - Marzo":
        periodo_anterior = "Diciembre - Enero"
        
    elif periodo_actual == "Marzo - Abril":
        periodo_anterior = "Enero - Febrero"
        
    elif periodo_actual == "Abril - Mayo":
        periodo_anterior = "Febrero - Marzo"
        
    elif periodo_actual == "Mayo - Junio":
        periodo_anterior = "Marzo - Abril"
        
    elif periodo_actual == "Junio - Julio":
        periodo_anterior = "Abril - Mayo"
        
    elif periodo_actual == "Julio - Agosto":
        periodo_anterior = "Mayo - Junio"
        
    elif periodo_actual == "Agosto - Septiembre":
        periodo_anterior = "Junio - Julio"
        
    elif periodo_actual == "Septiembre - Octubre":
        periodo_anterior = "Julio - Agosto"
        
    elif periodo_actual == "Octubre - Noviembre":
        periodo_anterior = "Agosto - Septiembre"
        
    elif periodo_actual == "Noviembre - Diciembre":
        periodo_anterior = "Septiembre - Octubre"
        
    elif periodo_actual == "Diciembre - Enero":
        periodo_anterior = "Octubre - Noviembre"
    
    else:
        periodo_anterior = "ERROR"
    
    return periodo_anterior


def obtener_periodo_siguiente(periodo_actual: str) -> str:
    """Recibe una cadena con el período actual y retorna otra con el período siguiente.

    :param periodo_actual: Período actual
    :type periodo_actual: str

    :rtype: str
    """
    if periodo_actual == "Enero - Febrero":
        periodo_siguiente = "Marzo - Abril"

    elif periodo_actual == "Febrero - Marzo":
        periodo_siguiente = "Abril - Mayo"

    elif periodo_actual == "Marzo - Abril":
        periodo_siguiente = "Mayo - Junio"

    elif periodo_actual == "Abril - Mayo":
        periodo_siguiente = "Junio - Julio"

    elif periodo_actual == "Mayo - Junio":
        periodo_siguiente = "Julio - Agosto"

    elif periodo_actual == "Junio - Julio":
        periodo_siguiente = "Agosto - Septiembre"

    elif periodo_actual == "Julio - Agosto":
        periodo_siguiente = "Septiembre - Octubre"

    elif periodo_actual == "Agosto - Septiembre":
        periodo_siguiente = "Octubre - Noviembre"

    elif periodo_actual == "Septiembre - Octubre":
        periodo_siguiente = "Noviembre - Diciembre"

    elif periodo_actual == "Octubre - Noviembre":
        periodo_siguiente = "Diciembre - Enero"

    elif periodo_actual == "Noviembre - Diciembre":
        periodo_siguiente = "Enero - Febrero"

    elif periodo_actual == "Diciembre - Enero":
        periodo_siguiente = "Febrero - Marzo"

    else:
        periodo_siguiente = "ERROR"

    return periodo_siguiente


def obtener_datos_nicho(cod_nicho: str) -> tuple:
    """Recupera de la base de datos toda la información de un nicho
    específico a partir de su código único y la retorna en una tupla.

    :param cod_nicho: Código único de nicho
    :type cod_nicho: str

    :rtype: tuple
    """
    with sql.connect(mant.DATABASE) as conn:
        cursor = conn.cursor()
        instruccion = f"SELECT * FROM nichos WHERE codigo = '{cod_nicho}'"
        cursor.execute(instruccion)
        datos = cursor.fetchone()

    cod, pan, pis, fil, num, cat, ocu, fall = datos
    return cod, pan, pis, fil, num, cat, ocu, fall


def obtener_datos_socio(nro_socio: int) -> tuple:
    """Recupera de la base de datos toda la información de
    un asociado a partir de su ID de asociado y la retorna
    en una tupla.

    :param nro_socio: ID de asociado.
    :type nro_socio: int

    :rtype: tuple
    """
    with sql.connect(mant.DATABASE) as conn:
        cursor = conn.cursor()
        instruccion = f"SELECT * FROM socios WHERE nro_socio = '{nro_socio}'"
        cursor.execute(instruccion)
        datos = cursor.fetchone()

    nro, nom, dni, te_1, te_2, mail, dom, loc, c_p, f_n, f_a, act = datos
    return nro, nom, dni, te_1, te_2, mail, dom, loc, c_p, f_n, f_a, act


def obtener_categoria(id_cat: int) -> tuple:
    """Recupera de la base de datos toda la información de una categoría
    de nicho específica a través de su ID y la retorna en una tupla.

    :param id_cat: ID de categoría de nicho
    :type id_cat: int

    :rtype: tuple
    """
    with sql.connect(mant.DATABASE) as conn:
        cursor = conn.cursor()
        instruccion = f"SELECT * FROM cat_nichos WHERE id = {id_cat}"
        cursor.execute(instruccion)
        datos = cursor.fetchone()

    i_d, cat, val_mant_bic, val_mant_nob = datos
    return i_d, cat, val_mant_bic, val_mant_nob


def obtener_panteon(id_pant: int) -> str:
    """Recupera de la base de datos el nombre de un panteón
    específico y lo retorna.
    
    :param id_pant: ID de panteón.
    :type id_pant: int

    :rtype: str
    """
    with sql.connect(mant.DATABASE) as conn:
        cursor = conn.cursor()
        instruccion = f"SELECT panteon FROM panteones WHERE id = {id_pant}"
        cursor.execute(instruccion)
        datos = cursor.fetchone()

    return datos[0]


def obtener_nro_recibo() -> int:
    """Recupera de la base de datos el número del último recibo
    y lo retorna.

    :rtype: int
    """
    with sql.connect(mant.DATABASE) as conn:
        cursor = conn.cursor()
        instruccion = f"SELECT nro_recibo FROM recibos ORDER BY nro_recibo DESC LIMIT 1"
        cursor.execute(instruccion)
        datos = cursor.fetchone()

    return datos[0]


def evitar_duplicado(mes: str, año2c: str, id_op: int):
    """Modifica el último recibo de una operación específica.
    
    :param mes: Mes (cadena, dos dígitos)
    :type mes: str
    
    :param año2c: Año (cadena, dos dígitos)
    :type año2c: str
    
    :param id_op: ID de operación
    :type id_op: int
    """
    with sql.connect(mant.DATABASE) as conn:
        cursor = conn.cursor()
        instruccion = f"UPDATE operaciones SET ult_rec = '{mes}-{año2c}' WHERE id = '{id_op}'"
        cursor.execute(instruccion)


def obtener_recibos_impagos_op(id_op: int) -> list:
    """Recupera de la base de datos toda la información de los recibos
    impagos pertenecientes a una operación específica, ordenados por
    número de recibo y la retorna en una lista.
    
    :param id_op: ID de operación
    :type id_op: int

    :rtype: list
    """
    with sql.connect(mant.DATABASE) as conn:
        cursor = conn.cursor()
        instruccion = f"SELECT * FROM recibos WHERE operacion = {id_op} AND pago = 0 ORDER BY nro_recibo ASC"
        cursor.execute(instruccion)
        datos = cursor.fetchall()

    return datos


def set_moroso(id_op: int):
    """Marca una operación específica como morosa y se le asigna el cobrador cinco.
    
    :param id_op: ID de operación
    :type id_op: int
    """
    with sql.connect(mant.DATABASE) as conn:
        cursor = conn.cursor()
        instruccion = f"UPDATE operaciones SET moroso = '{1}', cobrador = '{5}' WHERE id = {id_op}"
        cursor.execute(instruccion)


def obtener_valor_doc(id_op: int) -> float | int:
    """Recupera de la vase de datos el valor de la cuota de documento
    de una operación específica y la retorna.
    
    :param id_op: ID de operación
    :type id_op: int

    :rtype: float or int
    """
    with sql.connect(mant.DATABASE) as conn:
        cursor = conn.cursor()
        instruccion = f"SELECT val_cuotas FROM documentos WHERE id_op = {id_op}"
        cursor.execute(instruccion)
        datos = cursor.fetchone()
        
    return datos[0]


def buscar_recibos_impagos(id_op: int) -> list:
    """Recupera de la base de datos todos los recibos impagos que posee una
    operación y los retorna en una lista ordenada por número de recibo.
    
    :param id_op: ID de operación
    :type id_op: int

    :rtype: list
    """
    with sql.connect(mant.DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM recibos WHERE operacion = {id_op} AND pago = 0 ORDER BY nro_recibo;")
        datos = cursor.fetchall()
    return datos
