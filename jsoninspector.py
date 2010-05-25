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


# Ejecucion del programa principal

if __name__ == "__main__":

    logicObject = LogicObject()
    mainWindow = MainWindowMethods(logicObject)
    gtk.main()
