# find_there_tkinter.py
import os
import sys

# ——— Make your utils and lib packages importable ——————————————
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from utils.commands import Commands  # Import the Commands class
from utils import commands, tfunctions
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))
from lib import input_color, message
# ————————————————————————————————————————————————————————————————————

import tkinter as tk
from tkinter import ttk
from datetime import datetime
import sqlite3  # Import SQLite for database operations

class FindThereApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Find-There")
        self.geometry("1000x700")
        self.configure(bg="#f4f4f4")
        # Set a custom icon
        self.icon_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "assets", "find-there.ico"))
        if os.path.exists(self.icon_path):
            self.iconbitmap(self.icon_path)
        else:
            print(f"Warning: Icon file not found at {self.icon_path}")

        # instantiate your command‑handler
        self.cmd = commands

        # ——— NAV BAR ——————————————————————————————————————————————
        nav = tk.Frame(self, bg="#ffffff", height=40)
        nav.pack(fill=tk.X, side=tk.TOP)
        for page in ("add", "update", "transaction", "search"):
            btn = tk.Button(nav, text=page.title(),
                            bg="#ffffff", fg="#000000",
                            relief=tk.FLAT, padx=10, pady=2,
                            cursor="hand2",
                            command=lambda p=page: self.show_page(p))
            btn.pack(side=tk.LEFT, padx=5, pady=5)
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg="#f5f5f5"))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg="#ffffff"))

        # ——— CONTAINER FOR PAGES ————————————————————————————————
        container = tk.Frame(self, bg="#f4f4f4")
        container.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)
        container.grid_rowconfigure(1, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Title
        tk.Label(container, text="Find-There",
             font=("Arial", 24, "bold"), fg="#333", bg="#f4f4f4")\
          .grid(row=0, column=0, sticky="w")

        # Instantiate all pages
        self.pages = {}
        for PageClass, name in (
            (AddPage,        "add"),
            (UpdatePage,     "update"),
            (TransactionPage,"transaction"),
            (SearchPage,     "search"),
        ):
            frame = PageClass(container, self)
            frame.grid(row=1, column=0, sticky="nsew")
            self.pages[name] = frame

        # show Add by default
        self.show_page("add")

    def show_page(self, name):
        self.pages[name].tkraise()

class AddPage(tk.Frame):
    def __init__(self, parent, app: FindThereApp):
        super().__init__(parent, bg="#ffffff", padx=15, pady=15)
        self.app = app

        # Use the same database path as the Commands class
        self.commands = Commands()
        self.conn = sqlite3.connect(self.commands.db_path)
        self.cursor = self.conn.cursor()

        # Pagination variables
        self.page = 0
        self.page_size = 10

        # Form
        self.entries = {}
        for field in ("Product", "Description", "Price", "Quantity"):
            grp = tk.Frame(self, bg="#ffffff")
            grp.pack(fill=tk.X, pady=5)
            tk.Label(grp, text=field, bg="#ffffff",
                     font=("Arial", 10)).pack(anchor="w", pady=(0, 2))
            ent = tk.Entry(grp, font=("Arial", 10), relief=tk.SOLID, bd=1)
            ent.pack(fill=tk.X, ipady=6)
            self.entries[field.lower()] = ent

        self.err = tk.Label(self, text="", fg="red",
                            bg="#ffffff", font=("Arial", 9))
        self.err.pack(anchor="w", pady=(5, 0))

        # Add and Update Buttons
        btn_frame = tk.Frame(self, bg="#ffffff")
        btn_frame.pack(fill=tk.X, pady=(10, 0))

        tk.Button(btn_frame, text="Agregar Registro",
                  bg="#4CAF50", fg="white",
                  activebackground="#45a049",
                  relief=tk.FLAT, padx=12, pady=6,
                  cursor="hand2",
                  command=self.on_add)\
          .pack(side=tk.LEFT, padx=5)

        tk.Button(btn_frame, text="Actualizar Registro",
                  bg="#2196F3", fg="white",
                  activebackground="#1976D2",
                  relief=tk.FLAT, padx=12, pady=6,
                  cursor="hand2",
                  command=self.on_update)\
          .pack(side=tk.LEFT, padx=5)

        # Table
        cols = ("id", "product", "description", "price", "quantity", "created", "updated")
        self.tree = ttk.Treeview(self, columns=cols, show="headings", height=8)
        for c in cols:
            self.tree.heading(c, text=c.replace("_", " ").title())
            self.tree.column(c, anchor="w", width=120)
        self.tree.pack(fill=tk.BOTH, expand=True, pady=(20, 0))

        style = ttk.Style()
        style.configure("Treeview", font=("Arial", 10), rowheight=28)
        style.configure("Treeview.Heading", font=("Arial", 10, "bold"))

        # Pagination Buttons
        pagination_frame = tk.Frame(self, bg="#ffffff")
        pagination_frame.pack(fill=tk.X, pady=(10, 0))

        tk.Button(pagination_frame, text="Backward",
                  bg="#2196F3", fg="white",
                  activebackground="#1976D2",
                  relief=tk.FLAT, padx=12, pady=6,
                  cursor="hand2",
                  command=self.on_backward)\
          .pack(side=tk.LEFT, padx=5)

        tk.Button(pagination_frame, text="Forward",
                  bg="#4CAF50", fg="white",
                  activebackground="#45a049",
                  relief=tk.FLAT, padx=12, pady=6,
                  cursor="hand2",
                  command=self.on_forward)\
          .pack(side=tk.LEFT, padx=5)

        tk.Button(pagination_frame, text="Goto",
                  bg="#FFC107", fg="black",
                  activebackground="#FFB300",
                  relief=tk.FLAT, padx=12, pady=6,
                  cursor="hand2",
                  command=self.on_goto)\
          .pack(side=tk.LEFT, padx=5)

        self._next_id = 1

        # Load data from the database
        self.load_data()

        # Bind Treeview selection
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

    def load_data(self):
        """Fetch data from the database and populate the Treeview."""
        try:
            offset = self.page * self.page_size
            self.cursor.execute("SELECT * FROM data LIMIT ? OFFSET ?", (self.page_size, offset))
            rows = self.cursor.fetchall()

            # Clear the current rows in the Treeview
            for row in self.tree.get_children():
                self.tree.delete(row)

            for row in rows:
                self.tree.insert("", "end", values=row)
        except sqlite3.Error as e:
            self.err.config(text=f"Database error: {e}")

    def on_forward(self):
        """Move to the next page."""
        self.page += 1
        self.load_data()

    def on_backward(self):
        """Move to the previous page."""
        if self.page > 0:
            self.page -= 1
            self.load_data()

    def on_goto(self):
        """Prompt the user to enter a page number and navigate to it."""
        goto_window = tk.Toplevel(self)
        goto_window.title("Goto Page")
        goto_window.geometry("200x100")
        goto_window.configure(bg="#ffffff")

        tk.Label(goto_window, text="Enter Page Number:", bg="#ffffff").pack(pady=5)
        page_entry = tk.Entry(goto_window)
        page_entry.pack(pady=5)

        def goto_page():
            try:
                page_number = int(page_entry.get())
                if page_number < 1:
                    raise ValueError
                self.page = page_number - 1
                self.load_data()
                goto_window.destroy()
            except ValueError:
                tk.Label(goto_window, text="Invalid page number.", fg="red", bg="#ffffff").pack()

        tk.Button(goto_window, text="Go", command=goto_page).pack(pady=5)

        
    def __init__(self, parent, app: FindThereApp):
        super().__init__(parent, bg="#ffffff", padx=15, pady=15)
        self.app = app

        # Use the same database path as the Commands class
        self.commands = Commands()
        self.conn = sqlite3.connect(self.commands.db_path)
        self.cursor = self.conn.cursor()

        # Form
        self.entries = {}
        for field in ("Product", "Description", "Price", "Quantity"):
            grp = tk.Frame(self, bg="#ffffff")
            grp.pack(fill=tk.X, pady=5)
            tk.Label(grp, text=field, bg="#ffffff",
                     font=("Arial", 10)).pack(anchor="w", pady=(0, 2))
            ent = tk.Entry(grp, font=("Arial", 10), relief=tk.SOLID, bd=1)
            ent.pack(fill=tk.X, ipady=6)
            self.entries[field.lower()] = ent

        self.err = tk.Label(self, text="", fg="red",
                            bg="#ffffff", font=("Arial", 9))
        self.err.pack(anchor="w", pady=(5, 0))

        # Add and Update Buttons
        btn_frame = tk.Frame(self, bg="#ffffff")
        btn_frame.pack(fill=tk.X, pady=(10, 0))

        tk.Button(btn_frame, text="Agregar Registro",
                  bg="#4CAF50", fg="white",
                  activebackground="#45a049",
                  relief=tk.FLAT, padx=12, pady=6,
                  cursor="hand2",
                  command=self.on_add)\
          .pack(side=tk.LEFT, padx=5)

        tk.Button(btn_frame, text="Actualizar Registro",
                  bg="#2196F3", fg="white",
                  activebackground="#1976D2",
                  relief=tk.FLAT, padx=12, pady=6,
                  cursor="hand2",
                  command=self.on_update)\
          .pack(side=tk.LEFT, padx=5)

        # Table
        cols = ("id", "product", "description", "price", "quantity", "created", "updated")
        self.tree = ttk.Treeview(self, columns=cols, show="headings", height=8)
        for c in cols:
            self.tree.heading(c, text=c.replace("_", " ").title())
            self.tree.column(c, anchor="w", width=120)
        self.tree.pack(fill=tk.BOTH, expand=True, pady=(20, 0))

        style = ttk.Style()
        style.configure("Treeview", font=("Arial", 10), rowheight=28)
        style.configure("Treeview.Heading", font=("Arial", 10, "bold"))

        self._next_id = 1

        # Load data from the database
        self.load_data()

        # Bind Treeview selection
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

    def load_data(self):
        """Fetch data from the database and populate the Treeview."""
        try:
            self.cursor.execute("SELECT * FROM data")  # Use the table name from Commands
            rows = self.cursor.fetchall()
            for row in rows:
                self.tree.insert("", "end", values=row)
        except sqlite3.Error as e:
            self.err.config(text=f"Database error: {e}")

    def on_add(self):
        p = self.entries["product"].get().strip()
        d = self.entries["description"].get().strip()
        pr = self.entries["price"].get().strip()
        q = self.entries["quantity"].get().strip()

        if not p or not pr or not q:
            self.err.config(text="Please fill all required fields.")
            return
        try:
            prf = float(pr)
            qi = int(q)
        except ValueError:
            self.err.config(text="Price must be a number, quantity an integer.")
            return

        # Insert into the database
        try:
            ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.cursor.execute(
                "INSERT INTO data (product, description, price, quantity, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?)",
                (p, d, prf, qi, ts, ts)
            )
            self.conn.commit()
            self.err.config(text="")

            # Clear the form fields
            for e in self.entries.values():
                e.delete(0, tk.END)

            # Reload the table data
            self.reload_table()
        except sqlite3.Error as e:
            self.err.config(text=f"Database error: {e}")

    def on_update(self):
        """Update the selected record in the database."""
        selected_item = self.tree.selection()
        if not selected_item:
            self.err.config(text="Please select a record to update.")
            return

        item = self.tree.item(selected_item)
        record_id = item["values"][0]  # Get the ID of the selected record

        p = self.entries["product"].get().strip()
        d = self.entries["description"].get().strip()
        pr = self.entries["price"].get().strip()
        q = self.entries["quantity"].get().strip()

        if not p or not pr or not q:
            self.err.config(text="Please fill all required fields.")
            return
        try:
            prf = float(pr)
            qi = int(q)
        except ValueError:
            self.err.config(text="Price must be a number, quantity an integer.")
            return

        # Update the database
        try:
            ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.cursor.execute(
                "UPDATE data SET product = ?, description = ?, price = ?, quantity = ?, updated_at = ? WHERE id = ?",
                (p, d, prf, qi, ts, record_id)
            )
            self.conn.commit()
            self.err.config(text="Record updated successfully.")

            # Reload the table data
            self.reload_table()
        except sqlite3.Error as e:
            self.err.config(text=f"Database error: {e}")

    def on_tree_select(self, event):
        """Populate the form fields with the selected record's data."""
        selected_item = self.tree.selection()
        if not selected_item:
            return

        item = self.tree.item(selected_item)
        values = item["values"]

        # Populate the form fields
        self.entries["product"].delete(0, tk.END)
        self.entries["product"].insert(0, values[1])

        self.entries["description"].delete(0, tk.END)
        self.entries["description"].insert(0, values[2])

        self.entries["price"].delete(0, tk.END)
        self.entries["price"].insert(0, values[3])

        self.entries["quantity"].delete(0, tk.END)
        self.entries["quantity"].insert(0, values[4])

    def reload_table(self):
        """Clear and reload the Treeview with the latest data from the database."""
        # Clear the current rows in the Treeview
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Fetch and insert the updated data
        self.load_data()

class UpdatePage(tk.Frame):
    def __init__(self, parent, app: FindThereApp):
        super().__init__(parent, bg="#ffffff", padx=15, pady=15)
        self.app = app
        self.entries = {}
        for field in ("ID","Product","Description","Price","Quantity"):
            grp = tk.Frame(self, bg="#ffffff")
            grp.pack(fill=tk.X, pady=5)
            tk.Label(grp, text=field, bg="#ffffff",
                     font=("Arial",10)).pack(anchor="w", pady=(0,2))
            ent = tk.Entry(grp, font=("Arial",10), relief=tk.SOLID, bd=1)
            ent.pack(fill=tk.X, ipady=6)
            self.entries[field.lower()] = ent

        tk.Button(self, text="Actualizar Registro",
                  bg="#4CAF50", fg="white",
                  activebackground="#45a049",
                  relief=tk.FLAT, padx=12, pady=6,
                  cursor="hand2",
                  command=self.on_update)\
          .pack(pady=(10,0), anchor="e")

    def on_update(self):
        vals = {k: e.get().strip() for k,e in self.entries.items()}
        if not all(vals.values()):
            message.error("Please fill all fields.")
            return
        # call existing update()
        self.app.cmd.update(
            vals["id"], vals["product"],
            vals["description"], vals["price"],
            vals["quantity"]
        )


class TransactionPage(tk.Frame):
    def __init__(self, parent, app: FindThereApp):
        super().__init__(parent, bg="#ffffff", padx=15, pady=15)
        self.app = app

        # identifier
        for label in ("Identifier (ID or Product)", "Amount (±)"):
            grp = tk.Frame(self, bg="#ffffff")
            grp.pack(fill=tk.X, pady=5)
            tk.Label(grp, text=label, bg="#ffffff",
                     font=("Arial",10)).pack(anchor="w", pady=(0,2))
            ent = tk.Entry(grp, font=("Arial",10), relief=tk.SOLID, bd=1)
            ent.pack(fill=tk.X, ipady=6)
            key = "identifier" if "Identifier" in label else "amount"
            setattr(self, key+"_entry", ent)

        tk.Button(self, text="Realizar Transacción",
                  bg="#4CAF50", fg="white",
                  activebackground="#45a049",
                  relief=tk.FLAT, padx=12, pady=6,
                  cursor="hand2",
                  command=self.on_transaction)\
          .pack(pady=(10,0), anchor="e")

    def on_transaction(self):
        ident = self.identifier_entry.get().strip()
        amt   = self.amount_entry.get().strip()
        if not ident or not amt:
            message.error("Please fill both fields.")
            return
        self.app.cmd.transaction(ident, amt)


class SearchPage(tk.Frame):
    def __init__(self, parent, app: FindThereApp):
        super().__init__(parent, bg="#ffffff", padx=15, pady=15)
        self.app = app

        # search box
        grp = tk.Frame(self, bg="#ffffff"); grp.pack(fill=tk.X, pady=5)
        tk.Label(grp, text="Search term", bg="#ffffff",
                 font=("Arial",10)).pack(anchor="w", pady=(0,2))
        self.term_ent = tk.Entry(grp, font=("Arial",10),
                                 relief=tk.SOLID, bd=1)
        self.term_ent.pack(fill=tk.X, ipady=6)

        tk.Button(self, text="Buscar",
                  bg="#4CAF50", fg="white",
                  activebackground="#45a049",
                  relief=tk.FLAT, padx=12, pady=6,
                  cursor="hand2",
                  command=self.on_search)\
          .pack(pady=(10,0), anchor="e")

    def on_search(self):
        term = self.term_ent.get().strip()
        if not term:
            message.error("Please enter a search term.")
            return
        # calls your existing search()
        self.app.cmd.search(term)


if __name__ == "__main__":
    FindThereApp().mainloop()
