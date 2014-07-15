#!/usr/bin/env python
# -*- coding: utf-8 -*-

from jsoninspector import LogicObject, MainWindowMethods

def main_start():
    """
    So setuptools makes a nice startup script
    """
    logicObject = LogicObject()

    mainWindow = MainWindowMethods(logicObject)
    mainWindow.run(None)
