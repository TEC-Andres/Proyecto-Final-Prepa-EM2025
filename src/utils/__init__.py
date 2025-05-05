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
#       Creado:                   03/05/2024
#       Última Modificación:      05/05/2024
'''

from .commands import Commands
from .tfunctions import TerminalFunctions

commands = Commands()
tfunctions = TerminalFunctions()

__all__ = ['message', 'input_color']
__version__ = "1.0.0"