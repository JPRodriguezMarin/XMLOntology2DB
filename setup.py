from setuptools import setup, find_packages

setup(
    name="ontology2db",
    version="1.0.0",
    author="Tu Nombre",
    author_email="tu@email.com",
    description="Conversor de ontologías XML a modelos SQLAlchemy",
    packages=find_packages(),
    python_requires=">=3.10",
    install_requires=[
        "lxml>=4.9.0",
        "SQLAlchemy>=2.0.0",
        "networkx>=3.0",
    ],
    entry_points={
        "console_scripts": [
            "ontology2db=ontology2db.cli:main",
        ],
    },
)
