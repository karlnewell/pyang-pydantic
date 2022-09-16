"""Export YANG models as Pydantic models

"""

import optparse

from pyang import plugin
from pyang import util
from pyang import statements


def pyang_plugin_init():
    plugin.register_plugin(PydanticPlugin())

class PydanticPlugin(plugin.PyangPlugin):
    def add_output_format(self, fmts):
        self.multiple_modules = True
        fmts['pydantic'] = self
    def emit(self, ctx, modules, fd):

        # Output import statements
        fd.write(f"from typing import List, Optional, Union\n")
        fd.write(f"from pydantic import BaseModel, Field\n\n\n")

        for module in modules:
            chs = [ch for ch in module.i_children
                if ch.keyword in statements.data_definition_keywords]

            if len(chs) > 0:
                for ch in chs:
                    fd.write(print_children(ch))

            mods = [module]
            for m in mods:
                for augment in m.search('augment'):
                    if hasattr(augment, 'i_children'):
                        chs = [ch for ch in augment.i_children if ch.keyword in statements.data_definition_keywords]

                        if len(chs) > 0:
                            for ch in chs:
                                fd.write(print_children(ch))



def print_children(node):
    paths = ""

    path = syntax(node, is_attr=False)

    if node.i_children:
        for child in node.i_children:
            if child.keyword in ['leaf']:
                path += syntax(child, keyword=child.keyword)
            elif child.keyword in ['leaf-list']:
                path += syntax(child, keyword=child.keyword)
            elif child.keyword in ['container', 'list']:
                # we determine if a child is a choice statement so we create the appropriate Union attr
                if child.search_one("choice"):
                    for ch in child.i_children:
                        # we use the parent to determine the attr name or we end up with the choice name which shouldn't show up in the schema
                        path += syntax(ch, keyword=ch.keyword, parent=child)
                        # Choices are nested two more levels, hence the double for loop
                        for c in ch.i_children:
                            for _c in c.i_children:
                                paths += print_children(_c)
                else:
                    path += syntax(child, keyword=child.keyword)
                    paths += print_children(child)
    # We get here if there's a Class statement without any attributes so we add a pass
    else:
        path += "    pass\n"

    paths += f"{path}\n"
    return paths


def syntax(node, keyword=None, is_attr=True, parent=None) -> str:
    rv = ""
    arg = node.arg.replace("-", "_")
    if parent:
        par = parent.arg.replace("-", "_")

    if is_attr == False:
        rv += f"class {arg.title()}(BaseModel):\n"
        return rv

    match keyword:
        case "leaf":
            rv += f"    {arg}: str\n"
        case "leaf-list":
            rv += f"    {arg}: List[str]\n"
        case "list":
            rv += f"    {arg}: List[{arg.title()}]\n"
        case "container":
            rv += f"    {arg}: {arg.title()}\n"
        case "choice":
            rv += f"    {par}: Union["
            chs = ",".join([child.arg.title() for child in node.i_children])
            rv += f"{chs}"
            rv += f"]\n"

    return rv


def debug(node):
    for d in dir(node):
        if hasattr(node, d):
            print(f"{d}: {getattr(node, d)}\n")