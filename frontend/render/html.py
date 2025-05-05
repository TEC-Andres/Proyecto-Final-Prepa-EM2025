import tkinter as tk
from tkinterweb import HtmlFrame
import os
from urllib.parse import urlparse

class MyRenderer:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("HTML Renderer")
        self.root.geometry("800x600")

        # Create HtmlFrame with on_link_click handler
        self.frame = HtmlFrame(
            self.root,
            horizontal_scrollbar="auto",
            on_link_click=self._handle_link
        )
        self.frame.pack(fill="both", expand=True)

        # Load and inline HTML and CSS
        html_dir = os.path.join(os.path.dirname(__file__), "..", "webpage")
        with open(os.path.join(html_dir, "index.html"), encoding="utf-8") as f:
            html = f.read()
        with open(os.path.join(html_dir, "styles.css"), encoding="utf-8") as f:
            css = "<style>\n" + f.read() + "\n</style>"

        # Inject CSS into HTML
        html = html.replace("</head>", css + "</head>")

        # Load the modified HTML
        self.frame.load_html(html)

    def _handle_link(self, url: str):
        # parse out the file:// path and grab only the final component
        parsed = urlparse(url)
        cmd = os.path.basename(parsed.path)

        if cmd == "test":
            self.test()
        else:
            print(f"Unknown command: {cmd}")

    def test(self):
        print("✅ test() was called from your HTML button!")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    MyRenderer().run()
