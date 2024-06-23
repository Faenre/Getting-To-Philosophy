"""Enumerated exit codes with descriptions for what they mean."""

from enum import Enum


class ExitCode(Enum):
    """Exit codes with an upward scaling enumeration and their string descriptions."""

    SUCCESS                     = 0, "Target found successfully!"
    TOO_MANY_HOPS               = 1, "Path exceeded maximum hop limit."
    DEAD_END                    = 2, 'Dead-end found. No more pages to search.'
    NO_CURRENT_PAGE             = 3, 'No current page. Aborting.'
    TARGET_PAGE_DOES_NOT_EXIST  = 4, 'Destination page does not exist.'

    def __new__(cls, value, description):
        obj = object.__new__(cls)
        obj._value_ = value
        obj.description = description
        return obj

    def __int__(self):
        return self.value
