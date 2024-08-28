import os
os.environ["DJANGO_READ_DOT_ENV_FILE"] = "true"
from .base import * # noqa
from .base import env

DEBUG = True

SECRET_KEY = env(
    "DJANGO_SECRET_KEY",
    default='django-insecure-lz%p#j7#%@adn7v56l+(iob-gz^s+09yyieh7&!y9yc1_8@zl1'
)

ALLOWED_HOSTS = ["localhost", "0.0.0.0", "127.0.0.1"]

# Application definition
# INSTALLED_APPS += []

