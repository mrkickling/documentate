from abc import abstractmethod
import ast


class Node:
    @abstractmethod
    def to_markdown(self, depth) -> str:
        pass

    def print(self):
        print(self.to_markdown(1))


class Module(Node):
    def __init__(self, name, node):
        self.name = name
        self.globals = []
        self.classes = []
        self.docstring = ast.get_docstring(node)
        self.get_module_body(node.body)

    def get_module_body(self, body):
        for node in body:
            if isinstance(node, ast.ClassDef):
                c = Class(node)
                self.classes.append(c)

    def to_markdown(self, depth):
        pre = "#" * depth
        result = ""
        result += pre + " Module " + self.name + "\n" * 2
        result += pre + "# Classes" + "\n"
        for c in self.classes:
            result += c.to_markdown(depth + 2)
        return result + "\n"


class Class(Node):
    def __init__(self, node):
        self.name = node.name
        self.docstring = ast.get_docstring(node)
        self.bases = node.bases
        self.attributes = []
        self.methods = []
        self.class_variables = []
        self.get_class_body(node.body)

    def get_class_body(self, body):
        for node in body:
            if isinstance(node, ast.FunctionDef):
                f = Function(node)
                self.methods.append(f)
            if isinstance(node, ast.Assign):
                self.class_variables.append(node)

    def to_markdown(self, depth):
        pre = "#" * depth
        result = "\n"
        result += pre + " Class " + self.name + "\n"
        result += "based on " + str(self.bases) + "\n"
        if self.docstring:
            result += self.docstring + "\n"
        result += "\n\n"
        result += pre + "# Methods" + "\n\n"
        for method in self.methods:
            result += method.to_markdown(depth + 2)
        return result


class Function(Node):
    def __init__(self, node):
        self.name = node.name
        self.args = node.args.args
        self.returns = node.returns
        self.docstring = ast.get_docstring(node)

    def to_markdown(self, depth):
        pre = "#" * depth
        result = ""
        result += pre + " Function: " + self.name + "\n\n"
        result += " **Arguments**: "
        for arg in self.args:
            result += (arg.arg) + ", "
        if self.docstring:
            result += "\n" + self.docstring + "\n"
        result += "**Returns**: "
        if self.returns:
            result += self.returns.id + "\n"
        else:
            result += " unknown" + "\n"
        return result + "\n"
