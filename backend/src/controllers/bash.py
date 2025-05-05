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
import os
import sys
import shlex 
# Include all utils modules
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from utils import commands, tfunctions
# Include all lib modules
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..")) 
from lib import input_color, message

if __name__ == "__main__":
    print("Bienvenido al programa de visualización de SQL. Escribe 'help' para ver los comandos disponibles.")

    while True:
        try:
            comando = input_color.start_input().strip()
            if not comando:
                continue
            parts = shlex.split(comando)  # Use shlex.split to handle quoted arguments
            comando_name = parts[0]
            args = parts[1:]
            # Use getattr to call the method on either 'commands' or 'tfunctions' object
            method = getattr(commands, comando_name, None) or getattr(tfunctions, comando_name, None)
            if method is None:
                message.error(f"Error: Command '{comando_name}' not found.")
            else:
                method(*args)
        except KeyboardInterrupt:
            message.console("Programa terminado por el usuario.")
            break
        except AttributeError as e:
            message.error(f"Error: {e}")
        except Exception as e:
            message.error(f"An unexpected error occurred: {e}")
