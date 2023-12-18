import importlib.metadata

__author__ = "Ivan Zanardi"
__email__ = "ivan.zanardi.us@gmail.com"
__url__ = "https://github.com/ivanZanardi/pyharm"
__license__ = "MIT License"
__version__ = importlib.metadata.version("pyharm")
__all__ = ["PolyHarmInterpolator"]

from .interpolator import PolyHarmInterpolator
