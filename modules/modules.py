class MODULES:
    """
    Класс хранящий в себе список данных о всех активных модулях и путь к ним.

    Все данные хранятся в active_modules и представленны в виде словаря с следующими значениями:
    ```
    {
        "module_name" : {
            "full_name" : "module_full_name",
            "settings"  : { "setting_module" },
            "path"      : "module_path"
        },
        "module_name" : {
            ...
        }
    }
    ```
    """
    active_modules = {}
