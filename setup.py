from setuptools import setup, Extension, find_packages
import os

ext_module = Extension(
    'cautogui.cautogui_core',
    sources=[os.path.join('src', 'core.cpp')],
    libraries=['user32', 'gdi32', 'gdiplus'],
    extra_compile_args=['/O2', '/std:c++17', '/MT']
)

setup(
    # Las URLs se definen aquí porque en el .toml las marcamos como dynamic
    project_urls={
        "Source": "https://github.com/danckard/cautogui",
        "Tracker": "https://github.com/danckard/cautogui/issues",
    },
    packages=find_packages(),
    ext_modules=[ext_module],
    zip_safe=False,
    include_package_data=True,
)