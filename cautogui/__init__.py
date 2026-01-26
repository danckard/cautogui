"""
CAutoGUI - Motor de automatización de alto rendimiento
"""

from .cautogui import (
    cautogui,
    Tweens,
    # Exponemos los tweens más comunes directamente para facilidad de uso
    linear,
    easeInQuad,
    easeOutQuad,
    easeInOutQuad,
    easeInCubic,
    easeOutCubic,
    easeInOutCubic,
    easeInSine,
    easeOutSine,
    easeInOutSine,
    easeInExpo,
    easeOutExpo,
    easeInElastic,
    easeOutElastic,
    easeInBack,
    easeOutBack,
    easeInBounce,
    easeOutBounce
)

# Definimos qué se exporta cuando alguien hace 'from cautogui import *'
__all__ = [
    'cautogui',
    'Tweens',
    'linear',
    'easeInQuad',
    'easeOutQuad',
    'easeInOutQuad',
    'easeInCubic',
    'easeOutCubic',
    'easeInOutCubic',
    'easeInSine',
    'easeOutSine',
    'easeInOutSine',
    'easeInExpo',
    'easeOutExpo',
    'easeInElastic',
    'easeOutElastic',
    'easeInBack',
    'easeOutBack',
    'easeInBounce',
    'easeOutBounce'
]

__version__ = '1.0.0'