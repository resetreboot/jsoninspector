#!/bin/bash

intltool-extract --type="gettext/glade" *.glade
xgettext -k_ -kN_ -o messages.pot *.py *.h

