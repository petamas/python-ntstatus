__all__ = [
    'ThirtyTwoBits',
]

from dataclasses import dataclass

@dataclass(frozen=True)
class ThirtyTwoBits:
    """
    Class representing 32 bits that can be interpreted either as a signed or unsigned 32-bit integer.
    ThirtyTwoBits values can be equality-compared to integers; the comparision will return True for both the signed and unsigned interpretation of the underlying 32 bits.
    """

    underlying_unsigned_value: int

    def __init__(self, value: int) -> None:
        """
        Constructor a ThirtyTwoBits object. Argument can be any (signed or unsigned) value that can be represented in 32 bits, i.e. any value in the range [-2147483648, 4294967295].
        Passing a value not representable in 32 bits raises a ValueError, while passing any other type of value raises a TypeError.
        """

        if not isinstance(value, int):
            raise TypeError(f'Not a valid int value: {repr(value)}')

        min_signed = -2**31
        max_unsigned = 2**32-1
        if value < min_signed or value > max_unsigned:
            raise ValueError(f'Value must be in [{min_signed}, {max_unsigned}] to be representable in 32 bits: {value}')

        if value < 0:
            value = value + 2**32

        # Get around frozen=True's limitation
        # See details here: https://stackoverflow.com/a/58336722
        object.__setattr__(self, 'underlying_unsigned_value', value)

    @property
    def unsigned_value(self) -> int:
        """
        The numeric value of the ThirtyTwoBits object, interpreted as a 32-bit unsigned integer.
        Always will be in range [0, 4294967295].
        x == x.usigned_value returns True for all ThirtyTwoBits values.
        """

        return self.underlying_unsigned_value

    @property
    def signed_value(self) -> int:
        """
        The numeric value of the ThirtyTwoBits object, interpreted as a 32-bit signed integer.
        Always will be in range [-2147483648, 2147483647].
        x == x.signed_value returns True for all ThirtyTwoBits values.
        """

        return (self.underlying_unsigned_value ^ 0x80000000) - 0x80000000

    def __eq__(self, other: object) -> bool:
        """
        Equality check for NtStatus. It supports checking ThirtyTwoBits instances against other ThirtyTwoBits instances and ints.
        In the latter case, returns True for both the signed and unsigned interpretation of the underlying 32 bits.
        """

        if isinstance(other, ThirtyTwoBits):
            return self.underlying_unsigned_value == other.underlying_unsigned_value

        if isinstance(other, int):
            try:
                return self == ThirtyTwoBits(other)
            except ValueError:
                return False

        return NotImplemented
