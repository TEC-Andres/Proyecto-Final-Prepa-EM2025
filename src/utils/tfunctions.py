'''
#       Proyecto-Final-Prepa-EM2025
#       Fernando Chávez Nolasco ─ A01284698
#       Andrés Rodríguez Cantú ─ A01287002
#       Roberto André Guevara Martínez ─ A01287324
#       Víctor Manuel Sánchez Chávez ─ A01287522
#       
#       Copyright (C) Tecnológico de Monterrey
#
#       Archivo: sqlVisualizer.py
#
#       Creado:                   04/05/2024
#       Última Modificación:      04/05/2024
'''

import os
import sys

# Include all lib modules
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..")) 
from lib import message


class TerminalFunctions:
    def __init__(self):
        pass

    def exit(self):
        message.console("Saliendo del programa...")
        sys.exit(0)

    def cls(self):
        os.system('cls' if os.name == 'nt' else 'clear')