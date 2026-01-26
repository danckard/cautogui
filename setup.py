from setuptools import setup, Extension, find_packages

module = Extension(
    'cautogui_core',
    sources=['src/core.cpp'],
    libraries=['user32', 'gdi32'],
    extra_compile_args=['/O2'] # Optimización de velocidad máxima
)

setup(
    name='cautogui',
    version='1.0.0',
    author='danckard',
    description='High-performance automation engine',
    ext_modules=[module],
    packages=find_packages(),
    py_modules=['cautogui'],
    install_requires=['Pillow'],
    python_requires='>=3.7',
)