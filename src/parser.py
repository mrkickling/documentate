import os
import glob
import ast
from models import Module


class ProgramParser:
    def __init__(self, in_dir, out_dir):
        self.in_dir = in_dir
        self.out_dir = out_dir
        self.modules = []
        self.parse_modules()

    def parse_modules(self):
        files = glob.glob(os.path.join(self.in_dir, "*.py"))
        print(self.in_dir, files)
        for filepath in files:
            module_name = filepath.split("/")[-1]
            content = ""
            with open(filepath) as f:
                content = f.read()
            self.tree = ast.parse(content)
            module = Module(module_name, self.tree)
            self.modules.append(module)

    def generate_documentation(self):
        if not os.path.exists(self.out_dir):
            os.mkdir(self.out_dir)
        for module in self.modules:
            filepath = os.path.join(self.out_dir, module.name + ".md")
            with open(filepath, "w") as f:
                f.write(module.to_markdown(1))
                module.print()
