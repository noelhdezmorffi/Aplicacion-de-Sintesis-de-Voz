"""
Script de instalación para la aplicación Lector IA.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="lector-ia",
    version="1.0.0",
    author="Neutr",
    description="Aplicación offline para leer en voz alta documentos e imágenes",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/lector-ia",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "PyQt5>=5.15.0",
        "pyttsx3>=2.90",
        "PyPDF2>=3.0.0",
        "python-docx>=0.8.10",
        "Pillow>=9.0.0",
        "pytesseract>=0.3.10",
        "mss>=9.0.0",
    ],
    entry_points={
        "console_scripts": [
            "lector-ia=ui.main_window:main",
        ],
    },
)
