#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import sys
import pygtk

try:
    pygtk.require("2.0")
except:
    print "Versión de PyGTK incorrecta!\n"
    sys.exit(1)

import gtk

class MainWindowMethods(object):
    """
    Clase que contiene los métodos de la ventana principal
    """
    def __init__(self, logic):
        """
        Carga y conecta el XML de gtkBuilder, además de mostrar la ventana
        principal
        """
        self.builder = gtk.Builder()
        self.builder.add_from_file("jsoninspector.glade")
        self.builder.connect_signals(self)

        # Prepara los renderizados de columna y las asigna a los valores
        cell = gtk.CellRendererText()
        columns = self.builder.get_object("treeviewcolumn1")
        columns.pack_start(cell)
        columns.add_attribute(cell, 'text', 0)
        treeview = self.builder.get_object("treeview1")
        # Esta columna es la que tiene los nodos de apertura y cierre
        treeview.set_expander_column(columns)

        cell = gtk.CellRendererText()
        columns = self.builder.get_object("treeviewcolumn2")
        columns.pack_start(cell)
        columns.add_attribute(cell, 'text', 1)

        cell = gtk.CellRendererText()
        columns = self.builder.get_object("treeviewcolumn3")
        columns.pack_start(cell)
        columns.add_attribute(cell, 'text', 2)

        # Obtenemos la ventana y la mostramos completamente
        self.window = self.builder.get_object("MainWindow")
        self.window.show_all()

        # Obtenemos un enlace al objeto de lógica de aplicación
        self.logicObj = logic

    def onOpenMenuClicked(self, event):
        """
        El usuario ha presionado Abrir en el menu
        """
        # Creamos el dialogo de abrir fichero
        chooser = gtk.FileChooserDialog(title=None,
                                        action=gtk.FILE_CHOOSER_ACTION_OPEN,
                                        buttons=(gtk.STOCK_CANCEL,
                                        gtk.RESPONSE_CANCEL,
                                        gtk.STOCK_OPEN,
                                        gtk.RESPONSE_OK))
        chooser.set_default_response(gtk.RESPONSE_OK)

        # Lo lanzamos
        response = chooser.run()

        # Si hemos seleccionado un fichero, lo cargamos
        if response == gtk.RESPONSE_OK:
            filename = chooser.get_filename()
            label = self.builder.get_object("StatusLabel")

            # Según todo haya ido, actualizamos la barra de estado 
            if self.logicObj.loadjson(filename):
                
                label.set_text(filename)
                treeStore = self.builder.get_object("treestore1")
                treeStore.clear()
                self.logicObj.loadTree(treeStore)
                
            else:
                
                label.set_text("No hay JSON cargado")

        # Nos deshacemos del dialogo
        chooser.destroy()

    def onCopyJSONClicked(self, widget):
        """
        Se ha pulsado Copiar JSON
        """
        # Mostrar la ventana de texto
        textWindow = self.builder.get_object("TextWindow")
        textWindow.show_all()

    def onCopyJSONDelete(self, widget, event):
        """
        Se ha dado a cerrar la ventana de copiar texto
        """
        textWindow = self.builder.get_object("TextWindow")
        textWindow.hide()

        return True

    def onCopyJSONDestroy(self, widget):
        """
        Se ha cerrado la ventana
        """
        textWindow = self.builder.get_object("TextWindow")
        textWindow.hide()

        return True

    def onCopyJSONAcceptClicked(self, widget):
        """
        Se ha aceptado el código
        """
        textView = self.builder.get_object("textview1")
        jsonBuffer = textView.get_buffer()
        jsonText = jsonBuffer.get_text(jsonBuffer.get_start_iter(),
                                       jsonBuffer.get_end_iter())

        textWindow = self.builder.get_object("TextWindow")
        textWindow.hide()
        treestore = self.builder.get_object("treestore1")
        treestore.clear()

        if self.logicObj.loadJSONText(jsonText):
            
            status_label = self.builder.get_object("StatusLabel") 
            status_label.set_text("Cargado desde portapapeles.")
            self.logicObj.loadTree(treestore)

    def onCopyJSONCancelClicked(self, widget):
        """
        Se ha cancelado
        """
        textWindow = self.builder.get_object("TextWindow")
        textWindow.hide()

    def onExitMenuClicked(self, widget):
        """
        Se ha pulsado salir
        """
        gtk.main_quit()
        sys.exit(0)

    def onMainWindowDelete(self, widget, event):
        """
        Se ha destruido o mandado cerrar la ventana principal
        """
        gtk.main_quit()
        sys.exit(0)


class LogicObject(object):
    """
    Esta clase define un objeto que mantiene la lógica interna del programa y
    nos permite un acceso a las variables principales
    """
    def __init__(self):
        self.json = None

    def loadjson(self, filename):
        """
        Carga un fichero JSON y crea el objeto respectivo
        """
        f = open(filename, 'r')
        try:
            self.json = json.loads(f.read())
        except ValueError:
            print "JSON no válido!\n"
            self.json = None
            f.close()

            return False

        f.close()
        return True

    def loadJSONText(self, text):
        """
        Carga un texto JSON
        """
        try:
            self.json = json.loads(text)
        except ValueError:
            print "JSON no válido"
            self.json = None
            
            return False

        return True

    def loadTree(self, treestore):
        """
        Carga el JSON en el tree store para mostrarlo
        """
        for key_val in self.json.keys():

            # Si el elemento contiene un diccionario
            if type(self.json[key_val]) is dict:

                # Añadimos el nodo, y obtenemos la referencia
                parent_node = treestore.append(None, [str(key_val), "", ""])
                # De manera recursiva, entramos en el diccionario y obtenemos
                # los nodos, añadidos como hijos de este
                self._loadTreeRec(treestore, self.json[key_val], parent_node)

            else:

                # Tenemos un nodo hoja, obtenemos el valor y el tipo y lo
                # añadimos
                treestore.append(None, [str(key_val), 
                                        str(self.json[key_val]),
                                        str(type(self.json[key_val]))])

    def _loadTreeRec(self, treestore, elems, parent_node):
        """
        Adición recursiva de elementos al árbol
        """
        for key_val in elems.keys():

            # Si el elemento contiene un diccionario
            if type(elems[key_val]) is dict:

                # Añadimos el nodo, y obtenemos la referencia
                new_parent_node = treestore.append(parent_node, 
                                                   [str(key_val),
                                                   "", ""])
                # De manera recursiva, entramos en el diccionario y obtenemos
                # los nodos, añadidos como hijos de este
                self._loadTreeRec(treestore, elems[key_val], new_parent_node)

            else:

                # Tenemos un nodo hoja, obtenemos el valor y el tipo y lo
                # añadimos
                treestore.append(parent_node, [str(key_val), 
                                               str(elems[key_val]),
                                               str(type(elems[key_val]))])


# Ejecucion del programa principal

if __name__ == "__main__":

    logicObject = LogicObject()
    mainWindow = MainWindowMethods(logicObject)
    gtk.main()
