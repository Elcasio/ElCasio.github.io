import enum
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey, Enum as SQLAlchemyEnum
from sqlalchemy.orm import relationship, declarative_base

# Base declarativa para los modelos de SQLAlchemy
Base = declarative_base()

# --- Enums para estandarizar los estados ---
# Usar Enums previene errores de tipeo y mantiene los datos consistentes.

class EstadoPago(enum.Enum):
    PENDIENTE = "PENDIENTE"
    PAGADO = "PAGADO"
    DEUDA_PARCIAL = "DEUDA PARCIAL"
    SALDO_A_FAVOR = "SALDO A FAVOR"

class EstadoEntrega(enum.Enum):
    PENDIENTE = "PENDIENTE"
    EN_VIAJE = "EN VIAJE"
    ENTREGADO = "ENTREGADO"

class TipoMovimiento(enum.Enum):
    INGRESO = "INGRESO"
    EGRESO = "EGRESO"

# --- Modelos de las Tablas ---

class Cliente(Base):
    __tablename__ = 'clientes'
    id = Column(Integer, primary_key=True)
    nombre = Column(String, nullable=False, unique=True)
    telefono = Column(String)

    # Relación: Un cliente puede tener muchos pedidos
    pedidos = relationship("Pedido", back_populates="cliente")

class Remito(Base):
    __tablename__ = 'remitos'
    id = Column(Integer, primary_key=True)
    fecha_creacion = Column(DateTime, nullable=False, default=datetime.now)

    # Relación: Un remito agrupa varios pedidos
    pedidos = relationship("Pedido", back_populates="remito")

class Pedido(Base):
    __tablename__ = 'pedidos'
    id = Column(Integer, primary_key=True)
    fecha_carga = Column(DateTime, nullable=False, default=datetime.now)
    monto_total = Column(Float, nullable=False)
    monto_cobrado = Column(Float, default=0.0)
    descripcion = Column(String)

    estado_pago = Column(SQLAlchemyEnum(EstadoPago), default=EstadoPago.PENDIENTE)
    estado_entrega = Column(SQLAlchemyEnum(EstadoEntrega), default=EstadoEntrega.PENDIENTE)

    # Claves foráneas y relaciones
    cliente_id = Column(Integer, ForeignKey('clientes.id'), nullable=False)
    cliente = relationship("Cliente", back_populates="pedidos")

    remito_id = Column(Integer, ForeignKey('remitos.id'), nullable=True)
    remito = relationship("Remito", back_populates="pedidos")

    movimientos_caja = relationship("MovimientoCaja", back_populates="pedido")

class MovimientoCaja(Base):
    __tablename__ = 'caja'
    id = Column(Integer, primary_key=True)
    fecha = Column(DateTime, nullable=False, default=datetime.now)
    tipo = Column(SQLAlchemyEnum(TipoMovimiento), nullable=False)
    descripcion = Column(String, nullable=False)
    monto = Column(Float, nullable=False)

    # Relación opcional con un pedido (si es un cobro)
    pedido_id = Column(Integer, ForeignKey('pedidos.id'), nullable=True)
    pedido = relationship("Pedido", back_populates="movimientos_caja")
