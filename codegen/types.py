from .util import *
import clang.cindex
import asciitree # must be version 0.2
import sys


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
        elif is_enum(c):
            result.append(Enum(c,fname,qualification))
        elif is_enum_constant(c):
            result.append(c.spelling)
            
    return result



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
        self.values=[]
        self.hidden=False;
        if is_hidden(c):
            self.hidden=True
        self.values=translate(c,fname,qualification+self.name+"::")

    def generate(self):
        result=[]
        result.append('enum_<%s%s>("%s")\n'%(self.qualification,self.name,self.name ))
        for value in self.values:
            result.append('.value("%s",\t%s%s)\n'%(value,self.qualification,value))
        return result

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


        result.append('class_<%s>("%s",no_init)\n'%(self.qualification+self.name,self.name))
        for member in self.functions:
            result.extend(member.generate())

        for member in self.member_classes:
            result.extend(member.generate())
            result.append(";\n")

        result.append(";\n")

        return result


