import os

DEBUG = os.getenv("DEBUG", True)

if DEBUG:
    from .local import *  # noqa
else:
    from .production import *  # noqa
