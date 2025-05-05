'''
#       Proyecto-Final-Prepa-EM2025
#       Fernando Chávez Nolasco ─ A01284698
#       Andrés Rodríguez Cantú ─ A01287002
#       Roberto André Guevara Martínez ─ A01287324
#       Víctor Manuel Sánchez Chávez ─ A01287522
#       
#       Copyright (C) Tecnológico de Monterrey
#
#       Archivo: lib/messages.py
#
#       Creado:                   03/05/2024
#       Última Modificación:      04/05/2024
'''

from lib.color import FG, Style

class Messages:
    def __init__(self):
        pass

    def success(self, message):
        print(f"{Style.BRIGHT + FG.H00AA00}[{FG.RESET + FG.H55FF55}ÉXITO{FG.RESET + Style.BRIGHT + FG.H00AA00}] {FG.RESET + FG.H443A3B}―{FG.RESET + Style.RESET_ALL} {message}{FG.RESET + Style.RESET_ALL}")
    
    def error(self, message):
        print(f"{Style.BRIGHT + FG.HFF0000}[{FG.RESET + FG.HFF5555}ERROR{FG.RESET + Style.BRIGHT + FG.HFF0000}] {FG.RESET + FG.H443A3B}―{FG.RESET + Style.RESET_ALL} {message}{FG.RESET + Style.RESET_ALL}")
    
    def info(self, message):
        print(f"{Style.BRIGHT + FG.H5555FF}[{FG.RESET + FG.H00AAAA}INFO{FG.RESET + Style.BRIGHT + FG.H5555FF}] {FG.RESET + FG.H443A3B}―{FG.RESET + Style.RESET_ALL} {message}{FG.RESET + Style.RESET_ALL}")
    
    def warning(self, message):
        print(f"{Style.BRIGHT + FG.HFFA500}[{FG.RESET + FG.HFFFF00}WARNING{FG.RESET + Style.BRIGHT + FG.HFFA500}] {FG.RESET + FG.H443A3B}―{FG.RESET + Style.RESET_ALL} {message}{FG.RESET + Style.RESET_ALL}")
    
    def console(self, message):
        print(f"{Style.BRIGHT + FG.H555555}[{FG.RESET + FG.HAAAAAA}CONSOLA{FG.RESET + Style.BRIGHT + FG.H555555}] {FG.RESET + FG.H443A3B}―{FG.RESET + Style.RESET_ALL} {message}{FG.RESET + Style.RESET_ALL}")