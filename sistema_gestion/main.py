import customtkinter as ctk
from app.database.database_manager import DatabaseManager

class App(ctk.CTk):
    def __init__(self, db_manager):
        super().__init__()

        self.db_manager = db_manager

        # --- Basic Window Configuration ---
        self.title("El Programita 2.0")
        self.geometry("800x600")

        # --- Main Layout ---
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- Placeholder Frame ---
        # This is where we will build the "New Order" form in the next step.
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        self.label = ctk.CTkLabel(self.main_frame, text="Aplicación Iniciada. Base de datos conectada.", font=("Arial", 20))
        self.label.pack(expand=True)


if __name__ == "__main__":
    # This is the starting point of the whole application

    # 1. Instantiate the Database Manager
    db_manager = DatabaseManager()

    # 2. Ensure the database and tables are created
    db_manager.crear_base_de_datos()

    # 3. Create and run the main application window
    app = App(db_manager)
    app.mainloop()
