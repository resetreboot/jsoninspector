#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pkg_resources import resource_filename
from gi.repository import Gtk, Gio

import json, sys, os.path

# Internationalization support
import gettext
import locale

APP = "jsoninspector"

if os.path.exists('../locale/po'):
    # We're in the development tree
    DIR = "../locale/po/"

elif sys.platform != 'win32' and sys.platform != 'darwin':
    DIR = "/usr/share/locale/"

else:
    DIR = "po"

locale.setlocale(locale.LC_ALL, '')

gettext.bindtextdomain(APP, DIR)
locale.bindtextdomain(APP, DIR)


gettext.textdomain(APP)
_ = gettext.gettext


class MainWindowMethods(Gtk.Application):
    """
    Main Application object with the main window signals
    """
    def __init__(self, logic):
        Gtk.Application.__init__(self, application_id = "apps.gnome.jsoninspector",
                                 flags = Gio.ApplicationFlags.FLAGS_NONE)

        # We store the reference to the app logic
        self.logicObj = logic

        self.connect("activate", self.on_app_start)

    def on_app_start(self, data = None):
        """
        Loads the MainWindow widgets, shows it up and starts the main loop
        """
        self.builder = Gtk.Builder()
        self.builder.set_translation_domain(APP)
        self.builder.add_from_file(resource_filename(__name__,'jsoninspector.glade'))
        self.builder.connect_signals(self)

        # Prepares the renders of columns and assigns the values
        cell = Gtk.CellRendererText()
        columns = self.builder.get_object("treeviewcolumn1")
        columns.pack_start(cell, True)
        columns.add_attribute(cell, 'text', 0)
        treeview = self.builder.get_object("treeview1")
        # This column has the open and collapse nodes
        treeview.set_expander_column(columns)

        cell = Gtk.CellRendererText()
        columns = self.builder.get_object("treeviewcolumn2")
        columns.pack_start(cell, True)
        columns.add_attribute(cell, 'text', 1)

        cell = Gtk.CellRendererText()
        columns = self.builder.get_object("treeviewcolumn3")
        columns.pack_start(cell, True)
        columns.add_attribute(cell, 'text', 2)

        # We get the window and show it
        self.window = self.builder.get_object("MainWindow")
        self.add_window(self.window)
        self.window.show_all()

    def onOpenMenuClicked(self, event):
        """
        User has pressed Open in the menu
        """
        # Create the FileChooser Dialog
        chooser = Gtk.FileChooserDialog(_("Open JSON text file"), self.window,
                                        Gtk.FileChooserAction.OPEN,
                                        (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                        Gtk.STOCK_OPEN, Gtk.ResponseType.OK))

        # Launch it
        response = chooser.run()

        # If we choose a file, we load it
        if response == Gtk.ResponseType.OK:
            filename = chooser.get_filename()
            label = self.builder.get_object("StatusLabel")

            # We update the statusbar accordingly to what has happened
            if self.logicObj.loadjson(filename):
                
                label.set_text(filename)
                treeStore = self.builder.get_object("treestore1")
                treeStore.clear()
                self.logicObj.loadTree(treeStore)
                
            else:
                
                label.set_text(_("No JSON loaded."))

        # We finish the dialog
        chooser.destroy()

    def onCopyJSONClicked(self, widget):
        """
        User asked to paste a JSON code
        """
        # Show up the TextWindow
        textWindow = self.builder.get_object("TextWindow")
        textWindow.show_all()

    def onCopyJSONDelete(self, widget, event):
        """
        We've been told to close the CopyJSON Window
        """
        textWindow = self.builder.get_object("TextWindow")
        textWindow.hide()

        return True

    def onCopyJSONDestroy(self, widget):
        """
        We've been tasked with removing the CopyJSON window
        """
        textWindow = self.builder.get_object("TextWindow")
        textWindow.hide()

        return True

    def onCopyJSONAcceptClicked(self, widget):
        """
        The input is finished and accepted.
        """
        textView = self.builder.get_object("textview1")
        jsonBuffer = textView.get_buffer()
        jsonText = jsonBuffer.get_text(jsonBuffer.get_start_iter(),
                                       jsonBuffer.get_end_iter(), True)

        textWindow = self.builder.get_object("TextWindow")
        textWindow.hide()
        treestore = self.builder.get_object("treestore1")
        treestore.clear()

        if self.logicObj.loadJSONText(jsonText):
            
            status_label = self.builder.get_object("StatusLabel") 
            status_label.set_text(_("Loaded from the clipboard."))
            self.logicObj.loadTree(treestore)

    def onCopyJSONCancelClicked(self, widget):
        """
        The user changed its mind and pressed cancel
        """
        textWindow = self.builder.get_object("TextWindow")
        textWindow.hide()

    def onExitMenuClicked(self, widget):
        """
        Menu option Exit has been clicked
        """
        self.quit()

    def onAboutMenuActivate(self, widget):
        """
        About option clicked
        """
        about_dialog = self.builder.get_object("AboutDialog")
        about_dialog.run()
        about_dialog.hide()

    def onMainWindowDelete(self, widget, event):
        """
        Our MainWindow has been deleted or closed
        """
        pass

    def onAboutDialogClose(self, widget, event = None):
        pass

    def onAboutDialogDeleteEvent(self, widget, event = None):
        pass


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
            print _("Not valid JSON!\n")
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
            print _("Not valid JSON")
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


# Main procedure
if __name__ == "__main__":
    
    logicObject = LogicObject()

    mainWindow = MainWindowMethods(logicObject)
    mainWindow.run(None)
