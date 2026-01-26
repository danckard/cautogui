from setuptools import setup, Extension, find_packages
import os

ext_module = Extension(
    'cautogui_core',
    sources=[os.path.join('src', 'core.cpp')],
    libraries=['user32', 'gdi32', 'gdiplus'],
    extra_compile_args=['/O2', '/std:c++17']
)

setup(
    ext_modules=[ext_module],
    packages=find_packages(),
    include_package_data=True,
)