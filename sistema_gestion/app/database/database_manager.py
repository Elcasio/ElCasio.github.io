from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base, Cliente, Pedido, Remito
from datetime import datetime

class DatabaseManager:
    """
    Clase para manejar todas las operaciones de la base de datos.
    """
    def __init__(self, db_name='sistema_gestion.db'):
        self.engine = create_engine(f'sqlite:///{db_name}')
        self.Session = sessionmaker(bind=self.engine)

    def crear_base_de_datos(self):
        Base.metadata.create_all(self.engine)
        print("Base de datos y tablas revisadas/creadas exitosamente.")

    def get_or_create_client(self, nombre, telefono=""):
        """
        Busca un cliente por nombre. Si no existe, lo crea.
        Devuelve el objeto Cliente.
        """
        session = self.Session()
        cliente = session.query(Cliente).filter_by(nombre=nombre).first()
        if not cliente:
            cliente = Cliente(nombre=nombre, telefono=telefono)
            session.add(cliente)
            session.commit()
            print(f"Cliente '{nombre}' creado.")
        session.close()
        return cliente

    def create_pedido(self, cliente_nombre, monto_total, descripcion=""):
        """
        Crea un nuevo pedido en la base de datos.
        """
        session = self.Session()

        # 1. Obtener o crear el cliente
        cliente = self.get_or_create_client(cliente_nombre)

        # 2. Crear el objeto Pedido
        nuevo_pedido = Pedido(
            monto_total=monto_total,
            descripcion=descripcion,
            cliente_id=cliente.id,
            fecha_carga=datetime.now()
        )

        # 3. Añadir y guardar en la base de datos
        session.add(nuevo_pedido)
        session.commit()

        print(f"Pedido #{nuevo_pedido.id} para {cliente.nombre} creado exitosamente.")
        session.close()

        return nuevo_pedido
