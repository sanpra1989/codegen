import clang.cindex
def print_node(node):
    text = node.spelling or node.displayname
    kind = str(node.kind)[str(node.kind).index('.')+1:]
    return '{} {}'.format(kind, text)


def is_hidden(node):
    return "py_hidden" in [c.displayname for c in node.get_children()
            if c.kind == clang.cindex.CursorKind.ANNOTATE_ATTR]

def is_exported(node):
    return "py_exported" in [c.displayname for c in node.get_children()
            if c.kind == clang.cindex.CursorKind.ANNOTATE_ATTR]

def is_class(node):
    return  node.kind == clang.cindex.CursorKind.CLASS_DECL

def is_enum(node):
    return  node.kind == clang.cindex.CursorKind.ENUM_DECL

def is_enum_constant(node):
    return  node.kind == clang.cindex.CursorKind.ENUM_CONSTANT_DECL

def is_public_function(node):
    return  node.kind == clang.cindex.CursorKind.CXX_METHOD and node.access_specifier == clang.cindex.AccessSpecifier.PUBLIC

def node_children(node):
    return [c for c in node.get_children() if c.location.file.name == sys.argv[1]]


