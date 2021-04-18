import functools
from .log import getLogger
from .exceptions import APIError


def network_try_except(function):
    """
        Wrap a function with a try/except and log on error
    """
    @functools.wraps(function)
    def wrap(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except APIError as e:
            getLogger().error(f"Error from API call: {e}")
            raise e
        except Exception as e:
            getLogger().error(f"Error from API call: {e}")
            raise APIError(f"Error in the call for {function.__name__}: {e}")
    return wrap


def is_login(function):
    """
        Check if the instance has a token (=is_login), if not, attempt to login.
    """
    @functools.wraps(function)
    def wrap(*args, **kwargs):
        if not args[0]:
            getLogger().critical(f"The decorator @is_login must get SPApi instance to be executed")
            raise APIError("Invalid call for @is_login")
        try:
            if not args[0].token:
                args[0].login()
        except Exception as e:
            getLogger().error(f"Failure to login the user")
            raise APIError(f"The user must be logged")
        return function(*args, **kwargs)
    return wrap


def supported_parameters(parameters):
    """
        Check if the given parameters are all supported

        :param parameters [str]: List of str, which represents the supported parameters
    """
    def _supported_parameters(function):
        def wrap(*args, **kwargs):
            invalid_keys = False
            for key, value in kwargs.items():
                if key not in parameters:
                    invalid_keys = True
                    getLogger().error(f"Invalid parameter {key}, not supported for {function.__name__}")
            if invalid_keys:
                raise APIError(f"Cancel call for {function.__name__}")
            return function(*args, **kwargs)
        return wrap
    return _supported_parameters
