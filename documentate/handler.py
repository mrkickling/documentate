import os
import glob
import ast
from models import Module
from jinja2 import Environment, PackageLoader, select_autoescape


class DocumentateHandler:
    def __init__(self, in_dir, out_dir):
        self.in_dir = in_dir
        self.out_dir = out_dir
        self.modules = []
        templateLoader = PackageLoader("templates", "default")
        self.env = Environment(loader=templateLoader)
        self.parse_modules()

    def parse_modules(self):
        """finds all .py files in the input directory, and parse each file (module)"""
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
        """Generate HTML documentation using Jinja2"""
        module_template = self.env.get_template("module.html")
        index_template = self.env.get_template("index.html")
        if not os.path.exists(self.out_dir):
            os.mkdir(self.out_dir)

        # Write each module to a HTML file
        for module in self.modules:
            filepath = os.path.join(self.out_dir, module.name + ".html")
            with open(filepath, "w") as f:
                # Have to send the modules as well for navigation to work
                f.write(module_template.render(module=module, modules=self.modules))

        # Write index.html file
        filepath = os.path.join(self.out_dir, "index.html")
        with open(filepath, "w") as f:
            f.write(index_template.render(modules=self.modules))
