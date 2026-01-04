import os
from datetime import datetime
from typing import List
from .io import get_dir_files


def apply_date(
        cmd_list: List[str],
        token: str,
        format: str = "%Y-%m-%d"
) -> List[str]:
    for cmd_idx, cmd in enumerate(cmd_list):
        cmd_list[cmd_idx] = cmd.replace(token, datetime.now().strftime(format))
    
    return cmd_list


def apply_dir_files(
        cmd_list: List[str],
        token: str,
        dir: str,
        ext: str,
        recursive: bool = True
) -> List[str]:
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
    for cmd_idx, cmd in enumerate(cmd_list):
        cmd_list[cmd_idx] = cmd.replace(
            token,
            os.path.dirname(os.path.normpath(path))
        )
    
    return cmd_list


def apply_replace(cmd_list: List[str], **kwargs) -> List[str]:
    for cmd_idx, cmd in enumerate(cmd_list):
        for k, v in kwargs.items():
            cmd_list[cmd_idx] = cmd.replace(k, v)
    
    return cmd_list


def apply_repeat(cmd_list: List[str], n: int) -> List[str]:
    return cmd_list * n


def get_apply_registy() -> dict:
    return {
        "date": apply_date,
        "dir_files": apply_dir_files,
        "parent_dir": apply_parent_dir,
        "replace": apply_replace,
        "repeat": apply_repeat
    }
