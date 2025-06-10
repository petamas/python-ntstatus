# ntstatus

`ntstatus` is a library that defines a Python constants to represent [WinAPI NTSTATUS values](https://learn.microsoft.com/en-us/windows-hardware/drivers/kernel/using-ntstatus-values).

## `ntstatus.NtStatus`

This class defines all named [WinAPI NTSTATUS values](https://learn.microsoft.com/en-us/windows-hardware/drivers/kernel/using-ntstatus-values) as attributes.

Constants are represented using the `ntstatus.ThirtyTwoBits` class which can be equality-compared to integers; the comparision will return True for both the signed and unsigned interpretation of the underlying 32 bits.

Static methods:
- `NtStatus.decode(code)`: Looks up an NTSTATUS constant by its numeric value and returns it as an `ntstatus.ThirtyTwoBits` object, with its name set to the the name of the constant. Returns `None` if argument is not a known NTSTATUS constant.
- `NtStatus.decode_name(code, default='')`: Returns the name of the NTSTATUS value associated with the first argument if there is such a value. Otherwise, returns the second argument.
- `NtStatus.make(code)`: Looks up an NTSTATUS constant by its numeric value and returns it as an `ntstatus.ThirtyTwoBits` object, with its name set to the the name of the constant. Raises `ValueError` if argument is not a known NTSTATUS value.
- `NtStatus.severity(status)`: Returns the severity of an NTSTATUS value represented by an `ntstatus.ThirtyTwoBits` object as an `ntstatus.NtStatusSeverity`.

The complete list of NTSTATUS values can be found [here](https://learn.microsoft.com/en-us/openspecs/windows_protocols/ms-erref/596a1078-e883-4972-9bbc-49e60bebca55). `NtStatus` encodes most of them, with the exception of:

- `STATUS_WAIT_n`, where `n` is 0, 1, 2, 3, and 63
- `STATUS_ABANDONED_WAIT_n`, where `n` is 0 and 63
- `STATUS_FLT_DISALLOW_FSFILTER_IO`

## `ntstatus.ThirtyTwoBits`

This class represents 32 bits that can be interpreted either as a signed or unsigned 32-bit integer, with an additional name field.
`ntstatus.ThirtyTwoBits` values can be equality-compared to integers; the comparision will return `True` for both the signed and unsigned interpretation of the underlying 32 bits.

Properties:
- `signed_value`: The numeric value, interpreted as a 32-bit signed integer.
- `unsigned_value`: The numeric value, interpreted as a 32-bit unsigned integer.
- `exit_code`: The numeric value, interpreted in a way that it can be passed to `sys.exit()` without information loss. (Alias to `signed_value`.)
- `name`: Name that can be used to refer to the value in human contexts. Typically the name of a WinAPI constant.

Static methods:
- `ThirtyTwoBits.check(value)`: Checks if `value` can be represented as a 32-bit signed or unsigned integer. If `value` is not an `int`, raises `TypeError`. If `value` is an `int`, but it cannot fit into 32 bits, raises `ValueError`.

## Usage examples

Import the `NtStatus` class:

```
>>> from ntstatus import NtStatus
```

`ntstatus.ThirtyTwoBits` values can be interpreted both as signed and unsigned integer:

```
>>> NtStatus.STATUS_DLL_NOT_FOUND
ThirtyTwoBits(0xC0000135, 'STATUS_DLL_NOT_FOUND')

>>> NtStatus.STATUS_DLL_NOT_FOUND.unsigned_value
3221225781

>>> NtStatus.STATUS_DLL_NOT_FOUND.signed_value
-1073741515
```

`ntstatus.ThirtyTwoBits` values can be compared to both the signed and unsigned interpretation of the underlying 32 bits:

```
>>> NtStatus.STATUS_DLL_NOT_FOUND == 0xC0000135
True

>>> NtStatus.STATUS_DLL_NOT_FOUND == 3221225781
True

>>> NtStatus.STATUS_DLL_NOT_FOUND == -1073741515
True
```

NTSTATUS constants can be looked up based on both the signed and unsigned interpretation of the underlying 32 bits:

```
>>> NtStatus.decode(0xC0000135)
ThirtyTwoBits(0xC0000135, 'STATUS_DLL_NOT_FOUND')

>>> NtStatus.decode(3221225781)
ThirtyTwoBits(0xC0000135, 'STATUS_DLL_NOT_FOUND')

>>> NtStatus.decode(-1073741515)
ThirtyTwoBits(0xC0000135, 'STATUS_DLL_NOT_FOUND')

>>> NtStatus.make(0xC0000135)
ThirtyTwoBits(0xC0000135, 'STATUS_DLL_NOT_FOUND')

>>> NtStatus.make(3221225781)
ThirtyTwoBits(0xC0000135, 'STATUS_DLL_NOT_FOUND')

>>> NtStatus.make(-1073741515)
ThirtyTwoBits(0xC0000135, 'STATUS_DLL_NOT_FOUND')
```

`NtStatus.make()` raises `ValueError` if the value is not representable in 32 bits, or if it is not a known NTSTATUS:

```
>>> NtStatus.make(0xCC0300000)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "d:\projects\python-libs\ntstatus\ntstatus\_ntstatus.py", line 78, in make
    status = NtStatus.decode(code)
  File "d:\projects\python-libs\ntstatus\ntstatus\_ntstatus.py", line 55, in decode
    ThirtyTwoBits.check(code)
  File "d:\projects\python-libs\ntstatus\ntstatus\_thirtytwobits.py", line 28, in check
    raise ValueError(f'Value must be in [{min_signed}, {max_unsigned}] to be representable in 32 bits: {value}')
ValueError: Value must be in [-2147483648, 4294967295] to be representable in 32 bits: 54763978752

>>> NtStatus.make(0xC0300000)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "d:\projects\python-libs\ntstatus\ntstatus\_ntstatus.py", line 82, in make
    raise ValueError(f'Unknown NTSTATUS value: {code}')
ValueError: Unknown NTSTATUS value: 3224371200
```

`NtStatus.decode()` returns `None` in both cases:

```
>>> NtStatus.decode(0xC0300000) is None
True

>>> NtStatus.decode(0xCC0300000) is None
True
```

Name for numeric values can be safely queried:

```
>>> NtStatus.decode_name(-1073741515)
'STATUS_DLL_NOT_FOUND'

>>> NtStatus.decode_name(0xC0000135)
'STATUS_DLL_NOT_FOUND'

>>> NtStatus.decode_name(0xC0300000)
''

>>> NtStatus.decode_name(-1073741515, 'No NTSTATUS definition found')
'STATUS_DLL_NOT_FOUND'

>>> NtStatus.decode_name(0xC0000135, 'No NTSTATUS definition found')
'STATUS_DLL_NOT_FOUND'

>>> NtStatus.decode_name(0xC0300000, 'No NTSTATUS definition found')
'No NTSTATUS definition found'
```

`exit_code` can be used in `sys.exit()` without information loss:
```
>>> import sys
>>> sys.exit(NtStatus.STATUS_DLL_NOT_FOUND.exit_code)

(.venv) d:\projects\ntstatus>echo %ERRORLEVEL%
-1073741515
```

Using the unsigned interpretation would lead to information loss ([see explanation](https://stackoverflow.com/a/63387879)):

```
>>> import sys
>>> sys.exit(NtStatus.STATUS_DLL_NOT_FOUND.unsigned_value)

(.venv) d:\projects\ntstatus>echo %ERRORLEVEL%
-1
```

## List of values


## Licensing

This library is licensed under the MIT license.

