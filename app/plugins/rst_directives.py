import docutils
from docutils import nodes, utils
from docutils.parsers import rst
from docutils.parsers.rst import roles

def item_meta_role(name, rawtext, text, lineno, inliner, options={}, content=[]):
    new_element = nodes.inline(rawtext, utils.unescape(text), **options)
    new_element.set_class('item-meta')

    return [new_element], []

def register_roles():
    rst.roles.register_local_role('item-meta', item_meta_role)

def register():
    register_roles()
