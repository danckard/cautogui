from setuptools import setup, Extension, find_packages
import os

ext_module = Extension(
    'cautogui_core',
    sources=[os.path.join('src', 'core.cpp')],
    libraries=['user32', 'gdi32', 'gdiplus'],
    extra_compile_args=['/O2', '/std:c++17']
)

setup(
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
    include_package_data=True,
)