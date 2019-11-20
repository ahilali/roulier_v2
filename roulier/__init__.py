# -*- coding: utf-8 -*-

from . import roulier
from . import exception
import logging
from . import carrier
from . import codec
from . import transport
__all__ = [roulier]
#__version__ = open('VERSION').read().strip()
log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())
