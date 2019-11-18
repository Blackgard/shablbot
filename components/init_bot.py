"""
Файл инициализации бота. Подгружает все статичные данные о группах и активированные модули.
"""

from settings import SETTINGS
from importlib.util import find_spec, module_from_spec

def check_module(module_path):
    module_spec = find_spec(module_path)
    return module_spec

def import_module_from_spec(module_spec):
    module = module_from_spec(module_spec)
    module_spec.loader.exec_module(module)

    if module:
        return module
    return None

def load_cache():
    """
    Функция загрузки статичных данных бота.
    """
    from components.chat_settings import get_settings_chat
    from components.cache import save_chat_to_cache

    err = []

    for chat_id, _settings in SETTINGS.settings_chat.items():
        settings_chat = get_settings_chat(
            chat_id, 
            _settings.get('type'), 
            _settings.get('from'), 
            _settings.get('to'), 
            _settings.get('included')
        )

        save_chat_to_cache(chat_id, settings_chat)

    if err == []:
        return None
    return err 

def load_modules():
    """
    Функция загрузки активированных в settings.py модулей бота.
    """
    from modules.modules import MODULES

    load_name = 'modules'
    for module_name in SETTINGS.active_modules:
        err = []

        module_spec = check_module(f'{load_name}.{module_name}')
        init_module = import_module_from_spec(module_spec)

        if not init_module:
            err.append(f"Модуль {module} не был подключен.")
        else:
            MODULES.active_modules[module_name] = {
                "full_name" : module_spec.name,
                "settings"  : init_module.settings,
                "path"      : module_spec.loader.path
            }
            
    if err == []:
        return None
    return err 

def init_components():
    """
    Функция инициализации всех необходимых для работы бота модулей и значений.
    Производится инициализация:

        CACHE   - подргузка всех данных о группах (указанных в файле setting.py) 
        MODULES - подгрузка всех активных модулей (указанных в файле setting.py) 
    
    Функция возвращает 2 параметра типа bool и list:\n
    `(bool) state_init` - Параметр отражает работоспособность бота, если True - 
    тогда все компоненты были загруженны успешно, если False - не успешно.\n
    `(list) error_init` - Параметр содержащий в себе ошибки, вызванные в процессе 
    инициализации компонентов.
    ```
    Примеры:
    ==> True, None  
    ==> False, [    
        Проблемы с cache    - None,
        Проблемы с модулями - [ Модуль games.flip_and_roll не был подключен. ]
    ]
    ```
    """

    err_load_cache    = load_cache()
    err_load_modules  = load_modules()

    if err_load_cache is None and err_load_modules is None:
        return True, None
    else:
        err = f"Проблемы с cache - {err_load_cache}\nПроблемы с модулями - {err_load_modules}"
        return False, err