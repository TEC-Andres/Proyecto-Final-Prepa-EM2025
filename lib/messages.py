from lib.color import FG, Style

class Messages:
    def __init__(self):
        pass

    def success(self, message):
        print(f"\n{Style.BRIGHT + FG.H00AA00}[{FG.RESET + FG.H55FF55}ÉXITO{FG.RESET + Style.BRIGHT + FG.H00AA00}] {FG.RESET + FG.H443A3B}―{FG.RESET + Style.RESET_ALL} {message}{FG.RESET + Style.RESET_ALL}")
    
    def error(self, message):
        print(f"\n{Style.BRIGHT + FG.HFF0000}[{FG.RESET + FG.HFF5555}ERROR{FG.RESET + Style.BRIGHT + FG.HFF0000}] {FG.RESET + FG.H443A3B}―{FG.RESET + Style.RESET_ALL} {message}{FG.RESET + Style.RESET_ALL}")
    
    def info(self, message):
        print(f"\n{Style.BRIGHT + FG.H5555FF}[{FG.RESET + FG.H00AAAA}INFO{FG.RESET + Style.BRIGHT + FG.H5555FF}] {FG.RESET + FG.H443A3B}―{FG.RESET + Style.RESET_ALL} {message}{FG.RESET + Style.RESET_ALL}")
    
    def warning(self, message):
        print(f"\n{Style.BRIGHT + FG.HFFA500}[{FG.RESET + FG.HFFFF00}WARNING{FG.RESET + Style.BRIGHT + FG.HFFA500}] {FG.RESET + FG.H443A3B}―{FG.RESET + Style.RESET_ALL} {message}{FG.RESET + Style.RESET_ALL}")
    
    def console(self, message):
        print(f"\n{Style.BRIGHT + FG.H555555}[{FG.RESET + FG.HAAAAAA}CONSOLA{FG.RESET + Style.BRIGHT + FG.H555555}] {FG.RESET + FG.H443A3B}―{FG.RESET + Style.RESET_ALL} {message}{FG.RESET + Style.RESET_ALL}")