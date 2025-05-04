import sqlite3
import os
import sys
import prettytable
sys.path.append(os.path.join(os.path.dirname(__file__), "..")) 
from lib import input_color, messages

class Main:
    def __init__(self):
        self.db_path = os.path.join(os.path.dirname(__file__), "db", "example.db")
        pass

    def create(self):
        try:
            self.conn = sqlite3.connect("example.db")
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
                os.remove("example.db")
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
    
if __name__ == "__main__":
    main = Main()

    while True:
        try:
            comando = input_color.start_input().strip()
            if not comando:
                continue
            parts = comando.split()
            comando_name = parts[0]
            args = parts[1:]
            # Use getattr to call the method on the 'main' object
            method = getattr(main, comando_name, None)
            if method is None:
                print(f"Error: Command '{comando_name}' not found.")
            else:
                method(*args)
        except KeyboardInterrupt:
            messages.console("Programa terminado por el usuario.")
            break
        except AttributeError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")