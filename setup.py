from setuptools import setup, Extension

# Definimos la extensión
# El nombre 'cautogui_core' debe coincidir con el de PyInit_cautogui_core en C++
core_module = Extension(
    'cautogui_core',
    sources=['src/core.cpp'],
    # Aquí puedes añadir optimizaciones de compilador más adelante
    extra_compile_args=['-O3'] 
)

setup(
    name='cautogui',
    version='0.1.0',
    description='C++ Backend for GUI Automation',
    ext_modules=[core_module],
)