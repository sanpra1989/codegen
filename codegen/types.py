import clang.cindex
import asciitree # must be version 0.2
import sys

class Function:
    def __init__(self,c,fname,qualification=""):
        self.name=c.spelling
        self.qualification=qualification
        self.hidden=False
        if is_hidden(c):
            self.hidden=True

    def generate(self):
        result=[]
        if self.hidden:
            return result

        result.append('.def("%s",\t &%s)\n'%(self.name,self.qualification+self.name))
        return result

class Enum:
    def __init__(self,c,fname,qualification=""):
        self.name=c.spelling
        self.qualification=qualification

class Variable:
    def __init__(self,c,fname,qualification=""):
        self.name=c.spelling
        self.qualification=qualification


class Class:
    def __init__(self,c,fname,qualification=""):
        self.name=c.spelling
        self.qualification=qualification
        members=translate(c,fname,qualification+self.name+"::")
        self.member_classes=[]
        self.functions=[]
        self.enums=[]
        self.member_vars=[]
        self.exported=False
        if is_exported(c):
            self.exported=True

        for member in members:
            if isinstance(member,Class):
                self.member_classes.append(member)
            elif isinstance(member,Function):
                self.functions.append(member)
            if isinstance(member,Enum):
                self.enums.append(member)
            elif isinstance(member,Variable):
                self.member_vars.append(member)


    def generate(self):

        result=[]
        if not self.exported:
            return result

        for member in self.enums:
            result.extend(member.generate())
            result.append(";\n")

        result.append('class_<%s>("%s",no_init)\n'%(self.qualification+self.name,self.name))
        for member in self.functions:
            result.extend(member.generate())

        for member in self.member_classes:
            result.extend(member.generate())
            result.append(";\n")

        result.append(";\n")

        return result

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

def is_public_function(node):
    return  node.kind == clang.cindex.CursorKind.CXX_METHOD and node.access_specifier == clang.cindex.AccessSpecifier.PUBLIC

def translate(cursor,fname,qualification=""):
    global exported
    global hidden
    result = []
    for c in cursor.get_children():
        if not c.location.file.name == fname:
            continue
        if (is_class(c)):
            result.append(Class(c,fname,qualification))
        elif is_public_function(c):
            result.append(Function(c,fname,qualification))

    return result

def node_children(node):
    return [c for c in node.get_children() if c.location.file.name == sys.argv[1]]


if len(sys.argv) != 2:
    print("Usage: translator.py [header file name]")
    sys.exit()

#print clang.cindex.CursorKind.get_all_kinds()
#sys.exit()

clang.cindex.Config.set_library_file('/usr/lib/llvm-3.5/lib/libclang.so')
index = clang.cindex.Index.create()
translation_unit = index.parse(sys.argv[1], ['-x', 'c++', '-std=c++11', '-D__CODE_GENERATOR__'])

translated = translate(translation_unit.cursor,sys.argv[1])
for cls in translated:
    for line in cls.generate():
        print line

#print(asciitree.draw_tree(translation_unit.cursor, node_children, print_node))

