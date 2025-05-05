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
import sqlite3
import os
import sys
import prettytable
import shlex  # Add this import for parsing input
import re
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
                    product TEXT NOT NULL,
                    description TEXT NOT NULL,
                    price REAL NOT NULL,
                    quantity INTEGER NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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

    def read(self, page=1, limit=10):
        try:
            offset = (int(page) - 1) * limit  # Calculate the offset based on the page number
            self.conn = sqlite3.connect(self.db_path)  # Connect to the database using the constructed path
            self.cursor = self.conn.cursor()
            self.cursor.execute("SELECT * FROM data LIMIT ? OFFSET ?", (limit, offset))
            rows = self.cursor.fetchall()

            # Create a PrettyTable object for better display
            table = prettytable.PrettyTable()
            table.field_names = ["ID", "Product", "Description", "Price", "Quantity", "Created At", "Updated At"]
            for row in rows:
                table.add_row(row)

            print(table)  # Display the table in the terminal
        except sqlite3.Error as e:
            print(f"Database error occurred: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
        finally:
            if hasattr(self, 'conn') and self.conn:
                self.conn.close()  # Close the connection after reading

    def update(self, id, product, description, price, quantity):
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()
            self.cursor.execute("""
                UPDATE data 
                SET product = ?, description = ?, price = ?, quantity = ?, updated_at = CURRENT_TIMESTAMP 
                WHERE id = ?
            """, (product, description, price, quantity, id))
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

    def add(self, product, description, price, quantity):
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()
            self.cursor.execute("""
                INSERT INTO data (product, description, price, quantity) 
                VALUES (?, ?, ?, ?)
            """, (product, description, price, quantity))
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
                table.field_names = ["ID", "Product", "Description", "Price", "Quantity", "Created At", "Updated At"]
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

    def help(self):
        commands = {
            "create [name]": "Crea una nueva base de datos con el nombre especificado.",
            "read [limit] [offset]": "Lee registros de la base de datos con límite y desplazamiento.",
            "update [id] [product] [description] [price] [quantity]": "Actualiza un registro existente.",
            "add [product] [description] [price] [quantity]": "Agrega un nuevo registro.",
            "delete [id]": "Elimina un registro por ID.",
            "goto [id]": "Muestra un registro específico por ID.",
            "cls": "Limpia la pantalla.",
            "exit": "Sale del programa.",
            "help": "Muestra esta ayuda."
        }
        print("\n".join([f"  {cmd} - {desc}" for cmd, desc in commands.items()]))

    def search(self, term):
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()
            # Use parameterized query to prevent SQL injection
            self.cursor.execute("SELECT * FROM data WHERE product LIKE ? OR description LIKE ?", (f'%{term}%', f'%{term}%'))
            rows = self.cursor.fetchall()

            if not rows:
                print(f"No records found for search term '{term}'.")
                return

            # Create a PrettyTable object for better display
            table = prettytable.PrettyTable()
            table.field_names = ["ID", "Product", "Description", "Price", "Quantity", "Created At", "Updated At"]
            for row in rows:
                table.add_row(row)

            print(table)  # Display the table in the terminal
        except sqlite3.Error as e:
            print(f"Database error occurred: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
        finally:
            if hasattr(self, 'conn') and self.conn:
                self.conn.close()

    def transaction(self, id, amount):
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()
            
            # Fetch the current quantity of the item
            self.cursor.execute("SELECT quantity FROM data WHERE id = ?", (id,))
            row = self.cursor.fetchone()
            
            if not row:
                print(f"Error: No record found with id {id}.")
                return
            
            current_quantity = row[0]
            new_quantity = current_quantity + int(amount)  # Add or subtract the amount
            
            if new_quantity < 0:
                message.error(f"Insufficient stock. Current quantity is {current_quantity}.")
                return
            
            # Update the quantity in the database
            self.cursor.execute("""
                UPDATE data 
                SET quantity = ?, updated_at = CURRENT_TIMESTAMP 
                WHERE id = ?
            """, (new_quantity, id))
            
            self.conn.commit()
            print(f"Transaction successful. New quantity for id {id} is {new_quantity}.")
        except sqlite3.Error as e:
            print(f"Database error occurred: {e}")
        except ValueError:
            print("Error: Amount must be a valid integer.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
        finally:
            if hasattr(self, 'conn') and self.conn:
                self.conn.close()
    
    
if __name__ == "__main__":
    main = Main()
    tfunctions = Functions()
    print("Bienvenido al programa de visualización de SQL. Escribe 'help' para ver los comandos disponibles.")

    while True:
        try:
            comando = input_color.start_input().strip()
            if not comando:
                continue
            parts = shlex.split(comando)  # Use shlex.split to handle quoted arguments
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
