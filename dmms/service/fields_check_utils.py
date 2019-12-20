from typing import Any, Iterable
from flask_restful import abort


def all_parameters_is_filled(args: dict) -> None:
    """Check if all parameter is filled"""
    if not all(args.values()):
        abort(400, message=f"You haven't pass these parameters: "
                           f"{[x for x in args.keys() if not args[x]]}")
    return None


def any_parameter_is_filled(args: dict) -> None:
    """Check if any parameter is filled"""
    if not any(args.values()):
        abort(400, message='Please provide at least one value to update')
    return None


def item_exists(result: Any, item_type: str, identificator: str) -> None:
    """Check if item is not None"""
    if not result:
        abort(404, message=f"{item_type} {identificator} doesn't exist")
    return None


def value_is_positive(keys: Iterable[str], args: dict) -> None:
    """Check if value is positive"""
    for key in keys:
        if args[key] and args[key] <= 0:
            abort(406, message=f'Please provide higher then zero value '
                               f'for {key}')
        return None


def value_provided(value: Any, operation: str) -> None:
    """Check if value is provided"""
    if not value:
        abort(406, message=f'Please provide id for {operation}')
    return None


def not_wrong_url(value) -> None:
    """Check if value is not provided"""
    if value:
        abort(404, message='Page not found')
    return None
