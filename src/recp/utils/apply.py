import os
from datetime import datetime
from typing import List
from .io import get_dir_files


def apply_date(
        cmd_list: List[str],
        token: str,
        format: str = "%Y-%m-%d"
) -> List[str]:
    """Replaces a given token by a date.

    Args:
        cmd_list (List[str]): Input commands.
        token (str): The token within the command strings to be replaced.
        format (str): Date format to use.
    
    Returns:
        List[str]: List of modified commands.
    """
    for cmd_idx, cmd in enumerate(cmd_list):
        cmd_list[cmd_idx] = cmd.replace(token, datetime.now().strftime(format))
    
    return cmd_list


def apply_dir_files(
        cmd_list: List[str],
        token: str,
        dir: str,
        ext: str | List[str],
        recursive: bool = True
) -> List[str]:
    """Replaces a given token by the path to each file in a foleder.

    Args:
        cmd_list (List[str]): Input commands.
        token (str): The token within the command strings to be replaced.
        dir (str): Path to the folder to be searched.
        ext (str | List[str]): The file extension(s) used to filter files. Only
            files matching these extension(s) will be considered.
        recursive (bool): If `True`, the search is done recursively. 
    
    Returns:
        List[str]: List of modified commands.
    """
    for cmd in cmd_list:
        files = get_dir_files(dir=dir, ext=ext, recursive=recursive)
        cmd_expanded_list = []

        for file in files:
            cmd_expanded_list.append(cmd.replace(token, file))
 
    return cmd_expanded_list


def apply_parent_dir(
        cmd_list: List[str],
        token: str,
        path: str
) -> List[str]:
    """Replaces a given token by the parent path of a given path.

    Args:
        cmd_list (List[str]): Input commands.
        token (str): The token within the command strings to be replaced.
        path (str): The file system path from which the parent directory will
            be extracted.
    
    Returns:
        List[str]: List of modified commands.
    """
    for cmd_idx, cmd in enumerate(cmd_list):
        cmd_list[cmd_idx] = cmd.replace(
            token,
            os.path.dirname(os.path.normpath(path))
        )
    
    return cmd_list


def apply_replace(cmd_list: List[str], **kwargs) -> List[str]:
    """Replace placeholders by specified values.
    
    Args:
        cmd_list (List[str]): Input commands.
        **kwargs: Each subsequent argument corresponds to the value to be
            replaced, and the value is the updated value it will take.
    
    Returns:
        List[str]: List of modified commands.
    """
    for cmd_idx, cmd in enumerate(cmd_list):
        for k, v in kwargs.items():
            cmd_list[cmd_idx] = cmd.replace(k, v)
    
    return cmd_list


def apply_repeat(cmd_list: List[str], n: int) -> List[str]:
    """Repeat a command or command list `n` times.
    
    Args:
        cmd_list (List[str]): Input commands.
        n (int): Number of repetitions.
    
    Returns:
        List[str]: List of modified commands.
    """
    return cmd_list * n


def get_apply_registy() -> dict:
    """Returns the registry of all functions that can be used withing the `run`
    key of a recipe `.yaml` file.
    """
    return {
        "date": apply_date,
        "dir_files": apply_dir_files,
        "parent_dir": apply_parent_dir,
        "replace": apply_replace,
        "repeat": apply_repeat
    }
