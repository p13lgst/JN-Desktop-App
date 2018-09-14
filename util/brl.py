import re
from decimal import Decimal


def parse_brl(s):
    """Parse formated BRL string into Decimal."""

    # Return zero if empty.
    if not s:
        return Decimal()

    # Split into integer and decimal parts.
    s = re.split('[.,]', s, maxsplit=1)

    # Unpack values, with default.
    integer_part = s[0]
    decimal_part = s[1] if len(s) == 2 else ''

    # Filter the digits.
    integer_part = ''.join(i for i in integer_part if i.isdigit())
    decimal_part = ''.join(i for i in decimal_part if i.isdigit())

    # Return zero if borh parts don't exist.
    if not (integer_part or decimal_part):
        return Decimal()

    # Return one parsed part if other doesn't exist.
    elif not decimal_part:
        return Decimal(integer_part)
    elif not integer_part:
        return Decimal('.' + decimal_part)

    # Return parsed decimal with both parts because both exist.
    return Decimal('.'.join((integer_part, decimal_part)))


def format_brl(n):
    """Format a Decimal into BRL format."""
    # Split into integer and decimal parts.
    n = str(n).split('.')

    # Upack and parse the values hanling missing values.
    integer_part = n[0]
    if len(n) == 1:
        decimal_part = '00'
    else:
        decimal_part = n[1][:2]
        if len(decimal_part) == 1:
            decimal_part += '0'

    return "R${0},{1}".format(integer_part, decimal_part)
