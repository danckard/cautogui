"""
CAutoGUI - Motor de automatización de alto rendimiento
"""
try:
    import cautogui_core
except ImportError:
    from . import cautogui_core

from .cautogui import (
    cautogui,
    Tweens,
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