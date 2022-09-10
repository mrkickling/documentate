import argparse
import sys
from parser import ProgramParser

arg_parser = argparse.ArgumentParser(
    prog="documentate", description="Generate documentation from python projects."
)
arg_parser.add_argument(
    "-i",
    "--input",
    help="the directory of the python project to generate documentation for",
    required=True,
)
arg_parser.add_argument(
    "-o",
    "--output",
    help="the directory to put the generated documentation in",
    required=True,
)

if __name__ == "__main__":
    args = arg_parser.parse_args(sys.argv[1:])
    in_dir = args.input
    out_dir = args.output

    parser = ProgramParser(in_dir, out_dir)
    parser.generate_documentation()
