import customtkinter as ctk
from app.database.database_manager import DatabaseManager

class NewOrderForm(ctk.CTkFrame):
    """
    A frame containing the form to create a new order.
    """
    def __init__(self, master, db_manager):
        super().__init__(master)
        self.db_manager = db_manager

        # --- Configure Grid Layout ---
        self.grid_columnconfigure(1, weight=1)

        # --- Widgets ---
        # Client
        self.client_label = ctk.CTkLabel(self, text="Cliente:")
        self.client_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.client_entry = ctk.CTkEntry(self, placeholder_text="Nombre del cliente")
        self.client_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        # Amount
        self.amount_label = ctk.CTkLabel(self, text="Monto Total:")
        self.amount_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.amount_entry = ctk.CTkEntry(self, placeholder_text="Ej: 15000.50")
        self.amount_entry.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        # Description
        self.desc_label = ctk.CTkLabel(self, text="Descripción:")
        self.desc_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.desc_entry = ctk.CTkEntry(self, placeholder_text="Detalles del pedido")
        self.desc_entry.grid(row=2, column=1, padx=10, pady=10, sticky="ew")

        # Save Button
        self.save_button = ctk.CTkButton(self, text="Guardar Pedido", command=self.save_order)
        self.save_button.grid(row=3, column=1, padx=10, pady=20, sticky="e")

    def save_order(self):
        """
        Gets data from entries and calls the database manager to save the order.
        """
        client_name = self.client_entry.get()
        amount_str = self.amount_entry.get()
        description = self.desc_entry.get()

        # --- Basic Validation ---
        if not client_name or not amount_str:
            print("Error: Cliente y Monto son campos obligatorios.")
            # Here we could show a popup error message.
            return

        try:
            amount = float(amount_str)
        except ValueError:
            print("Error: El monto debe ser un número válido.")
            # Here we could show a popup error message.
            return

        # --- Call Database Manager ---
        self.db_manager.create_pedido(
            cliente_nombre=client_name,
            monto_total=amount,
            descripcion=description
        )

        # --- Clear fields for next entry ---
        self.client_entry.delete(0, 'end')
        self.amount_entry.delete(0, 'end')
        self.desc_entry.delete(0, 'end')
        self.client_entry.focus() # Set focus back to the first field
        print("Formulario limpiado.")


class App(ctk.CTk):
    def __init__(self, db_manager):
        super().__init__()
        self.db_manager = db_manager

        self.title("El Programita 2.0")
        self.geometry("800x400") # Adjusted size for the form

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- Instantiate and place the form ---
        self.order_form = NewOrderForm(master=self, db_manager=self.db_manager)
        self.order_form.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")


if __name__ == "__main__":
    db_manager = DatabaseManager()
    db_manager.crear_base_de_datos()

    app = App(db_manager)
    app.mainloop()
