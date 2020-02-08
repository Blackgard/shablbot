"""
Файл инициализации бота. Подгружает все статичные данные о группах и активированные модули.
"""

from settings import SETTINGS
from importlib.util import find_spec, module_from_spec

def check_module(module_path):
    module_spec = find_spec(module_path)
    return module_spec

def import_module_from_spec(module_spec):
    try:
        module = module_from_spec(module_spec)
        module_spec.loader.exec_module(module)
        return module, None
    except Exception as err:
        return None, err

def load_cache():
    """
    Функция загрузки статичных данных бота.
    """
    from components.chat_settings import get_settings_chat
    from components.cache import save_chat_to_cache

    for chat_id, _settings in SETTINGS.settings_chat.items():
        settings_chat = get_settings_chat(chat_id)
        save_chat_to_cache(chat_id, settings_chat)

    return None

def load_modules():
    """
    Функция загрузки активированных в settings.py модулей бота.
    """
    from modules.modules import MODULES

    folder_name = 'modules'
    err = []
    
    for module_name in SETTINGS.active_modules:
        module_spec = check_module(f'{folder_name}.{module_name}')
        init_module, import_err = import_module_from_spec(module_spec)
        
        if init_module is not None:
            MODULES.active_modules[module_name] = {
                "full_name" : module_spec.name,
                "settings"  : init_module.settings,
                "path"      : module_spec.loader.path
            }
        else:            
            err.append({
                module_name : str(import_err)           
            })
    
    if err is None:
        return err
    return None
            

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
    ==> False, "
        Проблемы с модулями: 
        [ 
            { 'games.flip_and_roll' : '' }
        ]
    "
    ```
    """
     
    load_cache()
    err_load_modules = load_modules()

    if err_load_modules is None:
        return True, None
    else:
        import json
        err = "\nПроблемы с модулями:\n" + json.dumps(err_load_modules, indent=4, sort_keys=True)
        return False, err
