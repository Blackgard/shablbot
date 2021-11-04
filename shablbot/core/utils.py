from typing import Any, List, Dict

from anytree import Node, RenderTree, ContRoundStyle


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
