from typing import Optional, Dict, List, Tuple
from types import ModuleType

import loguru

from pydantic.error_wrappers import ValidationError

from importlib.machinery import ModuleSpec
from importlib.util import find_spec, module_from_spec

from shablbot.models.module import ModuleSettings
from shablbot.settings.settings_model import SettingsModel

from shablbot.core.color import ColorText
from shablbot.core.utils import render_state


class Module:
    """Model description of the module for the bot"""

    def __init__(
        self, module_name: str, module_folder: str, logger: loguru.logger
    ) -> None:
        self.logger = logger
        self.module_folder = module_folder

        self.module_name = module_name
        self.module_fullname = None
        self.module_settings: Optional[ModuleSettings] = None

        self.module_path = f"{self.module_folder}.{self.module_name}"
        self.is_loaded = self.load_module()

        if not self.is_loaded:
            self.logger.warning(f"Модуль {self.module_name} не был подключен!")

    def __get_module_spec(self, module_path: str) -> Optional[ModuleSpec]:
        """Get module spec for path module.

        Args:
            module_path (str): path to find modules

        Returns:
            Optional[ModuleSpec]: Specification for a module, used for loading.
        """
        module_spec = find_spec(module_path)
        return module_spec

    def __import_module_from_spec(
        self, module_spec: ModuleSpec
    ) -> Optional[ModuleType]:
        """Import module from spec

        Args:
            module_spec (ModuleSpec): Specification for a module, used for loading.

        Returns:
            Optional[ModuleType]: Module type with settings module
        """
        module = module_from_spec(module_spec)
        module_spec.loader.exec_module(module)
        return module

    def load_module(self) -> bool:
        "Load module from info."
        module_spec = self.__get_module_spec(self.module_path)
        if not module_spec:
            return False

        module = self.__import_module_from_spec(module_spec)
        if not module:
            return False

        self.module_fullname = module_spec.name

        try:
            self.module_settings = ModuleSettings(**module.settings)
        except ValidationError as e:
            self.logger.error(f"Couldn't load module! Error:\n{e}")
            return False

        return True

    def __str__(self):
        is_active_str = f'{ColorText.OKGREEN}включен{ColorText.ENDC}' if self.is_loaded else f'{ColorText.FAIL}выключен{ColorText.ENDC}'
        return "{0} - {1}".format(self.module_name, is_active_str)

class Modules:
    """Modules class for work with module"""

    def __init__(self, settings: SettingsModel, logger: loguru.logger):
        self.settings = settings
        self.logger = logger

        self.folder = self.settings.KEYBOARDS_FOLDER
        self.modules: Dict[str, Module] = {
            module_name: Module(module_name, self.settings.MODULES_FOLDER, self.logger)
            for module_name in self.settings.ACTIVE_MODULES
        }

    def get_module(self, module_name: str) -> Optional[Module]:
        """Get module for module name

        Args:
            module_name (str): module name how need get

        Returns:
            Optional[Module]: Module object or None
        """
        return self.modules[module_name]

    def get_modules(self) -> List[Tuple[str, Module]]:
        """Get add modules in list

        Returns:
            List[Tuple[str, Module]]: List with modules for tuple. First elem is name, second is module object.
        """
        return list(self.modules.items())

    def render_state(self) -> None:
        """ Render state module to console tree """
        render_state(self.__class__.__name__, self.modules)

    def get_main_data_object(self):
        return self.modules
