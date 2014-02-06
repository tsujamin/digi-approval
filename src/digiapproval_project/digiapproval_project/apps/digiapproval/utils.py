"""Various useful utilities."""
from functools import wraps
from django.utils.cache import patch_cache_control


def never_cache(function=None):
    """
    Decorator to make sure that pages are not cached.
    More rigorous than the built in Django one: see
    http://stackoverflow.com/a/13512008/463510 which is implementing
    http://stackoverflow.com/q/49547/463510
    """
    @wraps(function)
    def wrapper(*args, **kwargs):
        response = function(*args, **kwargs)
        patch_cache_control(
            response, no_cache=True, no_store=True, must_revalidate=True,
            max_age=0)
        return response

    return wrapper
