from typing import Union, Any
from os import environ


def get_env(name: str, default: Any = None, required: bool = False, type: Union[int, bool, str] = str) -> Union[int, bool, str]:
    value = environ.get(name, default)

    if value is None and required:
        raise ValueError(f'Environment variable "{name}" must be set')

    if type == bool:
        return value in (True, 'True')
    elif type == int:
        return int(value)

    return value
