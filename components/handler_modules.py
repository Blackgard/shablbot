from modules.modules import MODULES

def parse_message_module(message, user_id, chat_id, botAPI):

    for module, parameters in MODULES.active_modules.items():
        settings_module = parameters["settings"]
        templates       = settings_module["templates"]
        
        found_matches   = find_mathes(message, templates)

        if found_matches is not None:
            func          = found_matches
            entry_point   = settings_module["entry_point"]
            answer_module = entry_point(
                func=func
            )
            return chat_id, answer_module

    return None, None

def find_mathes(message, templates):

    import re

    for name_tmp, tmps in templates.items():
        for tmp in tmps:
            if re.search(tmp, message):
                return name_tmp
    return None