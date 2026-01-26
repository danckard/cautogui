from setuptools import setup, Extension, find_packages
from pathlib import Path
import os

# Leer el README.md para que aparezca en PyPI
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

# Tu extensión tal cual la pediste
ext_module = Extension(
    'cautogui_core',
    sources=[os.path.join('src', 'core.cpp')],
    libraries=['user32', 'gdi32', 'gdiplus'],
    extra_compile_args=['/O2', '/std:c++17']
)

setup(
    name="cautogui",
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
    
    # Metadatos para danckard en PyPI
    author="danckard",
    description="High-performance GUI automation with C++ core",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/danckard/cautogui",
    
    project_urls={
        "Source": "https://github.com/danckard/cautogui",
        "Tracker": "https://github.com/danckard/cautogui/issues",
    },

    packages=find_packages(),
    ext_modules=[ext_module], # Usamos tu objeto aquí
    
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
    ],
    python_requires='>=3.8',
    zip_safe=False,
)