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

        cell = gtk.CellRendererText()
        columns = self.builder.get_object("treeviewcolumn1")
        columns.pack_start(cell)
        columns.add_attribute(cell, 'text', 0)
        treeview = self.builder.get_object("treeview1")
        treeview.set_expander_column(columns)
        
        cell = gtk.CellRendererText()
        columns = self.builder.get_object("treeviewcolumn2")
        columns.pack_start(cell)
        columns.add_attribute(cell, 'text', 1)

        cell = gtk.CellRendererText()
        columns = self.builder.get_object("treeviewcolumn3")
        columns.pack_start(cell)
        columns.add_attribute(cell, 'text', 2)

        self.window = self.builder.get_object("MainWindow")
        self.window.show_all()

        # We get the logic and help object
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
    Holds the some external logic of the app and persisten variables all across
    the execution
    """
    def __init__(self):
        self.json = None

    def loadjson(self, filename):
        """
        Loads a JSON file string and creates the respective object
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

    def loadTree(self, treestore):
        """
        Loads the JSON into the tree store for display purposes
        """
        for key_val in self.json.keys():

            if type(self.json[key_val]) is dict:

                parent_node = treestore.append(None, [str(key_val), "", ""])
                self._loadTreeRec(treestore, self.json[key_val], parent_node)

            else:

                treestore.append(None, [str(key_val), 
                                        str(self.json[key_val]),
                                        str(type(self.json[key_val]))])

    def _loadTreeRec(self, treestore, elems, parent_node):
        """
        Recursive element adding to the tree
        """
        for key_val in elems.keys():

            if type(elems[key_val]) is dict:

                new_parent_node = treestore.append(parent_node, 
                                                   [str(key_val),
                                                   "", ""])
                self._loadTreeRec(treestore, elems[key_val], new_parent_node)

            else:

                treestore.append(parent_node, [str(key_val), 
                                               str(elems[key_val]),
                                               str(type(elems[key_val]))])



# Ejecucion del programa principal

if __name__ == "__main__":

    logicObject = LogicObject()
    mainWindow = MainWindowMethods(logicObject)
    gtk.main()
