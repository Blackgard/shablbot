import sys
from pathlib import Path
from typing import Any, Dict, List

from anytree import Node, RenderTree, ContRoundStyle

_STD_STREAMS = {
    "stderr": sys.stderr,
    "stdout": sys.stdout,
}


def normalize_logger_config(logger_config: Dict[str, Any]) -> Dict[str, Any]:
    """Привести LOGGER_CONFIG к формату, совместимому с loguru."""
    config = dict(logger_config)
    handlers = []

    for handler in config.get("handlers") or []:
        normalized = dict(handler)
        sink = normalized.get("sink")

        if sink in _STD_STREAMS:
            normalized["sink"] = _STD_STREAMS[sink]
        elif isinstance(sink, Path):
            normalized["sink"] = str(sink)
        elif isinstance(sink, str):
            Path(sink).parent.mkdir(parents=True, exist_ok=True)
        elif type(sink).__name__ == "SerializationIterator":
            # Pydantic v2 ломает sys.stderr при model_dump — восстанавливаем по index
            normalized["sink"] = sys.stderr if getattr(sink, "index", 0) == 0 else sys.stdout

        handlers.append(normalized)

    config["handlers"] = handlers
    return config


class RenderState:
    " Render state class. View shablbot module active in tree style. "
    def __init__(self, modules: Dict[str, Any], main_root: Node = None):
        self.modules = modules
        self.main_root = main_root

        self.node: Node = self.__create_node()

    def __create_node(self) -> Node:
        root = self.main_root

        for name_module, object in self.modules.items():
            if not root: subroot = Node(name_module)
            else: subroot = Node(name_module, parent=root)

            if isinstance(object, Dict):
                [Node(str(v), parent=subroot) for _, v in  object.items()]
            elif isinstance(object, List):
                [Node(str(item), parent=subroot) for item in object]

        return root if root else subroot

    def render(self, style = ContRoundStyle) -> None:
        """ Render tree with state bot modules.

        Args:
            style ([type], optional): Style how need rendered items. Defaults to ContRoundStyle.
        """
        print(RenderTree(self.node, style=style()).by_attr())


def render_state(name_module: str, module: Any) -> None:
    """ Render state module bot. Use tree.

    Args:
        name_module (str): Modules name
        module (Any): Object for check node
    """
    render_state = RenderState({ name_module: module })
    render_state.render()


def render_state_all_components(list_components: List[Any]) -> None:
    """ Render state all modules bot in tree style.

    Args:
        list_components (List[Any]): components bot for need rebder state. All componnets have 'get_main_data_object()' function"
    """
    render_state = RenderState(
        modules={
            comp.__class__.__name__ : comp.get_main_data_object()
            for comp in list_components
        },
        main_root=Node("Shablbot")
    )
    render_state.render()
