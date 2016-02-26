__author__ = 'Yanesita&Machy'

from PyQt5.QtGui import *
from PyQt5.QtWidgets import (QApplication, QGridLayout, QLabel, QLineEdit,
        QVBoxLayout, QMainWindow, QGroupBox, QRadioButton, QPushButton, QSpinBox,QTableWidgetItem)
from PyQt5.QtCore import  *
from PyQt5.QtSvg import *
import Utils
from PyQt5 import uic
import sys


class MainWindowsInicial(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self,parent)
        self.ui = uic.loadUi("inicial.ui",self)
        self.ui.buttonBox.accepted.connect(self.ok)
        self.ui.buttonBox.rejected.connect(self.cancel)
        self.ui.radioButton_2.toggled.connect(self.set_mochila)
        self.es_mochila=True

    def set_mochila(self,valor):
        self.es_mochila= valor

    def ok(self):
        inf= MainWindowsInformacion(self.es_mochila)
        inf.show()
        self.close()

    def cancel(self):
        self.close()

class MainWindowsInformacion(QMainWindow):
    def __init__(self, es_mochila ,parent=None):
        QMainWindow.__init__(self,parent)
        self.ui = uic.loadUi("informacion.ui",self)
        self.ui.buttonBox.accepted.connect(self.ok)
        self.ui.buttonBox.rejected.connect(self.cancel)
        self.ui.radioButton_2.toggled.connect(self.set_maximizar)
        self.ui.spinBox.valueChanged.connect(self.set_variables)
        self.ui.spinBox_2.valueChanged.connect(self.set_cant_rest)
        self.es_mochila=es_mochila
        if self.es_mochila:
            self.ui.radioButton.setEnabled(False)
            self.ui.spinBox_2.setMaximum(1)
        self.es_maximizar=True
        self.cant_var=1
        self.cant_rest=1

    def set_maximizar(self,valor):
        self.es_maximizar=valor

    def set_variables(self,valor):
        self.cant_var=valor

    def set_cant_rest(self,valor):
        self.cant_rest=valor
        #self.ui.label_5.setText(str(cant_rest))

    def ok(self):
        dat= MainWindowsDatos(self.es_mochila,self.es_maximizar,self.cant_var,self.cant_rest)
        dat.show()
        self.close()

    def cancel(self):
        self.close()

class MainWindowsDatos(QMainWindow):
    def __init__(self,es_mochila,es_maximizar,cant_var,cant_rest,parent=None):
        QMainWindow.__init__(self,parent)
        self.ui = uic.loadUi("datos.ui",self)
        self.ui.buttonBox.accepted.connect(self.ok)
        self.ui.buttonBox.rejected.connect(self.cancel)
        self.rest={}
        self.fo=[]
        self.es_mochila=es_mochila
        self.es_maximizar=es_maximizar
        self.cant_var=cant_var
        self.cant_rest=cant_rest
        self.termInd=[]
        self.init_tabla()

    def init_tabla(self):
        self.restTable.clear()
        self.restTable.setColumnCount(self.cant_var + 2)
        self.restTable.setHorizontalHeaderLabels(
            ['x%d' % i for i in range(self.cant_var)] + ['--', 'Peso Total'])
        self.restTable.setRowCount(self.cant_rest)
        self.restTable.setVerticalHeaderLabels(['r%d' % i for i in range(self.cant_rest)])
        for x in range(self.cant_rest):
            item2 = QTableWidgetItem(str('<='))
            for y in range(self.cant_var + 2):
                item = QTableWidgetItem(str(0))
                if y == self.cant_var:
                    item2.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    self.restTable.setItem(x, y, item2)
                    continue
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.restTable.setItem(x, y, item)

        self.foTable.clear()
        self.foTable.setColumnCount(self.cant_var)
        self.foTable.setHorizontalHeaderLabels(
            ['x%d' % i for i in range(self.cant_var)])
        self.foTable.setRowCount(1)
        self.foTable.setVerticalHeaderLabels(['z='])
        for x in range(self.cant_var):
            item = QTableWidgetItem(str(0))
            item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.foTable.setItem(0, x, item)

    def ok(self):
        for x in range(self.cant_rest):
            self.rest[x]=[]
            for y in range(self.cant_var):
                a=self.restTable.item(x,y)
                if a:
                    self.rest[x].append(int(a.text()))
            self.termInd.append(int(self.restTable.item(x,self.cant_var+1).text()))
        for x in range(self.cant_var):
                a=self.foTable.item(0,x)
                if a:
                    self.fo.append(int(a.text()))
        alg= MainWindowsAlgoritmos(self.es_mochila,self.es_maximizar,self.cant_rest,self.fo,self.rest,self.termInd)
        alg.show()
        self.close()

    def cancel(self):
        self.close()

class MainWindowsAlgoritmos(QMainWindow):
    def __init__(self,es_mochila,es_maximizar,cant_rest,fo,rest,termInd, parent=None):
        QMainWindow.__init__(self,parent)
        self.ui = uic.loadUi("algoritmos.ui",self)
        self.algoritmo=0
        self.ui.buttonBox.accepted.connect(self.ok)
        self.ui.buttonBox.rejected.connect(self.cancel)
        self.ui.radioButton.toggled.connect(self.balas)
        self.ui.radioButton_2.toggled.connect(self.greedy)
        self.ui.radioButton_5.toggled.connect(self.genetico)
        self.es_mochila=es_mochila
        self.es_maximizar=es_maximizar
        if not self.es_mochila:
            self.ui.radioButton_2.setEnabled(False)
            self.ui.radioButton_5.setEnabled(False)
        self.cant_rest=cant_rest
        self.fo=fo
        self.rest=rest
        self.termInd=termInd

    def balas(self,valor):
        if valor: self.algoritmo=0

    def greedy(self,valor):
        if valor: self.algoritmo=1

    def genetico(self,valor):
        if valor: self.algoritmo=2

    def ok(self):
        if self.algoritmo==0:
            m=MainWindowsAlgoritmoBalas(self.fo,self.rest,self.termInd, es_maximizar=self.es_maximizar,es_mochila=self.es_mochila)
            m.show()
        if self.algoritmo==1:
            m=MainWindowsAlgoritmoGreedy(self.fo,self.rest[0],self.termInd[0])
            m.show()
        elif self.algoritmo==2:
            m=MainWindowsAlgoritmoGenetico(self.fo,self.rest[0],self.termInd[0])
            m.show()
        self.close()

    def cancel(self):
        self.close()

class MainWindowsAlgoritmoGenetico(QMainWindow):
    def __init__(self,fo,rest,termInd, parent=None):
        QMainWindow.__init__(self,parent)
        self.ui = uic.loadUi("solucion_genetico.ui",self)
        self.tipo_sel=0
        self.tipo_emp=0
        self.tipo_cruz=0
        self.cant_gen=1
        self.cant_ind=2
        self.fo=fo
        self.rest=rest
        self.termInd=termInd
        self.ui.buttonBox.accepted.connect(self.ok)
        self.ui.buttonBox.rejected.connect(self.cancel)
        self.ui.s_ruleta.toggled.connect(self.set_seleccion_ruleta)
        self.ui.s_todos_un_hijo.toggled.connect(self.set_seleccion_tuh)
        self.ui.e_por_orden.toggled.connect(self.set_emparejamiento_por_orden)
        self.ui.e_ruleta.toggled.connect(self.set_emparejamiento_ruleta)
        self.ui.c_cruz_simple.toggled.connect(self.set_cruzamiento_simple)
        self.ui.c_cruz_unif.toggled.connect(self.set_cruzamiento_uniforme)
        self.ui.gener.valueChanged.connect(self.set_generaciones)
        self.ui.ind.valueChanged.connect(self.set_poblacion)
        self.set_fo()
        self.set_rest()

    def set_fo(self):
        s=str(self.fo[0])+'x0 '
        for x in range(1,len(self.fo),1):
            s+= '+'+str(self.fo[x])+'x%d '% x
        self.ui.fo_label.setText(s)

    def set_rest(self):
        s=str(self.rest[0])+'x0 '
        for x in range(1,len(self.rest),1):
            s+= '+'+str(self.rest[x])+'x%d '% x
        s+='<='+ str(self.termInd)
        self.ui.rest_label.setText(s)

    def set_seleccion_ruleta(self,valor):
        if valor:
            self.tipo_sel=0

    def set_seleccion_tuh(self,valor):
        if valor:
            self.tipo_sel=1

    def set_emparejamiento_por_orden(self,valor):
        if valor:
            self.tipo_emp=0

    def set_emparejamiento_ruleta(self,valor):
        if valor:
            self.tipo_emp=1

    def set_cruzamiento_simple(self,valor):
        if valor:
            self.tipo_cruz=0

    def set_cruzamiento_uniforme(self,valor):
        if valor:
            self.tipo_cruz=1

    def set_generaciones(self,valor):
        self.cant_gen=valor

    def set_poblacion(self,valor):
        self.cant_ind=valor

    def ok(self):
        u = Utils.Utils()
        import time
        t=time.time()
        sol=u.algoritmo_genetico(cant_ind=self.cant_ind,cant_var=len(self.fo),fo=self.fo,rest=self.rest,
                                 c=self.termInd,cant_gen=self.cant_gen,tipo_seleccion=self.tipo_sel,
                                 tipo_emparejamiento=self.tipo_emp,tipo_cruzamiento=self.tipo_cruz)
        self.optimo=sol[0]
        self.ui.optimo_label.setText(str(self.optimo))
        t=int(time.time()-t)
        self.ui.tiempo.setText(str(t)+'ms')
        aux=sol[1]
        s=''
        for x in range(len(aux)):
            s+= 'x%d' % x +'='+str(aux[x] )+'  '
        self.ui.sol.setText(s)
        self.ui.cant_g.setText(str(sol[2]))
        #self.close()

    def set_valor_optimo(self):
        self.ui.optimo.setText(str(self.optimo))

    def cancel(self):
        self.close()

class MainWindowsAlgoritmoGreedy(QMainWindow):
    def __init__(self,fo,rest,termInd, parent=None):
        QMainWindow.__init__(self,parent)
        self.ui = uic.loadUi("solucion_greedy.ui",self)
        self.tipo_estrategia=0
        self.fo=fo
        self.rest=rest
        self.termInd=termInd
        self.ui.buttonBox.accepted.connect(self.ok)
        self.ui.buttonBox.rejected.connect(self.cancel)
        self.ui.peso_radioButton.toggled.connect(self.set_estrategia_peso)
        self.ui.valor_radioButton.toggled.connect(self.set_estrategia_valor)
        self.ui.vp_radioButton.toggled.connect(self.set_estrategia_vp)
        self.set_fo()
        self.set_rest()

    def set_fo(self):
        s=str(self.fo[0])+'x0 '
        for x in range(1,len(self.fo),1):
            s+= '+'+str(self.fo[x])+'x%d '% x
        self.ui.fo_label.setText(s)

    def set_rest(self):
        s=str(self.rest[0])+'x0 '
        for x in range(1,len(self.rest),1):
            s+= '+'+str(self.rest[x])+'x%d '% x
        s+='<='+ str(self.termInd)
        self.ui.rest_label.setText(s)

    def set_estrategia_peso(self,valor):
        if valor:
            self.tipo_estrategia=1

    def set_estrategia_valor(self,valor):
        if valor:
            self.tipo_estrategia=0

    def set_estrategia_vp(self,valor):
        if valor:
            self.tipo_estrategia=2

    def ok(self):
        u = Utils.Utils()
        import time
        t=time.time()
        vp=[]
        for x in range(len(self.fo)):
            vp.append(self.fo[x]/self.rest[x])
        sol=u.mochila_alg({0:self.fo,1:self.rest,2:vp},self.tipo_estrategia,self.termInd)
        self.optimo=sol[1]
        self.ui.optimo_label.setText(str(self.optimo))
        t=int(time.time()-t)
        self.ui.tiempo.setText(str(t)+'ms')
        aux=sol[0]
        s=''
        for x in range(len(self.fo)):
            if x in aux:
                s+= 'x%d' % x +'='+str(1)+'  '
            else:
                s+= 'x%d' % x +'='+str(0)+'  '
        self.ui.sol.setText(s)
        #self.close()

    def set_valor_optimo(self):
        self.ui.optimo.setText(str(self.optimo))

    def cancel(self):
        self.close()

class MainWindowsAlgoritmoBalas(QMainWindow):
    def __init__(self,fo,rest,termInd,es_maximizar,es_mochila, parent=None):
        QMainWindow.__init__(self,parent)
        self.ui = uic.loadUi("solucion_balas.ui",self)
        self.es_mochila=es_mochila
        self.es_maximizar=es_maximizar
        self.fo=fo
        self.rest=rest
        self.termInd=termInd
        self.ui.buttonBox.accepted.connect(self.ok)
        self.ui.buttonBox.rejected.connect(self.cancel)
        self.set_fo()
        self.set_rest()

    def set_fo(self):
        s=str(self.fo[0])+'x0 '
        for x in range(1,len(self.fo),1):
            s+= '+'+str(self.fo[x])+'x%d '% x
        self.ui.fo_label.setText(s)

    def set_rest(self):
        s=''
        for x in range(len(self.rest.keys())):
            s+=str(self.rest[x][0])+'x0 '
            for y in range(1,len(self.rest[x]),1):
                s+= '+'+str(self.rest[x][y])+'x%d '% y
            s+='<='+ str(self.termInd[x])+ ' \n '
        self.ui.rest_label.setText(s)

    def ok(self):
        u = Utils.Utils()
        import time
        t=time.time()
        datos=u.estandarizando(self.es_maximizar,self.fo,self.rest,self.termInd)
        sol=u.algoritmo_balas(datos[0])
        self.ui.optimo_label.setText(str(sol[0]+datos[0]['z']))
        t=int(time.time()-t)
        self.ui.tiempo.setText(str(t)+'ms')
        aux=sol[1]
        variables=datos[1]
        var_sol=[]
        for x in aux.keys():
            var_sol.append(aux[x])
        s=''
        for x in range(len(self.fo)):
            if x in var_sol and x in variables:
                s+= 'x%d' % x +'='+str(0)+'  '
            elif x in var_sol and not x in variables:
                s+= 'x%d' % x +'='+str(1)+'  '
            elif x not in var_sol and not x in variables:
                s+= 'x%d' % x +'='+str(0)+'  '
            elif x not in var_sol and x in variables:
                s+= 'x%d' % x +'='+str(1)+'  '
        self.ui.sol.setText(s)
        #self.close()

    def set_valor_optimo(self):
        self.ui.optimo.setText(str(self.optimo))

    def cancel(self):
        self.close()

app = QApplication(sys.argv)
m = MainWindowsInicial()
m.show()
app.exec_()

