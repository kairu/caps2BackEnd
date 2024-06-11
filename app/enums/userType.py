from .common import enum

class user_type(enum.IntEnum):
    SUPER_ADMIN = 1
    ADMIN = 2
    OWNER = 3
    TENANT = 4
    GUEST = 5