import os

if os.getenv('K_SERVICE', None) or os.getenv('CLOUD_BUILD', None):
    PROD = True
else:
    PROD = False

from .base import *

if PROD:
    from .prod import *
else:
    from .dev import *
