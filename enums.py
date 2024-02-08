import enum

class Cms_Enum(enum.Enum):
    ANNOUNCEMENT = 1
    NEWS = 2
    EVENT = 3
    RESERVATION = 4
    MAINTENANCE = 5
    FEEDBACK = 6
    COMPLAINT = 7

class user_type(enum.Enum):
    SUPER_ADMIN = 1
    ADMIN = 2
    OWNER = 3
    TENANT = 4

class month(enum.Enum):
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

class status(enum.Enum):
    PENDING = 1
    REVIEW = 2
    PAID = 3

class bill_type(enum.Enum):
    UTILITY = 1
    ASSOCIATION = 2
    PARKING = 3
    MAINTENANCE = 4
    INTERNETCABLE = 5
    ETC = 6