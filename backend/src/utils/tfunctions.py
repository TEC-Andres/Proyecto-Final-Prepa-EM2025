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