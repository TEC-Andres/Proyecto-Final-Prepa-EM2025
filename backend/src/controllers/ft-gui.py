import tkinter as tk
from tkinterweb import HtmlFrame
import os
import sqlite3
from urllib.parse import urlparse

class MyRenderer:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Find There")
        self.root.state("zoomed")
        icon_path = os.path.join(os.path.dirname(__file__), "..", "..", "..", "frontend", "assets", "find-there.ico")
        if os.path.exists(icon_path):
            self.root.iconbitmap(icon_path)
        else:
            print(f"Icon file not found at: {icon_path}")

        # Create HtmlFrame with on_link_click handler
        self.frame = HtmlFrame(
            self.root,
            horizontal_scrollbar="auto",
            on_link_click=self._handle_link
        )
        self.frame.pack(fill="both", expand=True)

        # Load and inline HTML and CSS
        html_dir = os.path.join(os.path.dirname(__file__), "..", "..", "..", "frontend", "webpage")
        with open(os.path.join(html_dir, "index.html"), encoding="utf-8") as f:
            html = f.read()
        with open(os.path.join(html_dir, "styles.css"), encoding="utf-8") as f:
            css = "<style>\n" + f.read() + "\n</style>"

        # Inject CSS into HTML
        html = html.replace("</head>", css + "</head>")

        # Fetch data from the database
        db_path = os.path.join(os.path.dirname(__file__), "..", "..", "..", "backend", "src", "db", "example.db")
        if not os.path.exists(db_path):
            raise FileNotFoundError(f"Database file not found at: {db_path}")
        data = self._fetch_data_from_db(db_path)

        # Inject database data into HTML
        data_html = self._generate_data_html(data)
        html = html.replace("<!-- DATA_PLACEHOLDER -->", data_html)

        # Load the modified HTML
        self.frame.load_html(html)

    def _fetch_data_from_db(self, db_path):
        """Fetch data from the SQLite database."""
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Example query: Adjust based on your database schema
        cursor.execute("SELECT id, product, price, quantity, created_at, updated_at FROM data")
        data = cursor.fetchall()

        conn.close()
        return data

    def _generate_data_html(self, data):
        """Generate HTML from database data."""
        rows = ""
        for row in data[:10]:  # Fetch the first 10 rows
            rows += f"""
            <tr>
            <th>{row[0]}</th>
            <th>{row[1]}</th>
            <th>{row[2]}</th>
            <th>{row[3]}</th>
            <th>{row[4]}</th>
            <th>{row[5]}</th>
            </tr>
            """ if len(row) >= 6 else f"""
            <tr>
            {"".join(f"<th>{cell}</th>" for cell in row)}
            </tr>
            """
        return f"""
        <table border="1">
            <thead>
            <tr>
                <th>ID</th>
                <th>Product</th>
                <th>Description</th>
                <th>Price</th>
                <th>Quantity</th>
                <th>Created At</th>
                <th>Updated At</th>
            </tr>
            </thead>
            <tbody>
            {rows}
            </tbody>
        </table>
        """

    def _handle_link(self, url: str):
        parsed = urlparse(url)
        cmd = os.path.basename(parsed.path)

        if cmd == "python-test":
            self.test()
        else:
            print(f"Unknown command: {cmd}")

    def test(self):
        print("✅ test() was called from your HTML button!")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    MyRenderer().run()