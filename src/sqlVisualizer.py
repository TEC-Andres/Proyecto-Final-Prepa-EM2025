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
#       Última Modificación:      04/05/2024
'''
import sqlite3
import os
import sys
import prettytable
# Include all useful lib modules
sys.path.append(os.path.join(os.path.dirname(__file__), "..")) 
from lib import input_color, message

class Functions:
    def __init__(self):
        pass

    def exit(self):
        message.console("Saliendo del programa...")
        sys.exit(0)

    def cls(self):
        os.system('cls' if os.name == 'nt' else 'clear')

class Main:
    def __init__(self):
        self.db_path = os.path.join(os.path.dirname(__file__), "db", "example.db")
        pass

    def create(self, name="example"):
        try:
            db_dir = os.path.join(os.path.dirname(__file__), "db")
            os.makedirs(db_dir, exist_ok=True)  # Ensure the directory exists
            self.db_path = os.path.join(db_dir, f'{name}.db')  
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS data (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    age INTEGER NOT NULL
                )
            """)
            self.conn.commit()
            print("Database and table created successfully.")
        except sqlite3.DatabaseError as e:
            if "malformed" in str(e).lower():
                print("Database is corrupted. Recreating the database...")
                if hasattr(self, 'conn') and self.conn:
                    self.conn.close()
                os.remove(self.db_path)
                self.create()
            else:
                print(f"Database error occurred: {e}")
        finally:
            if hasattr(self, 'conn') and self.conn:
                self.conn.close()

    def read(self, limit=20, offset=0):

        self.conn = sqlite3.connect(self.db_path)  # Connect to the database using the constructed path
        self.cursor = self.conn.cursor()
        self.cursor.execute("SELECT * FROM data LIMIT ? OFFSET ?", (limit, offset))
        rows = self.cursor.fetchall()

        # Create a PrettyTable object for better display
        table = prettytable.PrettyTable()
        table.field_names = ["ID", "Name", "Age"]
        for row in rows:
            table.add_row(row)

        print(table)  # Display the table in the terminal
        self.conn.close()  # Close the connection after reading

    def update(self, id, name, age):
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()
            self.cursor.execute("UPDATE data SET name = ?, age = ? WHERE id = ?", (name, age, id))
            if self.cursor.rowcount == 0:
                print(f"Error: No record found with id {id}.")
            else:
                self.conn.commit()
                print(f"Record with id {id} updated successfully.")
        except sqlite3.Error as e:
            print(f"Database error occurred: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
        finally:
            if hasattr(self, 'conn') and self.conn:
                self.conn.close()

    def add(self, name, age):
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()
            self.cursor.execute("INSERT INTO data (name, age) VALUES (?, ?)", (name, age))
            self.conn.commit()
            print("Record added successfully.")
        except sqlite3.Error as e:
            print(f"Database error occurred: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
        finally:
            if hasattr(self, 'conn') and self.conn:
                self.conn.close()

    def delete(self, id):
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()
            self.cursor.execute("DELETE FROM data WHERE id = ?", (id,))
            if self.cursor.rowcount == 0:
                print(f"Error: No record found with id {id}.")
            else:
                self.conn.commit()
                print(f"Record with id {id} deleted successfully.")
        except sqlite3.Error as e:
            print(f"Database error occurred: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
        finally:
            if hasattr(self, 'conn') and self.conn:
                self.conn.close()

    def goto(self, id):
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()
            self.cursor.execute("SELECT * FROM data WHERE id = ?", (id,))
            row = self.cursor.fetchone()
            if row:
                table = prettytable.PrettyTable()
                table.field_names = ["ID", "Name", "Age"]
                table.add_row(row)
                print(table)  # Display the table in the terminal
            else:
                print(f"Error: No record found with id {id}.")
        except sqlite3.Error as e:
            print(f"Database error occurred: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
        finally:
            if hasattr(self, 'conn') and self.conn:
                self.conn.close()
    
if __name__ == "__main__":
    main = Main()
    tfunctions = Functions()

    while True:
        try:
            comando = input_color.start_input().strip()
            if not comando:
                continue
            parts = comando.split()
            comando_name = parts[0]
            args = parts[1:]
            # Use getattr to call the method on either 'main' or 'tfunctions' object
            method = getattr(main, comando_name, None) or getattr(tfunctions, comando_name, None)
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