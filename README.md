# Proyecto-Final-Prepa-EM2025

## Descripción
Este proyecto es una aplicación de gestión de inventarios y transacciones, diseñada para facilitar la administración de productos, búsqueda, actualizaciones y transacciones en una base de datos SQLite. Incluye una interfaz gráfica de usuario (GUI) desarrollada con `tkinter` y una interfaz de línea de comandos (CLI) para mayor flexibilidad.

## Autores
- Fernando Chávez Nolasco ─ A01284698
- Andrés Rodríguez Cantú ─ A01287002
- Roberto André Guevara Martínez ─ A01287324
- Víctor Manuel Sánchez Chávez ─ A01287522

## Características
- **Interfaz gráfica (GUI):** Permite agregar, actualizar, buscar y realizar transacciones de productos.
- **Interfaz de línea de comandos (CLI):** Ofrece comandos para gestionar la base de datos y realizar operaciones directamente desde la terminal.
- **Colores personalizados:** Utiliza colores para mejorar la experiencia visual en la terminal.
- **Historial de comandos:** Navegación por comandos anteriores en la CLI.
- **Soporte para transacciones:** Gestión de inventarios con validación de cantidades.
- **Base de datos SQLite:** Almacena los datos de productos y transacciones.

## Requisitos
- Python 3.10 o superior
- Dependencias adicionales (instalables con `pip`):
  - `tkinterweb`
  - `prettytable`

## Instalación
1. Clona este repositorio:
   ```bash
   git clone https://github.com/TEC-Andres/Proyecto-Final-Prepa-EM2025
   cd Proyecto-Final-Prepa-EM2025
   ```
2. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

## Uso
### Interfaz Gráfica (GUI)
1. Ejecuta el archivo `ft-gui.py`:
   ```bash
   python src/controllers/ft-gui.py
   ```
2. Usa la interfaz para agregar, actualizar, buscar y realizar transacciones.

### Interfaz de Línea de Comandos (CLI)
1. Ejecuta el archivo `ft-bash.py`:
   ```bash
   python src/controllers/ft-bash.py
   ```
2. Escribe `help` para ver los comandos disponibles.

### Comandos Disponibles
- `create [name]`: Crea una nueva base de datos.
- `read [page] [limit]`: Lee registros con paginación.
- `add [product] [description] [price] [quantity]`: Agrega un nuevo registro.
- `update [id] [product] [description] [price] [quantity]`: Actualiza un registro existente.
- `delete [id]`: Elimina un registro por ID.
- `search [term]`: Busca registros por término.
- `transaction [id/product] [amount]`: Realiza una transacción de inventario.
- `cls`: Limpia la pantalla.
- `exit`: Sale del programa.

## Funcionalidades Clave
### Gestión de Base de Datos
El archivo [`commands.py`](src/utils/commands.py) contiene las funciones principales para interactuar con la base de datos SQLite. Por ejemplo, la función `add` permite agregar un nuevo producto:
```python
def add(self, product, description, price, quantity):
    self.cursor.execute("""
        INSERT INTO data (product, description, price, quantity) 
        VALUES (?, ?, ?, ?)
    """, (product, description, price, quantity))
    self.conn.commit()
    message.success("Record added successfully.")
```

### Interfaz Gráfica
El archivo [`ft-gui.py`](src/controllers/ft-gui.py) implementa la GUI utilizando `tkinter`. Por ejemplo, la clase `AddPage` permite agregar productos y mostrarlos en una tabla:
```python
self.tree = ttk.Treeview(self, columns=cols, show="headings", height=8)
for c in cols:
    self.tree.heading(c, text=c.replace("_", " ").title())
    self.tree.column(c, anchor="w", width=120)
self.tree.pack(fill=tk.BOTH, expand=True, pady=(20, 0))
```

### Interfaz de Línea de Comandos
El archivo [`ft-bash.py`](src/controllers/ft-bash.py) permite ejecutar comandos directamente desde la terminal. Por ejemplo, el comando `transaction` realiza una transacción de inventario:
```python
def transaction(self, identifier, amount):
    self.cursor.execute("SELECT id, product, quantity FROM data WHERE id = ?", (int(identifier),))
    row = self.cursor.fetchone()
    new_quantity = current_quantity + int(amount)
    self.cursor.execute("UPDATE data SET quantity = ? WHERE id = ?", (new_quantity, id))
    self.conn.commit()
```

## Estructura del Proyecto
```
Proyecto-Final-Prepa-EM2025/
├── lib/                # Módulos de soporte (colores, mensajes, entrada personalizada)
├── src/
│   ├── controllers/    # Controladores para GUI y CLI
│   ├── utils/          # Funciones y comandos de utilidad
├── requirements.txt    # Dependencias del proyecto
├── README.md           # Documentación del proyecto
└── .gitignore          # Archivos ignorados por Git
```

## Licencia
Este proyecto es propiedad del Tecnológico de Monterrey y fue desarrollado como parte del curso **Innovación Tecnológica**.

## Créditos
Agradecimientos a los autores y colaboradores por su dedicación y esfuerzo en el desarrollo de este proyecto.
