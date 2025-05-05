'''
#       Proyecto-Final-Prepa-EM2025
#       Fernando Chávez Nolasco ─ A01284698
#       Andrés Rodríguez Cantú ─ A01287002
#       Roberto André Guevara Martínez ─ A01287324
#       Víctor Manuel Sánchez Chávez ─ A01287522
#       
#       Copyright (C) Tecnológico de Monterrey
#
#       Archivo: lib/__init__.py
#
#       Creado:                   03/05/2024
#       Última Modificación:      04/05/2024
'''

from .messages import Messages
from .inputcolor import InputColor

message = Messages()
input_color = InputColor()

__all__ = ['message', 'input_color']
__version__ = "1.0.0"