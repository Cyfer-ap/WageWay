from django.core.cache import cache
import time

def set_user_online(user):
    cache.set(f'online_{user.id}', time.time(), timeout=300)

def is_user_online(user):
    return cache.get(f'online_{user.id}') is not None

