############ INICIO DE IMPORTACIONES ############

import funciones_caja as caja
import funciones_rendiciones as rend
import funciones_cuentas as ctas
import funciones_mantenimiento as mant
import funciones_ventas as vent
import correo as email
from fpdf import FPDF
from datetime import datetime, date
import os
import psycopg2 as sql
import psycopg2.errors
from openpyxl import Workbook
from smtplib import SMTPAuthenticationError
from socket import gaierror
from pprint import pprint

############ FIN DE IMPORTACIONES ############


######## INICIO DE FUNCIONES  GRALES #########


########## FIN DE FUNCIONES GRALES ###########


######### INICIO DE VARIABLES GRALES #########


########### FIN DE VARIABLES GRALES ##########




    #################################################################################################################
    ############################################# REPORT CAJA DIARIA ################################################
    #################################################################################################################

def report_caja_diaria(s_final):
    ############ INICIO DE VARIABLES INDEPENDIENTES ############

    fecha = caja.obtener_fecha()
    hora = datetime.now().strftime('%H:%M')
    total_ing = 0
    total_egr = 0
    saldo_inicial = float(caja.obtener_saldo_inicial())
    saldo_final = s_final
    categ_ing = caja.obtener_categ_ing()
    categ_egr = caja.obtener_categ_egr()
    errores = {}

    ############ FIN DE VARIABLES INDEPENDIENTES ############
    
    
    ############ INICIO DE FUNCIONES ############

    def buscar_imp_reg(categ):
        categ = categ
        conn = caja.sql.connect(caja.database)
        cursor = conn.cursor()
        instruccion = f"SELECT * FROM caja WHERE categoria='{categ}' AND cerrada = '0'"
        cursor.execute(instruccion)
        datos = cursor.fetchall()
        conn.close()
        return datos


    def tot_cat_ing(categ):
        categ = categ
        i = 0
        total = 0
        for i in buscar_imp_reg(categ):
            i_d, cat, des, tra, ing, egr, obs, dia, mes, año, cer, use = i
            total = total + ing
        return total


    def tot_cat_egr(categ):
        categ = categ
        i = 0
        total = 0
        for i in buscar_imp_reg(categ):
            i_d, cat, des, tra, ing, egr, obs, dia, mes, año, cer, use = i
            total = total + egr
        return total


    def select_categ(categ):
        lista_categ = []
        for i in categ:
            cat = buscar_imp_reg(i)
            if cat != []:
                lista_categ.append(i)
        return lista_categ


    def imprimir_registros_ing(categ):
        categ = categ
        pdf.set_font('Arial', 'B', 10)
        pdf.cell(0, 5, f'{categ}', 0, 1, 'L')
        pdf.set_font('Arial', '', 10)
        for i in buscar_imp_reg(categ):
            i_d, cat, des, tra, ing, egr, obs, dia, mes, año, cer, use = i
            pdf.set_font('Arial', '', 10)
            pdf.cell(5, 5, '', 0, 0, 'L')
            pdf.cell(50, 5, f'{des}', 0, 0, 'L')
            pdf.cell(1, 5, '', 0, 0, 'L')
            pdf.cell(15, 5, f'{tra}', 0, 0, 'L')
            pdf.cell(5, 5, '', 0, 0, 'L')
            pdf.cell(10, 5, f'{ing}', 0, 0, 'R')
            pdf.cell(25, 5, f'', 0, 0, 'L')
            pdf.cell(1, 5, '', 0, 0, 'L')
            pdf.cell(0, 5, f'{obs}', 0, 1, 'L')
        pdf.ln(2)
        pdf.set_font('Arial', 'B', 10)
        pdf.cell(0, 5, f'$ {tot_cat_ing(categ):.2f}', 0, 0, 'R')
        pdf.cell(-27, 5, f'Total {categ}: ', 0, 1, 'R')
        pdf.ln(2)
        

    def imprimir_registros_egr(categ):
        categ = categ
        pdf.set_font('Arial', 'B', 10)
        pdf.cell(0, 5, f'{categ}', 0, 1, 'L')
        pdf.set_font('Arial', '', 10)
        for i in buscar_imp_reg(categ):
            i_d, cat, des, tra, ing, egr, obs, dia, mes, año, cer, use = i
            pdf.set_font('Arial', '', 10)
            pdf.cell(5, 5, '', 0, 0, 'L')
            pdf.cell(50, 5, f'{des}', 0, 0, 'L')
            pdf.cell(1, 5, '', 0, 0, 'L')
            pdf.cell(15, 5, f'{tra}', 0, 0, 'L')
            pdf.cell(5, 5, '', 0, 0, 'L')
            pdf.cell(15, 5, f'', 0, 0, 'L')
            pdf.cell(20, 5, f'({egr})', 0, 0, 'R')
            pdf.cell(1, 5, '', 0, 0, 'L')
            pdf.cell(0, 5, f'{obs}', 0, 1, 'L')
        pdf.ln(2)
        pdf.set_font('Arial', 'B', 10)
        pdf.cell(0, 5, f'($ {tot_cat_egr(categ):.2f})', 0, 0, 'R')
        pdf.cell(-27, 5, f'Total {categ}: ', 0, 1, 'R')
        pdf.ln(2)


    def total_ingresos(saldo_inicial):
        total = 0
        for i in categ_ing:
            total = total + tot_cat_ing(i)
        total = total + saldo_inicial
        return total


    def total_egresos(saldo_final):
        total = 0
        for i in categ_egr:
            total = total + tot_cat_egr(i)
        total = total + saldo_final
        return total

    ############ FIN DE FUNCIONES ############

    ############ INICIO DE VARIABLES DEPENDIENTES ############

    total_ing = total_ingresos(saldo_inicial)
    total_egr = total_egresos(saldo_final)
    final = total_ing - total_egr
    contador = caja.obtener_contador()

    ########### FIN DE VARIABLES DEPENDIENTES ############
    
    ############ INICIO DE REPORT ############

    class PDF(FPDF):
        # Page header
        def header(self):
            # Logo
            self.image('../docs/logo_bicon.jpg', 14.5, 12, 15)
            # Arial bold 15
            self.set_font('Arial', 'B', 15)
            # Title
            self.cell(0, 20, 'CAJA DIARIA', 1, 0, 'C')
            # Arial 10
            self.set_font('Arial', '', 10)
            # Fecha
            self.cell(0, 35, f'{fecha} - {hora} hs', 0, 0, 'R')
            # N° de cierre
            self.cell(-74, 35, f'Número de cierre: {str(contador).rjust(6, "0")}', 0, 0, 'R')
            # Line break
            self.ln(22)
            self.set_font('Arial', 'B', 10)
            self.cell(45, 5, 'Descripción', 0, 0, 'L ')
            pdf.cell(1, 5, '', 0, 0, 'L')
            self.cell(20, 5, 'N°Transacción', 0, 0, 'L')
            pdf.cell(10, 5, '', 0, 0, 'L')
            self.cell(15, 5, 'Ingreso', 0, 0, 'L')
            pdf.cell(20, 5, 'Egreso', 0, 0, 'L')
            pdf.cell(1, 5, '', 0, 0, 'L')
            pdf.cell(0, 5, 'Observaciones', 0, 1, 'L')
            self.cell(0, 1, '_________________________________________________________________________________________________', 0, 1, 'C')
            self.ln(5)
            
        # Page footer
        def footer(self):
            # Position at 2.5 cm from bottom
            self.set_y(-25)
            # Arial italic 8
            self.set_font('Arial', 'I', 8)
            self.cell(0, 1, '_______________________________________________________________________________________________', 0, 1, 'C')
            # Page number
            self.cell(0, 10, 'Página ' + str(self.page_no()) + ' de {nb}', 0, 0, 'C')
            # Firma
            self.set_font('Arial', 'I', 8)
            self.cell(-10, 10, f'Reporte generado en *MORELLA v{mant.SHORT_VERSION}* by ', 0, 0, 'R')
            self.image('../docs/mf_logo.jpg', 190, 274, 8)

    # Instantiation of inherited class
    pdf = PDF()
    pdf.set_auto_page_break(True, 25)
    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 10)
    pdf.cell(0, 5, 'CAJA INICIAL: ', 0, 0, "L")
    pdf.cell(0, 5, f'$ {saldo_inicial:.2f}', 0, 1, 'R')
    pdf.set_font('Arial', '', 10)
    for i in select_categ(categ_ing):
        imprimir_registros_ing(i)
    for e in select_categ(categ_egr):
        imprimir_registros_egr(e)
    pdf.set_font('Arial', 'B', 10)
    pdf.cell(0, 5, 'CIERRE DE CAJA: ', 0, 0, "L")
    pdf.cell(0, 5, f'($ {saldo_final:.2f})', 0, 1, 'R')
    pdf.ln(15)
    pdf.cell(0, 5, f' {total_ing:.2f} ', 0, 0, 'R')
    pdf.cell(-27, 5, f'TOTAL INGRESOS: $ ', 0, 1, 'R')
    pdf.cell(0, 5, f'( {total_egr:.2f})', 0, 0, 'R')
    pdf.cell(-27, 5, f'TOTAL EGRESOS: $ ', 0, 1, 'R')
    pdf.cell(0, 5, f'_____________________________', 0, 1, 'R')
    if final == 0:
        pdf.cell(0, 5, f' {final:.2f} ', 0, 0, 'R')
        pdf.cell(-27, 5, f'DIFERENCIA: $ ', 0, 1, 'R')
    elif final > 0:
        pdf.cell(0, 5, f' {final:.2f} ', 0, 0, 'R')
        pdf.cell(-27, 5, f'FALTANTE: $ ', 0, 1, 'R')
    elif final < 0:
        pdf.cell(0, 5, f' {-1*final:.2f}', 0, 0, 'R')
        pdf.cell(-27, 5, f'SOBRANTE: $ ', 0, 1, 'R')
    pdf.ln(2)
    pdf.output(f'../reports/caja/diaria/caja_diaria-{str(contador).rjust(6, "0")}.pdf', 'F')


    ############ ABRIR REPORT ############

    if errores:
        print('\n\n\n\n')
        print('     ATENCIÓN! Durante la emisión del reporte se produjeron los siguientes errores:')
        print()
        pprint(errores)
        print('\n\n\n\n')

    print("Abriendo reporte. Luego de cerrarlo presione enter para continuar...")
    ruta = f'../reports/caja/diaria'
    arch = f'caja_diaria-{str(contador).rjust(6, "0")}.pdf'
    os.chdir(ruta)
    os.system(arch)
    ruta = '../../../modulos/'
    os.chdir(ruta)

            ######################################## FIN DE REPORT ############################################






    #################################################################################################################
    ######################################## REPORT CAJA MENSUAL DETALLADA ##########################################
    #################################################################################################################

def report_caja_mensual_det(mes, año):
    ############ INICIO DE VARIABLES INDEPENDIENTES ############

    fecha = caja.obtener_fecha()
    hora = datetime.now().strftime('%H:%M')
    mes = f'{mes}'.rjust(2, '0')
    año = f'{año}'.rjust(3, '0').rjust(4, '2')
    total_ing = 0
    total_egr = 0
    categ_ing = caja.obtener_categ_ing()
    categ_egr = caja.obtener_categ_egr()
    errores = {}

    ############ FIN DE VARIABLES INDEPENDIENTES ############
    
    
    ############ INICIO DE FUNCIONES ############

    def buscar_imp_reg(categ):
        categ = categ
        conn = caja.sql.connect(caja.database)
        cursor = conn.cursor()
        instruccion = f"SELECT * FROM caja WHERE categoria='{categ}' AND mes='{mes}' AND año='{año}'"
        cursor.execute(instruccion)
        datos = cursor.fetchall()
        conn.close()
        return datos


    def tot_cat_ing(categ):
        categ = categ
        i = 0
        total = 0
        for i in buscar_imp_reg(categ):
            i_d, cat, des, tra, ing, egr, obs, dia, mes, año, cer, use = i
            total = total + ing
        return total


    def tot_cat_egr(categ):
        categ = categ
        i = 0
        total = 0
        for i in buscar_imp_reg(categ):
            i_d, cat, des, tra, ing, egr, obs, dia, mes, año, cer, use = i
            total = total + egr
        return total


    def select_categ(categ):
        lista_categ = []
        for i in categ:
            cat = buscar_imp_reg(i)
            if cat != []:
                lista_categ.append(i)
        return lista_categ


    def imprimir_registros_ing_mes(categ):
        categ = categ
        pdf.set_font('Arial', 'B', 10)
        pdf.cell(0, 5, f'{categ}', 0, 1, 'L')
        pdf.set_font('Arial', '', 10)
        for i in buscar_imp_reg(categ):
            i_d, cat, des, tra, ing, egr, obs, dia, mes, año, cer, use = i
            pdf.set_font('Arial', '', 10)
            pdf.cell(5, 5, '', 0, 0, 'L')
            pdf.cell(50, 5, f'{des}', 0, 0, 'L')
            pdf.cell(1, 5, '', 0, 0, 'L')
            pdf.cell(15, 5, f'{tra}', 0, 0, 'L')
            pdf.cell(5, 5, '', 0, 0, 'L')
            pdf.cell(10, 5, f'{ing}', 0, 0, 'R')
            pdf.cell(25, 5, f'', 0, 0, 'L')
            pdf.cell(1, 5, '', 0, 0, 'L')
            pdf.cell(60, 5, f'{obs}', 0, 0, 'L')
            pdf.cell(0, 5 , f'{mes}/{año}', 0, 1, 'L')
        pdf.ln(2)
        pdf.set_font('Arial', 'B', 10)
        pdf.cell(0, 5, f'$ {tot_cat_ing(categ):.2f}', 0, 0, 'R')
        pdf.cell(-27, 5, f'Total {categ}: ', 0, 1, 'R')
        pdf.ln(2)
        

    def imprimir_registros_egr_mes(categ):
        categ = categ
        pdf.set_font('Arial', 'B', 10)
        pdf.cell(0, 5, f'{categ}', 0, 1, 'L')
        pdf.set_font('Arial', '', 10)
        for i in buscar_imp_reg(categ):
            i_d, cat, des, tra, ing, egr, obs, dia, mes, año, cer, use = i
            pdf.set_font('Arial', '', 10)
            pdf.cell(5, 5, '', 0, 0, 'L')
            pdf.cell(50, 5, f'{des}', 0, 0, 'L')
            pdf.cell(1, 5, '', 0, 0, 'L')
            pdf.cell(15, 5, f'{tra}', 0, 0, 'L')
            pdf.cell(5, 5, '', 0, 0, 'L')
            pdf.cell(15, 5, f'', 0, 0, 'L')
            pdf.cell(20, 5, f'({egr})', 0, 0, 'R')
            pdf.cell(1, 5, '', 0, 0, 'L')
            pdf.cell(60, 5, f'{obs}', 0, 0, 'L')
            pdf.cell(0, 5 , f'{mes}/{año}', 0, 1, 'L')
        pdf.ln(2)
        pdf.set_font('Arial', 'B', 10)
        pdf.cell(0, 5, f'($ {tot_cat_egr(categ):.2f})', 0, 0, 'R')
        pdf.cell(-27, 5, f'Total {categ}: ', 0, 1, 'R')
        pdf.ln(2)


    def total_ingresos_mensual():
        total = 0
        for i in categ_ing:
            total = total + tot_cat_ing(i)
        return total


    def total_egresos_mensual():
        total = 0
        for i in categ_egr:
            total = total + tot_cat_egr(i)
        return total


    def str_mes(mes):
        if mes == '01':
            string_mes = 'Enero'
        if mes == '02':
            string_mes = 'Febrero'
        elif mes == '03':
            string_mes = 'Marzo'
        elif mes == '04':
            string_mes = 'Abril'
        elif mes == '05':
            string_mes = 'Mayo'
        elif mes == '06':
            string_mes = 'Junio'
        elif mes == '07':
            string_mes = 'Julio'
        elif mes == '08':
            string_mes = 'Agosto'
        elif mes == '09':
            string_mes = 'Septiembre'
        elif mes == '10':
            string_mes = 'Octubre'
        elif mes == '11':
            string_mes = 'Noviembre'
        elif mes == '12':
            string_mes = 'Diciembre'
        return string_mes

    ############ FIN DE FUNCIONES ############

    ############ INICIO DE VARIABLES DEPENDIENTES ############

    string_mes = str_mes(mes)
    total_ing = total_ingresos_mensual()
    total_egr = total_egresos_mensual()
    # final = total_ing - total_egr

    ########### FIN DE VARIABLES DEPENDIENTES ############

    ############ INICIO DE REPORT ############

    class PDF(FPDF):
        # Page header
        def header(self):
            # Logo
            self.image('../docs/logo_bicon.jpg', 14.5, 12, 15)
            # Arial bold 15
            self.set_font('Arial', 'B', 15)
            # Title
            self.cell(0, 20, 'CAJA MENSUAL DETALLADA', 1, 0, 'C')
            # Arial 10
            self.set_font('Arial', '', 10)
            # Fecha
            self.cell(0, 35, f'{fecha} - {hora} hs', 0, 0, 'R')
            self.set_font('Arial', 'B', 10)
            # Mes de cierre
            self.cell(-81, 35, f'{string_mes} de {año}', 0, 0, 'R')
            # Line break
            self.ln(22)
            self.cell(45, 5, 'Descripción', 0, 0, 'L ')
            pdf.cell(1, 5, '', 0, 0, 'L')
            self.cell(20, 5, 'N°Transacción', 0, 0, 'L')
            pdf.cell(10, 5, '', 0, 0, 'L')
            self.cell(15, 5, 'Ingreso', 0, 0, 'L')
            pdf.cell(20, 5, 'Egreso', 0, 0, 'L')
            pdf.cell(1, 5, '', 0, 0, 'L')
            pdf.cell(60, 5, 'Observaciones', 0, 0, 'L')
            pdf.cell(0, 5, 'Fecha', 0, 1, 'L')
            self.cell(0, 1, '_________________________________________________________________________________________________', 0, 1, 'C')
            self.ln(5)
            
        # Page footer
        def footer(self):
            # Position at 2.5 cm from bottom
            self.set_y(-25)
            # Arial italic 8
            self.set_font('Arial', 'I', 8)
            self.cell(0, 1, '_______________________________________________________________________________________________', 0, 1, 'C')
            # Page number
            self.cell(0, 10, 'Página ' + str(self.page_no()) + ' de {nb}', 0, 0, 'C')
            # Firma
            self.set_font('Arial', 'I', 8)
            self.cell(-10, 10, f'Reporte generado en *MORELLA v{mant.SHORT_VERSION}* by ', 0, 0, 'R')
            self.image('../docs/mf_logo.jpg', 190, 274, 8)

    # Instantiation of inherited class
    pdf = PDF()
    pdf.set_auto_page_break(True, 25)
    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.set_font('Arial', '', 10)
    for i in select_categ(categ_ing):
        imprimir_registros_ing_mes(i)
    for e in select_categ(categ_egr):
        imprimir_registros_egr_mes(e)
    pdf.ln(15)
    pdf.cell(0, 5, f' {total_ing:.2f} ', 0, 0, 'R')
    pdf.cell(-27, 5, f'TOTAL INGRESOS: $ ', 0, 1, 'R')
    pdf.cell(0, 5, f'( {total_egr:.2f})', 0, 0, 'R')
    pdf.cell(-27, 5, f'TOTAL EGRESOS: $ ', 0, 1, 'R')
    pdf.ln(2)
    pdf.output(f'../reports/caja/mensual/detallada/caja_{str.lower(string_mes)}-{año}.pdf', 'F')


    ############ ABRIR REPORT ############

    if errores:
        print('\n\n\n\n')
        print('     ATENCIÓN! Durante la emisión del reporte se produjeron los siguientes errores:')
        print()
        pprint(errores)
        print('\n\n\n\n')

    print("Abriendo reporte. Cierre el archivo para continuar...")
    ruta = f'../reports/caja/mensual/detallada/'
    arch = f'caja_{str.lower(string_mes)}-{año}.pdf'
    os.chdir(ruta)
    os.system(arch)
    ruta = '../../../../modulos/'
    os.chdir(ruta)

            ######################################## FIN DE REPORT ############################################





    #################################################################################################################
    ######################################### REPORT CAJA MENSUAL COMPRIMIDA ########################################
    #################################################################################################################

def report_caja_mensual_comp(mes, año):
    ############ INICIO DE VARIABLES INDEPENDIENTES ############

    fecha = caja.obtener_fecha()
    hora = datetime.now().strftime('%H:%M')
    mes = f'{mes}'.rjust(2, '0')
    año = f'{año}'.rjust(3, '0').rjust(4, '2')
    total_ing = 0
    total_egr = 0
    categ_ing = caja.obtener_categ_ing()
    categ_egr = caja.obtener_categ_egr()
    errores = {}

    ############ FIN DE VARIABLES INDEPENDIENTES ############
    
    
    ############ INICIO DE FUNCIONES ############

    def buscar_imp_reg(categ):
        categ = categ
        conn = caja.sql.connect(caja.database)
        cursor = conn.cursor()
        instruccion = f"SELECT * FROM caja WHERE categoria='{categ}' AND mes='{mes}' AND año='{año}'"
        cursor.execute(instruccion)
        datos = cursor.fetchall()
        conn.close()
        return datos


    def tot_cat_ing(categ):
        categ = categ
        i = 0
        total = 0
        for i in buscar_imp_reg(categ):
            i_d, cat, des, tra, ing, egr, obs, dia, mes, año, cer, use = i
            total = total + ing
        return total


    def tot_cat_egr(categ):
        categ = categ
        i = 0
        total = 0
        for i in buscar_imp_reg(categ):
            i_d, cat, des, tra, ing, egr, obs, dia, mes, año, cer, use = i
            total = total + egr
        return total


    def select_categ(categ):
        lista_categ = []
        for i in categ:
            cat = buscar_imp_reg(i)
            if cat != []:
                lista_categ.append(i)
        return lista_categ


    def imprimir_registros_ing_mes(categ):
        categ = categ
        pdf.set_font('Arial', '', 10)
        pdf.cell(0, 5, f'{categ}', 0, 0, 'L')
        pdf.cell(-58, 5, f'$ {tot_cat_ing(categ):.2f}', 0, 1, 'R')
        pdf.ln(2)
        

    def imprimir_registros_egr_mes(categ):
        categ = categ
        pdf.set_font('Arial', '', 10)
        pdf.cell(0, 5, f'{categ}', 0, 0, 'L')
        pdf.cell(0, 5, f'($ {tot_cat_egr(categ):.2f})', 0, 1, 'R')
        pdf.ln(2)


    def total_ingresos_mensual():
        total = 0
        for i in categ_ing:
            total = total + tot_cat_ing(i)
        return total


    def total_egresos_mensual():
        total = 0
        for i in categ_egr:
            total = total + tot_cat_egr(i)
        return total


    def str_mes(mes):
        if mes == '01':
            string_mes = 'Enero'
        if mes == '02':
            string_mes = 'Febrero'
        elif mes == '03':
            string_mes = 'Marzo'
        elif mes == '04':
            string_mes = 'Abril'
        elif mes == '05':
            string_mes = 'Mayo'
        elif mes == '06':
            string_mes = 'Junio'
        elif mes == '07':
            string_mes = 'Julio'
        elif mes == '08':
            string_mes = 'Agosto'
        elif mes == '09':
            string_mes = 'Septiembre'
        elif mes == '10':
            string_mes = 'Octubre'
        elif mes == '11':
            string_mes = 'Noviembre'
        elif mes == '12':
            string_mes = 'Diciembre'
        return string_mes

    ############ FIN DE FUNCIONES ############


    ############ INICIO DE VARIABLES DEPENDIENTES ############

    string_mes = str_mes(mes)
    total_ing = total_ingresos_mensual()
    total_egr = total_egresos_mensual()
    # final = total_ing - total_egr

    ########### FIN DE VARIABLES DEPENDIENTES ############
    

    ############ INICIO DE REPORT ############

    class PDF(FPDF):
        # Page header
        def header(self):
            # Logo
            self.image('../docs/logo_bicon.jpg', 14.5, 12, 15)
            # Arial bold 15
            self.set_font('Arial', 'B', 15)
            # Title
            self.cell(0, 20, 'CAJA MENSUAL COMPRIMIDA', 1, 0, 'C')
            # Arial 10
            self.set_font('Arial', '', 10)
            # Fecha
            self.cell(0, 35, f'{fecha} - {hora} hs', 0, 0, 'R')
            self.set_font('Arial', 'B', 10)
            # Mes de cierre
            self.cell(-81, 35, f'{string_mes} de {año}', 0, 0, 'R')
            # Line break
            self.ln(22)
            self.cell(45, 5, 'Categoría', 0, 0, 'L ')
            pdf.cell(1, 5, '', 0, 0, 'L')
            self.cell(20, 5, '', 0, 0, 'L')
            pdf.cell(10, 5, '', 0, 0, 'L')
            self.cell(15, 5, '', 0, 0, 'L')
            pdf.cell(20, 5, '', 0, 0, 'L')
            pdf.cell(7, 5, '', 0, 0, 'L')
            pdf.cell(55, 5, 'Ingreso', 0 , 0, 'L')
            pdf.cell(0, 5, 'Egreso', 0, 1, 'L')
            self.cell(0, 1, '_________________________________________________________________________________________________', 0, 1, 'C')
            self.ln(5)
            
        # Page footer
        def footer(self):
            # Position at 2.5 cm from bottom
            self.set_y(-25)
            # Arial italic 8
            self.set_font('Arial', 'I', 8)
            self.cell(0, 1, '_______________________________________________________________________________________________', 0, 1, 'C')
            # Page number
            self.cell(0, 10, 'Página ' + str(self.page_no()) + ' de {nb}', 0, 0, 'C')
            # Firma
            #self.set_font('Arial', 'BI', 8)
            #self.cell(0, 10, 'Solutions.', 0, 0, 'R')
            #self.set_font('Arial', 'BIU', 8)
            #self.cell(-15, 10, 'MF!', 0, 0, 'R')
            self.set_font('Arial', 'I', 8)
            self.cell(-10, 10, f'Reporte generado en *MORELLA v{mant.SHORT_VERSION}* by ', 0, 0, 'R')
            self.image('../docs/mf_logo.jpg', 190, 274, 8)

    # Instantiation of inherited class
    pdf = PDF()
    pdf.set_auto_page_break(True, 25)
    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.set_font('Arial', '', 10)
    for i in select_categ(categ_ing):
        imprimir_registros_ing_mes(i)
    for e in select_categ(categ_egr):
        imprimir_registros_egr_mes(e)
    pdf.ln(15)
    pdf.set_font('Arial', 'B', 10)
    pdf.cell(0, 5, f' {total_ing:.2f} ', 0, 0, 'R')
    pdf.cell(-27, 5, f'TOTAL INGRESOS: $ ', 0, 1, 'R')
    pdf.cell(0, 5, f'( {total_egr:.2f})', 0, 0, 'R')
    pdf.cell(-27, 5, f'TOTAL EGRESOS: $ ', 0, 1, 'R')
    pdf.ln(2)
    pdf.output(f'../reports/caja/mensual/comprimida/caja_{str.lower(string_mes)}-{año}-COMP.pdf', 'F')


    ############ ABRIR REPORT ############

    if errores:
        print('\n\n\n\n')
        print('     ATENCIÓN! Durante la emisión del reporte se produjeron los siguientes errores:')
        print()
        pprint(errores)
        print('\n\n\n\n')

    print("Abriendo reporte. Cierre el archivo para continuar...")
    ruta = f'../reports/caja/mensual/comprimida/'
    arch = f'caja_{str.lower(string_mes)}-{año}-COMP.pdf'
    os.chdir(ruta)
    os.system(arch)
    ruta = '../../../../modulos/'
    os.chdir(ruta)

            ######################################## FIN DE REPORT ############################################





    #################################################################################################################
    ####################################### REPORT CAJA MENSUAL POR COBRADOR ########################################
    #################################################################################################################


def report_caja_mensual_por_cob(mes, año):
    ############ INICIO DE VARIABLES INDEPENDIENTES ############

    fecha = caja.obtener_fecha()
    hora = datetime.now().strftime('%H:%M')
    mes = f'{mes}'.rjust(2, '0')
    año = f'{año}'.rjust(3, '0').rjust(4, '2')
    cobradores = caja.obtener_cobrador()
    counter = 0
    errores = {}

    ############ FIN DE VARIABLES INDEPENDIENTES ############
    
    
    ############ INICIO DE FUNCIONES ############

    def buscar_imp_reg_por_cob(cobrador, mes, año):
        conn = caja.sql.connect(caja.database)
        cursor = conn.cursor()
        instruccion = f"SELECT * FROM caja WHERE descripcion='{cobrador}' AND mes='{mes}' AND año='{año}'"
        cursor.execute(instruccion)
        datos = cursor.fetchall()
        conn.close()
        return datos


    def select_cob(cob, mes, año):
        lista_cob = []
        for i in cob:
            cob = buscar_imp_reg_por_cob(i, mes, año)
            if cob != []:
                lista_cob.append(i)
        return lista_cob


    def imprimir_registros_por_cob(cobrador, mes, año):
        tot_i_por_cob = caja.total_ing_por_cob(cobrador, mes, año)
        tot_e_por_cob = caja.total_egr_por_cob(cobrador, mes, año)
        total_por_cob = tot_i_por_cob - tot_e_por_cob
        pdf.set_font('Arial', 'B', 10)
        pdf.cell(0, 5, f'{cobrador}', 0, 1, 'L')
        pdf.set_font('Arial', '', 10)
        for i in buscar_imp_reg_por_cob(cobrador, mes, año):
            i_d, cat, des, tra, ing, egr, obs, dia, mes, año, cer, use = i
            if egr != '':
                continue
            pdf.set_font('Arial', '', 10)
            pdf.cell(5, 5, '', 0, 0, 'L')
            pdf.cell(60, 5, f'{cat}', 0, 0, 'L')
            pdf.cell(1, 5, '', 0, 0, 'L')
            pdf.cell(10, 5, f'{tra}', 0, 0, 'L')
            pdf.cell(15, 5, '', 0, 0, 'L')
            pdf.cell(10, 5, f'{ing}', 0, 0, 'R')
            pdf.cell(1, 5, '', 0, 0, 'L')
            pdf.cell(73, 5, f'{obs}', 0, 0, 'L')
            pdf.cell(0, 5 , f'{mes}/{año}', 0, 1, 'L')
        pdf.ln(2)
        pdf.set_font('Arial', 'B', 10)
        pdf.cell(0, 5, f'$ {tot_i_por_cob:.2f}', 0, 0, 'R')
        pdf.cell(-27, 5, f'Total {cobrador}: ', 0, 1, 'R')
        pdf.ln(2)


    def total_mensual_cobradores():
        total_cobradores=0
        for i in cobradores:
            ing_por_cob = caja.total_ing_por_cob(i, mes, año)
            egr_por_cob = caja.total_egr_por_cob(i, mes, año)
            total_por_cob = ing_por_cob - egr_por_cob
            total_cobradores = total_cobradores + ing_por_cob
        return total_cobradores


    def str_mes(mes):
        if mes == '01':
            string_mes = 'Enero'
        if mes == '02':
            string_mes = 'Febrero'
        elif mes == '03':
            string_mes = 'Marzo'
        elif mes == '04':
            string_mes = 'Abril'
        elif mes == '05':
            string_mes = 'Mayo'
        elif mes == '06':
            string_mes = 'Junio'
        elif mes == '07':
            string_mes = 'Julio'
        elif mes == '08':
            string_mes = 'Agosto'
        elif mes == '09':
            string_mes = 'Septiembre'
        elif mes == '10':
            string_mes = 'Octubre'
        elif mes == '11':
            string_mes = 'Noviembre'
        elif mes == '12':
            string_mes = 'Diciembre'
        return string_mes

    ############ FIN DE FUNCIONES ############

    ############ INICIO DE VARIABLES DEPENDIENTES ############

    string_mes = str_mes(mes)
    total_mes_cob = total_mensual_cobradores()

    ########### FIN DE VARIABLES DEPENDIENTES ############
    
    ############ INICIO DE REPORT ############

    class PDF(FPDF):
        # Page header
        def header(self):
            # Logo
            self.image('../docs/logo_bicon.jpg', 14.5, 12, 15)
            # Arial bold 15
            self.set_font('Arial', 'B', 15)
            # Title
            self.cell(0, 20, 'CAJA MENSUAL POR COBRADOR', 1, 0, 'C')
            # Arial 10
            self.set_font('Arial', '', 10)
            # Fecha
            self.cell(0, 35, f'{fecha} - {hora} hs', 0, 0, 'R')
            self.set_font('Arial', 'B', 10)
            # Mes de cierre
            self.cell(-81, 35, f'{string_mes} de {año}', 0, 0, 'R')
            # Line break
            self.ln(22)
            self.cell(53, 5, 'Panteón', 0, 0, 'L ')
            pdf.cell(1, 5, '', 0, 0, 'L')
            self.cell(20, 5, 'N°Transacción', 0, 0, 'L')
            pdf.cell(12, 5, '', 0, 0, 'L')
            pdf.cell(15, 5, 'Ingreso', 0, 0, 'L')
            pdf.cell(1, 5, '', 0, 0, 'L')
            pdf.cell(75, 5, 'Observaciones', 0, 0, 'L')
            pdf.cell(0, 5, 'Fecha', 0, 1, 'L')
            self.cell(0, 1, '_________________________________________________________________________________________________', 0, 1, 'C')
            self.ln(5)
            
        # Page footer
        def footer(self):
            # Position at 2.5 cm from bottom
            self.set_y(-25)
            # Arial italic 8
            self.set_font('Arial', 'I', 8)
            self.cell(0, 1, '_______________________________________________________________________________________________', 0, 1, 'C')
            # Page number
            self.cell(0, 10, 'Página ' + str(self.page_no()) + ' de {nb}', 0, 0, 'C')
            # Firma
            self.set_font('Arial', 'I', 8)
            self.cell(-10, 10, f'Reporte generado en *MORELLA v{mant.SHORT_VERSION}* by ', 0, 0, 'R')
            self.image('../docs/mf_logo.jpg', 190, 274, 8)

    # Instantiation of inherited class
    pdf = PDF()
    pdf.set_auto_page_break(True, 25)
    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.set_font('Arial', '', 10)
    datos = select_cob(cobradores, mes, año)
    for i in datos:
        imprimir_registros_por_cob(i, mes, año)
        counter += 1
        mant.barra_progreso(counter, len(datos), titulo=f'Morella v{mant.VERSION} - MF! Soluciones informáticas')
    os.system(f'TITLE Morella v{mant.VERSION} - MF! Soluciones informáticas')
    pdf.ln(15)
    pdf.cell(0, 5, f' {total_mes_cob:.2f} ', 0, 0, 'R')
    pdf.cell(-27, 5, f'TOTAL: $ ', 0, 1, 'R')
    pdf.ln(2)
    pdf.output(f'../reports/caja/mensual/por_cobrador/caja_{str.lower(string_mes)}-{año}-por_cobrador.pdf', 'F')
        

    ############ ABRIR REPORT ############

    if errores:
        print('\n\n\n\n')
        print('     ATENCIÓN! Durante la emisión del reporte se produjeron los siguientes errores:')
        print()
        pprint(errores)
        print('\n\n\n\n')

    print("Abriendo reporte. Cierre el archivo para continuar...")
    ruta = f'../reports/caja/mensual/por_cobrador/'
    arch = f'caja_{str.lower(string_mes)}-{año}-por_cobrador.pdf'
    os.chdir(ruta)
    os.system(arch)
    ruta = '../../../../modulos/'
    os.chdir(ruta)

            ######################################## FIN DE REPORT ############################################





    #################################################################################################################
    ################################################### RECIBOS #####################################################    
    #################################################################################################################

def recibos(facturacion, id_cobrador, recibos):
    ############ INICIO DE VARIABLES INDEPENDIENTES ############
    periodo_actual = rend.obtener_periodo()
    dia = datetime.now().strftime('%d')
    mes = datetime.now().strftime('%m')
    año = datetime.now().strftime('%Y')
    año2c = datetime.now().strftime('%y')
    fecha = f"{mes}/{año}"
    counter = 0
    errores = {}

    ############ FIN DE VARIABLES INDEPENDIENTES ############

        
    ############ INICIO DE FUNCIONES ############
    

    ############ FIN DE FUNCIONES ############


    ############ INICIO DE VARIABLES DEPENDIENTES ############

    ########### FIN DE VARIABLES DEPENDIENTES ############
    

    ############ INICIO DE REPORT ############
    # Logo NOB
    class PDF(FPDF):
        def header(self):
            self.image('../docs/logo_nob.jpg', 11, 4, 10)
            self.image('../docs/logo_nob.jpg', 108, 4, 10)
            self.image('../docs/logo_nob.jpg', 11, 78, 10)
            self.image('../docs/logo_nob.jpg', 108, 78, 10)
            self.image('../docs/logo_nob.jpg', 11, 152, 10)
            self.image('../docs/logo_nob.jpg', 108, 152, 10)
            self.image('../docs/logo_nob.jpg', 11, 226, 10)
            self.image('../docs/logo_nob.jpg', 108, 226, 10)
    if facturacion == 'bicon':
        pdf = FPDF()
    elif facturacion == 'nob':
        pdf = PDF()
    pdf.set_margins(10, 0, 10)
    pdf.set_auto_page_break(True, 0)
    pdf.alias_nb_pages()
    pdf.add_page()
    for rec in recibos:
        # Variables individuales
        id_o, soc, nic, fac, cob, tar, rut, ult, u_a, fup, mor, c_f, u_r, paga, op_cob, nom_alt, dom_alt = rec
        nro, nom, dni, te_1, te_2, mail, dom, loc, c_p, f_n, f_a, act = rend.obtener_datos_socio(soc)
        if act == 1:
            try:
                cod, pan, pis, fil, num, cat, ocu, fall = rend.obtener_datos_nicho(nic)
            except UnboundLocalError:
                if 'Operaciones sin nicho' not in errores:
                    errores['Operaciones sin nicho'] = [str(id_o).rjust(7, '0')]
                else:
                    errores['Operaciones sin nicho'].append(str(id_o).rjust(7, '0'))
                continue
            id_c, cat, val_mant_bic, val_mant_nob = rend.obtener_categoria(cat)
            pant = rend.obtener_panteon(pan)
            nco = rend.obtener_nom_cobrador(cob)
            val_mant = 0
            ultimo_pago = f'{ult}{u_a}'
            if nom_alt != None:
                nom = f"[{nom_alt}]"
            if dom_alt != None:
                dom = f"[{dom_alt}]"
            if fac == 'bicon':
                val_mant = val_mant_bic
            elif fac == 'nob':
                val_mant = val_mant_nob
            if ultimo_pago != f'{periodo_actual}{año}' and c_f > 0 and u_r != f"{mes}-{año2c}":
                añovar = 0
                if periodo_actual == "Enero - Febrero":
                    añovar = f"{int(datetime.now().strftime('%Y'))+1}"
                else:
                    añovar = datetime.now().strftime('%Y')
                c_f -= 1
                rend.ingresar_cobro_auto(id_o, c_f, f"{mes}-{año2c}")
            elif ultimo_pago != f'{periodo_actual}{año}' and c_f <= 0 and u_r != f"{mes}-{año2c}":
                # Ingresando recibo en la base de datos
                añovar = 0
                if periodo_actual == "Enero - Febrero":
                    añovar = f"{int(datetime.now().strftime('%Y'))+1}"
                else:
                    añovar = datetime.now().strftime('%Y')
                parameters = str((id_o, periodo_actual, añovar, 0))
                query = f"INSERT INTO recibos (operacion, periodo, año, pago) VALUES {parameters}"
                rend.run_query(query)
                ndr = rend.obtener_nro_recibo()
                # Header
                if fac == 'bicon':
                    # Línea 1
                    pdf.set_font('Arial', 'I', 7)
                    pdf.cell(190, 3.1, '', 0, 1, 'L')
                    pdf.cell(71, 3, '', 0, 0, 'L')
                    pdf.cell(25, 3, 'Talón para control', 0, 0, 'L')
                    pdf.cell(61, 3, '', 0, 0, 'L')
                    pdf.cell(31, 3, 'Talón para el contribuyente', 0, 1, 'L')
                    pdf.ln(1)
                    # Línea 2
                    pdf.set_font('Arial', 'B', 8)
                    pdf.cell(7, 3, '', 0, 0, 'L')
                    pdf.cell(87, 3, 'ADMINISTRACIÓN de PANTEONES SOCIALES', 0, 0, 'L')
                    pdf.cell(7, 3, '', 0, 0, 'L')
                    pdf.cell(87, 3, 'ADMINISTRACIÓN de PANTEONES SOCIALES', 0, 1, 'L')
                    # Línea 3
                    pdf.cell(22, 3, '', 0, 0, 'L')
                    pdf.cell(76, 3, 'Tel.: 430 9999 / 430 8800', 0, 0, 'L')
                    pdf.cell(18, 3, '', 0, 0, 'L')
                    pdf.cell(76, 3, 'Tel.: 430 9999 / 430 8800', 0, 1, 'L')
                    # Línea 4
                    pdf.cell(19, 3, '', 0, 0, 'L')
                    pdf.cell(45, 3, 'CORDOBA 2915 - ROSARIO', 0, 0, 'L')
                    pdf.cell(17, 3, 'Recibo nro.', 'LTB', 0, 'L')
                    pdf.cell(12, 3, f'{ndr}'.rjust(7, '0'), 'RTB', 0, 'R')
                    pdf.cell(13, 3, '', 0, 0, 'L')
                    pdf.cell(55, 3, 'CORDOBA 2915 - ROSARIO', 0, 0, 'L')
                    pdf.cell(17, 3, 'Recibo nro.', 'LTB', 0, 'L')
                    pdf.cell(12, 3, f'{ndr}'.rjust(7, '0'), 'RTB', 1, 'R')
                    pdf.ln(1)
                elif fac == 'nob':
                    # Línea 1
                    pdf.set_font('Arial', 'I', 7)
                    pdf.cell(190, 3.1, '', 0, 1, 'L')
                    pdf.ln(1)
                    pdf.set_font('Arial', 'B', 8)
                    pdf.cell(12, 3, '', 0, 0, 'L')
                    pdf.cell(60, 3, "Club Atlético Newell's Old Boys", 0, 0, 'L')
                    pdf.set_font('Arial', 'I', 7)
                    pdf.cell(14, 3, 'Talón para control', 0, 0, 'L')
                    pdf.set_font('Arial', 'B', 8)
                    pdf.cell(24, 3, '', 0, 0, 'L')
                    pdf.cell(49, 3, "Club Atlético Newell's Old Boys", 0, 0, 'L')
                    pdf.set_font('Arial', 'I', 7)
                    pdf.cell(14, 3, 'Talón para el contribuyente', 0, 1, 'L')
                    # Línea 2
                    pdf.set_font('Arial', 'B', 6)
                    pdf.cell(12, 3, '', 0, 0, 'L')
                    pdf.cell(16, 3, 'Panteón Social', 0, 0, 'L')
                    pdf.set_font('Arial', 'I', 6)
                    pdf.cell(48, 3, '(Cementerio "El Salvador")', 0, 0, 'L')
                    pdf.cell(15, 3, '', 0, 0, 'L')
                    pdf.set_font('Arial', 'B', 6)
                    pdf.cell(19, 3, '', 0, 0, 'L')
                    pdf.cell(16, 3, 'Panteón Social', 0, 0, 'L')
                    pdf.set_font('Arial', 'I', 6)
                    pdf.cell(47, 3, '(Cementerio "El Salvador")', 0, 0, 'L')
                    pdf.cell(15, 3, '', 0, 1, 'L')
                    # Línea 3
                    pdf.set_font('Arial', 'B', 6)
                    pdf.cell(12, 3, '', 0, 0, 'L')
                    pdf.cell(60, 3, 'ADMINISTRACIÓN PANTEÓN SOCIAL', 0, 0, 'L')
                    pdf.cell(38, 3, '', 0, 0, 'L')
                    pdf.cell(49, 3, 'ADMINISTRACIÓN PANTEÓN SOCIAL', 0, 1, 'L')
                    # Línea 4
                    pdf.set_font('Arial', '', 6)
                    pdf.cell(12, 3, '', 0, 0, 'L')
                    pdf.cell(52, 3, 'Córdoba 2915 - Tel. 430 9999 / 8800', 0, 0, 'L')
                    pdf.set_font('Arial', 'B', 8)
                    pdf.cell(17, 3, 'Recibo nro.', 'LTB', 0, 'L')
                    pdf.cell(12, 3, f'{ndr}'.rjust(7, '0'), 'RTB', 0, 'R')
                    pdf.set_font('Arial', '', 6)
                    pdf.cell(17, 3, '', 0, 0, 'L')
                    pdf.cell(51, 3, 'Córdoba 2915 - Tel. 430 9999 / 8800', 0, 0, 'L')
                    pdf.set_font('Arial', 'B', 8)
                    pdf.set_font('Arial', 'B', 8)
                    pdf.cell(17, 3, 'Recibo nro.', 'LTB', 0, 'L')
                    pdf.cell(12, 3, f'{ndr}'.rjust(7, '0'), 'RTB', 1, 'R')
                    pdf.ln(1)
                # Línea 1
                pdf.set_font('Arial', 'B', 9)
                pdf.cell(13, 4, 'Socio/a: ', 'LTB', 0, 'L')
                pdf.set_font('Arial', '', 9)
                pdf.cell(12, 4, f'{nro}'.rjust(6, '0'), 'TB', 0, 'L')
                pdf.cell(68, 4, f'{nom}', 'TRB', 0, 'L')
                pdf.cell(4, 4, '', 0, 0, 'L')
                pdf.set_font('Arial', 'B', 9)
                pdf.cell(13, 4, 'Socio/a: ', 'LT', 0, 'L')
                pdf.set_font('Arial', '', 9)
                pdf.cell(12, 4, f'{nro}'.rjust(6, '0'), 'T', 0, 'L')
                pdf.cell(68, 4, f'{nom}', 'TR', 1, 'L')
                # Línea 2
                pdf.set_font('Arial', 'B', 9)
                pdf.cell(95, 1, '', 0, 0, 'L')
                pdf.cell(2, 1, '', 0, 0, 'L')
                pdf.cell(93, 1, '', 'LR', 1, 'L')
                pdf.cell(19, 5, 'Cobrador/a: ', 'LT', 0, 'L')
                pdf.set_font('Arial', '', 9)
                pdf.cell(5, 5, f'{cob}'.rjust(2, '0'), 'T', 0, 'L')
                pdf.cell(39, 5, f'{nco}', 'T', 0, 'L')
                pdf.set_font('Arial', 'B', 9)
                pdf.cell(9, 5, 'Ruta:', 'T', 0, 'L')
                pdf.set_font('Arial', '', 9)
                pdf.cell(21, 5, f'{rut}'.rjust(3, '0'), 'RT', 0, 'L')
                pdf.cell(4, 5, '', 0, 0, 'L')
                pdf.set_font('Arial', 'B', 9)
                pdf.cell(17, 5, 'Domicilio: ', 'L', 0, 'L')
                pdf.set_font('Arial', '', 9)
                pdf.cell(76, 5, f'{dom}', 'R', 1, 'L')
                # Línea 3
                pdf.set_font('Arial', 'B', 9)
                pdf.cell(17, 4, 'Categoría: ', 'LB', 0, 'L')
                pdf.set_font('Arial', '', 9)
                pdf.cell(76, 4, f'{cat}', 'RB', 0, 'L')
                pdf.cell(4, 4, '', 0, 0, 'L')
                pdf.set_font('Arial', 'B', 9)
                pdf.cell(17, 4, 'Localidad:', 'LB', 0, 'L')
                pdf.set_font('Arial', '', 9)
                pdf.cell(76, 4, f'{loc} - {c_p}', 'BR', 1, 'L')
                pdf.ln(1)
                # Línea 4
                pdf.set_font('Arial', 'B', 9)
                pdf.cell(19, 5, 'Cod. Nicho:', 'LTB', 0, 'L')
                pdf.set_font('Arial', '', 9)
                pdf.cell(44, 5, f'{cod}'.rjust(10, '0'), 'TB', 0, 'L')
                pdf.set_font('Arial', 'B', 9)
                pdf.cell(7, 5, f'Op:', 'TB', 0, 'L')
                pdf.set_font('Arial', '', 9)
                pdf.cell(23, 5, f'{id_o}'.rjust(7, "0"), 'RTB', 0, 'L')
                pdf.cell(4, 5, '', 0, 0, 'L')
                pdf.set_font('Arial', 'B', 9)
                pdf.cell(16, 5, 'Cobrador:', 'LTB', 0, 'L')
                pdf.set_font('Arial', '', 9)
                pdf.cell(5, 5, f'{cob}'.rjust(2, '0'), 'TB', 0, 'L')
                pdf.cell(72, 5, f'{nco}', 'RTB', 1, 'L')
                pdf.ln(1)
                # Línea 5
                pdf.set_font('Arial', 'B', 9)
                pdf.cell(44, 4, 'Panteón', 'LTR', 0, 'C')
                pdf.cell(16, 4, 'Piso', 'LTR', 0, 'C')
                pdf.cell(16, 4, 'Fila', 'LTR', 0, 'C')
                pdf.cell(17, 4, 'Nicho', 'LTR', 0, 'C')
                pdf.cell(4, 4, '', 0, 0, 'C')
                pdf.cell(29, 4, 'Categoría', 'LTR', 0, 'C')
                pdf.cell(34, 4, 'Panteón', 'LTR', 0, 'C')
                pdf.cell(9, 4, 'Piso', 'LTR', 0, 'C')
                pdf.cell(9, 4, 'Fila', 'LTR', 0, 'C')
                pdf.cell(12, 4, 'Nicho', 'LTR', 1, 'C')
                # Línea 6
                pdf.set_font('Arial', '', 9)
                pdf.cell(44, 5, f'{pant}', 'LBR', 0, 'C')
                pdf.cell(16, 5, f'{pis}'.rjust(2, '0'), 'LBR', 0, 'C')
                pdf.cell(16, 5, f'{fil}'.rjust(2, '0'), 'LBR', 0, 'C')
                pdf.cell(17, 5, f'{num}'.rjust(3, '0'), 'LBR', 0, 'C')
                pdf.cell(4, 5, '', 0, 0, 'C')
                pdf.cell(29, 5, f'{cat}', 'LBR', 0, 'C')
                pdf.cell(34, 5, f'{pant}', 'LBR', 0, 'C')
                pdf.cell(9, 5, f'{pis}'.rjust(2, '0'), 'LBR', 0, 'C')
                pdf.cell(9, 5, f'{fil}'.rjust(2, '0'), 'LBR', 0, 'C')
                pdf.cell(12, 5, f'{num}'.rjust(3, '0'), 'LBR', 1, 'C')
                pdf.ln(3)
                # Línea 7
                if periodo_actual == "Enero - Febrero":
                    pdf.set_font('Arial', 'B', 9)
                    pdf.cell(14, 5, 'Período: ', 'LTB', 0, 'L')
                    pdf.set_font('Arial', '', 9)
                    pdf.cell(44, 5, f'{periodo_actual} - {int(año)+1}', 'RTB', 0, 'L')
                    pdf.set_font('Arial', 'B', 9)
                    pdf.cell(14, 5, 'Importe:', 'LTB', 0, 'L')
                    pdf.set_font('Arial', '', 9)
                    pdf.cell(21, 5, f'$ {val_mant:.2f}', 'RTB', 0, 'R')
                    pdf.cell(4, 5, '', 0, 0, 'C')
                    pdf.set_font('Arial', 'B', 9)
                    pdf.cell(14, 5, 'Período: ', 'LTB', 0, 'L')
                    pdf.set_font('Arial', '', 9)
                    pdf.cell(44, 5, f'{periodo_actual} - {int(año)+1}', 'RTB', 0, 'L')
                    pdf.set_font('Arial', 'B', 9)
                    pdf.cell(14, 5, 'Importe:', 'LTB', 0, 'L')
                    pdf.set_font('Arial', '', 9)
                    pdf.cell(21, 5, f'$ {val_mant:.2f}', 'RTB', 1, 'R')
                    pdf.ln(2)
                elif periodo_actual == "Diciembre - Enero":
                    pdf.set_font('Arial', 'B', 9)
                    pdf.cell(14, 5, 'Período: ', 'LTB', 0, 'L')
                    pdf.set_font('Arial', '', 9)
                    pdf.cell(44, 5, f'{periodo_actual} - {año}/{int(año2c)+1}', 'RTB', 0, 'L')
                    pdf.set_font('Arial', 'B', 9)
                    pdf.cell(14, 5, 'Importe:', 'LTB', 0, 'L')
                    pdf.set_font('Arial', '', 9)
                    pdf.cell(21, 5, f'$ {val_mant:.2f}', 'RTB', 0, 'R')
                    pdf.cell(4, 5, '', 0, 0, 'C')
                    pdf.set_font('Arial', 'B', 9)
                    pdf.cell(14, 5, 'Período: ', 'LTB', 0, 'L')
                    pdf.set_font('Arial', '', 9)
                    pdf.cell(44, 5, f'{periodo_actual} - {año}/{int(año2c)+1}', 'RTB', 0, 'L')
                    pdf.set_font('Arial', 'B', 9)
                    pdf.cell(14, 5, 'Importe:', 'LTB', 0, 'L')
                    pdf.set_font('Arial', '', 9)
                    pdf.cell(21, 5, f'$ {val_mant:.2f}', 'RTB', 1, 'R')
                    pdf.ln(2)
                else:
                    pdf.set_font('Arial', 'B', 9)
                    pdf.cell(14, 5, 'Período: ', 'LTB', 0, 'L')
                    pdf.set_font('Arial', '', 9)
                    pdf.cell(44, 5, f'{periodo_actual} - {año}', 'RTB', 0, 'L')
                    pdf.set_font('Arial', 'B', 9)
                    pdf.cell(14, 5, 'Importe:', 'LTB', 0, 'L')
                    pdf.set_font('Arial', '', 9)
                    pdf.cell(21, 5, f'$ {val_mant:.2f}', 'RTB', 0, 'R')
                    pdf.cell(4, 5, '', 0, 0, 'C')
                    pdf.set_font('Arial', 'B', 9)
                    pdf.cell(14, 5, 'Período: ', 'LTB', 0, 'L')
                    pdf.set_font('Arial', '', 9)
                    pdf.cell(44, 5, f'{periodo_actual} - {año}', 'RTB', 0, 'L')
                    pdf.set_font('Arial', 'B', 9)
                    pdf.cell(14, 5, 'Importe:', 'LTB', 0, 'L')
                    pdf.set_font('Arial', '', 9)
                    pdf.cell(21, 5, f'$ {val_mant:.2f}', 'RTB', 1, 'R')
                    pdf.ln(2)
                # Línea 8
                q_rec_impagos = len(rend.obtener_recibos_impagos_op(id_o))
                debe = 0
                if c_f < 0:
                    debe += abs(c_f)
                debe += q_rec_impagos - 1
                if debe:
                    pdf.cell(93, 4, f'----------- ATENCIÓN: El asociado adeuda {debe} cuotas. ----------', 1, 1, 'C')
                    # Margen
                    pdf.cell(190, 13, ' ', 0, 1, 'L')
                else:
                    pdf.cell(190, 17, ' ', 0, 1, 'L')
        counter += 1
        mant.barra_progreso(counter, len(recibos), titulo=f'Morella v{mant.VERSION} - MF! Soluciones informáticas', solo_titulo=True)
    os.system(f'TITLE Morella v{mant.VERSION} - MF! Soluciones informáticas')
    try:
        if not os.path.isdir(f'../reports/recibos/{nco}'):
            os.mkdir(f'../reports/recibos/{nco}')
        output_counter = 0
        output_name = f"recibos_{año}-{mes}-{dia}.pdf"
        while os.path.isfile(f'../reports/recibos/{nco}/{output_name}'):
            output_counter += 1
            output_name = f"recibos_{año}-{mes}-{dia}_({output_counter}).pdf"
        pdf.output(f'../reports/recibos/{nco}/{output_name}', 'F')

        ############ ABRIR REPORT ############

        if errores:
            print('\n\n\n\n')
            print('     ATENCIÓN! Durante la emisión de los recibos se produjeron los siguientes errores:')
            print()
            pprint(errores)
            print('\n\n\n\n')

        print("Abriendo recibos...")
        ruta = f'../reports/recibos/{nco}/'
        arch = output_name.replace('(', '^(')
        os.chdir(ruta)
        os.system(arch)
        ruta = '../../../modulos/'
        os.chdir(ruta)
        return recibos
    except UnboundLocalError:
        print("")
        print("No se encontraron recibos impagos.")
        print("")
    except:
        mant.log_error()
        print("")
        input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
        print()
        return

            ######################################## FIN DE REPORT ############################################





    #################################################################################################################
    ############################################## LISTADO DE RECIBOS ###############################################
    #################################################################################################################

def listado_recibos(facturacion, id_cobrador, recibos):
    ############ INICIO DE VARIABLES INDEPENDIENTES ############

    fecha = caja.obtener_fecha()
    hora = datetime.now().strftime('%H:%M')
    periodo_actual = rend.obtener_periodo()
    periodo_anterior = rend.obtener_periodo_anterior(periodo_actual)
    dia = datetime.now().strftime('%d')
    mes = datetime.now().strftime('%m')
    año = datetime.now().strftime('%Y')
    año2c = datetime.now().strftime('%y')
    imp_acu = float(0)
    nco = rend.obtener_nom_cobrador(id_cobrador)
    counter = 0
    errores = {}

    ############ FIN DE VARIABLES INDEPENDIENTES ############

        
    ############ INICIO DE FUNCIONES ############
    def days_between(d1, d2):
        return abs(d2-d1).days

    ############ FIN DE FUNCIONES ############


    ############ INICIO DE VARIABLES DEPENDIENTES ############

    ########### FIN DE VARIABLES DEPENDIENTES ############
    

    ############ INICIO DE REPORT ############
    class PDF(FPDF):
        # Page header
        def header(self):
            # Logo
            self.image('../docs/logo_bicon.jpg', 14.5, 12, 15)
            # Arial bold 15
            self.set_font('Arial', 'B', 15)
            # Title
            self.cell(0, 20, 'LISTADO DE RECIBOS EMITIDOS', 1, 0, 'C')
            # Arial 10
            self.set_font('Arial', '', 10)
            # Fecha
            self.cell(0, 35, f'{fecha} - {hora} hs', 0, 0, 'R')
            # N° de cierre
            self.set_font('Arial', 'B', 10)
            self.cell(-77, 35, f'Cobrador: {nco}', 0, 0, 'R')
            # Line break
            self.ln(22)
            self.cell(14, 5, 'Socio/a', 0, 0, 'L ')
            self.cell(65, 5, 'Apellido y Nombre', 0, 0, 'L')
            pdf.cell(1, 5, '', 0, 0, 'L')
            self.cell(79, 5, 'Domicilio', 0, 0, 'L')
            pdf.cell(1, 5, '', 0, 0, 'L')
            self.cell(15, 5, 'Ruta', 0, 0, 'L')
            pdf.cell(20, 5, 'Importe', 0, 1, 'L')
            self.cell(0, 1, '_________________________________________________________________________________________________', 0, 1, 'C')
            self.ln(3)
            
        # Page footer
        def footer(self):
            # Position at 3 cm from bottom
            self.set_y(-30)
            # Arial italic 8
            self.set_font('Arial', 'I', 8)
            self.cell(0, 5, '* El asociado adeuda cuotas', 0, 1, 'L')
            self.cell(0, 1, '_______________________________________________________________________________________________', 0, 1, 'C')
            # Page number
            self.cell(0, 10, 'Página ' + str(self.page_no()) + ' de {nb}', 0, 0, 'C')
            # Firma
            self.set_font('Arial', 'I', 8)
            self.cell(-10, 10, f'Reporte generado en *MORELLA v{mant.SHORT_VERSION}* by ', 0, 0, 'R')
            self.image('../docs/mf_logo.jpg', 190, 274, 8)

    # Instantiation of inherited class
    pdf = PDF()
    pdf.set_auto_page_break(True, 30)
    pdf.alias_nb_pages()
    pdf.add_page()
    for rec in recibos:
        id_o, soc, nic, fac, cob, tar, rut, ult, u_a, fup, mor, c_f, u_r, paga, op_cob, nom_alt, dom_alt = rec
        nro, nom, dni, te_1, te_2, mail, dom, loc, c_p, f_n, f_a, act = rend.obtener_datos_socio(soc)
        if act == 1:
            try:
                cod, pan, pis, fil, num, cat, ocu, fall = rend.obtener_datos_nicho(nic)
            except UnboundLocalError:
                continue
            id_c, cat, val_mant_bic, val_mant_nob = rend.obtener_categoria(cat)
            fup_sep = str(fup).split("/")
            fup_date = date(year = int(fup_sep[1]), month = int(fup_sep[0]), day = 1)
            hoy = datetime.now().date()
            cuenta = int(days_between(hoy, fup_date)/730)
            ultimo_pago = f'{ult}{u_a}'
            val_mant = 0
            if nom_alt != None:
                nom = f"[{nom_alt}]"
            if dom_alt != None:
                dom = f"[{dom_alt}]"
            if fac == 'bicon':
                val_mant = val_mant_bic
            elif fac == 'nob':
                val_mant = val_mant_nob
            if ultimo_pago != f'{periodo_actual}{año}' and c_f <= 0 and u_r != f"{mes}-{año2c}":
                counter = counter + 1
                q_rec_impagos = len(rend.obtener_recibos_impagos_op(id_o))
                debe = 0
                if c_f < 0:
                    debe += abs(c_f)
                debe += q_rec_impagos
                if q_rec_impagos:
                    if rend.obtener_recibos_impagos_op(id_o)[-1][2] == periodo_actual:
                        debe -= 1
                if debe > 0:
                    pdf.set_font('Arial', '', 10)
                    pdf.cell(14, 5, f'{nro}'.rjust(6, '0'), 0, 0, 'L ')
                    pdf.cell(65,5, f'{nom}*', 0, 0, 'L')
                    pdf.cell(1, 5, '', 0, 0, 'L')
                    pdf.cell(79, 5, f'{dom}', 0, 0, 'L')
                    pdf.cell(1, 5, '', 0, 0, 'L')
                    pdf.cell(10, 5, f'{rut}'.rjust(3, '0'), 0, 0, 'L')
                    pdf.cell(20, 5, f'{val_mant:.2f}', 0, 1, 'R')
                    imp_acu = imp_acu + float(val_mant)
                else:
                    pdf.set_font('Arial', '', 10)
                    pdf.cell(14, 5, f'{nro}'.rjust(6, '0'), 0, 0, 'L ')
                    pdf.cell(65,5, f'{nom}', 0, 0, 'L')
                    pdf.cell(1, 5, '', 0, 0, 'L')
                    pdf.cell(79, 5, f'{dom}', 0, 0, 'L')
                    pdf.cell(1, 5, '', 0, 0, 'L')
                    pdf.cell(10, 5, f'{rut}'.rjust(3, '0'), 0, 0, 'L')
                    pdf.cell(20, 5, f'{val_mant:.2f}', 0, 1, 'R')
                    imp_acu = imp_acu + float(val_mant)
                # Evitar duplicado de recibos
                rend.evitar_duplicado(mes, año2c, id_o)
                # Envío de recordatorio vía mail     <---------------------------------- Buscar alternativa, demora mucho.
                if False:
                    if mail != None and cob != 6 and mor == 0:
                        try:
                            email.recordatorio_cobrador(nro, periodo_actual, cod, pan, nco)
                        except SMTPAuthenticationError:
                            pass
                        except gaierror:
                             pass
                        except:
                           mant.log_error()
                           print("")
                           input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
                           print()
                           return
                # Revisión estado de mora
                if cuenta > 0:
                    rend.set_moroso(id_o)
                    if False:                      # <---------------------------------- Buscar alternativa, demora mucho.
                        # Generar reporte de estado de cuenta
                        report_estado_cta_mail(nro, nom, dni, fac, dom, te_1, te_2, mail, c_p, loc, act)
                        # Envío de aviso de mora vía mail
                        try:
                            email.aviso_de_mora(id_o)
                        except SMTPAuthenticationError:
                            mant.log_error()
                            pass
                        except gaierror:
                            mant.log_error()
                            pass
                        except:
                            mant.log_error()
                            print("")
                            input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
                            print()
                            return
    pdf.ln(2)
    pdf.cell(91, 5, '', 0, 0, 'L')
    pdf.cell(33, 5, 'Cantidad de recibos:', 'LTB', 0, 'L')
    pdf.cell(8, 5, f'{counter}', 'RTB', 0, 'R')
    pdf.cell(2, 5, '', 0, 0, 'L')
    pdf.cell(33, 5, 'Importe acumulado:', 'LTB', 0, 'L')
    pdf.cell(23, 5, f'$ {imp_acu:.2f}', 'RTB', 0, 'R')
    try:
        if not os.path.isdir(f'../reports/recibos/{nco}'):
            os.mkdir(f'../reports/recibos/{nco}')
        output_counter = 0
        output_name = f"listado_recibos_{año}-{mes}-{dia}.pdf"
        while os.path.isfile(f'../reports/recibos/{nco}/{output_name}'):
            output_counter += 1
            output_name = f'listado_recibos_{año}-{mes}-{dia}_({output_counter}).pdf'
        pdf.output(f'../reports/recibos/{nco}/{output_name}', 'F')

    ############ ABRIR REPORT ############

        if errores:
            print('\n\n\n\n')
            print('     ATENCIÓN! Durante la emisión del listado se produjeron los siguientes errores:')
            print()
            pprint(errores)
            print('\n\n\n\n')
            
        print("Abriendo Listado...")
        ruta = f'../reports/recibos/{nco}/'
        arch = output_name.replace('(', '^(')
        os.chdir(ruta)
        os.system(arch)
        ruta = '../../../modulos/'
        os.chdir(ruta)
    except UnboundLocalError:
        print("")
        print("No se encontraron recibos impagos.")
        print("")
    except:
        mant.log_error()
        print("")
        input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
        print()
        return
          
            ######################################## FIN DE REPORT ############################################





    #################################################################################################################
    ############################################## RECIBOS DEB. AUT. ################################################    
    #################################################################################################################

def recibos_deb_aut(facturacion, recibos):
    ############ INICIO DE VARIABLES INDEPENDIENTES ############
    periodo_actual = rend.obtener_periodo()
    mes = datetime.now().strftime('%m')
    año = datetime.now().strftime('%Y')
    año2c = datetime.now().strftime('%y')
    fecha = f"{mes}/{año}"
    counter = 0
    errores = {}

    ############ FIN DE VARIABLES INDEPENDIENTES ############

        
    ############ INICIO DE FUNCIONES ############

    ############ FIN DE FUNCIONES ############


    ############ INICIO DE VARIABLES DEPENDIENTES ############

    ########### FIN DE VARIABLES DEPENDIENTES ############
    

    ############ INICIO DE REPORT ############
    for rec in recibos:
        pdf = FPDF()
        pdf.alias_nb_pages()
        pdf.add_page()
        # Variables individuales
        id_o, soc, nic, fac, cob, tar, rut, ult, u_a, fup, mor, c_f, u_r, paga, op_cob, nom_alt, dom_alt = rec
        try:
            cod, pan, pis, fil, num, cat, ocu, fall = rend.obtener_datos_nicho(nic)
        except UnboundLocalError:
            if 'Operaciones sin nicho' not in errores:
                errores['Operaciones sin nicho'] = [str(id_o).rjust(7, '0')]
            else:
                errores['Operaciones sin nicho'].append(str(id_o).rjust(7, '0'))
            continue
        nro, nom, dni, te_1, te_2, mail, dom, loc, c_p, f_n, f_a, act = rend.obtener_datos_socio(soc)
        id_c, cat, val_mant_bic, val_mant_nob = rend.obtener_categoria(cat)
        t01, t02, t03, t04 = rend.split_nro_tarjeta(tar)
        panteon = rend.obtener_panteon(pan)
        nco = rend.obtener_nom_cobrador(cob)
        val_mant = 0
        if nom_alt != None:
            nom = f"[{nom_alt}]"
        if dom_alt != None:
            dom = f"[{dom_alt}]"
        if fac == 'bicon':
            val_mant = val_mant_bic
        elif fac == 'nob':
            val_mant = val_mant_nob
        if act == 1:
            if not ult == periodo_actual and u_a == año and c_f > 0:
                añovar = 0
                if periodo_actual == "Enero - Febrero":
                    añovar = f"{int(datetime.now().strftime('%Y'))+1}"
                else:
                    añovar = datetime.now().strftime('%Y')
                c_f -= 1
                rend.ingresar_cobro_auto(id_o, c_f)
            elif not ult == periodo_actual and u_a == año and c_f == 0 and u_r != f"{mes}-{año2c}":
                # Ingresando recibo en la base de datos
                añovar = 0
                if periodo_actual == "Enero - Febrero":
                    añovar = f"{int(datetime.now().strftime('%Y'))+1}"
                else:
                    añovar = datetime.now().strftime('%Y')
                parameters = str((id_o, periodo_actual, añovar, 0))
                query = f"INSERT INTO recibos (operacion, periodo, año, pago) VALUES {parameters}"
                rend.run_query(query)
                ndr = rend.obtener_nro_recibo()
                # Header
                # Bicon
                if fac == 'bicon':
                    pdf.set_font('Arial', 'B', 11)
                    pdf.cell(85, 5, 'ADMINISTRACIÓN de PANTEONES SOCIALES', 0, 1, 'C')
                    pdf.cell(85, 5, 'Tel.: 430 9999 / 430 8800', 0, 1, 'C')
                    pdf.cell(85, 5, 'CORDOBA 2915 - ROSARIO', 0, 1, 'C')
                    pdf.set_font('Arial', 'B', 10)
                    pdf.cell(49, 5, '', 0, 0, 'L')
                    pdf.cell(20, 5, 'Recibo nro.', 'LTB', 0, 'L')
                    pdf.cell(16, 5, f'{ndr}'.rjust(7, '0'), 'RTB', 1, 'R')
                    pdf.ln(1)
                elif fac == 'nob':
                    # Logo
                    pdf.image('../docs/logo_nob.jpg', 11, 14, 10)
                    pdf.set_font('Arial', 'I', 7)
                    pdf.cell(190, 3.1, '', 0, 1, 'L')
                    pdf.ln(1)
                    # Línea 1
                    pdf.set_font('Arial', 'B', 8)
                    pdf.cell(12, 3, '', 0, 0, 'L')
                    pdf.cell(60, 3, "Club Atlético Newell's Old Boys", 0, 1, 'L')
                    # Línea 2
                    pdf.set_font('Arial', 'B', 6)
                    pdf.cell(12, 3, '', 0, 0, 'L')
                    pdf.cell(16, 3, 'Panteón Social', 0, 0, 'L')
                    pdf.set_font('Arial', 'I', 6)
                    pdf.cell(48, 3, '(Cementerio "El Salvador")', 0, 0, 'L')
                    pdf.cell(15, 3, '', 0, 1, 'L')
                    # Línea 3
                    pdf.set_font('Arial', 'B', 6)
                    pdf.cell(12, 3, '', 0, 0, 'L')
                    pdf.cell(60, 3, 'ADMINISTRACIÓN PANTEÓN SOCIAL', 0, 1, 'L')
                    # Línea 4
                    pdf.set_font('Arial', '', 6)
                    pdf.cell(12, 3, '', 0, 0, 'L')
                    pdf.cell(44, 3, 'Córdoba 2915 - Tel. 430 9999 / 8800', 0, 0, 'L')
                    pdf.set_font('Arial', 'B', 8)
                    pdf.cell(17, 3, 'Recibo nro.', 'LTB', 0, 'L')
                    pdf.cell(12, 3, f'{ndr}'.rjust(7, '0'), 'RTB', 1, 'R')
                    pdf.ln(1)
                # Línea 1
                pdf.set_font('Arial', 'B', 9)
                pdf.cell(13, 4, 'Socio/a: ', 'LTB', 0, 'L')
                pdf.set_font('Arial', '', 9)
                pdf.cell(12, 4, f'{nro}'.rjust(6, '0'), 'TB', 0, 'L')
                pdf.cell(60, 4, f'{nom}', 'TRB', 1, 'L')
                # Línea 2
                pdf.set_font('Arial', 'B', 9)
                pdf.cell(85, 1, '', 0, 1, 'L')
                pdf.cell(19, 5, 'Cobrador/a: ', 'LT', 0, 'L')
                pdf.set_font('Arial', '', 9)
                pdf.cell(5, 5, f'{cob}'.rjust(2, '0'), 'T', 0, 'L')
                pdf.cell(41, 5, f'{nco}', 'T', 0, 'L')
                pdf.set_font('Arial', 'B', 9)
                pdf.cell(10, 5, 'Tarjeta: ', 'T', 0, 'R')
                pdf.set_font('Arial', '', 9)
                pdf.cell(10, 5, f'{t04}', 'TR', 1, 'L')
                # Línea 3
                pdf.set_font('Arial', 'B', 9)
                pdf.cell(17, 4, 'Categoría: ', 'LB', 0, 'L')
                pdf.set_font('Arial', '', 9)
                pdf.cell(68, 4, f'{cat}', 'BR', 1, 'L')
                pdf.ln(1)
                # Línea 4
                pdf.set_font('Arial', 'B', 9)
                pdf.cell(19, 5, 'Cod. Nicho:', 'LTB', 0, 'L')
                pdf.set_font('Arial', '', 9)
                pdf.cell(66, 5, f'{cod}'.rjust(10, '0'), 'RTB', 1, 'L')
                pdf.ln(1)
                # Línea 5
                pdf.set_font('Arial', 'B', 9)
                pdf.cell(44, 4, 'Panteón', 'LTR', 0, 'C')
                pdf.cell(13, 4, 'Piso', 'LTR', 0, 'C')
                pdf.cell(13, 4, 'Fila', 'LTR', 0, 'C')
                pdf.cell(15, 4, 'Nicho', 'LTR', 1, 'C')
                # Línea 6
                pdf.set_font('Arial', '', 9)
                pdf.cell(44, 5, f'{panteon}', 'LBR', 0, 'C')
                pdf.cell(13, 5, f'{pis}'.rjust(2, '0'), 'LBR', 0, 'C')
                pdf.cell(13, 5, f'{fil}'.rjust(2, '0'), 'LBR', 0, 'C')
                pdf.cell(15, 5, f'{num}'.rjust(3, '0'), 'LBR', 1, 'C')
                pdf.ln(3)
                # Línea 7
                if periodo_actual == "Enero - Febrero":
                    pdf.set_font('Arial', 'B', 9)
                    pdf.cell(14, 5, 'Período: ', 'LTB', 0, 'L')
                    pdf.set_font('Arial', '', 9)
                    pdf.cell(54, 5, f'{periodo_actual} - {int(año)+1}', 'RTB', 0, 'L')
                    pdf.set_font('Arial', '', 9)
                    pdf.cell(17, 5, f'$ {val_mant:.2f}', 'RTB', 1, 'C')
                    pdf.ln(2)
                elif periodo_actual == "Diciembre - Enero":
                    pdf.set_font('Arial', 'B', 9)
                    pdf.cell(14, 5, 'Período: ', 'LTB', 0, 'L')
                    pdf.set_font('Arial', '', 9)
                    pdf.cell(54, 5, f'{periodo_actual} - {año}/{int(año2c)+1}', 'RTB', 0, 'L')
                    pdf.set_font('Arial', '', 9)
                    pdf.cell(17, 5, f'$ {val_mant:.2f}', 'RTB', 1, 'C')
                    pdf.ln(2)
                else:
                    pdf.set_font('Arial', 'B', 9)
                    pdf.cell(14, 5, 'Período: ', 'LTB', 0, 'L')
                    pdf.set_font('Arial', '', 9)
                    pdf.cell(54, 5, f'{periodo_actual} - {año}', 'RTB', 0, 'L')
                    pdf.set_font('Arial', '', 9)
                    pdf.cell(17, 5, f'$ {val_mant:.2f}', 'RTB', 1, 'C')
                    pdf.ln(2)
        try:

            if errores:
                print('\n\n\n\n')
                print('     ATENCIÓN! Durante la emisión de los recibos se produjeron los siguientes errores:')
                print()
                pprint(errores)
                print('\n\n\n\n')

            num_soc = f'{nro}'.rjust(6, '0')
            num_rec = f'{ndr}'.rjust(7, '0')
            if not os.path.isdir(f'../reports/recibos/{nco}'):
                os.mkdir(f'../reports/recibos/{nco}')
            if not os.path.isdir(f'../reports/recibos/{nco}/{num_soc}-{nom}'):
                os.mkdir(f'../reports/recibos/{nco}/{num_soc}-{nom}')
            pdf.output(f'../reports/recibos/{nco}/{num_soc}-{nom}/recibo-{num_rec}.pdf', 'F')
        except UnboundLocalError:
            print("")
            print("No se encontraron recibos impagos.")
            print("")
        except:
            mant.log_error()
            print("")
            input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
            print()
            return
        counter += 1
        mant.barra_progreso(counter, len(recibos), titulo=f'Morella v{mant.VERSION} - MF! Soluciones informáticas', solo_titulo=True)
    os.system(f'TITLE Morella v{mant.VERSION} - MF! Soluciones informáticas')
    print("\n")
        
            ######################################## FIN DE REPORT ############################################





    #################################################################################################################
    ######################################## LISTADO DE RECIBOS DEB. AUT. ###########################################    
    #################################################################################################################

def listado_recibos_deb_aut(facturacion, recibos):
    ############ INICIO DE VARIABLES INDEPENDIENTES ############
    id_cobrador = 6
    fecha = caja.obtener_fecha()
    hora = datetime.now().strftime('%H:%M')
    periodo_actual = rend.obtener_periodo()
    periodo_anterior = rend.obtener_periodo_anterior(periodo_actual)
    dia = datetime.now().strftime('%d')
    mes = datetime.now().strftime('%m')
    año = datetime.now().strftime('%Y')
    año2c = datetime.now().strftime('%y')
    año_sig_2c = int(año2c)+1
    imp_acu = float(0)
    nco = rend.obtener_nom_cobrador(id_cobrador)
    counter = 0
    contador_fiserv = 0
    val_total = 0
    nro_comercio_fiserv = "25476675"
    filler = " "
    errores = {}

    ############ FIN DE VARIABLES INDEPENDIENTES ############

        
    ############ INICIO DE FUNCIONES ############
    if os.path.isfile('../reports/presentaciones_fiserv/temp/pres_det.txt') == True:
        os.remove('../reports/presentaciones_fiserv/temp/pres_det.txt')

    ############ FIN DE FUNCIONES ############


    ############ INICIO DE VARIABLES DEPENDIENTES ###########

    if periodo_actual == 'Enero - Febrero':
        periodo_fiserv = f"1/{año2c} "
        vto_fiserv = f"2802{año2c}"
    elif periodo_actual == 'Febrero - Marzo':
        periodo_fiserv = f"1/{año2c} "
        vto_fiserv = f"3103{año2c}"
    elif periodo_actual == 'Marzo - Abril':
        periodo_fiserv = f"2/{año2c} "
        vto_fiserv = f"3004{año2c}"
    elif periodo_actual == 'Abril - Mayo':
        periodo_fiserv = f"2/{año2c} "
        vto_fiserv = f"3105{año2c}"
    elif periodo_actual == 'Mayo - Junio':
        periodo_fiserv = f"3/{año2c} "
        vto_fiserv = f"3006{año2c}"
    elif periodo_actual == 'Junio - Julio':
        periodo_fiserv = f"3/{año2c} "
        vto_fiserv = f"3107{año2c}"
    elif periodo_actual == 'Julio - Agosto':
        periodo_fiserv = f"4/{año2c} "
        vto_fiserv = f"3108{año2c}"
    elif periodo_actual == 'Agosto - Septiembre':
        periodo_fiserv = f"4/{año2c} "
        vto_fiserv = f"3009{año2c}"
    elif periodo_actual == 'Septiembre - Octubre':
        periodo_fiserv = f"5/{año2c} "
        vto_fiserv = f"3110{año2c}"
    elif periodo_actual == 'Octubre - Noviembre':
        periodo_fiserv = f"5/{año2c} "
        vto_fiserv = f"3011{año2c}"
    elif periodo_actual == 'Noviembre - Diciembre':
        periodo_fiserv = f"6/{año2c} "
        vto_fiserv = f"3112{año2c}"
    elif periodo_actual == 'Diciembre - Enero':
        periodo_fiserv = f"6/{año2c} "
        vto_fiserv = f"3101{año_sig_2c}"

    ########### FIN DE VARIABLES DEPENDIENTES ############
    

    ############ INICIO DE REPORT ############
    class PDF(FPDF):
        # Page header
        def header(self):
            # Logo
            self.image('../docs/logo_bicon.jpg', 14.5, 12, 15)
            # Arial bold 15
            self.set_font('Arial', 'B', 15)
            # Title
            self.cell(0, 20, 'LISTADO DE RECIBOS EMITIDOS', 1, 0, 'C')
            # Arial 10
            self.set_font('Arial', '', 10)
            # Fecha
            self.cell(0, 35, f'{fecha} - {hora} hs', 0, 0, 'R')
            # N° de cierre
            self.set_font('Arial', 'B', 10)
            self.cell(-77, 35, f'Cobrador: {nco}', 0, 0, 'R')
            # Line break
            self.ln(22)
            self.cell(14, 5, 'Socio/a', 0, 0, 'L ')
            self.cell(98, 5, 'Apellido y Nombre', 0, 0, 'L')
            pdf.cell(1, 5, '', 0, 0, 'L')
            pdf.cell(16, 5, ' Recibo', 0, 0, 'L')
            pdf.cell(1, 5, '', 0, 0, 'L')
            self.cell(37, 5, '       Nro. Tarjeta', 0, 0, 'L')
            pdf.cell(22, 5, 'Importe', 0, 1, 'R')
            self.cell(0, 1, '_________________________________________________________________________________________________', 0, 1, 'C')
            self.ln(3)
            
        # Page footer
        def footer(self):
            # Position at 3 cm from bottom
            self.set_y(-30)
            # Arial italic 8
            self.set_font('Arial', 'I', 8)
            self.cell(0, 5, '* El asociado adeuda cuotas', 0, 1, 'L')
            self.cell(0, 1, '_______________________________________________________________________________________________', 0, 1, 'C')
            # Page number
            self.cell(0, 10, 'Página ' + str(self.page_no()) + ' de {nb}', 0, 0, 'C')
            # Firma
            self.set_font('Arial', 'I', 8)
            self.cell(-10, 10, f'Reporte generado en *MORELLA v{mant.SHORT_VERSION}* by ', 0, 0, 'R')
            self.image('../docs/mf_logo.jpg', 190, 274, 8)

    # Instantiation of inherited class
    pdf = PDF()
    pdf.set_auto_page_break(True, 30)
    pdf.alias_nb_pages()
    pdf.add_page()
    for rec in recibos:
        # Variables individuales
        id_o, soc, nic, fac, cob, tar, rut, ult, u_a, fup, mor, c_f, u_r, paga, op_cob, nom_alt, dom_alt = rec
        try:
            cod, pan, pis, fil, num, cat, ocu, fall = rend.obtener_datos_nicho(nic)
        except UnboundLocalError:
            continue
        nro, nom, dni, te_1, te_2, mail, dom, loc, c_p, f_n, f_a, act = rend.obtener_datos_socio(soc)
        t01, t02, t03, t04 = rend.split_nro_tarjeta(tar)
        id_c, cat, val_mant_bic, val_mant_nob = rend.obtener_categoria(cat)
        ult_rec = str(rend.obtener_ult_rec_de_op(id_o)).rjust(7, '0')
        val_mant = 0
        if nom_alt != None:
            nom = f"[{nom_alt}]"
        if dom_alt != None:
            dom = f"[{dom_alt}]"
        if fac == 'bicon':
            val_mant = val_mant_bic
        elif fac == 'nob':
            val_mant = val_mant_nob
        if act == 1:
            if not ult == periodo_actual and u_a == año and c_f == 0 and u_r != f"{mes}-{año2c}":
                counter = counter + 1
                if ult == periodo_anterior and u_a == año:
                    pdf.set_font('Arial', '', 10)
                    pdf.cell(14, 5, f'{nro}'.rjust(6, '0'), 0, 0, 'L ')
                    pdf.cell(98,5, f'{nom}', 0, 0, 'L')
                    pdf.cell(1, 5, '', 0, 0, 'L')
                    pdf.cell(16, 5, f'{ult_rec}', 0, 0, 'L')
                    pdf.cell(1, 5, '', 0, 0, 'L')
                    pdf.cell(37, 5, f'{t01} {t02} {t03} {t04}', 0, 0, 'L')
                    pdf.cell(22, 5, f'$ {val_mant:.2f}', 0, 1, 'R')
                    imp_acu = imp_acu + float(val_mant)
                elif ult == "Diciembre - Enero" and u_a == f'{int(año)-1}':
                    pdf.set_font('Arial', '', 10)
                    pdf.cell(14, 5, f'{nro}'.rjust(6, '0'), 0, 0, 'L ')
                    pdf.cell(98,5, f'{nom}', 0, 0, 'L')
                    pdf.cell(1, 5, '', 0, 0, 'L')
                    pdf.cell(16, 5, f'{ult_rec}', 0, 0, 'L')
                    pdf.cell(1, 5, '', 0, 0, 'L')
                    pdf.cell(37, 5, f'{t01} {t02} {t03} {t04}', 0, 0, 'L')
                    pdf.cell(22, 5, f'$ {val_mant:.2f}', 0, 1, 'R')
                    imp_acu = imp_acu + float(val_mant)
                elif ult == "Noviembre - Diciembre" and u_a == f'{int(año)-1}':
                    pdf.set_font('Arial', '', 10)
                    pdf.cell(14, 5, f'{nro}'.rjust(6, '0'), 0, 0, 'L ')
                    pdf.cell(98,5, f'{nom}', 0, 0, 'L')
                    pdf.cell(1, 5, '', 0, 0, 'L')
                    pdf.cell(16, 5, f'{ult_rec}', 0, 0, 'L')
                    pdf.cell(1, 5, '', 0, 0, 'L')
                    pdf.cell(37, 5, f'{t01} {t02} {t03} {t04}', 0, 0, 'L')
                    pdf.cell(22, 5, f'$ {val_mant:.2f}', 0, 1, 'R')
                    imp_acu = imp_acu + float(val_mant)
                else:
                    pdf.set_font('Arial', '', 10)
                    pdf.cell(14, 5, f'{nro}'.rjust(6, '0'), 0, 0, 'L ')
                    pdf.cell(98,5, f'{nom} *', 0, 0, 'L')
                    pdf.cell(1, 5, '', 0, 0, 'L')
                    pdf.cell(16, 5, f'{ult_rec}', 0, 0, 'L')
                    pdf.cell(1, 5, '', 0, 0, 'L')
                    pdf.cell(37, 5, f'{t01} {t02} {t03} {t04}', 0, 0, 'L')
                    pdf.cell(22, 5, f'$ {val_mant:.2f}', 0, 1, 'R')
                    imp_acu = imp_acu + float(val_mant)
                # Evitar duplicado de recibos
                rend.evitar_duplicado(mes, año2c, id_o)
                # Inscripción en el TXT de detalle de presentación para FiServ
                if os.path.isdir('../reports/presentaciones_fiserv') == False:
                    os.mkdir('../reports/presentaciones_fiserv')
                if os.path.isdir('../reports/presentaciones_fiserv/temp') == False:
                    os.mkdir('../reports/presentaciones_fiserv/temp')
                detalle = open('../reports/presentaciones_fiserv/temp/pres_det.txt', 'a')
                detalle.write(f"\n{nro_comercio_fiserv}2{str(tar)}{str(id_o).rjust(12, '0')}00199902{str(int(val_mant)).rjust(9, '0')}00{periodo_fiserv} {vto_fiserv}{60*filler}")
                detalle.close()
                contador_fiserv = contador_fiserv + 1
                val_total = val_total + val_mant
    pdf.ln(2)
    pdf.cell(91, 5, '', 0, 0, 'L')
    pdf.cell(33, 5, 'Cantidad de recibos:', 'LTB', 0, 'L')
    pdf.cell(8, 5, f'{counter}', 'RTB', 0, 'R')
    pdf.cell(2, 5, '', 0, 0, 'L')
    pdf.cell(33, 5, 'Importe acumulado:', 'LTB', 0, 'L')
    pdf.cell(23, 5, f'$ {imp_acu:.2f}', 'RTB', 0, 'R')
    # Generando TXT de presentación para FiServ
    if os.path.isfile(f'../reports/presentaciones_fiserv/presentacion_{año}-{mes}-{dia}.txt') == True:
        print()
        print("ATENCIÓN!")
        print()
        print(f"Ya existe un archivo de presentación con el nombre 'presentacion_{año}-{mes}-{dia}.txt'. Si continúa, éste será eliminado.")
        print("Por favor asegúrese de guardar la infomación que necesite.")
        print()
        input("Para continuar presione enter (Esta acción no puede deshacerse)")
        os.remove(f'../reports/presentaciones_fiserv/presentacion_{año}-{mes}-{dia}.txt')
    presentacion = open(f'../reports/presentaciones_fiserv/presentacion_{año}-{mes}-{dia}.txt', 'a')
    presentacion.write(f"{nro_comercio_fiserv}1{dia}{mes}{año2c}{str(contador_fiserv).rjust(7, '0')}0{str(int(val_total)).rjust(12, '0')}00{91*filler}")
    presentacion.close()
    try:
        detalle = open('../reports/presentaciones_fiserv/temp/pres_det.txt', 'r')
        lista = detalle.readlines()
        detalle.close()
        for linea in lista:
            presentacion = open(f'../reports/presentaciones_fiserv/presentacion_{año}-{mes}-{dia}.txt', 'a')
            presentacion.write(linea)
            presentacion.close()
    except FileNotFoundError:
        print("         ERROR. No se encontraron recibos.")
    except:
        mant.log_error()
        print("")
        input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
        print()
        return
    try:
        if not os.path.isdir(f'../reports/recibos/{nco}'):
            os.mkdir(f'../reports/recibos/{nco}')
        if not os.path.isfile(f'../reports/recibos/{nco}/listado_recibos_{año}-{mes}-{dia}.pdf'):
            pdf.output(f'../reports/recibos/{nco}/listado_recibos_{año}-{mes}-{dia}.pdf', 'F')
        else:
            print("ATENCIÓN!")
            print("Está a punto de sobreescribir un archivo existente. Antes de continuar asegurese de hacer copia de toda la información que sea útil.")
            input("Para continuar con la sobreescritura presiones enter. Tenga en cuenta que esta acción no puede deshacerse. ")
            pdf.output(f'../reports/recibos/{nco}/listado_recibos_{año}-{mes}-{dia}.pdf', 'F')
        
    ############ ABRIR REPORT ############

        if errores:
            print('\n\n\n\n')
            print('     ATENCIÓN! Durante la emisión del listado se produjeron los siguientes errores:')
            print()
            pprint(errores)
            print('\n\n\n\n')

        print("Abriendo reporte. Cierre el archivo para continuar...")
        ruta = f'../reports/recibos/{nco}/'
        arch = f'listado_recibos_{año}-{mes}-{dia}.pdf'
        os.chdir(ruta)
        os.system(arch)
        ruta = '../../../modulos/'
        os.chdir(ruta)
    except UnboundLocalError:
        print("")
        print("No se encontraron recibos impagos.")
        print("")
    except:
        mant.log_error()
        print("")
        input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
        print()
        return
         
            ######################################## FIN DE REPORT ############################################





    #################################################################################################################
    ############################################ RECIBOS  DE DOCUMENTOS #############################################    
    #################################################################################################################

def recibos_documentos():
    ############ INICIO DE VARIABLES INDEPENDIENTES ############

    cobradores = vent.obtener_cobradores()
    dia = datetime.now().strftime('%d')
    mes = datetime.now().strftime('%m')
    str_mes_sig, int_mes_sig = rend.obtener_mes_siguiente(mes)
    año = datetime.now().strftime('%Y')
    año2c = datetime.now().strftime('%y')
    lista_recibos = []
    errores = {}

    ############ FIN DE VARIABLES INDEPENDIENTES ############

        
    ############ INICIO DE FUNCIONES ############
    def days_between(d1, d2):
        return abs(d2-d1).days

    def buscar_documentos():
        conn = sql.connect(mant.DATABASE)
        cursor = conn.cursor()
        instruccion = f"SELECT * FROM documentos ORDER BY id_op"
        cursor.execute(instruccion)
        documentos = cursor.fetchall()
        conn.commit()
        conn.close()
        return documentos

    def obtener_añovar(mes, año):
        añovar = int(año)
        if mes == '12':
            añovar += 1
        return añovar

    ############ FIN DE FUNCIONES ############


    ############ INICIO DE VARIABLES DEPENDIENTES ############

    ########### FIN DE VARIABLES DEPENDIENTES ############
    
    año_var = obtener_añovar(mes, año)

    ############ INICIO DE REPORT ############


    pdf = FPDF()
    pdf.set_margins(10, 0, 10)
    pdf.set_auto_page_break(True, 0)
    pdf.alias_nb_pages()
    pdf.add_page()
    for i, cobrador in enumerate(cobradores):
        counter = 0
        print(f"{i+1}/{len(cobradores)}: ")
        id_cob, nom_cob = cobrador
        documentos = buscar_documentos()
        if len(documentos) == 0:
            mant.barra_progreso(counter, len(documentos), titulo=f'Morella v{mant.VERSION} - MF! Soluciones informáticas - {i+1}/{len(cobradores)}')
        for documento in documentos:
            id_op, cant_cuotas, val_cuotas, ult_rec = documento
            if cant_cuotas > 0 and ult_rec != f'{int_mes_sig}-{año2c}':
                id_o, soc, nic, fac, cob, tar, rut, ult, u_a, fup, mor, c_f, u_r, paga, op_cob, nom_alt, dom_alt = ctas.buscar_op_nro_operacion(id_op, 1)
                if cob == id_cob:
                    # Variables individuales
                    try:
                        cod, pan, pis, fil, num, cat, ocu, fall = rend.obtener_datos_nicho(nic)
                    except UnboundLocalError:
                        if 'Operaciones sin nicho' not in errores:
                            errores['Operaciones sin nicho'] = [str(id_o).rjust(7, '0')]
                        else:
                            errores['Operaciones sin nicho'].append(str(id_o).rjust(7, '0'))
                        continue
                    nro, nom, dni, te_1, te_2, mail, dom, loc, c_p, f_n, f_a, act = rend.obtener_datos_socio(soc)
                    id_c, cat, val_mant_bic, val_mant_nob = rend.obtener_categoria(cat)
                    pant = rend.obtener_panteon(pan)
                    nco = rend.obtener_nom_cobrador(cob)
                    fup_sep = str(fup).split("/")
                    fup_date = date(year = int(fup_sep[1]), month = int(fup_sep[0]), day = 1)
                    hoy = datetime.now().date()
                    cuenta = int(days_between(hoy, fup_date)/365)
                    if nom_alt != None:
                        nom = f"[{nom_alt}]"
                    if dom_alt != None:
                        dom = f"[{dom_alt}]"
                    parameters = str((id_o, f'Doc: {str_mes_sig}', str(año_var), 0))
                    query = f"INSERT INTO recibos (operacion, periodo, año, pago) VALUES {parameters}"
                    rend.run_query(query)
                    ndr = rend.obtener_nro_recibo()
                    lista_recibos.append(ndr)
                    # Header                                                   <----- HAY QUE PENSAR COMO PONER LA IMG DE ÑUL Y SEPARARLOS   
                    #                                                           (asegurarse que el header de bicon comentado coincida con éste)
                    # Línea 1
                    pdf.set_font('Arial', 'I', 7)
                    pdf.cell(190, 3.1, '', 0, 1, 'L')
                    pdf.cell(71, 3, '', 0, 0, 'L')
                    pdf.cell(25, 3, 'Talón para control', 0, 0, 'L')
                    pdf.cell(61, 3, '', 0, 0, 'L')
                    pdf.cell(31, 3, 'Talón para el contribuyente', 0, 1, 'L')
                    pdf.ln(1)
                    # Línea 2
                    pdf.set_font('Arial', 'B', 8)
                    pdf.cell(7, 3, '', 0, 0, 'L')
                    pdf.cell(87, 3, 'ADMINISTRACIÓN de PANTEONES SOCIALES', 0, 0, 'L')
                    pdf.cell(7, 3, '', 0, 0, 'L')
                    pdf.cell(87, 3, 'ADMINISTRACIÓN de PANTEONES SOCIALES', 0, 1, 'L')
                    # Línea 3
                    pdf.cell(22, 3, '', 0, 0, 'L')
                    pdf.cell(76, 3, 'Tel.: 430 9999 / 430 8800', 0, 0, 'L')
                    pdf.cell(18, 3, '', 0, 0, 'L')
                    pdf.cell(76, 3, 'Tel.: 430 9999 / 430 8800', 0, 1, 'L')
                    # Línea 4
                    pdf.cell(19, 3, '', 0, 0, 'L')
                    pdf.cell(45, 3, 'CORDOBA 2915 - ROSARIO', 0, 0, 'L')
                    pdf.cell(17, 3, 'Recibo nro.', 'LTB', 0, 'L')
                    pdf.cell(12, 3, f'{ndr}'.rjust(7, '0'), 'RTB', 0, 'R')
                    pdf.cell(20, 3, '', 0, 0, 'L')
                    pdf.cell(48, 3, 'CORDOBA 2915 - ROSARIO', 0, 0, 'L')
                    pdf.cell(17, 3, 'Recibo nro.', 'LTB', 0, 'L')
                    pdf.cell(12, 3, f'{ndr}'.rjust(7, '0'), 'RTB', 1, 'R')
                    pdf.ln(1)

                    if fac == 'bicon': #                                                <----- HEADER DE BICON
                    #     # Línea 1
                    #     pdf.set_font('Arial', 'I', 7)
                    #     pdf.cell(190, 3.1, '', 0, 1, 'L')
                    #     pdf.cell(71, 3, '', 0, 0, 'L')
                    #     pdf.cell(25, 3, 'Talón para control', 0, 0, 'L')
                    #     pdf.cell(61, 3, '', 0, 0, 'L')
                    #     pdf.cell(31, 3, 'Talón para el contribuyente', 0, 1, 'L')
                    #     pdf.ln(1)
                    #     # Línea 2
                    #     pdf.set_font('Arial', 'B', 8)
                    #     pdf.cell(7, 3, '', 0, 0, 'L')
                    #     pdf.cell(87, 3, 'ADMINISTRACIÓN de PANTEONES SOCIALES', 0, 0, 'L')
                    #     pdf.cell(7, 3, '', 0, 0, 'L')
                    #     pdf.cell(87, 3, 'ADMINISTRACIÓN de PANTEONES SOCIALES', 0, 1, 'L')
                    #     # Línea 3
                    #     pdf.cell(22, 3, '', 0, 0, 'L')
                    #     pdf.cell(76, 3, 'Tel.: 430 9999 / 430 8800', 0, 0, 'L')
                    #     pdf.cell(18, 3, '', 0, 0, 'L')
                    #     pdf.cell(76, 3, 'Tel.: 430 9999 / 430 8800', 0, 1, 'L')
                    #     # Línea 4
                    #     pdf.cell(19, 3, '', 0, 0, 'L')
                    #     pdf.cell(45, 3, 'CORDOBA 2915 - ROSARIO', 0, 0, 'L')
                    #     pdf.cell(17, 3, 'Recibo nro.', 'LTB', 0, 'L')
                    #     pdf.cell(12, 3, f'{ndr}'.rjust(7, '0'), 'RTB', 0, 'R')
                    #     pdf.cell(20, 3, '', 0, 0, 'L')
                    #     pdf.cell(48, 3, 'CORDOBA 2915 - ROSARIO', 0, 0, 'L')
                    #     pdf.cell(17, 3, 'Recibo nro.', 'LTB', 0, 'L')
                    #     pdf.cell(12, 3, f'{ndr}'.rjust(7, '0'), 'RTB', 1, 'R')
                    #     pdf.ln(1)
                        borrar = 'Esta variable es para poder contraer el if'
                    elif fac == 'nob': #                                                <----- HEADER DE NOB
                    #     # Logo
                    #     pdf.image('../docs/logo_nob.jpg', 11, 4, 10)
                    #     pdf.image('../docs/logo_nob.jpg', 108, 4, 10)
                    #     pdf.set_font('Arial', 'I', 7)
                    #     pdf.cell(190, 3.1, '', 0, 1, 'L')
                    #     pdf.ln(1)
                    #     # Línea 1
                    #     pdf.set_font('Arial', 'B', 8)
                    #     pdf.cell(12, 3, '', 0, 0, 'L')
                    #     pdf.cell(60, 3, "Club Atlético Newell's Old Boys", 0, 0, 'L')
                    #     pdf.set_font('Arial', 'I', 7)
                    #     pdf.cell(14, 3, 'Talón para control', 0, 0, 'L')
                    #     pdf.set_font('Arial', 'B', 8)
                    #     pdf.cell(24, 3, '', 0, 0, 'L')
                    #     pdf.cell(49, 3, "Club Atlético Newell's Old Boys", 0, 0, 'L')
                    #     pdf.set_font('Arial', 'I', 7)
                    #     pdf.cell(14, 3, 'Talón para el contribuyente', 0, 1, 'L')
                    #     # Línea 2
                    #     pdf.set_font('Arial', 'B', 6)
                    #     pdf.cell(12, 3, '', 0, 0, 'L')
                    #     pdf.cell(16, 3, 'Panteón Social', 0, 0, 'L')
                    #     pdf.set_font('Arial', 'I', 6)
                    #     pdf.cell(48, 3, '(Cementerio "El Salvador")', 0, 0, 'L')
                    #     pdf.cell(15, 3, '', 0, 0, 'L')
                    #     pdf.set_font('Arial', 'B', 6)
                    #     pdf.cell(19, 3, '', 0, 0, 'L')
                    #     pdf.cell(16, 3, 'Panteón Social', 0, 0, 'L')
                    #     pdf.set_font('Arial', 'I', 6)
                    #     pdf.cell(47, 3, '(Cementerio "El Salvador")', 0, 0, 'L')
                    #     pdf.cell(15, 3, '', 0, 1, 'L')
                    #     # Línea 3
                    #     pdf.set_font('Arial', 'B', 6)
                    #     pdf.cell(12, 3, '', 0, 0, 'L')
                    #     pdf.cell(60, 3, 'ADMINISTRACIÓN PANTEÓN SOCIAL', 0, 0, 'L')
                    #     pdf.cell(38, 3, '', 0, 0, 'L')
                    #     pdf.cell(49, 3, 'ADMINISTRACIÓN PANTEÓN SOCIAL', 0, 1, 'L')
                    #     # Línea 4
                    #     pdf.set_font('Arial', '', 6)
                    #     pdf.cell(12, 3, '', 0, 0, 'L')
                    #     pdf.cell(52, 3, 'Córdoba 2915 - Tel. 430 9999 / 8800', 0, 0, 'L')
                    #     pdf.set_font('Arial', 'B', 8)
                    #     pdf.cell(17, 3, 'Recibo nro.', 'LTB', 0, 'L')
                    #     pdf.cell(12, 3, f'{ndr}'.rjust(7, '0'), 'RTB', 0, 'R')
                    #     pdf.set_font('Arial', '', 6)
                    #     pdf.cell(17, 3, '', 0, 0, 'L')
                    #     pdf.cell(51, 3, 'Córdoba 2915 - Tel. 430 9999 / 8800', 0, 0, 'L')
                    #     pdf.set_font('Arial', 'B', 8)
                    #     pdf.set_font('Arial', 'B', 8)
                    #     pdf.cell(17, 3, 'Recibo nro.', 'LTB', 0, 'L')
                    #     pdf.cell(12, 3, f'{ndr}'.rjust(7, '0'), 'RTB', 1, 'R')
                    #     pdf.ln(1)
                        borrar = 'Esta variable es para poder contraer el if'

                    # Línea 1
                    pdf.set_font('Arial', 'B', 9)
                    pdf.cell(13, 4, 'Socio/a: ', 'LTB', 0, 'L')
                    pdf.set_font('Arial', '', 9)
                    pdf.cell(12, 4, f'{nro}'.rjust(6, '0'), 'TB', 0, 'L')
                    pdf.cell(68, 4, f'{nom}', 'TRB', 0, 'L')
                    pdf.cell(4, 4, '', 0, 0, 'L')
                    pdf.set_font('Arial', 'B', 9)
                    pdf.cell(13, 4, 'Socio/a: ', 'LT', 0, 'L')
                    pdf.set_font('Arial', '', 9)
                    pdf.cell(12, 4, f'{nro}'.rjust(6, '0'), 'T', 0, 'L')
                    pdf.cell(68, 4, f'{nom}', 'TR', 1, 'L')
                    # Línea 2
                    pdf.set_font('Arial', 'B', 9)
                    pdf.cell(95, 1, '', 0, 0, 'L')
                    pdf.cell(2, 1, '', 0, 0, 'L')
                    pdf.cell(93, 1, '', 'LR', 1, 'L')
                    pdf.cell(19, 5, 'Cobrador/a: ', 'LT', 0, 'L')
                    pdf.set_font('Arial', '', 9)
                    pdf.cell(5, 5, f'{cob}'.rjust(2, '0'), 'T', 0, 'L')
                    pdf.cell(69, 5, f'{nco}', 'RT', 0, 'L')
                    pdf.cell(4, 4, '', 0, 0, 'L')
                    pdf.set_font('Arial', 'B', 9)
                    pdf.cell(17, 5, 'Domicilio: ', 'L', 0, 'L')
                    pdf.set_font('Arial', '', 9)
                    pdf.cell(76, 5, f'{dom}', 'R', 1, 'L')
                    # Línea 3
                    pdf.set_font('Arial', 'B', 9)
                    pdf.cell(17, 4, 'Categoría: ', 'LB', 0, 'L')
                    pdf.set_font('Arial', '', 9)
                    pdf.cell(46, 4, f'{cat}', 'B', 0, 'L')
                    pdf.set_font('Arial', 'B', 9)
                    pdf.cell(9, 4, 'Ruta:', 'B', 0, 'L')
                    pdf.set_font('Arial', '', 9)
                    pdf.cell(21, 4, f'{rut}'.rjust(3, '0'), 'RB', 0, 'L')
                    pdf.cell(4, 4, '', 0, 0, 'L')
                    pdf.set_font('Arial', 'B', 9)
                    pdf.cell(17, 4, 'Localidad:', 'LB', 0, 'L')
                    pdf.set_font('Arial', '', 9)
                    pdf.cell(76, 4, f'{loc} - {c_p}', 'BR', 1, 'L')
                    pdf.ln(1)
                    # Línea 4
                    pdf.set_font('Arial', 'B', 9)
                    pdf.cell(19, 5, 'Cod. Nicho:', 'LTB', 0, 'L')
                    pdf.set_font('Arial', '', 9)
                    pdf.cell(44, 5, f'{cod}'.rjust(10, '0'), 'TB', 0, 'L')
                    pdf.set_font('Arial', 'B', 9)
                    pdf.cell(7, 5, f'Op:', 'TB', 0, 'L')
                    pdf.set_font('Arial', '', 9)
                    pdf.cell(23, 5, f'{id_o}'.rjust(7, "0"), 'RTB', 0, 'L')
                    pdf.cell(4, 5, '', 0, 0, 'L')
                    pdf.set_font('Arial', 'B', 9)
                    pdf.cell(16, 5, 'Cobrador:', 'LTB', 0, 'L')
                    pdf.set_font('Arial', '', 9)
                    pdf.cell(5, 5, f'{cob}'.rjust(2, '0'), 'TB', 0, 'L')
                    pdf.cell(72, 5, f'{nco}', 'RTB', 1, 'L')
                    pdf.ln(1)
                    # Línea 5
                    pdf.set_font('Arial', 'B', 9)
                    pdf.cell(44, 4, 'Panteón', 'LTR', 0, 'C')
                    pdf.cell(16, 4, 'Piso', 'LTR', 0, 'C')
                    pdf.cell(16, 4, 'Fila', 'LTR', 0, 'C')
                    pdf.cell(17, 4, 'Nicho', 'LTR', 0, 'C')
                    pdf.cell(4, 4, '', 0, 0, 'C')
                    pdf.cell(29, 4, 'Categoría', 'LTR', 0, 'C')
                    pdf.cell(34, 4, 'Panteón', 'LTR', 0, 'C')
                    pdf.cell(9, 4, 'Piso', 'LTR', 0, 'C')
                    pdf.cell(9, 4, 'Fila', 'LTR', 0, 'C')
                    pdf.cell(12, 4, 'Nicho', 'LTR', 1, 'C')
                    # Línea 6
                    pdf.set_font('Arial', '', 9)
                    pdf.cell(44, 5, f'{pant}', 'LBR', 0, 'C')
                    pdf.cell(16, 5, f'{pis}'.rjust(2, '0'), 'LBR', 0, 'C')
                    pdf.cell(16, 5, f'{fil}'.rjust(2, '0'), 'LBR', 0, 'C')
                    pdf.cell(17, 5, f'{num}'.rjust(3, '0'), 'LBR', 0, 'C')
                    pdf.cell(4, 5, '', 0, 0, 'C')
                    pdf.cell(29, 5, f'{cat}', 'LBR', 0, 'C')
                    pdf.cell(34, 5, f'{pant}', 'LBR', 0, 'C')
                    pdf.cell(9, 5, f'{pis}'.rjust(2, '0'), 'LBR', 0, 'C')
                    pdf.cell(9, 5, f'{fil}'.rjust(2, '0'), 'LBR', 0, 'C')
                    pdf.cell(12, 5, f'{num}'.rjust(3, '0'), 'LBR', 1, 'C')
                    pdf.ln(3)
                    # Línea 7
                    if mes != "12":
                        pdf.set_font('Arial', 'B', 9)
                        pdf.cell(12, 5, 'Cuota:', 'LTB', 0, 'L')
                        pdf.set_font('Arial', '', 9)
                        pdf.cell(40, 5, f'{11-int(cant_cuotas)}/10  -  {str_mes_sig} de {año}', 'RTB', 0, 'L')
                        pdf.set_font('Arial', 'B', 9)
                        pdf.cell(14, 5, 'Importe:', 'LTB', 0, 'L')
                        pdf.set_font('Arial', '', 9)
                        pdf.cell(27, 5, f'$ {val_cuotas:.2f}', 'RTB', 0, 'R')
                        pdf.cell(4, 5, '', 0, 0, 'C')
                        pdf.set_font('Arial', 'B', 9)
                        pdf.cell(12, 5, 'Cuota: ', 'LTB', 0, 'L')
                        pdf.set_font('Arial', '', 9)
                        pdf.cell(40, 5, f'{11-int(cant_cuotas)}/10  -  {str_mes_sig} de {año}', 'RTB', 0, 'L')
                        pdf.set_font('Arial', 'B', 9)
                        pdf.cell(14, 5, 'Importe:', 'LTB', 0, 'L')
                        pdf.set_font('Arial', '', 9)
                        pdf.cell(27, 5, f'$ {val_cuotas:.2f}', 'RTB', 1, 'R')
                        pdf.ln(2)
                    elif mes == "12":
                        pdf.set_font('Arial', 'B', 9)
                        pdf.cell(12, 5, 'Cuota:', 'LTB', 0, 'L')
                        pdf.set_font('Arial', '', 9)
                        pdf.cell(40, 5, f'{11-int(cant_cuotas)}/10  -  {str_mes_sig} de {int(año)+1}', 'RTB', 0, 'L')
                        pdf.set_font('Arial', 'B', 9)
                        pdf.cell(14, 5, 'Importe:', 'LTB', 0, 'L')
                        pdf.set_font('Arial', '', 9)
                        pdf.cell(27, 5, f'$ {val_cuotas:.2f}', 'RTB', 0, 'R')
                        pdf.cell(4, 5, '', 0, 0, 'C')
                        pdf.set_font('Arial', 'B', 9)
                        pdf.cell(12, 5, 'Cuota: ', 'LTB', 0, 'L')
                        pdf.set_font('Arial', '', 9)
                        pdf.cell(40, 5, f'{11-int(cant_cuotas)}/10  -  {str_mes_sig} de {int(año)+1}', 'RTB', 0, 'L')
                        pdf.set_font('Arial', 'B', 9)
                        pdf.cell(14, 5, 'Importe:', 'LTB', 0, 'L')
                        pdf.set_font('Arial', '', 9)
                        pdf.cell(27, 5, f'$ {val_cuotas:.2f}', 'RTB', 1, 'R')
                        pdf.ln(2)
                    # Margen
                    pdf.cell(190, 17, ' ', 0, 1, 'L')
            counter += 1
            mant.barra_progreso(counter, len(documentos), titulo=f'Morella v{mant.VERSION} - MF! Soluciones informáticas - {i+1}/{len(cobradores)}')
        print()
    os.system(f'TITLE Morella v{mant.VERSION} - MF! Soluciones informáticas')

    ############ GUARDAR REPORT ############
    try:
        if not os.path.isdir(f'../reports/recibos/documentos'):
            os.mkdir(f'../reports/recibos/documentos')
        output_counter = 0
        output_name = f'recibos_{año}-{mes}-{dia}.pdf'
        while os.path.isfile(f'../reports/recibos/documentos/{output_name}'):
            output_counter += 1
            output_name = f'recibos_{año}-{mes}-{dia}_({output_counter}).pdf'
        pdf.output(f'../reports/recibos/documentos/{output_name}', 'F')

        ############ ABRIR REPORT ############

        if errores:
            print('\n\n\n\n')
            print('     ATENCIÓN! Durante la emisión de los recibos se produjeron los siguientes errores:')
            print()
            pprint(errores)
            print('\n\n\n\n')

        print("Abriendo reporte. Cierre el archivo para continuar...")
        ruta = f'../reports/recibos/documentos'
        arch = output_name.replace('(', '^(')
        os.chdir(ruta)
        os.system(arch)
        ruta = '../../../modulos/'
        os.chdir(ruta)
    except UnboundLocalError:
        print("")
        print("No se encontraron recibos impagos.")
        print("")
    except:
        mant.log_error()
        print("")
        input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
        print()
        return
    return lista_recibos

            ######################################## FIN DE REPORT ############################################





    #################################################################################################################
    ######################################## LISTADO DE RECIBOS DE DOCUMENTOS #######################################
    #################################################################################################################

def listado_recibos_documentos(lista_recibos):
    ############ INICIO DE VARIABLES INDEPENDIENTES ############

    dia = datetime.now().strftime('%d')
    mes = datetime.now().strftime('%m')
    str_mes_sig, int_mes_sig = rend.obtener_mes_siguiente(mes)
    año = datetime.now().strftime('%Y')
    año2c = datetime.now().strftime('%y')
    fecha = f"{mes}/{año}"
    hora = datetime.now().strftime('%H:%M')
    imp_acu = float(0)
    counter = 0
    errores = {}

    ############ FIN DE VARIABLES INDEPENDIENTES ############

        
    ############ INICIO DE FUNCIONES ############
    def buscar_documento(id_op):
        conn = sql.connect(mant.DATABASE)
        cursor = conn.cursor()
        instruccion = f"SELECT * FROM documentos WHERE id_op = {id_op}"
        cursor.execute(instruccion)
        documento = cursor.fetchone()
        conn.commit()
        conn.close()
        return documento

    def obtener_añovar(mes, año):
            añovar = int(año)
            if mes == '12':
                añovar += 1
            return añovar


    def restar_cuota(id_op, cant_cuotas):
        with sql.connect(mant.DATABASE) as conn:
            cursor = conn.cursor()
            instruccion = f"UPDATE documentos SET cant_cuotas = '{cant_cuotas-1}' WHERE id_op = '{id_op}'"
            cursor.execute(instruccion)

    ############ FIN DE FUNCIONES ############


    ############ INICIO DE VARIABLES DEPENDIENTES ############
    año_var = obtener_añovar(mes, año2c)

    ########### FIN DE VARIABLES DEPENDIENTES ############

    ############ INICIO DE FUNCIONES DEPENDIENTES ############
    def evitar_duplicado(id_op):
        ult_rec = f'{int_mes_sig}-{año_var}'
        with sql.connect(mant.DATABASE) as conn:
            cursor = conn.cursor()
            instruccion = f"UPDATE documentos SET ult_rec = '{ult_rec}' WHERE id_op = '{id_op}'"
            cursor.execute(instruccion)

    ############ FIN DE FUNCIONES DEPENDIENTES ############


    ############ INICIO DE REPORT ############
    class PDF(FPDF):
        # Page header
        def header(self):
            # Logo
            self.image('../docs/logo_bicon.jpg', 14.5, 12, 15)
            # Arial bold 15
            self.set_font('Arial', 'B', 15)
            # Title
            self.cell(0, 20, 'LISTADO DE RECIBOS EMITIDOS', 1, 0, 'C')
            # Arial 10
            self.set_font('Arial', '', 10)
            # Fecha
            self.cell(0, 35, f'{fecha} - {hora} hs', 0, 0, 'R')
            # N° de cierre
            self.set_font('Arial', 'B', 10)
            self.cell(-77, 35, f'DE DOCUMENTOS', 0, 0, 'R')
            # Line break
            self.ln(22)
            self.cell(14, 5, 'Socio/a', 0, 0, 'L ')
            self.cell(65, 5, 'Apellido y Nombre', 0, 0, 'L')
            pdf.cell(1, 5, '', 0, 0, 'L')
            self.cell(75, 5, 'Domicilio', 0, 0, 'L')
            pdf.cell(1, 5, '', 0, 0, 'L')
            pdf.cell(4, 5, 'Cob.', 0, 0, 'C')
            pdf.cell(1, 5, '', 0, 0, 'L')
            self.cell(15, 5, 'Ruta', 0, 0, 'L')
            pdf.cell(20, 5, 'Importe', 0, 1, 'L')
            self.cell(0, 1, '_________________________________________________________________________________________________', 0, 1, 'C')
            self.ln(3)
            
        # Page footer
        def footer(self):
            # Position at 3 cm from bottom
            self.set_y(-30)
            # Arial italic 8
            self.set_font('Arial', 'I', 8)
            self.cell(0, 5, '* El asociado adeuda cuotas', 0, 1, 'L')
            self.cell(0, 1, '_______________________________________________________________________________________________', 0, 1, 'C')
            # Page number
            self.cell(0, 10, 'Página ' + str(self.page_no()) + ' de {nb}', 0, 0, 'C')
            # Firma
            self.set_font('Arial', 'I', 8)
            self.cell(-10, 10, f'Reporte generado en *MORELLA v{mant.SHORT_VERSION}* by ', 0, 0, 'R')
            self.image('../docs/mf_logo.jpg', 190, 274, 8)

    # Instantiation of inherited class
    pdf = PDF()
    pdf.set_auto_page_break(True, 30)
    pdf.alias_nb_pages()
    pdf.add_page()
    if len(lista_recibos) == 0:
        mant.barra_progreso(counter, len(lista_recibos), titulo=f'Morella v{mant.VERSION} - MF! Soluciones informáticas')
    for rec in lista_recibos:
        nro, ope, per, año, pag = rend.obtener_datos_recibo(rec)
        id_op, cant_cuotas, val_cuota, ult_rec = buscar_documento(ope)
        id_o, soc, nic, fac, cob, tar, rut, ult, u_a, fup, mor, c_f, u_r, paga, op_cob, nom_alt, dom_alt = rend.obtener_datos_op(ope)
        try:
            cod, pan, pis, fil, num, cat, ocu, fall = rend.obtener_datos_nicho(nic)
        except UnboundLocalError:
            continue
        nro, nom, dni, te_1, te_2, mail, dom, loc, c_p, f_n, f_a, act = rend.obtener_datos_socio(soc)
        panteon = rend.obtener_panteon(pan)
        val_mant = 0
        if nom_alt != None:
            nom = f"[{nom_alt}]"
        if dom_alt != None:
            dom = f"[{dom_alt}]"
        pdf.set_font('Arial', '', 10)
        pdf.cell(14, 5, f'{nro}'.rjust(6, '0'), 0, 0, 'L ')
        pdf.cell(65,5, f'{nom}', 0, 0, 'L')
        pdf.cell(1, 5, '', 0, 0, 'L')
        pdf.cell(74, 5, f'{dom}', 0, 0, 'L')
        pdf.cell(1, 5, '', 0, 0, 'L')
        pdf.cell(4, 5, f'{cob}'.rjust(2, '0'), 0, 0, 'L')
        pdf.cell(1, 5, '', 0, 0, 'L')
        pdf.cell(10, 5, f'{rut}'.rjust(3, '0'), 0, 0, 'L')
        pdf.cell(20, 5, f'{val_cuota:.2f}', 0, 1, 'R')
        imp_acu = imp_acu + float(val_cuota)
        # Restando cuotas restantes
        restar_cuota(id_op, int(cant_cuotas))
        # Evitar duplicado de recibos
        evitar_duplicado(id_op)
        counter += 1
        mant.barra_progreso(counter, len(lista_recibos), titulo=f'Morella v{mant.VERSION} - MF! Soluciones informáticas')
    print()
    os.system(f'TITLE Morella v{mant.VERSION} - MF! Soluciones informáticas')
    pdf.ln(2)
    pdf.cell(91, 5, '', 0, 0, 'L')
    pdf.cell(33, 5, 'Cantidad de recibos:', 'LTB', 0, 'L')
    pdf.cell(8, 5, f'{len(lista_recibos)}', 'RTB', 0, 'R')
    pdf.cell(2, 5, '', 0, 0, 'L')
    pdf.cell(33, 5, 'Importe acumulado:', 'LTB', 0, 'L')
    pdf.cell(23, 5, f'$ {imp_acu:.2f}', 'RTB', 0, 'R')
    try:
        if not os.path.isdir(f'../reports/recibos/documentos'):
            os.mkdir(f'../reports/recibos/documentos')
        output_counter = 0
        output_name = f'listado_recibos_{año}-{mes}-{dia}.pdf'
        while os.path.isfile(f'../reports/recibos/documentos/{output_name}'):
            output_counter += 1
            output_name = f'listado_recibos_{año}-{mes}-{dia}_({output_counter}).pdf'
        pdf.output(f'../reports/recibos/documentos/{output_name}', 'F')

    ############ ABRIR REPORT ############

        if errores:
            print('\n\n\n\n')
            print('     ATENCIÓN! Durante la emisión del listado se produjeron los siguientes errores:')
            print()
            pprint(errores)
            print('\n\n\n\n')

        print("Abriendo reporte. Cierre el archivo para continuar...")
        ruta = f'../reports/recibos/documentos/'
        arch = output_name.replace('(', '^(')
        os.chdir(ruta)
        os.system(arch)
        ruta = '../../../modulos/'
        os.chdir(ruta)
    except UnboundLocalError:
        print("")
        print("No se encontraron recibos impagos.")
        print("")
    except:
        mant.log_error()
        print("")
        input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
        print()
        return
          
            ######################################## FIN DE REPORT ############################################




    #################################################################################################################
    ############################################# REIMPRESIÓN DE RECIBO #############################################
    #################################################################################################################

def reimpresion_recibo(ndr):
    ############ INICIO DE VARIABLES INDEPENDIENTES ############
    ndr, ope, per, año, pag = rend.obtener_datos_recibo(ndr)
    id_o, soc, nic, fac, cob, tar, rut, ult, u_a, fup, mor, c_f, u_r, paga, op_cob, nom_alt, dom_alt = rend.obtener_datos_op(ope)
    try:
        cod, pan, pis, fil, num, cat, ocu, fall = rend.obtener_datos_nicho(nic)
    except UnboundLocalError:
        print("")
        print("         ERROR. La operación no tiene nicho asociado.")
        print("")
        return
    nro, nom, dni, te_1, te_2, mail, dom, loc, c_p, f_n, f_a, act = rend.obtener_datos_socio(soc)
    id_c, cat, val_mant_bic, val_mant_nob = rend.obtener_categoria(cat)
    pant = rend.obtener_panteon(pan)
    nco = rend.obtener_nom_cobrador(cob)
    errores = {}
    if nom_alt != None:
        nom = f"[{nom_alt}]"
    if dom_alt != None:
        dom = f"[{dom_alt}]"
    if fac == 'bicon':
        val = val_mant_bic
    elif fac == 'nob':
        val = val_mant_nob
    if per[0:3] == 'Doc':
        val = rend.obtener_valor_doc(ope)
    
    ############ FIN DE VARIABLES INDEPENDIENTES ############

        
    ############ INICIO DE FUNCIONES ############

    ############ FIN DE FUNCIONES ############


    ############ INICIO DE VARIABLES DEPENDIENTES ############

    ########### FIN DE VARIABLES DEPENDIENTES ############
    

    ############ INICIO DE REPORT ############
    pdf = FPDF()
    pdf.set_margins(10, 0, 10)
    pdf.set_auto_page_break(True, 0)
    pdf.alias_nb_pages()
    pdf.add_page()
    # Header
    if fac == 'bicon':
        # Línea 1   
        pdf.set_font('Arial', 'I', 7)
        pdf.cell(190, 3.1, '', 0, 1, 'L')
        pdf.cell(52, 3, '', 0, 0, 'L')
        pdf.cell(40, 3, 'Talón para control (REIMPRESIÓN)', 0, 0, 'L')
        pdf.cell(47, 3, '', 0, 0, 'L')
        pdf.cell(46, 3, 'Talón para el contribuyente (REIMPRESIÓN)', 0, 1, 'L')
        pdf.ln(1)
        # Línea 2
        pdf.set_font('Arial', 'B', 8)
        pdf.cell(7, 3, '', 0, 0, 'L')
        pdf.cell(87, 3, 'ADMINISTRACIÓN de PANTEONES SOCIALES', 0, 0, 'L')
        pdf.cell(7, 3, '', 0, 0, 'L')
        pdf.cell(87, 3, 'ADMINISTRACIÓN de PANTEONES SOCIALES', 0, 1, 'L')
        # Línea 3
        pdf.cell(22, 3, '', 0, 0, 'L')
        pdf.cell(76, 3, 'Tel.: 430 9999 / 430 8800', 0, 0, 'L')
        pdf.cell(18, 3, '', 0, 0, 'L')
        pdf.cell(76, 3, 'Tel.: 430 9999 / 430 8800', 0, 1, 'L')
        # Línea 4
        pdf.cell(19, 3, '', 0, 0, 'L')
        pdf.cell(45, 3, 'CORDOBA 2915 - ROSARIO', 0, 0, 'L')
        pdf.cell(17, 3, 'Recibo nro.', 'LTB', 0, 'L')
        pdf.cell(12, 3, f'{ndr}'.rjust(7, '0'), 'RTB', 0, 'R')
        pdf.cell(13, 3, '', 0, 0, 'L')
        pdf.cell(55, 3, 'CORDOBA 2915 - ROSARIO', 0, 0, 'L')
        pdf.cell(17, 3, 'Recibo nro.', 'LTB', 0, 'L')
        pdf.cell(12, 3, f'{ndr}'.rjust(7, '0'), 'RTB', 1, 'R')
        pdf.ln(1)
    elif fac == 'nob':
        # Logo
        pdf.image('../docs/logo_nob.jpg', 11, 4, 10)
        pdf.image('../docs/logo_nob.jpg', 108, 4, 10)
        pdf.set_font('Arial', 'I', 7)
        pdf.cell(190, 3.1, '', 0, 1, 'L')
        pdf.ln(1)
        # Línea 1
        pdf.set_font('Arial', 'B', 8)
        pdf.cell(12, 3, '', 0, 0, 'L')
        pdf.cell(60, 3, "Club Atlético Newell's Old Boys", 0, 0, 'L')
        pdf.set_font('Arial', 'I', 7)
        pdf.cell(14, 3, 'Talón para control', 0, 0, 'L')
        pdf.set_font('Arial', 'B', 8)
        pdf.cell(24, 3, '', 0, 0, 'L')
        pdf.cell(49, 3, "Club Atlético Newell's Old Boys", 0, 0, 'L')
        pdf.set_font('Arial', 'I', 7)
        pdf.cell(14, 3, 'Talón para el contribuyente', 0, 1, 'L')
        # Línea 2
        pdf.set_font('Arial', 'B', 6)
        pdf.cell(12, 3, '', 0, 0, 'L')
        pdf.cell(16, 3, 'Panteón Social', 0, 0, 'L')
        pdf.set_font('Arial', 'I', 6)
        pdf.cell(48, 3, '(Cementerio "El Salvador")', 0, 0, 'L')
        pdf.cell(15, 3, '(REIMPRESIÓN)', 0, 0, 'L')
        pdf.set_font('Arial', 'B', 6)
        pdf.cell(19, 3, '', 0, 0, 'L')
        pdf.cell(16, 3, 'Panteón Social', 0, 0, 'L')
        pdf.set_font('Arial', 'I', 6)
        pdf.cell(47, 3, '(Cementerio "El Salvador")', 0, 0, 'L')
        pdf.cell(15, 3, '(REIMPRESIÓN)', 0, 1, 'L')
        # Línea 3
        pdf.set_font('Arial', 'B', 6)
        pdf.cell(12, 3, '', 0, 0, 'L')
        pdf.cell(60, 3, 'ADMINISTRACIÓN PANTEÓN SOCIAL', 0, 0, 'L')
        pdf.cell(38, 3, '', 0, 0, 'L')
        pdf.cell(49, 3, 'ADMINISTRACIÓN PANTEÓN SOCIAL', 0, 1, 'L')
        # Línea 4
        pdf.set_font('Arial', '', 6)
        pdf.cell(12, 3, '', 0, 0, 'L')
        pdf.cell(52, 3, 'Córdoba 2915 - Tel. 430 9999 / 8800', 0, 0, 'L')
        pdf.set_font('Arial', 'B', 8)
        pdf.cell(17, 3, 'Recibo nro.', 'LTB', 0, 'L')
        pdf.cell(12, 3, f'{ndr}'.rjust(7, '0'), 'RTB', 0, 'R')
        pdf.set_font('Arial', '', 6)
        pdf.cell(17, 3, '', 0, 0, 'L')
        pdf.cell(51, 3, 'Córdoba 2915 - Tel. 430 9999 / 8800', 0, 0, 'L')
        pdf.set_font('Arial', 'B', 8)
        pdf.set_font('Arial', 'B', 8)
        pdf.cell(17, 3, 'Recibo nro.', 'LTB', 0, 'L')
        pdf.cell(12, 3, f'{ndr}'.rjust(7, '0'), 'RTB', 1, 'R')
        pdf.ln(1)
    # Línea 1
    pdf.set_font('Arial', 'B', 9)
    pdf.cell(13, 4, 'Socio/a: ', 'LTB', 0, 'L')
    pdf.set_font('Arial', '', 9)
    pdf.cell(12, 4, f'{nro}'.rjust(6, '0'), 'TB', 0, 'L')
    pdf.cell(68, 4, f'{nom}', 'TRB', 0, 'L')
    pdf.cell(4, 4, '', 0, 0, 'L')
    pdf.set_font('Arial', 'B', 9)
    pdf.cell(13, 4, 'Socio/a: ', 'LT', 0, 'L')
    pdf.set_font('Arial', '', 9)
    pdf.cell(12, 4, f'{nro}'.rjust(6, '0'), 'T', 0, 'L')
    pdf.cell(68, 4, f'{nom}', 'TR', 1, 'L')
    # Línea 2
    pdf.set_font('Arial', 'B', 9)
    pdf.cell(95, 1, '', 0, 0, 'L')
    pdf.cell(2, 1, '', 0, 0, 'L')
    pdf.cell(93, 1, '', 'LR', 1, 'L')
    pdf.cell(19, 5, 'Cobrador/a: ', 'LT', 0, 'L')
    pdf.set_font('Arial', '', 9)
    pdf.cell(5, 5, f'{cob}'.rjust(2, '0'), 'T', 0, 'L')
    pdf.cell(69, 5, f'{nco}', 'RT', 0, 'L')
    pdf.cell(4, 4, '', 0, 0, 'L')
    pdf.set_font('Arial', 'B', 9)
    pdf.cell(17, 5, 'Domicilio: ', 'L', 0, 'L')
    pdf.set_font('Arial', '', 9)
    pdf.cell(76, 5, f'{dom}', 'R', 1, 'L')
    # Línea 3
    pdf.set_font('Arial', 'B', 9)
    pdf.cell(17, 4, 'Categoría: ', 'LB', 0, 'L')
    pdf.set_font('Arial', '', 9)
    pdf.cell(46, 4, f'{cat}', 'B', 0, 'L')
    pdf.set_font('Arial', 'B', 9)
    pdf.cell(9, 4, 'Ruta:', 'B', 0, 'L')
    pdf.set_font('Arial', '', 9)
    pdf.cell(21, 4, f'{rut}'.rjust(3, '0'), 'RB', 0, 'L')
    pdf.cell(4, 4, '', 0, 0, 'L')
    pdf.set_font('Arial', 'B', 9)
    pdf.cell(17, 4, 'Localidad:', 'LB', 0, 'L')
    pdf.set_font('Arial', '', 9)
    pdf.cell(76, 4, f'{loc} - {c_p}', 'BR', 1, 'L')
    pdf.ln(1)
    # Línea 4
    pdf.set_font('Arial', 'B', 9)
    pdf.cell(19, 5, 'Cod. Nicho:', 'LTB', 0, 'L')
    pdf.set_font('Arial', '', 9)
    pdf.cell(44, 5, f'{cod}'.rjust(10, '0'), 'TB', 0, 'L')
    pdf.set_font('Arial', 'B', 9)
    pdf.cell(7, 5, f'Op:', 'TB', 0, 'L')
    pdf.set_font('Arial', '', 9)
    pdf.cell(23, 5, f'{id_o}'.rjust(7, "0"), 'RTB', 0, 'L')
    pdf.cell(4, 5, '', 0, 0, 'L')
    pdf.set_font('Arial', 'B', 9)
    pdf.cell(16, 5, 'Cobrador:', 'LTB', 0, 'L')
    pdf.set_font('Arial', '', 9)
    pdf.cell(5, 5, f'{cob}'.rjust(2, '0'), 'TB', 0, 'L')
    pdf.cell(72, 5, f'{nco}', 'RTB', 1, 'L')
    pdf.ln(1)
    # Línea 5
    pdf.set_font('Arial', 'B', 9)
    pdf.cell(44, 4, 'Panteón', 'LTR', 0, 'C')
    pdf.cell(16, 4, 'Piso', 'LTR', 0, 'C')
    pdf.cell(16, 4, 'Fila', 'LTR', 0, 'C')
    pdf.cell(17, 4, 'Nicho', 'LTR', 0, 'C')
    pdf.cell(4, 4, '', 0, 0, 'C')
    pdf.cell(29, 4, 'Categoría', 'LTR', 0, 'C')
    pdf.cell(34, 4, 'Panteón', 'LTR', 0, 'C')
    pdf.cell(9, 4, 'Piso', 'LTR', 0, 'C')
    pdf.cell(9, 4, 'Fila', 'LTR', 0, 'C')
    pdf.cell(12, 4, 'Nicho', 'LTR', 1, 'C')
    # Línea 6
    pdf.set_font('Arial', '', 9)
    pdf.cell(44, 5, f'{pant}', 'LBR', 0, 'C')
    pdf.cell(16, 5, f'{pis}'.rjust(2, '0'), 'LBR', 0, 'C')
    pdf.cell(16, 5, f'{fil}'.rjust(2, '0'), 'LBR', 0, 'C')
    pdf.cell(17, 5, f'{num}'.rjust(3, '0'), 'LBR', 0, 'C')
    pdf.cell(4, 5, '', 0, 0, 'C')
    pdf.cell(29, 5, f'{cat}', 'LBR', 0, 'C')
    pdf.cell(34, 5, f'{pant}', 'LBR', 0, 'C')
    pdf.cell(9, 5, f'{pis}'.rjust(2, '0'), 'LBR', 0, 'C')
    pdf.cell(9, 5, f'{fil}'.rjust(2, '0'), 'LBR', 0, 'C')
    pdf.cell(12, 5, f'{num}'.rjust(3, '0'), 'LBR', 1, 'C')
    pdf.ln(3)
    # Línea 7
    pdf.set_font('Arial', 'B', 9)
    pdf.cell(14, 5, 'Período: ', 'LTB', 0, 'L')
    pdf.set_font('Arial', '', 9)
    if per == 'Diciembre - Enero':
        pdf.cell(44, 5, f'{per} - {año}/{int(str(año)[-2:])+1}', 'RTB', 0, 'L')
    else:
        pdf.cell(44, 5, f'{per} - {año}', 'RTB', 0, 'L')
    pdf.set_font('Arial', 'B', 9)
    pdf.cell(14, 5, 'Importe:', 'LTB', 0, 'L')
    pdf.set_font('Arial', '', 9)
    pdf.cell(21, 5, f'$ {val:.2f}', 'RTB', 0, 'R')
    pdf.cell(4, 5, '', 0, 0, 'C')
    pdf.set_font('Arial', 'B', 9)
    pdf.cell(14, 5, 'Período: ', 'LTB', 0, 'L')
    pdf.set_font('Arial', '', 9)
    if per == 'Diciembre - Enero':
        pdf.cell(44, 5, f'{per} - {año}/{int(str(año)[-2:])+1}', 'RTB', 0, 'L')
    else:
        pdf.cell(44, 5, f'{per} - {año}', 'RTB', 0, 'L')
    pdf.set_font('Arial', 'B', 9)
    pdf.cell(14, 5, 'Importe:', 'LTB', 0, 'L')
    pdf.set_font('Arial', '', 9)
    pdf.cell(21, 5, f'$ {val:.2f}', 'RTB', 1, 'R')
    pdf.ln(2)
    # Línea 8
    pdf.cell(190, 17, ' ', 0, 1, 'L')
    # Margen
    pdf.cell(190, 13, ' ', 0, 1, 'L')
    try:
        if not os.path.isdir(f'../reports/temp'):
            os.mkdir(f'../reports/temp')
        pdf.output(f'../reports/temp/recibo_{str(ndr).rjust(7, "0")}.pdf', 'F')

        ############ ABRIR REPORT ############

        if errores:
            print('\n\n\n\n')
            print('     ATENCIÓN! Durante la reimpresión del recibo se produjeron los siguientes errores:')
            print()
            pprint(errores)
            print('\n\n\n\n')

        print("Abriendo recibo. Cierre el archivo para continuar...")
        ruta = f'../reports/temp/'
        arch = f'recibo_{str(ndr).rjust(7, "0")}.pdf'
        os.chdir(ruta)
        os.system(arch)
        ruta = '../../modulos/'
        os.chdir(ruta)
    except UnboundLocalError:
        print("")
        print(f"No existe recibo con nro {str(ndr).rjust(7, '0')}.")
        print("")
    except:
        mant.log_error()
        print("")
        input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
        print()
        return
        
            ######################################## FIN DE REPORT ############################################





    #################################################################################################################
    ################################################ RECIBO ADELANTOS ###############################################
    #################################################################################################################

def recibo_adelanto(ndr, cobrador, periodo_h, año_h, valor_total):
    ############ INICIO DE VARIABLES INDEPENDIENTES ############
    ndr, ope, per, año, pag = rend.obtener_datos_recibo(ndr)
    id_o, soc, nic, fac, cob, tar, rut, ult, u_a, fup, mor, c_f, u_r, paga, op_cob, nom_alt, dom_alt = rend.obtener_datos_op(ope)
    try:
        cod, pan, pis, fil, num, cat, ocu, fall = rend.obtener_datos_nicho(nic)
    except UnboundLocalError:
        print("")
        print("         ERROR. La operación no tiene nicho asociado.")
        print("")
        return
    nro, nom, dni, te_1, te_2, mail, dom, loc, c_p, f_n, f_a, act = rend.obtener_datos_socio(soc)
    id_c, cat, val_mant_bic, val_mant_nob = rend.obtener_categoria(cat)
    panteon = rend.obtener_panteon(pan)
    nco = rend.obtener_nom_cobrador(cobrador)
    errores = {}
    if nom_alt != None:
        nom = f"[{nom_alt}]"
    if dom_alt != None:
        dom = f"[{dom_alt}]"    
    
    ############ FIN DE VARIABLES INDEPENDIENTES ############

        
    ############ INICIO DE FUNCIONES ############

    ############ FIN DE FUNCIONES ############


    ############ INICIO DE VARIABLES DEPENDIENTES ############

    ########### FIN DE VARIABLES DEPENDIENTES ############
    

    ############ INICIO DE REPORT ############
    pdf = FPDF()
    pdf.alias_nb_pages()
    pdf.add_page()
    # Header
    # Bicon
    if fac == 'bicon':
        pdf.set_font('Arial', 'B', 11)
        pdf.cell(85, 5, 'ADMINISTRACIÓN de PANTEONES SOCIALES', 0, 1, 'C')
        pdf.cell(85, 5, 'Tel.: 430 9999 / 430 8800', 0, 1, 'C')
        pdf.cell(85, 5, 'CORDOBA 2915 - ROSARIO', 0, 1, 'C')
        pdf.set_font('Arial', 'B', 10)
        pdf.cell(49, 5, '', 0, 0, 'L')
        pdf.cell(20, 5, 'Recibo nro.', 'LTB', 0, 'L')
        pdf.cell(16, 5, f'{ndr}'.rjust(7, '0'), 'RTB', 1, 'R')
        pdf.ln(1)
    elif fac == 'nob':
        # Logo
        pdf.image('../docs/logo_nob.jpg', 11, 14, 10)
        pdf.set_font('Arial', 'I', 7)
        pdf.cell(190, 3.1, '', 0, 1, 'L')
        pdf.ln(1)
        # Línea 1
        pdf.set_font('Arial', 'B', 8)
        pdf.cell(12, 3, '', 0, 0, 'L')
        pdf.cell(60, 3, "Club Atlético Newell's Old Boys", 0, 1, 'L')
        # Línea 2
        pdf.set_font('Arial', 'B', 6)
        pdf.cell(12, 3, '', 0, 0, 'L')
        pdf.cell(16, 3, 'Panteón Social', 0, 0, 'L')
        pdf.set_font('Arial', 'I', 6)
        pdf.cell(48, 3, '(Cementerio "El Salvador")', 0, 0, 'L')
        pdf.cell(15, 3, '', 0, 1, 'L')
        # Línea 3
        pdf.set_font('Arial', 'B', 6)
        pdf.cell(12, 3, '', 0, 0, 'L')
        pdf.cell(60, 3, 'ADMINISTRACIÓN PANTEÓN SOCIAL', 0, 1, 'L')
        # Línea 4
        pdf.set_font('Arial', '', 6)
        pdf.cell(12, 3, '', 0, 0, 'L')
        pdf.cell(44, 3, 'Córdoba 2915 - Tel. 430 9999 / 8800', 0, 0, 'L')
        pdf.set_font('Arial', 'B', 8)
        pdf.cell(17, 3, 'Recibo nro.', 'LTB', 0, 'L')
        pdf.cell(12, 3, f'{ndr}'.rjust(7, '0'), 'RTB', 1, 'R')
        pdf.ln(1)
    # Línea 1
    pdf.set_font('Arial', 'B', 9)
    pdf.cell(13, 4, 'Socio/a: ', 'LTB', 0, 'L')
    pdf.set_font('Arial', '', 9)
    pdf.cell(12, 4, f'{nro}'.rjust(6, '0'), 'TB', 0, 'L')
    pdf.cell(60, 4, f'{nom}', 'TRB', 1, 'L')
    # Línea 2
    pdf.set_font('Arial', 'B', 9)
    pdf.cell(85, 1, '', 0, 1, 'L')
    pdf.cell(16, 5, 'Domicilio: ', 'LT', 0, 'L')
    pdf.set_font('Arial', '', 9)
    pdf.cell(69, 5, f'{dom}', 'TR', 1, 'L')
    # Línea 3
    pdf.set_font('Arial', 'B', 9)
    pdf.cell(19, 5, 'Cobrador/a: ', 'L', 0, 'L')
    pdf.set_font('Arial', '', 9)
    pdf.cell(5, 5, f'{cobrador}'.rjust(2, '0'), 0, 0, 'L')
    pdf.cell(39, 5, f'{nco}', 0, 0, 'L')
    pdf.set_font('Arial', 'B', 9)
    pdf.cell(10, 5, 'Ruta: ', 0, 0, 'R')
    pdf.set_font('Arial', '', 9)
    pdf.cell(12, 5, f'{rut}', 'R', 1, 'L')
    # Línea 4
    pdf.set_font('Arial', 'B', 9)
    pdf.cell(17, 4, 'Categoría: ', 'LB', 0, 'L')
    pdf.set_font('Arial', '', 9)
    pdf.cell(68, 4, f'{cat}', 'BR', 1, 'L')
    pdf.ln(1)
    # Línea 5
    pdf.set_font('Arial', 'B', 9)
    pdf.cell(19, 5, 'Cod. Nicho:', 'LTB', 0, 'L')
    pdf.set_font('Arial', '', 9)
    pdf.cell(43, 5, f'{cod}'.rjust(10, '0'), 'TB', 0, 'L')
    pdf.set_font('Arial', 'B', 9)
    pdf.cell(7, 5, f'Op:', 'TB', 0, 'TB')
    pdf.set_font('Arial', '', 9)
    pdf.cell(16, 5, f'{id_o}'.rjust(7, "0"), 'RTB', 1, 'L')
    pdf.ln(1)
    # Línea 6
    pdf.set_font('Arial', 'B', 9)
    pdf.cell(44, 4, 'Panteón', 'LTR', 0, 'C')
    pdf.cell(13, 4, 'Piso', 'LTR', 0, 'C')
    pdf.cell(13, 4, 'Fila', 'LTR', 0, 'C')
    pdf.cell(15, 4, 'Nicho', 'LTR', 1, 'C')
    # Línea 7
    pdf.set_font('Arial', '', 9)
    pdf.cell(44, 5, f'{panteon}', 'LBR', 0, 'C')
    pdf.cell(13, 5, f'{pis}'.rjust(2, '0'), 'LBR', 0, 'C')
    pdf.cell(13, 5, f'{fil}'.rjust(2, '0'), 'LBR', 0, 'C')
    pdf.cell(15, 5, f'{num}'.rjust(3, '0'), 'LBR', 1, 'C')
    pdf.ln(3)
    # Línea 8
    pdf.set_font('Arial', 'B', 9)
    pdf.cell(11, 5, 'Hasta: ', 'LTB', 0, 'L')
    pdf.set_font('Arial', '', 9)
    if periodo_h == 'Diciembre - Enero':
        pdf.cell(49, 5, f'{periodo_h} - {año_h}/{int(str(año_h)[-2:])+1}', 'RTB', 0, 'L')
    else:
        pdf.cell(49, 5, f'{periodo_h} - {año_h}', 'RTB', 0, 'L')
    pdf.set_font('Arial', '', 9)
    pdf.cell(25, 5, f'$ {valor_total:.2f}', 'RTB', 1, 'C')
    pdf.ln(2)
    try:
        if not os.path.isdir(f'../reports/temp'):
            os.mkdir(f'../reports/temp')
        pdf.output(f'../reports/temp/recibo_{str(ndr).rjust(7, "0")}.pdf', 'F')

        ############ ABRIR REPORT ############

        if errores:
            print('\n\n\n\n')
            print('     ATENCIÓN! Durante la emisión del recibo se produjeron los siguientes errores:')
            print()
            pprint(errores)
            print('\n\n\n\n')

        print("Abriendo recibo. Cierre el archivo para continuar...")
        ruta = f'../reports/temp/'
        arch = f'recibo_{str(ndr).rjust(7, "0")}.pdf'
        os.chdir(ruta)
        os.system(arch)
        ruta = '../../modulos/'
        os.chdir(ruta)
    except UnboundLocalError:
        print("")
        print(f"No existe recibo con nro {str(ndr).rjust(7, '0')}.")
        print("")
    except:
        mant.log_error()
        print("")
        input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
        print()
        return
        
            ######################################## FIN DE REPORT ############################################





    #################################################################################################################
    ############################################### ESTADO DE CUENTA ################################################
    #################################################################################################################

def report_estado_cta(nro_socio, nombre, dni, facturacion, domicilio, te_1, te_2, mail, c_p, localidad, act):
    ############ INICIO DE VARIABLES INDEPENDIENTES ############
    fecha = caja.obtener_fecha()
    hora = datetime.now().strftime('%H:%M')
    errores = {}
    if act == 1:
        estado = 'ACTIVO'
    elif act == 0:
        estado = 'INACTIVO'
    if mail == None:
        mail = ''
    if te_1 == None:
        te_1 = ''
    if te_2 == None:
        te_2 = ''

    ############ FIN DE VARIABLES INDEPENDIENTES ############

        
    ############ INICIO DE FUNCIONES ############
    
    ############ FIN DE FUNCIONES ############


    ############ INICIO DE VARIABLES DEPENDIENTES ############

    ########### FIN DE VARIABLES DEPENDIENTES ############
    

    ############ INICIO DE REPORT ############
    class PDF(FPDF):
        # Page header
        def header(self):
            # Logo
            if facturacion == 'bicon':
                self.image('../docs/logo_bicon.jpg', 14.5, 12, 15)
            elif facturacion == 'nob':
                self.image('../docs/logo_nob.jpg', 14.5, 12, 13)
            # Arial bold 15
            self.set_font('Arial', 'B', 15)
            # Title
            self.cell(0, 20, 'ESTADO DE CUENTA', 1, 0, 'C')
            # Arial 10
            self.set_font('Arial', '', 10)
            # Fecha
            self.cell(0, 35, f'{fecha} - {hora} hs', 0, 0, 'R')
            # Line break
            self.ln(22)
            self.set_font('Arial', 'B', 10)
            self.cell(19, 5, 'Asociado:', 'LT', 0, 'L')
            self.cell(13, 5, f'{nro_socio}'.rjust(6, '0'), 'T', 0, 'L')
            self.cell(114, 5, f'-  {nombre}', 'T', 0, 'L')
            self.cell(15, 5, 'DNI:', 'T', 0, 'L')
            self.cell(29, 5, f'{dni}', 'TR', 1, 'R')
            self.cell(19, 5, 'E-Mail:', 'L', 0, 'L')
            self.cell(127, 5, f'{mail}', 0, 0, 'L')
            self.cell(20, 5, 'Tel 1:', 0, 0, 'L')
            self.cell(24, 5, f'{te_1}', 'R', 1, 'R')
            self.cell(19, 5, 'Domicilio:', 'L', 0, 'L')
            self.cell(127, 5, f'{domicilio}', 0, 0, 'L')
            self.cell(20, 5, 'Tel 2:', 0, 0, 'L')
            self.cell(24, 5, f'{te_2}', 'R', 1, 'R')
            self.cell(19, 5, 'Localidad:', 'LB', 0, 'L')
            self.cell(127, 5, f'{c_p} - {localidad}', 'B', 0, 'L')
            self.cell(14, 5, 'Estado:', 'B', 0, 'L')
            self.cell(30, 5, f'{estado}', 'BR', 1, 'R')
            # Line break
            self.ln(2)
        
        # Page footer
        def footer(self):
            # Position at 2.5 cm from bottom
            self.set_y(-25)
            # Arial italic 8
            self.set_font('Arial', 'I', 8)
            self.cell(0, 1, '_______________________________________________________________________________________________', 0, 1, 'C')
            # Page number
            self.cell(0, 10, 'Página ' + str(self.page_no()) + ' de {nb}', 0, 0, 'C')
            # Firma
            self.set_font('Arial', 'I', 8)
            self.cell(-10, 10, f'Reporte generado en *MORELLA v{mant.SHORT_VERSION}* by ', 0, 0, 'R')
            self.image('../docs/mf_logo.jpg', 190, 274, 8)

    # Instantiation of inherited class
    pdf = PDF()
    pdf.set_auto_page_break(True, 25)
    pdf.alias_nb_pages()
    pdf.add_page()
    operaciones = ctas.buscar_op_por_nro_socio(nro_socio)
    for o in operaciones:
        id_op, soc, nic, fac, cob, tar, rut, ult, u_a, fec, mor, c_f, u_r, paga, op_cob, nom_alt, dom_alt = o
        cob = caja.obtener_nom_cobrador(cob)
        pdf.ln(2)
        pdf.set_font('Arial', 'B', 10)
        pdf.cell(20, 5, 'Operación: ', 0, 0, 'L')
        pdf.set_font('Arial', '', 10)
        pdf.cell(16, 5, f'{id_op}'.rjust(7, '0'), 0, 0, 'L')
        pdf.set_font('Arial', 'B', 10)
        pdf.cell(34, 5, 'Última cuota paga: ', 0, 0, 'L')
        pdf.set_font('Arial', '', 10)
        if ult == 'Diciembre - Enero':
            pdf.cell(50, 5, f'{ult} - {u_a}/{int(str(u_a)[-2:])+1}', 0, 0, 'L')
        else:
            pdf.cell(50, 5, f'{ult} - {u_a}', 0, 0, 'L')
        pdf.set_font('Arial', 'B', 10)
        pdf.cell(19, 5, 'Cobrador: ', 0, 0, 'L')
        pdf.set_font('Arial', '', 10)
        pdf.cell(20, 5, f'{cob}', 0, 1, 'L')
        if op_cob != 0 or nom_alt != None or dom_alt != None:
            if op_cob == 0:
                op_cob = '-'
            if nom_alt == None:
                nom_alt = '-'
            if dom_alt == None:
                dom_alt = '-'
            pdf.ln(1)
            pdf.set_font('Arial', '', 8)
            pdf.cell(3, 3, '  (', 0, 0, 'L')
            pdf.set_font('Arial', 'B', 8)
            pdf.cell(16, 3, 'Op. Cobol: ', 0, 0, 'L')
            pdf.set_font('Arial', '', 8)
            pdf.cell(8, 3, f'{op_cob}', 0, 0, 'L')
            pdf.set_font('Arial', 'B', 8)
            pdf.cell(2, 3, '', 0, 0, 'L')
            pdf.cell(27, 3, 'Nombre alternativo: ', 0, 0, 'L')
            pdf.set_font('Arial', '', 8)
            pdf.cell(40, 3, f'{nom_alt}', 0, 0, 'L')
            pdf.set_font('Arial', 'B', 8)
            pdf.cell(2, 3, '', 0, 0, 'L')
            pdf.cell(29, 3, 'Domicilio alternativo: ', 0, 0, 'L')
            pdf.set_font('Arial', '', 8)
            pdf.cell(40, 3, f'{dom_alt})', 0, 1, 'L')
            pdf.ln(1)
        pdf.ln(1)
        pdf.set_font('Arial', 'B', 10)
        pdf.cell(10, 5, '', 0, 0, 'L')
        pdf.cell(17, 5, 'Recibo', 0, 0, 'L ')
        pdf.cell(1, 5, '', 0, 0, 'L')
        pdf.cell(11, 5, 'Cód. nicho', 0, 0, 'L')
        pdf.cell(12, 5, '', 0, 0, 'L')
        pdf.cell(47, 5, 'Período', 0, 0, 'L')
        pdf.cell(1, 5, '', 0, 0, 'L')
        pdf.cell(19, 5, 'Deuda', 0, 1, 'L')
        if c_f < 0:
            pdf.set_font('Arial', '', 10)
            pdf.cell(10, 5, '', 0, 0, 'L')
            pdf.cell(17, 5, f'N/D', 0, 0, 'L ')
            pdf.cell(1, 5, '', 0, 0, 'L')
            pdf.cell(11, 5, f'{ctas.buscar_nicho_por_op(id_op)}'.rjust(10, '0'), 0, 0, 'L')
            pdf.cell(12, 5, '', 0, 0, 'L')
            if fac == 'bicon':
                pdf.cell(49, 5, f'Hasta Agosto-Septiembre 2022', 0, 0, 'L')
            if fac == 'nob':
                pdf.cell(49, 5, f'Hasta Julio-Agosto 2022', 0, 0, 'L')
            pdf.cell(1, 5, '', 0, 0, 'L')
            pdf.cell(2, 5, '$', 0, 0, 'R')
            pdf.cell(23, 5, f'{float(ctas.deuda_vieja_por_op(id_op)):.2f}', 0, 1, 'R')
        recibos = ctas.buscar_recibos_por_op(id_op)
        for r in recibos:
            nro, ope, per, año, pag = r
            nic = ctas.buscar_nicho_por_op(ope)
            try:
                cod, pan, pis, fil, num, cat, ocu, fall = rend.obtener_datos_nicho(nic)
                id_cat, cat, val_mant_bic, val_mant_nob = rend.obtener_categoria(cat)
            except UnboundLocalError:
                if 'Operaciones sin nicho' not in errores:
                    errores['Operaciones sin nicho'] = [str(id_op).rjust(7, '0')]
                else:
                    errores['Operaciones sin nicho'].append(str(id_op).rjust(7, '0'))
                continue
            if fac == 'bicon':
                val = val_mant_bic
            elif fac == 'nob':
                val = val_mant_nob
            if per[0:3] == 'Doc':
                val = rend.obtener_valor_doc(ope)
            pdf.set_font('Arial', '', 10)
            pdf.cell(10, 5, '', 0, 0, 'L')
            pdf.cell(17, 5, f'{nro}'.rjust(7, '0'), 0, 0, 'L ')
            pdf.cell(1, 5, '', 0, 0, 'L')
            pdf.cell(11, 5, f'{ctas.buscar_nicho_por_op(ope)}'.rjust(10, '0'), 0, 0, 'L')
            pdf.cell(12, 5, '', 0, 0, 'L')
            if per == 'Diciembre - Enero':
                pdf.cell(49, 5, f'{per} - {año}{int(str(año)[-2:])+1}', 0, 0, 'L')
            else:
                pdf.cell(49, 5, f'{per} - {año}', 0, 0, 'L')
            pdf.cell(1, 5, '', 0, 0, 'L')
            pdf.cell(2, 5, '$', 0, 0, 'R')
            pdf.cell(23, 5, f'{float(val):.2f}', 0, 1, 'R')
        pdf.ln(3)
        pdf.set_font('Arial', 'B', 10)
        pdf.cell(40, 5, 'Deuda de operación: ', 0, 0, 'L')
        pdf.set_font('Arial', '', 10)
        pdf.cell(1, 5, '$', 0, 0, 'R')
        pdf.cell(0, 5, f'{ctas.deuda_por_op(id_op):.2f}', 0, 1, 'L')
        pdf.set_font('Arial', 'B', 10)
        pdf.cell(27, 5, 'Cuotas a favor: ', 0, 0, 'L')
        pdf.set_font('Arial', '', 10)
        if c_f < 0:
            pdf.cell(0, 5, f'0', 0, 1, 'L')
        else:
            pdf.cell(0, 5, f'{c_f}', 0, 1, 'L')
        pdf.ln(2)
        pdf.cell(0, 2, '________________________________________', 0, 1, 'L')
        pdf.ln(2)
    pdf.set_font('Arial', 'B', 10)
    pdf.ln(10)
    pdf.cell(100, 5, '', 0, 0, 'L')
    pdf.cell(47, 5, 'Deuda total del asociado: ', 0, 0, 'L')
    pdf.set_font('Arial', '', 10)
    pdf.cell(1, 5, '$', 0, 0, 'R')
    pdf.cell(0, 5, f'{float(ctas.deuda_por_socio(nro_socio)):.2f}', 0, 1, 'L')
    
    # Export
    pdf.output(f'../reports/temp/estado_cta.pdf', 'F')
        

    ############ ABRIR REPORT ############

    if errores:
        print('\n\n\n\n')
        print('     ATENCIÓN! Durante la emisión del reporte se produjeron los siguientes errores:')
        print()
        pprint(errores)
        print('\n\n\n\n')
            

    print("Abriendo reporte. Cierre el archivo para continuar...")
    print("")
    ruta = f'../reports/temp'
    arch = f'estado_cta.pdf'
    os.chdir(ruta)
    os.system(arch)
    ruta = '../../modulos/'
    os.chdir(ruta)
           
            ######################################## FIN DE REPORT ############################################





    #################################################################################################################
    ####################################### ESTADO DE CUENTA P/EMAIL ################################################
    #################################################################################################################

def report_estado_cta_mail(nro_socio, nombre, dni, facturacion, domicilio, te_1, te_2, mail, c_p, localidad, act):
    ############ INICIO DE VARIABLES INDEPENDIENTES ############
    fecha = caja.obtener_fecha()
    hora = datetime.now().strftime('%H:%M')
    errores = {}
    if act == 1:
        estado = 'ACTIVO'
    elif act == 0:
        estado = 'INACTIVO'

    ############ FIN DE VARIABLES INDEPENDIENTES ############

        
    ############ INICIO DE FUNCIONES ############
    
    ############ FIN DE FUNCIONES ############


    ############ INICIO DE VARIABLES DEPENDIENTES ############

    ########### FIN DE VARIABLES DEPENDIENTES ############
    

    ############ INICIO DE REPORT ############
    class PDF(FPDF):
        # Page header
        def header(self):
            # Logo
            if facturacion == 'bicon':
                self.image('../docs/logo_bicon.jpg', 14.5, 12, 15)
            elif facturacion == 'nob':
                self.image('../docs/logo_nob.jpg', 14.5, 12, 13)
            # Arial bold 15
            self.set_font('Arial', 'B', 15)
            # Title
            self.cell(0, 20, 'ESTADO DE CUENTA', 1, 0, 'C')
            # Arial 10
            self.set_font('Arial', '', 10)
            # Fecha
            self.cell(0, 35, f'{fecha} - {hora} hs', 0, 0, 'R')
            # Line break
            self.ln(22)
            self.set_font('Arial', 'B', 10)
            self.cell(19, 5, 'Asociado:', 'LT', 0, 'L')
            self.cell(13, 5, f'{nro_socio}'.rjust(6, '0'), 'T', 0, 'L')
            self.cell(114, 5, f'-  {nombre}', 'T', 0, 'L')
            self.cell(15, 5, 'DNI:', 'T', 0, 'L')
            self.cell(29, 5, f'{dni}', 'TR', 1, 'R')
            self.cell(19, 5, 'E-Mail:', 'L', 0, 'L')
            self.cell(127, 5, f'{mail}', 0, 0, 'L')
            self.cell(20, 5, 'Tel 1:', 0, 0, 'L')
            self.cell(24, 5, f'{te_1}', 'R', 1, 'R')
            self.cell(19, 5, 'Domicilio:', 'L', 0, 'L')
            self.cell(127, 5, f'{domicilio}', 0, 0, 'L')
            self.cell(20, 5, 'Tel 2:', 0, 0, 'L')
            if te_2 == None or te_2 == "":
                self.cell(24, 5, f'', 'R', 1, 'R')
            else:
                self.cell(24, 5, f'{te_2}', 'R', 1, 'R')
            self.cell(19, 5, 'Localidad:', 'LB', 0, 'L')
            self.cell(127, 5, f'{c_p} - {localidad}', 'B', 0, 'L')
            self.cell(14, 5, 'Estado:', 'B', 0, 'L')
            self.cell(30, 5, f'{estado}', 'BR', 1, 'R')
            # Line break
            self.ln(2)
        
        # Page footer
        def footer(self):
            # Position at 2.5 cm from bottom
            self.set_y(-25)
            # Arial italic 8
            self.set_font('Arial', 'I', 8)
            self.cell(0, 1, '_______________________________________________________________________________________________', 0, 1, 'C')
            # Page number
            self.cell(0, 10, 'Página ' + str(self.page_no()) + ' de {nb}', 0, 0, 'C')
            # Firma
            self.set_font('Arial', 'I', 8)
            self.cell(-10, 10, f'Reporte generado en *MORELLA v{mant.SHORT_VERSION}* by ', 0, 0, 'R')
            self.image('../docs/mf_logo.jpg', 190, 274, 8)

    # Instantiation of inherited class
    pdf = PDF()
    pdf.set_auto_page_break(True, 25)
    pdf.alias_nb_pages()
    pdf.add_page()
    operaciones = ctas.buscar_op_por_nro_socio(nro_socio)
    for o in operaciones:
        id_op, soc, nic, fac, cob, tar, rut, ult, u_a, fec, mor, c_f, u_r, paga, op_cob, nom_alt, dom_alt = o
        cob = caja.obtener_nom_cobrador(cob)
        pdf.ln(2)
        pdf.set_font('Arial', 'B', 10)
        pdf.cell(20, 5, 'Operación: ', 0, 0, 'L')
        pdf.set_font('Arial', '', 10)
        pdf.cell(16, 5, f'{id_op}'.rjust(7, '0'), 0, 0, 'L')
        pdf.set_font('Arial', 'B', 10)
        pdf.cell(34, 5, 'Última cuota paga: ', 0, 0, 'L')
        pdf.set_font('Arial', '', 10)
        if ult == 'Diciembre - Enero':
            pdf.cell(50, 5, f'{ult} - {u_a}/{int(str(u_a)[-2:])+1}', 0, 0, 'L')
        else:
            pdf.cell(50, 5, f'{ult} - {u_a}', 0, 0, 'L')
        pdf.set_font('Arial', 'B', 10)
        pdf.cell(19, 5, 'Cobrador: ', 0, 0, 'L')
        pdf.set_font('Arial', '', 10)
        pdf.cell(20, 5, f'{cob}', 0, 1, 'L')
        if op_cob != 0 or nom_alt != None or dom_alt != None:
            if op_cob == 0:
                op_cob = '-'
            if nom_alt == None:
                nom_alt = '-'
            if dom_alt == None:
                dom_alt = '-'
            pdf.ln(1)
            pdf.set_font('Arial', '', 8)
            pdf.cell(3, 3, '  (', 0, 0, 'L')
            pdf.set_font('Arial', 'B', 8)
            pdf.cell(16, 3, 'Op. Cobol: ', 0, 0, 'L')
            pdf.set_font('Arial', '', 8)
            pdf.cell(8, 3, f'{op_cob}', 0, 0, 'L')
            pdf.set_font('Arial', 'B', 8)
            pdf.cell(2, 3, '', 0, 0, 'L')
            pdf.cell(27, 3, 'Nombre alternativo: ', 0, 0, 'L')
            pdf.set_font('Arial', '', 8)
            pdf.cell(40, 3, f'{nom_alt}', 0, 0, 'L')
            pdf.set_font('Arial', 'B', 8)
            pdf.cell(2, 3, '', 0, 0, 'L')
            pdf.cell(29, 3, 'Domicilio alternativo: ', 0, 0, 'L')
            pdf.set_font('Arial', '', 8)
            pdf.cell(40, 3, f'{dom_alt})', 0, 1, 'L')
            pdf.ln(1)
        pdf.ln(1)
        pdf.set_font('Arial', 'B', 10)
        pdf.cell(10, 5, '', 0, 0, 'L')
        pdf.cell(17, 5, 'Recibo', 0, 0, 'L ')
        pdf.cell(1, 5, '', 0, 0, 'L')
        pdf.cell(11, 5, 'Cód. nicho', 0, 0, 'L')
        pdf.cell(12, 5, '', 0, 0, 'L')
        pdf.cell(43, 5, 'Período', 0, 0, 'L')
        pdf.cell(1, 5, '', 0, 0, 'L')
        pdf.cell(23, 5, 'Deuda', 0, 1, 'L')
        if c_f < 0:
            pdf.set_font('Arial', '', 10)
            pdf.cell(10, 5, '', 0, 0, 'L')
            pdf.cell(17, 5, f'N/D', 0, 0, 'L ')
            pdf.cell(1, 5, '', 0, 0, 'L')
            pdf.cell(11, 5, f'{ctas.buscar_nicho_por_op(id_op)}'.rjust(10, '0'), 0, 0, 'L')
            pdf.cell(12, 5, '', 0, 0, 'L')
            if fac == 'bicon':
                pdf.cell(49, 5, f'Hasta Agosto-Septiembre 2022', 0, 0, 'L')
            if fac == 'nob':
                pdf.cell(49, 5, f'Hasta Julio-Agosto 2022', 0, 0, 'L')
            pdf.cell(1, 5, '', 0, 0, 'L')
            pdf.cell(2, 5, '$', 0, 0, 'R')
            pdf.cell(23, 5, f'{float(ctas.deuda_vieja_por_op(id_op)):.2f}', 0, 1, 'R')
        recibos = ctas.buscar_recibos_por_op(id_op)
        for r in recibos:
            nro, ope, per, año, pag = r
            nic = ctas.buscar_nicho_por_op(ope)
            try:
                cod, pan, pis, fil, num, cat, ocu, fall = rend.obtener_datos_nicho(nic)
                id_cat, cat, val_mant_bic, val_mant_nob = rend.obtener_categoria(cat)
            except UnboundLocalError:
                if 'Operaciones sin nicho' not in errores:
                    errores['Operaciones sin nicho'] = [str(id_op).rjust(7, '0')]
                else:
                    errores['Operaciones sin nicho'].append(str(id_op).rjust(7, '0'))
                continue
            if fac == 'bicon':
                val = val_mant_bic
            elif fac == 'nob':
                val = val_mant_nob
            if per[0:3] == 'Doc':
                val = rend.obtener_valor_doc(ope)
            pdf.set_font('Arial', '', 10)
            pdf.cell(10, 5, '', 0, 0, 'L')
            pdf.cell(17, 5, f'{nro}'.rjust(7, '0'), 0, 0, 'L ')
            pdf.cell(1, 5, '', 0, 0, 'L')
            pdf.cell(11, 5, f'{ctas.buscar_nicho_por_op(ope)}'.rjust(10, '0'), 0, 0, 'L')
            pdf.cell(12, 5, '', 0, 0, 'L')
            if per == 'Diciembre - Enero':
                pdf.cell(49, 5, f'{per} - {año}{int(str(año)[-2:])+1}', 0, 0, 'L')
            else:
                pdf.cell(49, 5, f'{per} - {año}', 0, 0, 'L')
            pdf.cell(1, 5, '', 0, 0, 'L')
            pdf.cell(2, 5, '$', 0, 0, 'R')
            pdf.cell(23, 5, f'{float(val):.2f}', 0, 1, 'R')
        pdf.ln(3)
        pdf.set_font('Arial', 'B', 10)
        pdf.cell(40, 5, 'Deuda de operación: ', 0, 0, 'L')
        pdf.set_font('Arial', '', 10)
        pdf.cell(1, 5, '$', 0, 0, 'R')
        pdf.cell(0, 5, f'{ctas.deuda_por_op(id_op):.2f}', 0, 1, 'L')
        pdf.set_font('Arial', 'B', 10)
        pdf.cell(27, 5, 'Cuotas a favor: ', 0, 0, 'L')
        pdf.set_font('Arial', '', 10)
        if c_f < 0:
            pdf.cell(0, 5, f'0', 0, 1, 'L')
        else:
            pdf.cell(0, 5, f'{c_f}', 0, 1, 'L')
        pdf.ln(2)
        pdf.cell(0, 2, '________________________________________', 0, 1, 'L')
        pdf.ln(2)
    pdf.set_font('Arial', 'B', 10)
    pdf.ln(10)
    pdf.cell(100, 5, '', 0, 0, 'L')
    pdf.cell(47, 5, 'Deuda total del asociado: ', 0, 0, 'L')
    pdf.set_font('Arial', '', 10)
    pdf.cell(1, 5, '$', 0, 0, 'R')
    pdf.cell(0, 5, f'{float(ctas.deuda_por_socio(nro_socio)):.2f}', 0, 1, 'L')
    
    # Export

    if errores:
        print('\n\n\n\n')
        print('     ATENCIÓN! Durante la emisión del reporte se produjeron los siguientes errores:')
        print()
        pprint(errores)
        print('\n\n\n\n')

    pdf.output(f'../reports/temp/estado_cta_mail.pdf', 'F')
        
            ######################################## FIN DE REPORT ############################################





    #################################################################################################################
    ######################################### LISTADO DE MOROSOS DETALLADO ##########################################
    #################################################################################################################

def report_morosos_det():
    ############ INICIO DE VARIABLES INDEPENDIENTES ############
    fecha = caja.obtener_fecha()
    hora = datetime.now().strftime('%H:%M')
    morosos = ctas.obtener_op_morosos()
    lista_morosos = []
    deuda_total_morosos = 0
    counter = 0
    errores = {}

    ############ FIN DE VARIABLES INDEPENDIENTES ############

        
    ############ INICIO DE FUNCIONES ############
    def lista_morosos_limpia(morosos):
        for i in morosos:
            i_d, soc, nic, fac, cob, tar, rut, ult, u_a, fec_u_p, mor, c_f, u_r, paga, op_cob, nom_alt, dom_alt = i
            lista_morosos.append(soc)
        lista_morosos_limpia = set(lista_morosos)
        return lista_morosos_limpia

    ############ FIN DE FUNCIONES ############


    ############ INICIO DE VARIABLES DEPENDIENTES ############
    lista_limpia_morosos = lista_morosos_limpia(morosos)

    ########### FIN DE VARIABLES DEPENDIENTES ############


    ############ INICIO DE REPORT ############
    class PDF(FPDF):
        # Page header
        def header(self):
            # Logo
            self.image('../docs/logo_bicon.jpg', 14.5, 12, 15)
            # Arial bold 15
            self.set_font('Arial', 'B', 15)
            # Title
            self.cell(0, 20, 'LISTADO DETALLADO DE MOROSOS', 1, 0, 'C')
            # Arial 10
            self.set_font('Arial', '', 10)
            # Fecha
            self.cell(0, 35, f'{fecha} - {hora} hs', 0, 0, 'R')
            # Line break
            self.ln(22)
      
        # Page footer
        def footer(self):
            # Position at 2.5 cm from bottom
            self.set_y(-25)
            # Arial italic 8
            self.set_font('Arial', 'I', 8)
            self.cell(0, 1, '_______________________________________________________________________________________________', 0, 1, 'C')
            # Page number
            self.cell(0, 10, 'Página ' + str(self.page_no()) + ' de {nb}', 0, 0, 'C')
            # Firma
            self.set_font('Arial', 'I', 8)
            self.cell(-10, 10, f'Reporte generado en *MORELLA v{mant.SHORT_VERSION}* by ', 0, 0, 'R')
            self.image('../docs/mf_logo.jpg', 190, 274, 8)

    # Instantiation of inherited class
    pdf = PDF()
    pdf.set_auto_page_break(True, 25)
    pdf.alias_nb_pages()
    pdf.add_page()
    for i in lista_limpia_morosos:
        nro_soc, nom, dni, te_1, te_2, mail, dom, loc, c_p, f_n, f_a, act = rend.obtener_datos_socio(i)
        if act == 1:
            estado = 'ACTIVO'
        elif act == 0:
            estado = 'INACTIVO'
        pdf.ln(2)
        pdf.set_font('Arial', 'B', 10)
        pdf.cell(19, 5, 'Asociado:', 'LT', 0, 'L')
        pdf.cell(13, 5, f'{nro_soc}'.rjust(6, '0'), 'T', 0, 'L')
        pdf.cell(114, 5, f'-  {nom}', 'T', 0, 'L')
        pdf.cell(20, 5, 'Estado:', 'T', 0, 'L')
        pdf.cell(24, 5, f'{estado}', 'TR', 1, 'R')
        pdf.cell(19, 5, 'Domicilio:', 'L', 0, 'L')
        pdf.cell(127, 5, f'{dom}', 0, 0, 'L')
        pdf.cell(15, 5, 'Tel 1:', 0, 0, 'L')
        pdf.cell(29, 5, f'{te_1}', 'R', 1, 'R')
        pdf.cell(19, 5, 'Localidad:', 'LB', 0, 'L')
        pdf.cell(127, 5, f'{c_p} - {loc}', 'B', 0, 'L')
        pdf.cell(15, 5, 'Tel 2:', 'B', 0, 'L')
        if te_2 == None or te_2 == "":
            pdf.cell(29, 5, f'- ', 'BR', 1, 'R')
        else:
            pdf.cell(29, 5, f'{te_2}', 'BR', 1, 'R')        
        pdf.ln(2)
        for x in ctas.obtener_datos_op_por_nro_socio(nro_soc):
            id_op, soc, nic, fac, cob, tar, rut, ult, u_a, fec_u_p, mor, c_f, u_r, paga, op_cob, nom_alt, dom_alt = x
            pdf.set_font('Arial', 'B', 10)
            pdf.cell(10, 5, '', 0, 0, 'L')
            pdf.cell(20, 5, 'Operación: ', 0, 0, 'L')
            pdf.set_font('Arial', '', 10)
            pdf.cell(16, 5, f'{id_op}'.rjust(7, '0'), 0, 0, 'L')
            pdf.set_font('Arial', 'B', 10)
            pdf.cell(34, 5, 'Última cuota paga: ', 0, 0, 'L')
            pdf.set_font('Arial', '', 10)
            pdf.cell(40, 5, f'{ult} - {u_a}', 0, 1, 'L')
            if op_cob != 0 or nom_alt != None or dom_alt != None:
                if op_cob == 0:
                    op_cob = '-'
                if nom_alt == None:
                    nom_alt = '-'
                if dom_alt == None:
                    dom_alt = '-'
                pdf.ln(1)
                pdf.set_font('Arial', '', 8)
                pdf.cell(3, 3, '  (', 0, 0, 'L')
                pdf.set_font('Arial', 'B', 8)
                pdf.cell(16, 3, 'Op. Cobol: ', 0, 0, 'L')
                pdf.set_font('Arial', '', 8)
                pdf.cell(8, 3, f'{op_cob}', 0, 0, 'L')
                pdf.set_font('Arial', 'B', 8)
                pdf.cell(2, 3, '', 0, 0, 'L')
                pdf.cell(27, 3, 'Nombre alternativo: ', 0, 0, 'L')
                pdf.set_font('Arial', '', 8)
                pdf.cell(40, 3, f'{nom_alt}', 0, 0, 'L')
                pdf.set_font('Arial', 'B', 8)
                pdf.cell(2, 3, '', 0, 0, 'L')
                pdf.cell(29, 3, 'Domicilio alternativo: ', 0, 0, 'L')
                pdf.set_font('Arial', '', 8)
                pdf.cell(40, 3, f'{dom_alt})', 0, 1, 'L')
                pdf.ln(1)
            pdf.ln(1)
            pdf.set_font('Arial', 'B', 10)
            pdf.cell(20, 5, '', 0, 0, 'L')
            pdf.cell(15, 5, 'Recibo', 0, 0, 'L ')
            pdf.cell(1, 5, '', 0, 0, 'L')
            pdf.cell(11, 5, 'Cód. nicho', 0, 0, 'L')
            pdf.cell(12, 5, '', 0, 0, 'L')
            pdf.cell(38, 5, 'Período', 0, 0, 'L')
            pdf.cell(1, 5, '', 0, 0, 'L')
            pdf.cell(23, 5, 'Deuda', 0, 1, 'L')
            recibos = ctas.buscar_recibos_por_op(id_op)
            for r in recibos:
                nro_rec, ope, per, año, pag = r
                nic = ctas.buscar_nicho_por_op(ope)
                try:
                    cod, pan, pis, fil, num, cat, ocu, fall = rend.obtener_datos_nicho(nic)
                    id_cat, cat, val_mant_bic, val_mant_nob = rend.obtener_categoria(cat)
                except UnboundLocalError:
                    if 'Operaciones sin nicho' not in errores:
                        errores['Operaciones sin nicho'] = [str(id_op).rjust(7, '0')]
                    else:
                        errores['Operaciones sin nicho'].append(str(id_op).rjust(7, '0'))
                    continue
                if fac == 'bicon':
                    val = val_mant_bic
                elif fac == 'nob':
                    val = val_mant_nob
                if per[0:3] == 'Doc':
                    val = rend.obtener_valor_doc(ope)
                pdf.set_font('Arial', '', 10)
                pdf.cell(20, 5, '', 0, 0, 'L')
                pdf.cell(15, 5, f'{nro_rec}'.rjust(6, '0'), 0, 0, 'L ')
                pdf.cell(1, 5, '', 0, 0, 'L')
                pdf.cell(11, 5, f'{ctas.buscar_nicho_por_op(ope)}'.rjust(10, '0'), 0, 0, 'L')
                pdf.cell(12, 5, '', 0, 0, 'L')
                pdf.cell(40, 5, f'{per} - {año}', 0, 0, 'L')
                pdf.cell(1, 5, '', 0, 0, 'L')
                pdf.cell(2, 5, '$', 0, 0, 'R')
                pdf.cell(21, 5, f'{float(val):.2f}', 0, 1, 'R')
            pdf.set_font('Arial', 'B', 10)
            pdf.ln(3)
            pdf.cell(10, 5, '', 0, 0, 'L')
            pdf.cell(40, 5, 'Deuda de operación: ', 'LTB', 0, 'L')
            pdf.set_font('Arial', '', 10)
            pdf.cell(1, 5, '$', 'TB', 0, 'R')
            pdf.cell(23, 5, f'{float(ctas.deuda_por_op(id_op)):.2f}', 'RTB', 1, 'L')
            pdf.ln(2)
        pdf.set_font('Arial', 'B', 10)
        pdf.ln(10)
        pdf.cell(100, 5, '', 0, 0, 'L')
        pdf.cell(57, 5, 'Deuda total del asociado: ', 'LTB', 0, 'L')
        pdf.set_font('Arial', '', 10)
        pdf.cell(1, 5, '$', 'TB', 0, 'R')
        pdf.cell(23, 5, f'{float(ctas.deuda_por_socio(nro_soc)):.2f}', 'RTB', 1, 'L')
        deuda_total_morosos = deuda_total_morosos + ctas.deuda_por_socio(nro_soc)
        # Line break
        pdf.ln(3)
        counter += 1
        mant.barra_progreso(counter, len(lista_limpia_morosos), titulo=f'Morella v{mant.VERSION} - MF! Soluciones informáticas')
    pdf.set_font('Arial', 'B', 10)
    pdf.cell(0, 5, f'DEUDA TOTAL MOROSOS: $ {deuda_total_morosos:.2f}', 1, 1, 'R')
    
    # Export
    pdf.output(f'../reports/temp/morosos.pdf', 'F')
        

    ############ ABRIR REPORT ############

    if errores:
        print('\n\n\n\n')
        print('     ATENCIÓN! Durante la emisión del reporte se produjeron los siguientes errores:')
        print()
        pprint(errores)
        print('\n\n\n\n')

    print("Abriendo reporte. Cierre el archivo para continuar...")
    print("")
    ruta = f'../reports/temp'
    arch = f'morosos.pdf'
    os.chdir(ruta)
    os.system(arch)
    ruta = '../../modulos/'
    os.chdir(ruta)
    os.system(f'TITLE Morella v{mant.VERSION} - MF! Soluciones informáticas')
           
            ######################################## FIN DE REPORT ############################################





    #################################################################################################################
    ######################################### LISTADO DE MOROSOS COMPRIMIDO ##########################################
    #################################################################################################################


def report_morosos_comp():
    ############ INICIO DE VARIABLES INDEPENDIENTES ############
    fecha = caja.obtener_fecha()
    hora = datetime.now().strftime('%H:%M')
    morosos = ctas.obtener_op_morosos()
    lista_morosos = []
    deuda_total_morosos = 0
    counter = 0
    errores = {}

    ############ FIN DE VARIABLES INDEPENDIENTES ############

        
    ############ INICIO DE FUNCIONES ############
    def lista_morosos_limpia(morosos):
        for i in morosos:
            i_d, soc, nic, fac, cob, tar, rut, ult, u_a, fec_u_p, mor, c_f, u_r, paga, op_cob, nom_alt, dom_alt = i
            lista_morosos.append(soc)
        lista_morosos_limpia = set(lista_morosos)
        return lista_morosos_limpia

    def reducir_ult_pag(ult, u_a):
        if ult == 'Enero - Febrero':
            ult_pag = f'Ene-Feb/{u_a}'
        elif ult == 'Febrero - Marzo':
            ult_pag = f'Feb-Mar/{u_a}'
        elif ult == 'Marzo - Abril':
            ult_pag = f'Mar-Abr/{u_a}'
        elif ult == 'Abril - Mayo':
            ult_pag = f'Abr-May/{u_a}'
        elif ult == 'Mayo - Junio':
            ult_pag = f'May-Jun/{u_a}'
        elif ult == 'Junio - Julio':
            ult_pag = f'Jun-Jul/{u_a}'
        elif ult == 'Julio - Agosto':
            ult_pag = f'Jul-Ago/{u_a}'
        elif ult == 'Agosto - Septiembre':
            ult_pag = f'Ago-Sep/{u_a}'
        elif ult == 'Septiembre - Octubre':
            ult_pag = f'Sep-Oct/{u_a}'
        elif ult == 'Octubre - Noviembre':
            ult_pag = f'Oct-Nov/{u_a}'
        elif ult == 'Noviembre - Diciembre':
            ult_pag = f'Nov-Dic/{u_a}'
        elif ult == 'Diciembre - Enero':
            ult_pag = f'Dic-Ene/{u_a}-{int(u_a[2:4])+1}'
        return ult_pag

    ############ FIN DE FUNCIONES ############


    ############ INICIO DE VARIABLES DEPENDIENTES ############
    # lista_limpia_morosos = lista_morosos_limpia(morosos)

    ########### FIN DE VARIABLES DEPENDIENTES ############


    ############ INICIO DE REPORT ############
    class PDF(FPDF):
        # Page header
        def header(self):
            # Logo
            self.image('../docs/logo_bicon.jpg', 14.5, 12, 15)
            # Arial bold 15
            self.set_font('Arial', 'B', 15)
            # Title
            self.cell(0, 20, 'LISTADO COMPRIMIDO DE MOROSOS', 1, 0, 'C')
            # Arial 10
            self.set_font('Arial', '', 10)
            # Fecha
            self.cell(0, 35, f'{fecha} - {hora} hs', 0, 0, 'R')
            # Line break
            self.ln(22)
            self.set_font('Arial', 'B', 9)
            self.cell(16, 5, 'N° OPER.', 0, 0, 'L ')
            self.cell(1, 5, '', 0, 0, 'L')
            self.cell(13, 5, 'N° SOC.', 0, 0, 'L')
            self.cell(1, 5, '', 0, 0, 'L')
            self.cell(53, 5, 'APELLIDO Y NOMBRE (*)', 0, 0, 'L')
            self.cell(1, 5, '', 0, 0, 'L')
            self.cell(51, 5, 'TELÉFONOS', 0, 0, 'L')
            self.cell(1, 5, '', 0, 0, 'L')
            self.cell(31, 5, 'ÚLTIMO PAGO', 0, 0, 'L')
            self.cell(1, 5, '', 0, 0, 'L')
            self.cell(21, 5, 'DEUDA', 0, 1, 'L')
            self.cell(0, 1, '___________________________________________________________________________________________________________', 0, 1, 'C')
            self.ln(5)
        
        # Page footer
        def footer(self):
            # Position at 3 cm from bottom
            self.set_y(-30)
            # Arial italic 8
            self.set_font('Arial', 'I', 8)
            self.cell(0, 5, '* El asociado se encuentra INACTIVO', 0, 1, 'L')
            self.cell(0, 1, '_______________________________________________________________________________________________', 0, 1, 'C')
            # Page number
            self.cell(0, 10, 'Página ' + str(self.page_no()) + ' de {nb}', 0, 0, 'C')
            # Firma
            self.set_font('Arial', 'I', 8)
            self.cell(-10, 10, f'Reporte generado en *MORELLA v{mant.SHORT_VERSION}* by ', 0, 0, 'R')
            self.image('../docs/mf_logo.jpg', 190, 274, 8)

    # Instantiation of inherited class
    pdf = PDF()
    pdf.set_auto_page_break(True, 25)
    pdf.alias_nb_pages()
    pdf.add_page()
    for i in morosos:
        id_op, soc, nic, fac, cob, tar, rut, ult, u_a, fec_u_p, mor, c_f, u_r, paga, op_cob, nom_alt, dom_alt = i
        nro, nom, dni, te_1, te_2, mail, dom, loc, c_p, f_n, f_a, act = ctas.obtener_datos_socio(soc)
        if nom_alt != None:
            nom = f"[{nom_alt}]"
        pdf.set_font('Arial', '', 9)
        pdf.cell(16, 5, f'{id_op}'.rjust(7, '0'), 0, 0, 'L ')
        pdf.cell(1, 5, '', 0, 0, 'L')
        pdf.cell(13, 5, f'{nro}'.rjust(6, '0'), 0, 0, 'L')
        pdf.cell(1, 5, '', 0, 0, 'L')
        if act == 1:
            pdf.cell(53, 5, f'{nom}', 0, 0, 'L')
        elif act == 0:
            pdf.cell(53, 5, f'{nom} *', 0, 0, 'L')
        pdf.cell(1, 5, '', 0, 0, 'L')
        if te_2 == None or te_2 == "":
            pdf.cell(51, 5, f'{te_1}', 0, 0, 'L')
        else:
            pdf.cell(51, 5, f'{te_1} / {te_2}', 0, 0, 'L')
        pdf.cell(1, 5, '', 0, 0, 'L')
        pdf.cell(31, 5, f'{reducir_ult_pag(ult, u_a)}', 0, 0, 'L')
        pdf.cell(1, 5, '', 0, 0, 'L')
        pdf.cell(21, 5, f'$ {float(ctas.deuda_por_op(id_op)):.2f}', 0, 1, 'R')
        deuda_total_morosos = deuda_total_morosos + ctas.deuda_por_op(id_op)
        counter += 1
        mant.barra_progreso(counter, len(morosos), titulo=f'Morella v{mant.VERSION} - MF! Soluciones informáticas')

    pdf.ln(3)
    pdf.set_font('Arial', 'B', 10)
    pdf.cell(0, 5, f'DEUDA TOTAL MOROSOS: $ {deuda_total_morosos:.2f}', 1, 1, 'R')
    
    # Export
    pdf.output(f'../reports/temp/morosos-comp.pdf', 'F')
        

    ############ ABRIR REPORT ############

    if errores:
        print('\n\n\n\n')
        print('     ATENCIÓN! Durante la emisión del reporte se produjeron los siguientes errores:')
        print()
        pprint(errores)
        print('\n\n\n\n')

    print("Abriendo reporte. Cierre el archivo para continuar...")
    print("")
    ruta = f'../reports/temp'
    arch = f'morosos-comp.pdf'
    os.chdir(ruta)
    os.system(arch)
    ruta = '../../modulos/'
    os.chdir(ruta)
    os.system(f'TITLE Morella v{mant.VERSION} - MF! Soluciones informáticas')
           
            ######################################## FIN DE REPORT ############################################





    #################################################################################################################
    ########################################## LISTADO DE SOCIOS EN EXCEL ###########################################
    #################################################################################################################


def report_excel_socios():
    ############ INICIO DE VARIABLES INDEPENDIENTES ############
    fecha = datetime.today().strftime("%Y-%m-%d")
    counter = 0
    errores = {}

    ############ FIN DE VARIABLES INDEPENDIENTES ############


    ############ INICIO DE FUNCIONES ############

    ############ FIN DE FUNCIONES ############


    ############ INICIO DE VARIABLES DEPENDIENTES ############

    ########### FIN DE VARIABLES DEPENDIENTES ############


    ############ INICIO DE REPORT ############
    print("Generando archivo Excel")
    print("")
    print("Progreso: ")
    conn = sql.connect(mant.DATABASE)
    cursor = conn.cursor()
    instruccion = "SELECT * FROM socios"
    cursor.execute(instruccion)
    datos = cursor.fetchall()
    conn.commit()
    conn.close()

    wb = Workbook()
    ws = wb.active
    ws.title = "Socios"
    ws.append(('Nro. de socio', 'Nombre', 'DNI', 'Teléfono 1', 'Teléfono 2', 'Mail', 'Domicilio', 'Localidad', 'Código postal', 'Fecha de nacimiento', 'Fecha de alta', 'Activo'))
    for x in datos:
        nro, nom, dni, te_1, te_2, mail, dom, loc, c_p, f_n, f_a, act = x
        nro = f'{nro}'.rjust(6, '0')
        if act == 1:
            act = "SI"
        elif act == 2:
            act = "NO"
        datos_socio = (nro, nom, dni, te_1, te_2, mail, dom, loc, c_p, f_n, f_a, act)
        ws.append(datos_socio)
        counter += 1
        mant.barra_progreso(counter, len(datos), titulo=f'Morella v{mant.VERSION} - MF! Soluciones informáticas')
    print()
    os.system(f'TITLE Morella v{mant.VERSION} - MF! Soluciones informáticas')
    # Export
    try:
        wb.save(f"../reports/excel/listado_socios-{fecha}.xlsx")
        print("")
        print("Archivo creado exitosamente.")

        ############ ABRIR REPORT ############

        if errores:
            print('\n\n\n\n')
            print('     ATENCIÓN! Durante la emisión del reporte se produjeron los siguientes errores:')
            print()
            pprint(errores)
            print('\n\n\n\n')

        print("Abriendo reporte. Cierre el archivo para continuar...")
        print("")
        ruta = f'../reports/excel'
        arch = f'listado_socios-{fecha}.xlsx'
        os.chdir(ruta)
        os.system(arch)
        ruta = '../../modulos/'
        os.chdir(ruta)
    except PermissionError:
        print("")
        print("         ERROR. El archivo no pudo ser creado porque se encuentra en uso. Ciérrelo y vuelva a intentarlo.")
    except:
        mant.log_error()
        print("")
        input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
        print()
        return

            ######################################## FIN DE REPORT ############################################





    #################################################################################################################
    ############################################ MODIFICACIONES DE CAJA #############################################
    #################################################################################################################


def report_excel_modif_caja():
    ############ INICIO DE VARIABLES INDEPENDIENTES ############
    fecha = datetime.today().strftime("%Y-%m-%d")
    counter = 0
    errores = {}

    ############ FIN DE VARIABLES INDEPENDIENTES ############


    ############ INICIO DE FUNCIONES ############

    ############ FIN DE FUNCIONES ############


    ############ INICIO DE VARIABLES DEPENDIENTES ############

    ########### FIN DE VARIABLES DEPENDIENTES ############


    ############ INICIO DE REPORT ############
    print("Generando archivo Excel")
    print("")
    print("Progreso: ")
    conn = sql.connect(mant.DATABASE)
    cursor = conn.cursor()
    instruccion = "SELECT * FROM historial_caja"
    cursor.execute(instruccion)
    datos = cursor.fetchall()
    conn.commit()
    conn.close()
    wb = Workbook()
    ws = wb.active
    ws.title = "Socios"
    ws.append(('ID', 'Categoría', 'Descripción', 'Transacción', 'Ingreso', 'Egreso', 'Observación', 'Usuario que modificó', 'Fecha y hora de modificación'))
    for x in datos:
        id_caj, cat, des, tra, ing, egr, obs, usr, fyh = x
        id_u, nom, ape, tel, dom, use, pas, pri, act =  mant.buscar_usuario_por_id(usr)
        datos_reg = (id_caj, cat, des, tra, ing, egr, obs, use, fyh)
        ws.append(datos_reg)
        counter += 1
        mant.barra_progreso(counter, len(datos), titulo=f'Morella v{mant.VERSION} - MF! Soluciones informáticas')
    os.system(f'TITLE Morella v{mant.VERSION} - MF! Soluciones informáticas')    
    print("")

    # Export
    try:
        wb.save(f"../reports/excel/modificaciones_de_caja-{fecha}.xlsx")
        print("")
        print("Archivo creado exitosamente.")

        ############ ABRIR REPORT ############

        if errores:
            print('\n\n\n\n')
            print('     ATENCIÓN! Durante la emisión del reporte se produjeron los siguientes errores:')
            print()
            pprint(errores)
            print('\n\n\n\n')

        print("Abriendo reporte. Cierre el archivo para continuar...")
        print("")
        ruta = f'../reports/excel'
        arch = f'modificaciones_de_caja-{fecha}.xlsx'
        os.chdir(ruta)
        os.system(arch)
        ruta = '../../modulos/'
        os.chdir(ruta)
    except PermissionError:
        print("")
        print("         ERROR. El archivo no pudo ser creado porque se encuentra en uso. Ciérrelo y vuelva a intentarlo.")
    except:
        mant.log_error()
        print("")
        input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
        print()
        return

            ######################################## FIN DE REPORT ############################################





    #################################################################################################################
    ######################################## MOVIMIENTOS DEB. AUT. EN EXCEL #########################################
    #################################################################################################################


def report_deb_aut(mes, año):
    ############ INICIO DE VARIABLES INDEPENDIENTES ############
    fecha_hoy = datetime.today().strftime("%Y-%m-%d")
    counter = 0
    errores = {}

    ############ FIN DE VARIABLES INDEPENDIENTES ############


    ############ INICIO DE FUNCIONES ############

    ############ FIN DE FUNCIONES ############


    ############ INICIO DE VARIABLES DEPENDIENTES ############

    ########### FIN DE VARIABLES DEPENDIENTES ############


    ############ INICIO DE REPORT ############
    print("Generando archivo Excel")
    print("")
    print("Progreso: ")
    conn = sql.connect(mant.DATABASE)
    cursor = conn.cursor()
    instruccion = f"SELECT * FROM debitos_automaticos WHERE mes = '{mes}' AND año = '{año}'"
    cursor.execute(instruccion)
    datos = cursor.fetchall()
    conn.commit()
    conn.close()

    wb = Workbook()
    ws = wb.active
    ws.title = "Socios"
    ws.append(('ID', 'Categoría', 'Socio', 'Operación', 'Ingreso', 'Observación', 'Fecha', 'Usuario'))
    for x in datos:
        id_debaut, cat, socio, oper, ingr, obs, dia, mes, año, user = x
        fecha = f'{dia}/{mes}/{año}'
        usuario = mant.buscar_usuario_por_id(user)[5]
        datos_debaut = (id_debaut, cat, socio, oper, ingr, obs, fecha, usuario)
        ws.append(datos_debaut)
        counter += 1
        mant.barra_progreso(counter, len(datos), titulo=f'Morella v{mant.VERSION} - MF! Soluciones informáticas')
    os.system(f'TITLE Morella v{mant.VERSION} - MF! Soluciones informáticas')
    print()

    # Export
    try:
        wb.save(f"../reports/excel/listado_socios-{fecha_hoy}.xlsx")
        print("")
        print("Archivo creado exitosamente.")

        ############ ABRIR REPORT ############

        if errores:
            print('\n\n\n\n')
            print('     ATENCIÓN! Durante la emisión del reporte se produjeron los siguientes errores:')
            print()
            pprint(errores)
            print('\n\n\n\n')

        print("Abriendo reporte. Cierre el archivo para continuar...")
        print("")
        ruta = f'../reports/excel'
        arch = f'listado_socios-{fecha_hoy}.xlsx'
        os.chdir(ruta)
        os.system(arch)
        ruta = '../../modulos/'
        os.chdir(ruta)
    except PermissionError:
        print("")
        print("         ERROR. El archivo no pudo ser creado porque se encuentra en uso. Ciérrelo y vuelva a intentarlo.")
    except:
        mant.log_error()
        print("")
        input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
        print()
        return

            ######################################## FIN DE REPORT ############################################





    #################################################################################################################
    ############################################# LISTADO DE COBRADORES #############################################
    #################################################################################################################


def report_cobradores():
    ############ INICIO DE VARIABLES INDEPENDIENTES ############
    fecha_hoy = datetime.today().strftime("%Y-%m-%d")
    fecha = caja.obtener_fecha()
    hora = datetime.now().strftime('%H:%M')
    counter = 0
    errores = {}

    ############ FIN DE VARIABLES INDEPENDIENTES ############


    ############ INICIO DE FUNCIONES ############
    conn = sql.connect(mant.DATABASE)
    cursor = conn.cursor()
    instruccion = f"SELECT * FROM cobradores ORDER BY id"
    cursor.execute(instruccion)
    cobradores = cursor.fetchall()
    conn.commit()
    conn.close()

    ############ FIN DE FUNCIONES ############


    ############ INICIO DE VARIABLES DEPENDIENTES ############

    ########### FIN DE VARIABLES DEPENDIENTES ############


    ############ INICIO DE REPORT ############
    class PDF(FPDF):
        # Page header
        def header(self):
            # Logo
            self.image('../docs/logo_bicon.jpg', 14.5, 12, 15)
            # Arial bold 15
            self.set_font('Arial', 'B', 15)
            # Title
            self.cell(0, 20, 'LISTADO DE COBRADORES', 1, 0, 'C')
            # Arial 10
            self.set_font('Arial', '', 10)
            # Fecha
            self.cell(0, 35, f'{fecha} - {hora} hs', 0, 0, 'R')
            # Line break
            self.ln(22)
            self.set_font('Arial', 'B', 9)
            self.cell(10, 5, 'ID', 0, 0, 'L ')
            self.cell(1, 5, '', 0, 0, 'L')
            self.cell(90, 5, 'COBRADOR', 0, 1, 'L')
            self.cell(0, 1, '___________________________________________________________________________________________________________', 0, 1, 'C')
            self.ln(5)
        
        # Page footer
        def footer(self):
            # Position at 3 cm from bottom
            self.set_y(-30)
            # Arial italic 8
            self.set_font('Arial', 'I', 8)
            self.cell(0, 7, '_______________________________________________________________________________________________', 0, 1, 'C')
            # Page number
            self.cell(0, 10, 'Página ' + str(self.page_no()) + ' de {nb}', 0, 0, 'C')
            # Firma
            self.set_font('Arial', 'I', 8)
            self.cell(-10, 10, f'Reporte generado en *MORELLA v{mant.SHORT_VERSION}* by ', 0, 0, 'R')
            self.image('../docs/mf_logo.jpg', 190, 274, 8)

    # Instantiation of inherited class
    pdf = PDF()
    pdf.set_auto_page_break(True, 25)
    pdf.alias_nb_pages()
    pdf.add_page()
    for i in cobradores:
        i_d, cob = i
        pdf.cell(10, 5, f'{i_d}', 0, 0, 'L ')
        pdf.cell(1, 5, '', 0, 0, 'L')
        pdf.cell(90, 5, f'{cob}', 0, 1, 'L')
        counter += 1
        mant.barra_progreso(counter, len(cobradores), titulo=f'Morella v{mant.VERSION} - MF! Soluciones informáticas')
    print()
    os.system(f'TITLE Morella v{mant.VERSION} - MF! Soluciones informáticas')
    # Export
    pdf.output(f'../reports/temp/listado_cobradores.pdf', 'F')
        

    ############ ABRIR REPORT ############

    if errores:
        print('\n\n\n\n')
        print('     ATENCIÓN! Durante la emisión del reporte se produjeron los siguientes errores:')
        print()
        pprint(errores)
        print('\n\n\n\n')

    print("Abriendo reporte. Cierre el archivo para continuar...")
    print("")
    ruta = f'../reports/temp'
    arch = f'listado_cobradores.pdf'
    os.chdir(ruta)
    os.system(arch)
    ruta = '../../modulos/'
    os.chdir(ruta)

            ######################################## FIN DE REPORT ############################################





    #################################################################################################################
    ############################################# LISTADO DE COBRADORES #############################################
    #################################################################################################################


def report_panteones():
    ############ INICIO DE VARIABLES INDEPENDIENTES ############
    fecha_hoy = datetime.today().strftime("%Y-%m-%d")
    fecha = caja.obtener_fecha()
    hora = datetime.now().strftime('%H:%M')
    counter = 0
    errores = {}

    ############ FIN DE VARIABLES INDEPENDIENTES ############


    ############ INICIO DE FUNCIONES ############
    conn = sql.connect(mant.DATABASE)
    cursor = conn.cursor()
    instruccion = f"SELECT * FROM panteones ORDER BY id"
    cursor.execute(instruccion)
    panteones = cursor.fetchall()
    conn.commit()
    conn.close()

    ############ FIN DE FUNCIONES ############


    ############ INICIO DE VARIABLES DEPENDIENTES ############

    ########### FIN DE VARIABLES DEPENDIENTES ############


    ############ INICIO DE REPORT ############
    class PDF(FPDF):
        # Page header
        def header(self):
            # Logo
            self.image('../docs/logo_bicon.jpg', 14.5, 12, 15)
            # Arial bold 15
            self.set_font('Arial', 'B', 15)
            # Title
            self.cell(0, 20, 'LISTADO DE PANTEONES', 1, 0, 'C')
            # Arial 10
            self.set_font('Arial', '', 10)
            # Fecha
            self.cell(0, 35, f'{fecha} - {hora} hs', 0, 0, 'R')
            # Line break
            self.ln(22)
            self.set_font('Arial', 'B', 9)
            self.cell(10, 5, 'ID', 0, 0, 'L ')
            self.cell(1, 5, '', 0, 0, 'L')
            self.cell(90, 5, 'PANTEÓN', 0, 1, 'L')
            self.cell(0, 1, '___________________________________________________________________________________________________________', 0, 1, 'C')
            self.ln(5)
        
        # Page footer
        def footer(self):
            # Position at 3 cm from bottom
            self.set_y(-30)
            # Arial italic 8
            self.set_font('Arial', 'I', 8)
            self.cell(0, 7, '_______________________________________________________________________________________________', 0, 1, 'C')
            # Page number
            self.cell(0, 10, 'Página ' + str(self.page_no()) + ' de {nb}', 0, 0, 'C')
            # Firma
            self.set_font('Arial', 'I', 8)
            self.cell(-10, 10, f'Reporte generado en *MORELLA v{mant.SHORT_VERSION}* by ', 0, 0, 'R')
            self.image('../docs/mf_logo.jpg', 190, 274, 8)

    # Instantiation of inherited class
    pdf = PDF()
    pdf.set_auto_page_break(True, 25)
    pdf.alias_nb_pages()
    pdf.add_page()
    for i in panteones:
        i_d, cob = i
        pdf.cell(10, 5, f'{i_d}', 0, 0, 'L ')
        pdf.cell(1, 5, '', 0, 0, 'L')
        pdf.cell(90, 5, f'{cob}', 0, 1, 'L')
        counter += 1
        mant.barra_progreso(counter, len(panteones), titulo=f'Morella v{mant.VERSION} - MF! Soluciones informáticas')
    print()
    os.system(f'TITLE Morella v{mant.VERSION} - MF! Soluciones informáticas')
    # Export
    pdf.output(f'../reports/temp/listado_panteones.pdf', 'F')
        

    ############ ABRIR REPORT ############

    if errores:
        print('\n\n\n\n')
        print('     ATENCIÓN! Durante la emisión del reporte se produjeron los siguientes errores:')
        print()
        pprint(errores)
        print('\n\n\n\n')

    print("Abriendo reporte. Cierre el archivo para continuar...")
    print("")
    ruta = f'../reports/temp'
    arch = f'listado_panteones.pdf'
    os.chdir(ruta)
    os.system(arch)
    ruta = '../../modulos/'
    os.chdir(ruta)

            ######################################## FIN DE REPORT ############################################





    #################################################################################################################
    ############################################# LISTADO ÚLTIMO RECIBO #############################################
    #################################################################################################################


def report_ult_recibo(cobrador: int, facturacion: str):
    """Genera un reporte en Excel que contiene los datos de los últimos recibos
    impagos de cada operación de un cobrador y una facturación específicos.

    :param cobrador: id del cobrador
    :type cobrador: int

    :param facturacion: Categoría de facturación (bicon / nob)
    :type facturacion: str
    """
    ############ INICIO DE VARIABLES INDEPENDIENTES ############
    counter = 0
    errores = {}
    n_cob = rend.obtener_nom_cobrador(cobrador)
    title = f"Últimos recibos de {n_cob}"
    if len(title) > 31:
        title = f'Ult.rec.{n_cob}'[:31]
    
    ############ FIN DE VARIABLES INDEPENDIENTES ############


    ############ INICIO DE FUNCIONES ############
    def ult_rec_imp(cobrador: int, facturacion: str) -> list:
        """Retorna los siguientes datos de los últimos recibos impagos de todas
        las operaciones de un cobrador y una facturación específicos:

        - Número de socio
        - Nombre del asociado o nombre alternativo si posee
        - Número de recibo
        - Período y año
        - Importe

        :param cobrador: id del cobrador
        :type cobrador: int

        :param facturacion: Categoría de facturación (bicon / nob)
        :type facturacion: str
        
        :rtype: list

        """
        instruccion = f"""
        SELECT o.socio, s.nombre, o.nombre_alt, r.nro_recibo, r.periodo, r.año, cn.valor_mant_bicon, cn.valor_mant_nob
        FROM recibos r
        JOIN operaciones o
        ON r.operacion = o.id
        JOIN socios s
        ON o.socio = s.nro_socio
        JOIN nichos n
        ON o.nicho = n.codigo
        JOIN cat_nichos cn
        ON n.categoria = cn.id
        WHERE o.cobrador = {cobrador}
        AND r.pago = 0
        AND o.facturacion = '{facturacion}'
        AND nro_recibo IN(
            SELECT MAX(nro_recibo) 
            FROM recibos
            GROUP BY operacion
        )
        ORDER BY r.nro_recibo;
        """
        with sql.connect(mant.DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute(instruccion)
            ultimos_recibos = cursor.fetchall()
        return ultimos_recibos

    ############ FIN DE FUNCIONES ############
        

    ############ INICIO DE VARIABLES DEPENDIENTES ############
    ultimos_recibos = ult_rec_imp(cobrador, facturacion)

    ########### FIN DE VARIABLES DEPENDIENTES ############


    ############ INICIO DE REPORT ############
    print("Generando archivo Excel")
    print("")
    wb = Workbook()
    ws = wb.active
    ws.title = title
    ws.append(('Número de socio', 'Nombre asociado','Número de recibo', 'Período', 'Importe'))
    for recibo in ultimos_recibos:
        nro_soc, nombre, nombre_alt, nro_rec, periodo, año, val_mant_bic, val_mant_nob = recibo
        if nombre_alt:
            nombre = nombre_alt
        if periodo == 'Diciembre - Enero':
            periodo_recibo = f"{periodo} {año}/{int(str(año)[-2:])+1}"
        else:
            periodo_recibo = f"{periodo} {año}"
        if facturacion == 'bicon':
            importe = val_mant_bic
        elif facturacion == 'nob':
            importe = val_mant_nob
        datos_recibo = (nro_soc, nombre, nro_rec, periodo_recibo, importe)
        ws.append(datos_recibo)
        counter += 1
        mant.barra_progreso(counter, len(ultimos_recibos), titulo=f'Morella v{mant.VERSION} - MF! Soluciones informáticas')
    os.system(f'TITLE Morella v{mant.VERSION} - MF! Soluciones informáticas')
    print()

    # Export
    try:
        if ' ' in n_cob:
            n_cob = n_cob.replace(' ', '_')
        wb.save(f"../reports/excel/ultimos_recibos_{n_cob}.xlsx")
        print("")
        print("Archivo creado exitosamente.")

        ############ ABRIR REPORT ############

        if errores:
            print('\n\n\n\n')
            print('     ATENCIÓN! Durante la emisión del reporte se produjeron los siguientes errores:')
            print()
            pprint(errores)
            print('\n\n\n\n')

        print("Abriendo reporte. Cierre el archivo para continuar...")
        print("")
        ruta = f'../reports/excel'
        arch = f'ultimos_recibos_{n_cob}.xlsx'
        os.chdir(ruta)
        os.system(arch)
        ruta = '../../modulos/'
        os.chdir(ruta)
    except PermissionError:
        print("")
        print("         ERROR. El archivo no pudo ser creado porque se encuentra en uso. Ciérrelo y vuelva a intentarlo.")
    except:
        mant.log_error()
        print("")
        input("         ERROR. Comuníquese con el administrador...  Presione enter para continuar...")
        print()
        return

            ######################################## FIN DE REPORT ############################################
