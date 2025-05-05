import sqlite3
import os
import sys
import prettytable

# Include all lib modules
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..")) 
from lib import message

class Commands:
    def __init__(self):
        self.db_path = os.path.join(os.path.dirname(__file__), "..", "db", "example.db")
        pass

    def create(self, name="example"):
        try:
            db_dir = os.path.join(os.path.dirname(__file__), "..", "db")
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
            message.success("Record added successfully.")
        except sqlite3.Error as e:
            message.error(f"Database error occurred: {e}")
        except Exception as e:
            message.error(f"An unexpected error occurred: {e}")
        finally:
            if hasattr(self, 'conn') and self.conn:
                self.conn.close()

    def delete(self, id):
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()
            self.cursor.execute("DELETE FROM data WHERE id = ?", (id,))
            if self.cursor.rowcount == 0:
                message.error(f"Error: No record found with id {id}.")
            else:
                self.conn.commit()
                message.success(f"Record with id {id} deleted successfully.")
        except sqlite3.Error as e:
            message.error(f"Database error occurred: {e}")
        except Exception as e:
            message.error(f"An unexpected error occurred: {e}")
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
                message.error(f"Error: No record found with id {id}.")
        except sqlite3.Error as e:
            message.error(f"Database error occurred: {e}")
        except Exception as e:
            message.error(f"An unexpected error occurred: {e}")
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
            "help": "Muestra esta ayuda.",
            "search [term]": "Busca registros que contengan el término especificado.",
            "transaction [id/product] [amount]": "Realiza una transacción de stock.",
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
            message.error(f"Database error occurred: {e}")
        except Exception as e:
            message.error(f"An unexpected error occurred: {e}")
        finally:
            if hasattr(self, 'conn') and self.conn:
                self.conn.close()

    def transaction(self, identifier, amount):
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()
            
            # Determine if the identifier is an ID (integer) or a Product (string)
            if identifier.isdigit():
                self.cursor.execute("SELECT id, product, quantity FROM data WHERE id = ?", (int(identifier),))
            else:
                self.cursor.execute("SELECT id, product, quantity FROM data WHERE product = ?", (identifier,))
            
            row = self.cursor.fetchone()
            
            if not row:
                message.error(f"No record found with identifier '{identifier}'.")
                return
            
            id, product, current_quantity = row
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
            message.success(f"Transaction successful. New quantity for '{product}' is {new_quantity}.")
        except sqlite3.Error as e:
            message.error(f"Database error occurred: {e}")
        except ValueError:
            message.error("Error: Amount must be a valid integer.")
        except Exception as e:
            message.error(f"An unexpected error occurred: {e}")
        finally:
            if hasattr(self, 'conn') and self.conn:
                self.conn.close()