import os
import json
import shutil
from typing import Any
from platformdirs import PlatformDirs
from .exceptions import (
    FileExtensionError,
    FolderNotFoundError
)


class PackageConfig:
    def __init__(
            self,
            app_name: str,
            app_author: str
    ) -> None:
        super().__init__()

        # Params
        self._platform = PlatformDirs(appname=app_name, appauthor=app_author)
        self.maybe_reset_default_config()
        self.config_file = os.path.join(
            self._platform.user_data_dir,
            "settings.json"
        )
        
        with open(self.config_file, "r") as f:
            self.config = json.load(f)
        
    @property
    def recipes_dir(self) -> str:
        return self.config["recipes.dir"]
    
    def maybe_reset_default_config(self) -> None:
        BASE_DIR = self._platform.user_data_dir
        RECIPES_DIR = os.path.join(BASE_DIR, "recipes")
        BASE_SETTINGS_FILE = os.path.join(BASE_DIR, "settings.json")
        BASE_SETTINGS = {"recipes.dir": RECIPES_DIR}

        os.makedirs(BASE_DIR, exist_ok=True)
        os.makedirs(RECIPES_DIR, exist_ok=True)

        if not os.path.isfile(BASE_SETTINGS_FILE):
            with open(BASE_SETTINGS_FILE, "w") as f:
                json.dump(obj=BASE_SETTINGS, fp=f, indent=2)
    
    def save_config(self) -> None:
        with open(self.config_file, "w", encoding="utf-8") as f:
            json.dump(self.config, f)
 
    def set_param(self, param: str, value: Any) -> None:
        if param not in self.config:
            raise ValueError(
                f"Invalid parameter {param!r}. Run 'recp config' to list "
                "existing parameters"
            )
        
        match param:
            case "recipes.dir":
                if not os.path.isdir(value):
                    raise FolderNotFoundError(f"Invalid folder {value!r}")
                
                self.config[param] = value
            
            case _:
                raise AssertionError
        
        self.save_config()
    
    def add_recipe(self, file: str) -> None:
        if not os.path.isfile(file):
            raise FileNotFoundError(f"File {file!r} not found")
        
        if not file.endswith(".yaml"):
            raise FileExtensionError(
                "Only .yaml files can be added as recipes"
            )
        
        shutil.copy(file, self.recipes_dir)
        print(f"Recipe {file!r} successfully added to recipes folder")

    def print_params(self) -> None:
        print(f"file: {self.config_file!r}")

        for k, v in self.config.items():
            print(f"{k}: {v!r}")
