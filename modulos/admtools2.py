from PySide6.QtWidgets import (QApplication, QWidget, QPushButton, QMainWindow, QVBoxLayout, QHBoxLayout, 
QLabel, QLineEdit, QComboBox, QMessageBox, QFormLayout, QTableWidget, QTableWidgetItem, QHeaderView)
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QPixmap
from datetime import datetime, date
import psycopg2 as sql
import psycopg2.errors
from funciones_mantenimiento import VERSION

def obtener_database():
    arch = open("../databases/database.ini", "r")
    db = arch.readline()
    arch.close()
    return db
DATABASE = str(obtener_database())
HOY = datetime.now().date()
FECHA_NOB = date(year=2022, month=8, day=1)
FECHA_BICON = date(year=2022, month=9, day=1)

# Cambio de indentificador de aplicación
try:
    from ctypes import windll
    myappid = f'mfsolucionesinformaticas.morella.admtools.{VERSION}'
    windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except ImportError:
    pass

class Ventana(QMainWindow):
    _op_cobol_ingr = ''
    _op_morella_ingr = ''
    _facturacion = ''
    _pago_mes_ingr = ''
    _pago_año_ingr = ''
    _pago_año_ingr = ''
    _pago_año_ingr = ''
    _pago_año_ingr = ''
    _pago_año_ingr = ''

    def __init__(self):
        super().__init__()
        self.setWindowTitle(f'Registrar cambio en estado de cuenta manual    |   Morella v{VERSION} Admin Tools v2.1')
        self.setWindowIcon(QIcon('../docs/logo_morella.png'))
        self.setFixedSize(800, 400)
        self.componente_general = QWidget(self)
        self.setCentralWidget(self.componente_general)
        self.layout_principal = QVBoxLayout()
        self.componente_general.setLayout(self.layout_principal)
        self.mf_sol = QLabel('MF! Soluciones Informáticas')
        self.mf_sol.setAlignment(Qt.AlignRight)
        self.mf_sol.setStyleSheet("QLabel { color: gray}")
        # PUBLICACIÓN CAMPOS
        self._form_busqueda()
        self._form_registrar()
        self.layout_principal.addWidget(self.mf_sol)
        # CONEXIÓN DE SEÑALES
        self._conectar_eventos()
    
    def _calcular_mes(self, periodo):
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
        return f"{mes}".rjust(2, '0')

    def _days_between(self, d1, d2):
        return abs(d2-d1).days

    def _cuot_fav(self, d1, d2):
        return (d2-d1).days

    def _calcular_ult_pago(self, ult_mes_pag):
        if ult_mes_pag == '01':
            return 'Enero - Febrero'
        elif ult_mes_pag == '02':
            return 'Febrero - Marzo'
        elif ult_mes_pag == '03':
            return 'Marzo - Abril'
        elif ult_mes_pag == '04':
            return 'Abril - Mayo'
        elif ult_mes_pag == '05':
            return 'Mayo - Junio'
        elif ult_mes_pag == '06':
            return 'Junio - Julio'
        elif ult_mes_pag == '07':
            return 'Julio - Agosto'
        elif ult_mes_pag == '08':
            return 'Agosto - Septiembre'
        elif ult_mes_pag == '09':
            return 'Septiembre - Octubre'
        elif ult_mes_pag == '10':
            return 'Octubre - Noviembre'
        elif ult_mes_pag == '11':
            return 'Noviembre - Diciembre'
        elif ult_mes_pag == '12':
            return 'Diciembre - Enero'
    
    def _form_busqueda(self):
        self.tit_busqueda = QLabel('Buscar :')
        fuente = self.tit_busqueda.font()
        fuente.setUnderline(1)
        self.tit_busqueda.setStyleSheet("QLabel { color: gray}")
        self.tit_busqueda.setFont(fuente)
        self.layout_busqueda = QFormLayout()
        # Campo Nro. de Op. COBOL
        self.op_cobol_label = QLabel("Nro. de Op. COBOL: ")
        self.op_cobol_label.setFixedWidth(120)
        self.op_cobol_line = QLineEdit()
        self.op_cobol_line.setMaxLength(5)
        self.op_cobol_line.setFixedWidth(100)
        # Botón Buscar
        self.boton_buscar = QPushButton('Buscar')
        self.boton_buscar.setFixedWidth(50)
        # Layout buscar
        self.layout_buscar = QHBoxLayout()
        self.layout_buscar.addWidget(self.op_cobol_line)
        self.layout_buscar.addWidget(self.boton_buscar)
        # Campo Resultados
        self.resultados_label = QLabel("Resultados: ")
        self.resultados_label.setFixedWidth(120)
        self.resultados_tabla = QTableWidget()
        self.resultados_tabla.setColumnCount(7)
        header = self.resultados_tabla.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeToContents)
        self.resultados_tabla.setHorizontalHeaderLabels([
            'Op. Morella', 'Facturación', 'Último pago', 'Cuotas favor', 'Op. Cobol', 'Nombre', 'Domicilio'
            ])
        # Publicación de campos
        self.layout_busqueda.addRow(self.op_cobol_label, self.layout_buscar)
        self.layout_busqueda.addRow(self.resultados_label, self.resultados_tabla)
        self.layout_busqueda.addRow(QLabel(""))
        # Publicación del layout
        self.layout_principal.addWidget(self.tit_busqueda)
        self.layout_principal.addLayout(self.layout_busqueda)

    def _form_registrar(self):
        self.tit_registrar = QLabel('Registrar :')
        fuente = self.tit_registrar.font()
        fuente.setUnderline(1)
        self.tit_registrar.setStyleSheet("QLabel { color: gray}")
        self.tit_registrar.setFont(fuente)
        self.layout_registrar = QFormLayout()
        # Campo Nro. Op. Morella
        self.op_morella_label = QLabel('Nro. Op. Morella: ')
        self.op_morella_label.setFixedWidth(120)
        self.op_morella_line = QLineEdit()
        self.op_morella_line.setMaxLength(6)
        self.op_morella_line.setFixedWidth(100)
        # Campo Facturación
        self.facturacion_label = QLabel('Facturación: ')
        self.facturacion_label.setFixedWidth(120)
        self.facturacion_list= QComboBox()
        self.facturacion_list.setFixedWidth(100)
        self.facturacion_list.setPlaceholderText('---------------------')
        self.facturacion_list.addItems(['Bicon', 'NOB'])
        # Campo Pago
        self.pago_label = QLabel('Último pago: ')
        self.pago_label.setFixedWidth(120)
        self.mes_line = QLineEdit()
        self.mes_line.setMaxLength(2)
        self.mes_line.setFixedWidth(30)
        self.mes_line.setPlaceholderText('Mes')
        self.barra_fecha = QLabel('/')
        self.barra_fecha.setFixedWidth(5)
        self.año_line = QLineEdit()
        self.año_line.setMaxLength(4)
        self.año_line.setFixedWidth(60)
        self.año_line.setPlaceholderText('Año')
        self.boton_registrar = QPushButton('Registrar pago')
        self.boton_registrar.setFixedWidth(100)
        self.pago_layout = QHBoxLayout()
        # Publicación de campos
        self.pago_layout.addWidget(self.mes_line)
        self.pago_layout.addWidget(self.barra_fecha)
        self.pago_layout.addWidget(self.año_line)
        self.pago_layout.addWidget(self.boton_registrar)
        self.layout_registrar.addRow(self.op_morella_label, self.op_morella_line)
        self.layout_registrar.addRow(self.facturacion_label, self.facturacion_list)
        self.layout_registrar.addRow(self.pago_label, self.pago_layout)
        # Publicación del layout
        self.layout_principal.addWidget(self.tit_registrar)
        self.layout_principal.addLayout(self.layout_registrar)

    def _conectar_eventos(self):
        self.op_cobol_line.returnPressed.connect(self._buscar_db)
        self.boton_buscar.clicked.connect(self._buscar_db)
        self.op_morella_line.returnPressed.connect(self._registrar_pago)
        self.mes_line.returnPressed.connect(self._registrar_pago)
        self.año_line.returnPressed.connect(self._registrar_pago)
        self.boton_registrar.clicked.connect(self._registrar_pago)
        
    def _buscar_db(self):
        try:
            # Recuperación del Nro. de Op. de Cobol ingresado por el usuario
            self._op_cobol_ingr = int(self.op_cobol_line.text())
            # Búsqueda del dato ingresado en la base de datoas
            conn = sql.connect(DATABASE)
            cursor = conn.cursor()
            cursor.execute(f"SELECT id, facturacion, ult_pago, ult_año, cuotas_favor, op_cobol, nombre_alt, domicilio_alt FROM operaciones WHERE op_cobol={self._op_cobol_ingr}")
            self.datos_tabla = cursor.fetchall()
            conn.commit()
            conn.close()
            # Despliegue de los datos obtenidos desde la base de datos dentro de la tabla
            if self.datos_tabla:
                self.resultados_tabla.setRowCount(len(self.datos_tabla))
                for i in range(len(self.datos_tabla)):
                    ult_mes_pago = self._calcular_mes(self.datos_tabla[i][2])
                    ult_pago = f"{ult_mes_pago}/{self.datos_tabla[i][3]}"

                    col1 = QTableWidgetItem(str(self.datos_tabla[i][0]).rjust(6, '0'))
                    col2 = QTableWidgetItem(str(self.datos_tabla[i][1]))
                    col3 = QTableWidgetItem(str(ult_pago))
                    col4 = QTableWidgetItem(str(self.datos_tabla[i][4]))
                    col5 = QTableWidgetItem(str(self.datos_tabla[i][5]))
                    col6 = QTableWidgetItem(str(self.datos_tabla[i][6]))
                    col7 = QTableWidgetItem(str(self.datos_tabla[i][7]))

                    self.resultados_tabla.setItem(i, 0, col1)
                    self.resultados_tabla.setItem(i, 1, col2)
                    self.resultados_tabla.setItem(i, 2, col3)
                    self.resultados_tabla.setItem(i, 3, col4)
                    self.resultados_tabla.setItem(i, 4, col5)
                    self.resultados_tabla.setItem(i, 5, col6)
                    self.resultados_tabla.setItem(i, 6, col7)

                    col1.setFlags(Qt.ItemIsEnabled)
                    col2.setFlags(Qt.ItemIsEnabled)
                    col3.setFlags(Qt.ItemIsEnabled)
                    col4.setFlags(Qt.ItemIsEnabled)
                    col5.setFlags(Qt.ItemIsEnabled)
                    col6.setFlags(Qt.ItemIsEnabled)
                    col7.setFlags(Qt.ItemIsEnabled)
            else:
                # AVISO DE OPERACIÓN INEXISTENTE
                QMessageBox.warning(self, 'ERROR!', f'No se encontró ninguna operacion con el número {self._op_cobol_ingr}')
                    
        except ValueError:
            QMessageBox.warning(self, 'ERROR!', 'El dato solicitado debe ser de tipo numérico.')
        except sql.OperationalError:
            QMessageBox.warning(self, 'ERROR!', 'No fue posible conectarse a la base de datos.')

    def _registrar_pago(self):
        try:
            # Recuperación de los datos del último pago ingresados por el usuario
            self._op_morella_ingr = int(self.op_morella_line.text())
            self._facturacion = self.facturacion_list.currentText().lower()
            self._pago_mes_ingr = str(int(self.mes_line.text())).rjust(2, '0')
            self._pago_año_ingr = str(int(self.año_line.text())).rjust(3, '0').rjust(4, '2')
            # Cáculo de la información necesaria para el registro en la base de datos
            fup_date = date(year = int(self._pago_año_ingr), month = int(self._pago_mes_ingr), day = 1) # A PARTIR DE LA FECHA GENERA UN DATE DEL PRIMER DIA DE ESE MES
            cuenta = int(self._days_between(HOY, fup_date)/730)   # CALCULA DIFERENCIA CON HOY EN PERIODOS BIANUALES
            calculo = float(self._cuot_fav(HOY, fup_date)*6/365)  # CALCULA DIFERENCIA CON HOY EN BIMESTRES
            ult_pago = self._calcular_ult_pago(self._pago_mes_ingr)  # CALCULA EL ULT_PAGO (STRING BIMENSUAL)
            fecha_ult_pago = f"{self._pago_mes_ingr}/{self._pago_año_ingr}"   # FECHA_ULT_PAGO
            if cuenta > 0:  # SENTENCIA IF QUE 
                moroso = 1  # CALCULA SI LA OP
            else:           # ES MOROSA (1) O
                moroso = 0  # NO LO ES (0)
            cuotas_favor = round(calculo)
            if cuotas_favor < 1:
                cuotas_favor = 0
            else:
                if HOY.month % 2 == 0 and self._facturacion == 'nob':
                    cuotas_favor += 1
                elif HOY.month % 2 == 1 and self._facturacion == 'bicon':
                    cuotas_favor += 1
            if not self._facturacion:
                raise TypeError
            # TRASPASO A BASE DE DATOS
            conn = sql.connect(DATABASE)
            cursor = conn.cursor()
            instruccion = f"UPDATE operaciones SET ult_pago = '{ult_pago}', ult_año = '{self._pago_año_ingr}', fecha_ult_pago = '{fecha_ult_pago}', moroso = {moroso}, cuotas_favor = {cuotas_favor} WHERE id = {self._op_morella_ingr}"
            cursor.execute(instruccion)
            conn.commit()
            conn.close()
            # BÚSQUEDA DE DATOS CARGADOS EN LA BASE DE DATOS
            conn = sql.connect(DATABASE)
            cursor = conn.cursor()
            instruccion = f"SELECT * FROM operaciones WHERE id = {self._op_morella_ingr}"
            cursor.execute(instruccion)
            datos = cursor.fetchall()
            conn.commit()
            conn.close()
            if datos:
                # CÁLCULO DE DEUDA PREVIA A MORELLA
                i_d, soc, nic, fac, cob, tar, rut, ult, u_a, fec, mor, c_f, u_r, paga, op_cob, nom_alt, dom_alt = datos[0]
                fup_date = date(year=int(fec[3:]), month=int(fec[:2]), day=1)
                if fac == 'bicon':
                    fecha_calc = FECHA_BICON
                elif fac == 'nob':
                    fecha_calc = FECHA_NOB
                cuenta = int(self._cuot_fav(fup_date, fecha_calc)/365*6)
                if cuenta < 1:
                    pass
                else:
                    c_f = -cuenta
                    with sql.connect(DATABASE) as conn:
                        cursor = conn.cursor()
                        cursor.execute(
                            f"""
                            UPDATE operaciones SET cuotas_favor = {c_f} WHERE id = {i_d}
                            """
                        )
                # AVISO DE TRASPASO CORRECTO
                aviso_ok = QMessageBox(self)
                aviso_ok.setWindowTitle('Pago registrado correctamente')
                aviso_ok.setText('La última fecha de pago fue actualizada satisfactoriamente.')
                aviso_ok.setIconPixmap(QPixmap("../docs/ok.png"))
                aviso_ok.exec()
            else:
                # AVISO DE OPERACIÓN INEXISTENTE
                QMessageBox.warning(self, 'ERROR!', f'No se encontró ninguna operacion con el número {str(self._op_morella_ingr).rjust(6, "0")}')
        except ValueError:
            QMessageBox.warning(self, 'ERROR!', 'Los datos solicitados deben ser de tipo numérico.')
        except sql.OperationalError:
            QMessageBox.warning(self, 'ERROR!', 'No fue posible conectarse a la base de datos. No se han registrado cambios.')            
        except TypeError:
            QMessageBox.warning(self, 'ERROR!', 'Todos los campos son obligatorios.')
            

if __name__ == '__main__':
    app = QApplication()
    ventana = Ventana()
    ventana.show()
    app.exec()