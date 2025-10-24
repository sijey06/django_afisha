from pytils import translit

from .constants import SLUG_LENGTH


def get_slug(title=""):
    return translit.get_slug(title)[:SLUG_LENGTH].replace("-", "_")
