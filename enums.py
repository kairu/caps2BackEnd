import enum
from sqlalchemy import Enum
class Cms_Enum(enum.IntEnum):
    ANNOUNCEMENT = 1
    NEWS = 2
    EVENT = 3
    RESERVATION = 4
    MAINTENANCE = 5
    FEEDBACK = 6
    COMPLAINT = 7

class user_type(enum.IntEnum):
    SUPER_ADMIN = 1
    ADMIN = 2
    OWNER = 3
    TENANT = 4
    GUEST = 5

class month(enum.IntEnum):
    JANUARY = 1
    FEBRUARY = 2
    MARCH = 3
    APRIL = 4
    MAY = 5
    JUNE = 6
    JULY = 7
    AUGUST = 8
    SEPTEMBER = 9
    OCTOBER = 10
    NOVEMBER = 11
    DECEMBER = 12

class status(enum.IntEnum):
    PENDING = 1
    REVIEW = 2
    PAID = 3

class bill_type(enum.IntEnum):
    UTILITY = 1
    ASSOCIATION = 2
    PARKING = 3
    MAINTENANCE = 4
    INTERNETCABLE = 5
    ETC = 6