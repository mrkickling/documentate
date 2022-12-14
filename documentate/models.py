"""
models.py contains all classes that are used to store all parts of a python module
"""

from abc import abstractmethod
import ast


class Node:
    """
    An abstract class used for all parts of a python program (like in ast) but than can
    more easily be used in this project to produce human readable documentation.
    """

    pass


class Module(Node):
    """
    A Module is the same as a file in python. This class represents a module
    and includes its name, its docstring, its variables, functions and classes
    """

    def __init__(self, name, node) -> None:
        self.name = name
        self.globals = []
        self.classes = []
        self.docstring = ast.get_docstring(node)
        self.get_module_body(node.body)

    def get_module_body(self, body) -> None:
        for node in body:
            if isinstance(node, ast.ClassDef):
                c = Class(node)
                self.classes.append(c)


class Class(Node):
    """
    This class represents a class in the python language and contains
    a name, bases (inheritance), methods and docstring.
    """

    class ClassVariable:
        """
        This class represents a class variable and is only used within Class
        """

        def __init__(self, node: ast.AnnAssign) -> None:
            self.name = node.target.id
            self.type = node.annotation.id

    def __init__(self, node: ast.ClassDef) -> None:
        self.name = node.name
        self.docstring = ast.get_docstring(node)
        self.bases = node.bases
        self.methods = []
        self.class_variables = []
        self.get_class_body(node.body)

    def get_class_body(self, body) -> None:
        for node in body:
            if isinstance(node, ast.FunctionDef):
                f = Function(node)
                self.methods.append(f)
            if isinstance(node, ast.AnnAssign):
                class_variable = self.ClassVariable(node)
                self.class_variables.append(class_variable)


class Function(Node):
    """
    This class is used to represent a python function or method
    (which is just a function in a class in python). It has a name,
    potentially arguments, a docstring and return type.
    """

    class FunctionArgument:
        """
        This class represents a function or method argument, annotaded or not
        """

        def __init__(self, node: ast.arg) -> None:
            self.name = node.arg
            if node.annotation:
                self.type = node.annotation.value.id
            else:
                self.type = None

    class FunctionReturn:
        """
        This class represents a functions or methods return value
        """

        def __init__(self, ret) -> None:
            if type(ret) == ast.Name:
                self.type = ret.id
            elif type(ret) == ast.NameConstant:
                self.type = ret.value
            else:
                self.type = "None"

    def __init__(self, node: ast.FunctionDef) -> None:
        self.name = node.name
        self.args = []
        self.returns = []
        self.docstring = ast.get_docstring(node)
        self.get_function_head(node)

    def get_function_head(self, node: ast.FunctionDef) -> None:
        for argument in node.args.args:
            self.args.append(self.FunctionArgument(argument))
        self.returns = self.FunctionReturn(node.returns)
