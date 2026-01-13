"""
Modelos generados automáticamente desde ontología.
"""
from sqlalchemy import Column, Integer, String, Text, Float, Boolean, DateTime, Date, Time
from sqlalchemy import ForeignKey, Table, UniqueConstraint
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

Base = declarative_base()


class Author(Base):
    """Representa un autor de libros"""
    __tablename__ = "Author"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    birth_date = Column(Date)
    books = relationship("Book", back_populates="author")

    def __repr__(self):
        return f"<Author(id={self.id})>"


class Book(Base):
    """Representa un libro"""
    __tablename__ = "Book"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    isbn = Column(String, nullable=False)
    author_id = Column(Integer, ForeignKey("Author.id"), nullable=False)
    author = relationship("Author", back_populates="books")

    def __repr__(self):
        return f"<Book(id={self.id})>"



def create_database(db_url: str = "sqlite:///ontology.db"):
    """Crea la base de datos con todas las tablas."""
    engine = create_engine(db_url, echo=True)
    Base.metadata.create_all(engine)
    return engine

def get_session(engine):
    """Retorna una sesión de SQLAlchemy."""
    return Session(engine)

def export_ddl(db_url: str = "sqlite:///ontology.db"):
    """Exporta el DDL SQL."""
    from sqlalchemy.schema import CreateTable
    engine = create_engine(db_url)
    for table in Base.metadata.sorted_tables:
        print(f"\n-- Table: {table.name}")
        print(CreateTable(table).compile(engine))
