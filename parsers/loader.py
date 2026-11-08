from importlib import import_module


def get_parser(source):
    parser_name = source["parser"]
    module = import_module(f"parsers.{parser_name}")
    return module.parse