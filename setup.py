from setuptools import setup, Extension, find_packages
import os
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

ext_module = Extension(
    'cautogui_core',
    sources=[os.path.join('src', 'core.cpp')],
    libraries=['user32', 'gdi32', 'gdiplus'],
    extra_compile_args=['/O2', '/std:c++17']
)


setup(
    name="cautogui",
    # use_scm_version=True ya lo tienes para los tags
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
    
    # ESTO es lo que falta para PyPI:
    description="High-performance GUI automation with C++ core",
    long_description=long_description,
    long_description_content_type='text/markdown',
    
    author="danckard",
    url="https://github.com/danckard/cautogui",
    
    packages=find_packages(),
    ext_modules=[
        Extension(
            "cautogui.core",
            sources=["cautogui/core.cpp"],
            language='c++',
        ),
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
    ],
    python_requires='>=3.8',
)