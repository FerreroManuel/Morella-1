import psycopg2 as sql
import psycopg2.errors
import funciones_rendiciones as rend
import funciones_cuentas as ctas
import funciones_mantenimiento as mant
import smtplib 
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase 
from email import encoders 

def obtener_database():
    arch = open("../databases/database.ini", "r")
    db = arch.readline()
    arch.close()
    return db
database = obtener_database()

def obtener_mail(id):
    conn = sql.connect(database)
    cursor = conn.cursor()
    instruccion = f"SELECT * FROM mail WHERE id = '{id}'"
    cursor.execute(instruccion)
    datos = cursor.fetchone()
    conn.commit()
    conn.close()
    return datos


def envio_de_recibo(num_socio, id_op, periodo, nro_nicho, pan, t04, nom_cob, num_rec):

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
    # Apagamos conexion SMTP
    server.quit()


def recordatorio_cobrador(num_socio, periodo, nro_nicho, pan, nom_cob):

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


def aviso_de_mora(id_operacion):

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