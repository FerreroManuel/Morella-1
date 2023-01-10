import psycopg2 as sql
import psycopg2.errors
import smtplib 

from email import encoders 
from email.mime.base import MIMEBase 
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText 

import funciones_cuentas as ctas
import funciones_mantenimiento as mant
import funciones_rendiciones as rend


def obtener_mail(id: int) -> tuple:
    """Recibe un ID de cuenta de email, busca coincidencia en la
    base de datos y retorna una tupla con toda la información de
    la misma.

    :param id: ID de la cuenta de email
    :type id: int
    """
    with sql.connect(mant.DATABASE) as conn:
        cursor = conn.cursor()
        instruccion = f"SELECT * FROM mail WHERE id = '{id}'"
        cursor.execute(instruccion)
        datos = cursor.fetchone()
    return datos


def envio_de_recibo(num_socio: int, id_op: int, periodo: str, nro_nicho: str, pan: int, t04: str, nom_cob: str, num_rec: int):
    """Recibe los datos necesarios para generar un reporte de recibo y lo envía, como
    archivo adjunto a través de un email, al asociado.
    El email es enviado a través de la cuenta de email con ID número uno.

    :param num_socio: Número de socio (ID de asociado)
    :type num_socio: int
 
    :param id_op: ID de operación
    :type id_op: int
 
    :param periodo: Período al que corresponde el recibo
    :type periodo: str
 
    :param nro_nicho: Código de nicho
    :type nro_nicho: str
 
    :param pan: ID del panteón
    :type pan: int
 
    :param t04: Últimos cuatro dígitos de la tarjeta de crédito
    :type t04: str
 
    :param nom_cob: Nombre del cobrador
    :type nom_cob: str
 
    :param num_rec: Número de recibo
    :type num_rec: int
    """

    # Variables independientes
    nro, nom, dni, te_1, te_2, mail, dom, loc, c_p, f_n, f_a, act = rend.obtener_datos_socio(num_socio)
    id_o, soc, nic, fac, cob, tar, rut, ult, u_a, fup, mor, c_f, u_r, paga, op_cob, nom_alt, dom_alt = rend.obtener_datos_op(id_op)
    num_socio = str(num_socio).rjust(6, '0')
    num_rec = str(num_rec).rjust(7, '0')
    panteon = rend.obtener_panteon(pan)
    
    if nom_alt != None:
        nom = f"[{nom_alt}]"

    # Datos del remitente
    i_d, eti, addr_from, smtp_server, smtp_user, smtp_pass = obtener_mail(1)

    # Correo del receptor
    addr_to = f"{mail}"

    # Construimos el mail
    msg = MIMEMultipart() 
    msg['To'] = addr_to
    msg['From'] = addr_from
    msg['Subject'] = f"Recibo nro. {num_rec} correspondiente a {periodo} - Bicon S.A."

    # Cuerpo del mensaje
    # Si se redacta en HTML colocar 'html' en el 2do parámetro
    # Si se redacta en texto plano colocar 'plain' en el segundo parámetro
    msg.attach(MIMEText(f"Sr/a. <b>{nom}</b>, le acercamos su recibo de pago correspondiente a <u>{periodo}</u> por el mantenimiento del nicho <b>{str(nro_nicho).rjust(10, '0')}</b> ubicado en el panteón <b>{panteon}</b>. El mismo fue debitado de su tarjeta <i>XXXX XXXX XXXX {t04}</i>, según lo acordado.<br><br>Muchas Gracias por confiar en nosotros.<br><br>______________________________<br><br><b>Grupo Bicon S.A.</b><br>430 9999 / 430 8800<br>Córdoba 2915 - 2000<br>ROSARIO, Santa Fe<br><br><i>Este mensaje fue generado automáticamente, por favor no lo responda. Si usted cree que se trata de un error póngase en contacto con la administración para notificarlo. Muchas Gracias.</i>",'html'))

    # Cargamos el archivo a adjuntar
    fp = open(f"../reports/recibos/{nom_cob}/{num_socio}-{nom}/recibo-{num_rec}.pdf",'rb')
    adjunto = MIMEBase('multipart', 'encrypted')
    
    # Lo insertamos en una variable
    adjunto.set_payload(fp.read()) 
    fp.close()  
    
    # Lo encriptamos en base64 para enviarlo
    encoders.encode_base64(adjunto) 
    
    # Agregamos una cabecera y le damos un nombre al archivo que adjuntamos puede ser el mismo u otro
    adjunto.add_header('Content-Disposition', 'attachment', filename=f"recibo-{num_rec}.pdf")
    
    # Lo adjuntamos al mensaje
    msg.attach(adjunto) 

    # Inicializamos el SMTP para hacer el envío
    server = smtplib.SMTP(smtp_server, 587)
    server.starttls() 
    
    # Logeamos con los datos ya seteados en la parte superior
    server.login(smtp_user,smtp_pass)
    
    # Enviamos
    server.sendmail(addr_from, addr_to, msg.as_string())
    
    # Cerramos conexion SMTP
    server.quit()


def recordatorio_cobrador(num_socio: int, periodo: str, nro_nicho: str, pan: int, nom_cob: str):
    """Envía un email al asociado recordándole que su recibo fue generado y
    el cobrador pasará por su domicilio dentro del bimestre.

    :param num_socio: Número de socio (ID de asociado)
    :type num_socio: int
 
    :param periodo: Período al que corresponde el recibo
    :type periodo: str
 
    :param nro_nicho: Código de nicho
    :type nro_nicho: str
 
    :param pan: ID del panteón
    :type pan: int
 
    :param nom_cob: Nombre del cobrador
    :type nom_cob: str
    """

    # Variables independientes
    nro, nom, dni, te_1, te_2, mail, dom, loc, c_p, f_n, f_a, act = rend.obtener_datos_socio(num_socio)
    id_o, soc, nic, fac, cob, tar, rut, ult, u_a, fup, mor, c_f, u_r, paga, op_cob, nom_alt, dom_alt = ctas.obtener_datos_op_por_nro_socio(nro)
    num_socio = str(num_socio).rjust(6, '0')
    panteon = rend.obtener_panteon(pan)
    
    if nom_alt != None:
        nom = f"[{nom_alt}]"
    
    if dom_alt != None:
        dom = f"[{dom_alt}]"

    # Datos del remitente
    i_d, eti, addr_from, smtp_server, smtp_user, smtp_pass = obtener_mail(1)

    # Correo del receptor
    addr_to = f"{mail}"

    # Construimos el mail
    msg = MIMEMultipart() 
    msg['To'] = addr_to
    msg['From'] = addr_from
    msg['Subject'] = f"Recordatorio de cobro - Bicon S.A."

    # Cuerpo del mensaje
    # Si se redacta en HTML colocar 'html' en el 2do parámetro
    # Si se redacta en texto plano colocar 'plain' en el segundo parámetro
    msg.attach(MIMEText(f"Sr/a. <b>{nom}</b>, le recordamos que dentro del siguiente bimestre su cobradror/a <b>{nom_cob}</b> se estará acercando a su domicilio ubicado en <b>{dom}</b> para realizar el cobro correspondiente a <u>{periodo}</u> por el mantenimiento del nicho <b>{str(nro_nicho).rjust(10, '0')}</b> ubicado en el panteón <b>{panteon}</b>.<br><br>Muchas Gracias por confiar en nosotros.<br><br>______________________________<br><br><b>Grupo Bicon S.A.</b><br>430 9999 / 430 8800<br>Córdoba 2915 - 2000<br>ROSARIO, Santa Fe<br><br><i>Este mensaje fue generado automáticamente, por favor no lo responda. Si usted cree que se trata de un error póngase en contacto con la administración para notificarlo. Muchas Gracias.</i>",'html'))

    # Inicializamos el SMTP para hacer el envío
    server = smtplib.SMTP(smtp_server)
    server.starttls() 
    # Logeamos con los datos ya seteados en la parte superior
    server.login(smtp_user,smtp_pass)
    # Enviamos
    server.sendmail(addr_from, addr_to, msg.as_string())
    # Apagamos conexion SMTP
    server.quit()


def aviso_de_mora(id_operacion: int):
    """
    Envía un email al asociado para darle aviso que su operación cambió
    de estado a moroso debido a falta de pago.

    :param id_operacion: ID de operación
    :type id_operacion: int
    """

    # Variables independientes
    id_o, soc, nic, fac, cob, tar, rut, ult, u_a, fup, mor, c_f, u_r, paga, op_cob, nom_alt, dom_alt = rend.obtener_datos_op(id_operacion)
    nro, nom, dni, te_1, te_2, mail, dom, loc, c_p, f_n, f_a, act = rend.obtener_datos_socio(soc)
    
    if nom_alt:
        nom = f"[{nom_alt}]"
    
    if mail:
        # Datos del remitente
        i_d, eti, addr_from, smtp_server, smtp_user, smtp_pass = obtener_mail(1)

        # Correo del receptor
        addr_to = f"{mail}"

        # Construimos el mail
        msg = MIMEMultipart() 
        msg['To'] = addr_to
        msg['From'] = addr_from
        msg['Subject'] = f"Por favor regularice su situación - Bicon S.A."

        # Cuerpo del mensaje
        # Si se redacta en HTML colocar 'html' en el 2do parámetro
        # Si se redacta en texto plano colocar 'plain' en el segundo parámetro
        msg.attach(MIMEText(f"Sr/a. <b>{nom}</b>, le informamos que debido a la falta de pago durante dos años consecutivos de los servicios contratados en la operación con número {str(id_operacion).rjust(7, '0')}, su cuenta ha pasado a estado de moroso.<br>Le rogamos que se acerque a nuestras oficinas ubicadas en calle Córdoba 2915 (Rosario) a fin de regularizar dicha situación y así poder continuar brindándole nuestro mejor servicio.<br><br>Se adjunta una copia de su estado de cuenta actual.<br><br>Muchas Gracias por confiar en nosotros.<br><br>______________________________<br><br><b>Grupo Bicon S.A.</b><br>430 9999 / 430 8800<br>Córdoba 2915 - 2000<br>ROSARIO, Santa Fe<br><br><i>Este mensaje fue generado automáticamente, por favor no lo responda. Si usted cree que se trata de un error póngase en contacto con la administración para notificarlo. Muchas Gracias.</i>",'html'))

        # Cargamos el archivo a adjuntar
        try:
            fp = open(f'../reports/temp/estado_cta_mail.pdf','rb')
        
        except PermissionError:
            mant.log_error()
            pass
        except FileNotFoundError:
            mant.log_error()
            pass
        except:
            mant.log_error()
            print("")
            print("         ERROR. Comuníquese con el administrador...")
            print()
            pass
        
        adjunto = MIMEBase('multipart', 'encrypted')
        
        # Lo insertamos en una variable
        adjunto.set_payload(fp.read()) 
        fp.close()  
        
        # Lo encriptamos en base64 para enviarlo
        encoders.encode_base64(adjunto) 
        
        # Agregamos una cabecera y le damos un nombre al archivo que adjuntamos puede ser el mismo u otro
        adjunto.add_header('Content-Disposition', 'attachment', filename=f"Estado de cuenta - {str(soc).rjust(6, '0')}-{nom}.pdf")
        
        # Lo adjuntamos al mensaje
        msg.attach(adjunto) 

        # Inicializamos el SMTP para hacer el envío
        server = smtplib.SMTP(smtp_server)
        server.starttls() 
        
        # Logeamos con los datos ya seteados en la parte superior
        server.login(smtp_user,smtp_pass)
        
        # Enviamos
        server.sendmail(addr_from, addr_to, msg.as_string())
        
        # Apagamos conexion SMTP
        server.quit()