from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ontology2db",
    version="1.0.0",
    author="Tu Nombre",
    author_email="tu@email.com",
    description="Conversor de ontologías XML a modelos SQLAlchemy",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tuusuario/ontology2db",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Code Generators",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.10",
    install_requires=[
        "lxml>=4.9.0",
        "SQLAlchemy>=2.0.0",
        "networkx>=3.0",
    ],
    extras_require={
        "viz": ["pyvis>=0.3.2", "matplotlib>=3.7.0"],
        "dev": ["pytest>=7.4.0", "pytest-cov>=4.1.0"],
    },
    entry_points={
        "console_scripts": [
            "ontology2db=ontology2db.cli:main",
        ],
    },
)
