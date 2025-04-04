"""
Database for tests
"""

from pathlib import Path
from typing import List, Optional

from sqlalchemy import Engine, ForeignKey, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, MappedAsDataclass, Session, mapped_column, relationship, sessionmaker


class Base(DeclarativeBase, MappedAsDataclass):
    """Base class for declarative base"""

    pass


class TestExhExhorto(Base):
    """Exhorto"""

    __tablename__ = "test_exh_exhortos"

    # Clave primaria
    id: Mapped[int] = mapped_column(primary_key=True, init=False)

    # Columnas
    exhorto_origen_id: Mapped[str]
    estado_origen_id: Mapped[int]
    folio_seguimiento: Mapped[Optional[str]]
    estado: Mapped[str]

    # Hijos
    test_exh_exhortos_archivos: Mapped[List["TestExhExhortoArchivo"]] = relationship(
        "TestExhExhortoArchivo",
        back_populates="test_exh_exhorto",
        init=False,
    )
    test_exh_exhortos_respuestas: Mapped[List["TestExhExhortoRespuesta"]] = relationship(
        "TestExhExhortoRespuesta",
        back_populates="test_exh_exhorto",
        init=False,
    )
    test_exh_exhortos_promociones: Mapped[List["TestExhExhortoPromocion"]] = relationship(
        "TestExhExhortoPromocion",
        back_populates="test_exh_exhorto",
        init=False,
    )


class TestExhExhortoArchivo(Base):
    """Archivo de Exhorto"""

    __tablename__ = "test_exh_exhortos_archivos"

    # Clave primaria
    id: Mapped[int] = mapped_column(primary_key=True, init=False)

    # Clave foránea
    test_exh_exhorto_id: Mapped[int] = mapped_column(ForeignKey("test_exh_exhortos.id"))
    test_exh_exhorto: Mapped["TestExhExhorto"] = relationship(back_populates="test_exh_exhortos_archivos")

    # Columnas
    nombre_archivo: Mapped[str]
    hash_sha1: Mapped[str]
    hash_sha256: Mapped[str]
    tipo_documento: Mapped[int]
    estado: Mapped[str]


class TestExhExhortoRespuesta(Base):
    """Respuesta"""

    __tablename__ = "test_exh_exhortos_respuestas"

    # Clave primaria
    id: Mapped[int] = mapped_column(primary_key=True, init=False)

    # Clave foránea
    test_exh_exhorto_id: Mapped[int] = mapped_column(ForeignKey("test_exh_exhortos.id"))
    test_exh_exhorto: Mapped["TestExhExhorto"] = relationship(back_populates="test_exh_exhortos_respuestas")

    # Columnas
    respuesta_origen_id: Mapped[str]
    estado: Mapped[str]

    # Hijos
    test_exh_exhortos_respuestas_archivos: Mapped[List["TestExhExhortoRespuestaArchivo"]] = relationship(
        "TestExhExhortoRespuestaArchivo",
        back_populates="test_exh_exhorto_respuesta",
        init=False,
    )


class TestExhExhortoRespuestaArchivo(Base):
    """Archivo de Respuesta"""

    __tablename__ = "test_exh_exhortos_respuestas_archivos"

    # Clave primaria
    id: Mapped[int] = mapped_column(primary_key=True, init=False)

    # Clave foránea
    test_exh_exhorto_respuesta_id: Mapped[int] = mapped_column(ForeignKey("test_exh_exhortos_respuestas.id"))
    test_exh_exhorto_respuesta: Mapped["TestExhExhortoRespuesta"] = relationship(
        back_populates="test_exh_exhortos_respuestas_archivos"
    )

    # Columnas
    nombre_archivo: Mapped[str]
    hash_sha1: Mapped[str]
    hash_sha256: Mapped[str]
    tipo_documento: Mapped[int]
    estado: Mapped[str]


class TestExhExhortoPromocion(Base):
    """Promoción"""

    __tablename__ = "test_exh_exhortos_promociones"

    # Clave primaria
    id: Mapped[int] = mapped_column(primary_key=True, init=False)

    # Clave foránea
    test_exh_exhorto_id: Mapped[int] = mapped_column(ForeignKey("test_exh_exhortos.id"))
    test_exh_exhorto: Mapped["TestExhExhorto"] = relationship(back_populates="test_exh_exhortos_promociones")

    # Columnas
    folio_origen_promocion: Mapped[str]
    folio_seguimiento: Mapped[str]
    estado: Mapped[str]

    # Hijos
    test_exh_exhortos_promociones_archivos: Mapped[List["TestExhExhortoPromocionArchivo"]] = relationship(
        "TestExhExhortoPromocionArchivo",
        back_populates="test_exh_exhorto_promocion",
        init=False,
    )


class TestExhExhortoPromocionArchivo(Base):
    """Archivo de Promoción"""

    __tablename__ = "test_exh_exhortos_promociones_archivos"

    # Clave primaria
    id: Mapped[int] = mapped_column(primary_key=True, init=False)

    # Clave foránea
    test_exh_exhorto_promocion_id: Mapped[int] = mapped_column(ForeignKey("test_exh_exhortos_promociones.id"))
    test_exh_exhorto_promocion: Mapped["TestExhExhortoPromocion"] = relationship(
        back_populates="test_exh_exhortos_promociones_archivos"
    )

    # Columnas
    nombre_archivo: Mapped[str]
    hash_sha1: Mapped[str]
    hash_sha256: Mapped[str]
    tipo_documento: Mapped[int]
    estado: Mapped[str]


def get_engine() -> Engine:
    """Database engine"""

    # File for database
    database_file = Path("tests/database.sqlite")

    # Create engine
    engine = create_engine(f"sqlite:///{database_file}")

    # Create tables if tests.sqlite does not exist
    if not database_file.exists():
        with engine.begin() as connection:
            Base.metadata.create_all(connection)

    return engine


def get_database_session() -> Session:
    """Database session"""

    # Create engine
    engine = get_engine()

    # Create session
    session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    # Create database session
    database = session_local()

    return database
