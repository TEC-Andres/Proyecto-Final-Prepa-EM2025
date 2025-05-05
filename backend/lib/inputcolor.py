'''
#       Proyecto-Final-Prepa-EM2025
#       Fernando Chávez Nolasco ─ A01284698
#       Andrés Rodríguez Cantú ─ A01287002
#       Roberto André Guevara Martínez ─ A01287324
#       Víctor Manuel Sánchez Chávez ─ A01287522
#       
#       Copyright (C) Tecnológico de Monterrey
#
#       Archivo: lib/__iinputcolornit__.py
#
#       Creado:                   03/05/2024
#       Última Modificación:      05/05/2024
'''
import sys
import re
import msvcrt
from lib.color import FG, Style

class InputColor:
    SELECT_STYLE = "\033[7m"

    def __init__(self, prompt=">>> "):
        self.prompt = prompt
        self.user_input = ""
        self.cursor_position = 0
        self.history = []
        self.history_index = None 
        self.all_selected = False 

    def start_input(self):
        sys.stdout.write(self.prompt)
        sys.stdout.flush()

        while True:
            key = msvcrt.getch()
            match key:
                case b'\x03':  # Allow Ctrl+C (ETX) to raise KeyboardInterrupt
                    raise KeyboardInterrupt
                case b'\x00' | b'\xe0':  # Special keys (arrow keys and others)
                    key2 = msvcrt.getch()
                    match key2:
                        case b'H':  # Up arrow: history back
                            self._handle_history_up()
                        case b'P':  # Down arrow: history forward
                            self._handle_history_down()
                        case b'K':  # Left arrow: move cursor left
                            self._handle_left_arrow()
                        case b'M':  # Right arrow: move cursor right
                            self._handle_right_arrow()
                    continue
                case b'\x01':  # Ctrl+A (ASCII 1) selects everything
                    self._handle_ctrl_a()
                    continue
                case b"\r":  # Enter key ends input
                    break
                case b"\x08":  # Backspace (ASCII 8)
                    self._handle_backspace()
                    continue
                case _ if key.isascii() and key.decode("utf-8").isprintable():  # Printable characters
                    self._handle_printable(key.decode("utf-8"))
                    continue
        print() 
        result = self.user_input
        if result:
            self.history.append(result)
        self.user_input = ""
        self.cursor_position = 0
        self.history_index = None
        self.all_selected = False
        return result

    def _handle_history_up(self):
        if self.history:
            if self.history_index is None:
                self.history_index = len(self.history) - 1
            elif self.history_index > 0:
                self.history_index -= 1
            self.user_input = self.history[self.history_index]
            self.cursor_position = len(self.user_input)
            self.all_selected = False
            self._update_display()

    def _handle_history_down(self):
        if self.history and self.history_index is not None:
            if self.history_index < len(self.history) - 1:
                self.history_index += 1
                self.user_input = self.history[self.history_index]
            else:
                self.history_index = None
                self.user_input = ""
            self.cursor_position = len(self.user_input)
            self.all_selected = False
            self._update_display()

    def _handle_left_arrow(self):
        # If all text is selected, clear selection and move cursor to beginning.
        if self.all_selected:
            self.all_selected = False
            self.cursor_position = 0
        elif self.cursor_position > 0:
            self.cursor_position -= 1
        self._update_display()

    def _handle_right_arrow(self):
        # If all text is selected, clear selection and move cursor to end.
        if self.all_selected:
            self.all_selected = False
            self.cursor_position = len(self.user_input)
        elif self.cursor_position < len(self.user_input):
            self.cursor_position += 1
        self._update_display()

    def _handle_ctrl_a(self):
        # Select all: flag is set and we move the cursor to the end.
        self.all_selected = True
        self.cursor_position = len(self.user_input)
        self._update_display()

    def _handle_backspace(self):
        # If all text is selected, backspace clears the whole line.
        if self.all_selected:
            self.user_input = ""
            self.cursor_position = 0
            self.all_selected = False
        elif self.cursor_position > 0:
            self.user_input = (self.user_input[:self.cursor_position-1] +
                               self.user_input[self.cursor_position:])
            self.cursor_position -= 1
        self._update_display()

    def _handle_printable(self, char):
        # If text is selected, then replace it.
        if self.all_selected:
            self.user_input = ""
            self.cursor_position = 0
            self.all_selected = False
        # Insert the character at the current cursor position.
        self.user_input = (self.user_input[:self.cursor_position] +
                           char +
                           self.user_input[self.cursor_position:])
        self.cursor_position += 1
        self._update_display()

    def _update_display(self):
        # Hide the cursor
        sys.stdout.write("\033[?25l")
        
        if self.all_selected:
            colored_input = self.SELECT_STYLE + self.user_input + Style.RESET_ALL
        else:
            color_map = {
                "exit": FG.H00AAAA,
                "cls": FG.H888888,
                "help": FG.H00AAAA,
            }
            words = self.user_input.split()
            colored_input = self.user_input

            # Apply predefined colors
            if words and words[0] in color_map:
                colored_input = f"{color_map[words[0]]}{self.user_input}{Style.RESET_ALL}"
            elif words:
                first_word_colored = f"{FG.HFFFF00}{words[0]}{Style.RESET_ALL}"
                colored_input = first_word_colored + self.user_input[len(words[0]):]

            # Apply color to words after '--'
            def replace_dash_words(match):
                return f"{FG.H848484}--{match.group(1)}{Style.RESET_ALL}"

            def replace_negative_numbers(match):
                return f"{FG.HEA4335}{match.group(0)}{Style.RESET_ALL}"

            def replace_positive_numbers(match):
                return f"{FG.H34A853}{match.group(0)}{Style.RESET_ALL}"

            colored_input = re.sub(r"--\s*(\w+)", replace_dash_words, colored_input)
            colored_input = re.sub(r"-\d+", replace_negative_numbers, colored_input)
            colored_input = re.sub(r"\+\d+", replace_positive_numbers, colored_input)

        # Build the full line with prompt.
        colored_line = self.prompt + colored_input
        sys.stdout.write("\r" + colored_line + "\033[K")

        # Reposition the hardware cursor:
        cursor_abs_pos = len(self.prompt) + self.cursor_position
        sys.stdout.write(f"\r\033[{cursor_abs_pos+1}G")
        
        # Show the cursor again
        sys.stdout.write("\033[?25h")
        sys.stdout.flush()

