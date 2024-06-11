from .common import enum

class bill_type(enum.IntEnum):
    WATER = 1 
    ASSOCIATION = 2 # INterest
    PARKING = 3 # Interest
    MAINTENANCE = 4
    ETC = 5