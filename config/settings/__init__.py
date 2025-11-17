import os

ENV = os.getenv("DJANGO_ENV", "dev")  # default: dev

if ENV == "prod":
    from .production import *
else:
    from .local import *
