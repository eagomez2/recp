import sys


def get_text_color_tags() -> dict:
    return {
        "<error>": "\033[91m",
        "</error>": "\033[0m",
        "<warning>": "\033[93m",
        "</warning>": "\033[0m",
        "<green>": "\033[92m",
        "</green>": "\033[0m",
        "<magenta>": "\033[35m",
        "</magenta>": "\033[0m",
    }


def get_text_decorator_tags() -> dict:
    return {
        "<b>": "\033[1m",
        "</b>": "\033[0m",
        "<i>": "\033[3m",
        "</i>": "\033[0m",
        "<u>": "\033[4m",
        "</u>": "\033[0m"
    }


def _decorate_str(message: str) -> str:
    """Replaces colors and decorators in a string.

    Args:
        message (str): The input string to be decorated.

    Returns:
        str: The decorated string.
    """
    # Replace colors and decorators
    for k, v in get_text_decorator_tags().items():
        message = message.replace(k, v)

    for k, v in get_text_color_tags().items():
        message = message.replace(k, v)

    return message


def printc(message: str) -> None:
    """Prints a formatted string.

    Args:
        message (str): The string to print.
    """
    return print(_decorate_str(message))


def printc_exit(message: str, code: int = 0) -> None:
    """Prints a formatted string and exits the program with a specified exit
    code.

    Args:
        message (str): The string to print.
        code (int): Exit code.
    """
    printc(message=message)
    sys.exit(code)


def print_error(message: str) -> None:
    """Prints an error.
    
    Args:
        message (str): Error message print.
    """
    printc(f"<error>{message}</error>")


def print_warning(message: str) -> None:
    """Prints a warning.
    
    Args:
        message (str): Warning message to print.
    """
    printc(f"<warning>{message}</warning>")


def exit_error(message: str, code: int = 1) -> None:
    """Prints an error and stops the execution of the program.
    
    Args:
        message (str): Error message to print.
        code (int): Exit code.
    """
    print_error(message=message)
    sys.exit(code)


def exit_warning(message: str, code: int = 1) -> None:
    """Prints a warning and stops the execution of the program.

    Args:
        message (str): Warning message to print.
        code (int): Exit code.
    """
    print_warning(message=message)
    sys.exit(code)
